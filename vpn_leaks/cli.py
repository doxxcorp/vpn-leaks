"""CLI entry: `vpn-leaks run` and `vpn-leaks report`."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

from vpn_leaks.adapters.registry import get_adapter
from vpn_leaks.attribution.merge import merge_attribution
from vpn_leaks.auto_connection import (
    build_location_from_geo,
    fetch_geo_sync,
    find_prior_run_with_same_exit,
    quick_exit_ip,
)
from vpn_leaks.checks.baseline import write_baseline_json
from vpn_leaks.checks.browserleaks_probe import run_browserleaks_probe
from vpn_leaks.checks.competitor_probes import run_competitor_probes
from vpn_leaks.checks.dns import run_dns_checks_sync
from vpn_leaks.checks.fingerprint import run_fingerprint_snapshot
from vpn_leaks.checks.ip_check import run_ip_check_sync
from vpn_leaks.checks.ipv6 import run_ipv6_checks_sync
from vpn_leaks.checks.surface_probe import run_surface_probes
from vpn_leaks.checks.transition_tests import run_transition_tests
from vpn_leaks.checks.webrtc import run_webrtc_check
from vpn_leaks.checks.website_exposure_methodology import run_website_exposure_methodology
from vpn_leaks.checks.yourinfo_probe import run_yourinfo_probe
from vpn_leaks.config_loader import (
    load_attribution_config,
    load_leak_tests_config,
    load_vpn_config,
    methodology_config_hints,
    normalize_provider_slug,
    repo_root,
)
from vpn_leaks.framework import apply_framework
from vpn_leaks.models import ArtifactIndex, NormalizedRun, RunnerEnv, WebsiteExposureMethodology
from vpn_leaks.policy.fetch_policy import fetch_policies
from vpn_leaks.reporting.exposure_graph import write_exposure_graph
from vpn_leaks.reporting.generate_reports import (
    generate_provider_report,
    generate_vpn_report,
    write_run_summary,
)
from vpn_leaks.run_manifest import build_manifest, manifest_to_json
from vpn_leaks.run_progress import RunProgress, compute_run_total
from vpn_leaks.vpn_config_locations import append_location_if_missing, resolve_run_locations


def _utc_run_id(slug: str) -> str:
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{slug}-{ts}-{uuid.uuid4().hex[:8]}"


def cmd_run(args: argparse.Namespace) -> int:
    try:
        slug = normalize_provider_slug(args.provider)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    cfg_path = repo_root() / "configs" / "vpns" / f"{slug}.yaml"
    missing_cfg = not cfg_path.is_file()
    vpn_config = load_vpn_config(slug, create_if_missing=True)
    if missing_cfg:
        print(f"Created default VPN config: {cfg_path}", file=sys.stderr)
    for hint in methodology_config_hints(vpn_config):
        print(f"Hint: {hint}", file=sys.stderr)
    if getattr(args, "attach_capture", False) and getattr(args, "with_pcap", False):
        print(
            "Use either --attach-capture (existing `capture start` session) "
            "or --with-pcap (harness-managed tcpdump for this run), not both.",
            file=sys.stderr,
        )
        return 2

    if getattr(args, "attach_capture", False):
        from vpn_leaks.capture.session import load_active

        if load_active() is None:
            print(
                "--attach-capture requires an active PCAP session. "
                "Run `vpn-leaks capture start` first (see HANDOFF.md).",
                file=sys.stderr,
            )
            return 2

    if getattr(args, "with_pcap", False):
        from vpn_leaks.capture.session import load_active as load_cap

        if load_cap() is not None:
            print(
                "--with-pcap requires no other active capture session. "
                "`vpn-leaks capture abort` first, or use --attach-capture instead.",
                file=sys.stderr,
            )
            return 2
    leak_cfg = load_leak_tests_config()
    attr_cfg = load_attribution_config()

    v4, preflight_services = quick_exit_ip(leak_cfg)
    if not v4:
        print("Preflight failed: could not determine exit IPv4.", file=sys.stderr)
        return 1

    if not args.force:
        prior = find_prior_run_with_same_exit(vpn_provider=slug, exit_ip_v4=v4)
        if prior is not None:
            print(
                f"Skipping: this exit IPv4 ({v4}) was already benchmarked for provider {slug!r}.",
                file=sys.stderr,
            )
            print(f"Prior result: {prior}", file=sys.stderr)
            print("Use --force to run the full suite again anyway.", file=sys.stderr)
            return 0

    persist_locs = not args.no_persist_locations
    run_extra: dict[str, object] = {}

    if args.locations is None:
        if not args.auto_location:
            print(
                "Use auto location (default) or pass explicit --locations id [...].",
                file=sys.stderr,
            )
            return 1
        try:
            geo = fetch_geo_sync(v4)
        except Exception as e:
            print(
                f"Geo lookup failed ({e}); using exit-IP fallback for location id.",
                file=sys.stderr,
            )
            geo = {"success": False, "error": str(e)}
        lid, label, geo_snap = build_location_from_geo(geo, v4)
        if persist_locs:
            append_location_if_missing(slug, {"id": lid, "label": label})
        locations = [{"id": lid, "label": label}]
        run_extra["exit_geo"] = geo_snap
    else:
        if not args.locations:
            print(
                "Pass at least one id after --locations, or omit --locations for auto-detect.",
                file=sys.stderr,
            )
            return 1
        locations = resolve_run_locations(
            slug=slug,
            vpn_config=vpn_config,
            requested_ids=args.locations,
            location_label=args.location_label,
            persist=persist_locs,
        )

    if not locations:
        print("No locations selected.", file=sys.stderr)
        return 1

    runs_root = repo_root() / "runs"
    runs_root.mkdir(parents=True, exist_ok=True)

    run_id = args.run_id or _utc_run_id(slug)
    run_root = runs_root / run_id
    run_root.mkdir(parents=True, exist_ok=True)

    baseline_rel: str | None = None
    if args.capture_baseline:
        bp = run_root / "raw" / "baseline.json"
        write_baseline_json(bp, leak_cfg)
        baseline_rel = str(bp.relative_to(repo_root()))
        run_extra["baseline_path"] = baseline_rel

    manifest = build_manifest(run_id=run_id, vpn_provider=slug)
    (run_root / "run.json").write_text(
        json.dumps(manifest_to_json(manifest), indent=2),
        encoding="utf-8",
    )

    preflight_path = run_root / "raw" / "preflight.json"
    preflight_path.parent.mkdir(parents=True, exist_ok=True)
    preflight_path.write_text(
        json.dumps(
            {
                "exit_ip_v4": v4,
                "preflight_services": preflight_services,
                "auto_location": args.locations is None,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    adapter = get_adapter(slug, vpn_config)

    stabilize = float(leak_cfg.get("stabilize_seconds") or 3)
    skip_vpn = bool(args.skip_vpn or args.dry_run)
    normalized_paths: list[Path] = []
    fresh_normalized_paths: list[Path] = []

    connect_log = run_root / "raw" / "connect.log"
    connect_log.parent.mkdir(parents=True, exist_ok=True)
    log_fp = connect_log.open("a", encoding="utf-8")

    def log(msg: str) -> None:
        log_fp.write(msg + "\n")
        log_fp.flush()
        print(msg, file=sys.stderr)

    preflight_ip = v4
    mode = str(vpn_config.get("connection_mode") or "manual_gui")
    run_progress = RunProgress(
        compute_run_total(
            locations=locations,
            run_root=run_root,
            force=args.force,
            args=args,
            skip_vpn=skip_vpn,
            mode=mode,
        ),
        no_progress=args.no_progress,
    )

    capture_finalize_pending = bool(
        getattr(args, "attach_capture", False) or getattr(args, "with_pcap", False),
    )
    loop_completed_normally = False

    if getattr(args, "with_pcap", False):
        from vpn_leaks.capture.session import start as cap_short_start

        iface = os.environ.get("VPN_LEAKS_CAPTURE_INTERFACE", "en0")
        wp_desc, wp_err = cap_short_start(interface=str(iface), bpf=None)
        if wp_err or wp_desc is None:
            print(wp_err or "with-pcap: tcpdump start failed", file=sys.stderr)
            return 1
        log_fp.write(f"with-pcap: tcpdump session {wp_desc.session_id} on {iface}\n")
        log_fp.flush()
        print(
            f"with-pcap: started tcpdump session {wp_desc.session_id} on {iface}",
            file=sys.stderr,
        )

    try:
        n_locs = len(locations)
        for loc_idx, loc in enumerate(locations, start=1):
            loc_id = str(loc.get("id") or "default")
            loc_label = str(loc.get("label") or loc_id)
            run_progress.set_location(loc_idx, n_locs, loc_label)
            norm_path = run_root / "locations" / loc_id / "normalized.json"
            if norm_path.is_file() and not args.force:
                run_progress.step("Skipping (already have normalized.json)")
                log(f"skip (exists): {norm_path}")
                normalized_paths.append(norm_path)
                continue

            raw_base = run_root / "raw" / loc_id
            raw_base.mkdir(parents=True, exist_ok=True)
            policy_dir = raw_base / "policy"
            services_contacted: list[str] = []
            services_contacted.extend(preflight_services)
            if run_extra.get("exit_geo"):
                services_contacted.append(f"https://ipwho.is/{preflight_ip}")

            run_progress.step("VPN connect + stabilize")
            if not skip_vpn:
                log(f"connect: {loc_id} ({loc_label}) mode={mode}")
                adapter.connect(loc)
            else:
                log("skip_vpn: not invoking adapter.connect")

            time.sleep(stabilize)

            endpoints = leak_cfg.get("ip_endpoints") or [
                {"url": "https://api.ipify.org", "format": "text"},
            ]
            run_progress.step("Exit IP check")
            exit_sources, v4, v6 = run_ip_check_sync(
                raw_dir=raw_base,
                endpoints=endpoints,
                services_contacted=services_contacted,
            )

            run_progress.step("DNS leak tests")
            dns_obs, dns_flag, dns_notes = run_dns_checks_sync(
                raw_dir=raw_base / "dnsleak",
                leak_cfg=leak_cfg,
                exit_ip_v4=v4,
                services_contacted=services_contacted,
            )

            run_progress.step("IPv6 checks")
            ipv6_status, ipv6_flag, ipv6_notes = run_ipv6_checks_sync(
                raw_dir=raw_base / "ipv6",
                leak_cfg=leak_cfg,
                exit_ip_v6=v6,
                services_contacted=services_contacted,
            )

            run_progress.step("WebRTC")
            webrtc_cands, webrtc_flag, webrtc_notes = run_webrtc_check(
                raw_dir=raw_base / "webrtc",
                leak_cfg=leak_cfg,
                exit_ip_v4=v4,
                services_contacted=services_contacted,
            )

            run_progress.step("Fingerprint")
            fp = run_fingerprint_snapshot(
                raw_dir=raw_base / "fingerprint",
                leak_cfg=leak_cfg,
                services_contacted=services_contacted,
            )

            run_progress.step("Attribution (RIPE / Cymru / PeeringDB)")
            attribution = merge_attribution(
                exit_ip_v4=v4,
                exit_ip_v6=v6,
                attr_cfg=attr_cfg,
                raw_dir=raw_base,
            )

            run_progress.step("Privacy policies")
            vpn_urls = list(vpn_config.get("policy_urls") or [])
            vpn_pol = fetch_policies(
                policy_dir=policy_dir,
                urls=vpn_urls,
                role="vpn",
                services_contacted=services_contacted,
            )
            underlay_urls = list(vpn_config.get("underlay_policy_urls") or [])
            u_pol: list = []
            if underlay_urls:
                u_pol = fetch_policies(
                    policy_dir=policy_dir,
                    urls=underlay_urls,
                    role="underlay",
                    services_contacted=services_contacted,
                )

            policies = vpn_pol + u_pol

            run_progress.step("yourinfo.ai probe")
            yourinfo_snapshot = run_yourinfo_probe(
                raw_dir=raw_base,
                services_contacted=services_contacted,
                skip=args.skip_yourinfo,
            )

            run_progress.step("browserleaks probe")
            browserleaks_snapshot = run_browserleaks_probe(
                leak_cfg=leak_cfg,
                raw_dir=raw_base,
                services_contacted=services_contacted,
                skip=args.skip_browserleaks,
            )

            run_progress.step("Competitor probes")
            competitor_surface = run_competitor_probes(
                vpn_config,
                raw_base=raw_base,
                exit_ip_v4=v4,
                services_contacted=services_contacted,
                attr_cfg=attr_cfg,
                skip_dns=args.skip_competitor_dns,
                skip_web=args.skip_competitor_web,
                skip_portal=args.skip_competitor_portal,
                skip_transit=args.skip_competitor_transit,
                skip_stray_json=args.skip_competitor_stray_json,
            )

            loc_extra: dict[str, object] = dict(run_extra)
            run_progress.step("Surface probes")
            surface_data = run_surface_probes(
                vpn_config,
                raw_base=raw_base,
                services_contacted=services_contacted,
            )
            if surface_data:
                loc_extra["surface_probe"] = surface_data

            # Full disconnect/reconnect polling only when the adapter runs; for manual_gui
            # still record a stub (skipped) so `--transition-tests` produces transitions.json.
            if args.transition_tests and (not skip_vpn or mode == "manual_gui"):
                run_progress.step("Transition tests")
                tr = run_transition_tests(
                    leak_cfg=leak_cfg,
                    raw_dir=raw_base,
                    connection_mode=mode,
                    adapter=adapter,
                    loc=loc,
                    stabilize=stabilize,
                    log=log,
                )
                if tr is not None:
                    loc_extra["transition_tests"] = tr

            run_progress.step("Website exposure methodology")
            _sp_kw = loc_extra.get("surface_probe")
            surface_probe_kw = _sp_kw if isinstance(_sp_kw, dict) else None
            try:
                web_exp = run_website_exposure_methodology(
                    vpn_config=vpn_config,
                    competitor_surface=competitor_surface,
                    surface_probe=surface_probe_kw,
                    raw_dir=raw_base,
                    services_contacted=services_contacted,
                    attr_cfg=attr_cfg,
                )
            except Exception as e:
                err = f"website_exposure_methodology:{e}"[:480]
                web_exp = WebsiteExposureMethodology(errors=[err])

            run_progress.step("VPN disconnect")
            if not skip_vpn:
                log(f"disconnect: {loc_id}")
                adapter.disconnect()
            else:
                log("skip_vpn: not invoking adapter.disconnect")

            comp_rel = (
                str((raw_base / "competitor_probe").relative_to(repo_root()))
                if (raw_base / "competitor_probe").is_dir()
                else None
            )
            yi_rel = (
                str((raw_base / "yourinfo_probe").relative_to(repo_root()))
                if (raw_base / "yourinfo_probe").is_dir()
                else None
            )
            bl_rel = (
                str((raw_base / "browserleaks_probe").relative_to(repo_root()))
                if (raw_base / "browserleaks_probe").is_dir()
                else None
            )
            asn_pf_rel = (
                str((raw_base / "asn_prefixes.json").relative_to(repo_root()))
                if (raw_base / "asn_prefixes.json").is_file()
                else None
            )
            exit_dns_rel = (
                str((raw_base / "exit_dns.json").relative_to(repo_root()))
                if (raw_base / "exit_dns.json").is_file()
                else None
            )
            surf_rel = (
                str((raw_base / "surface_probe").relative_to(repo_root()))
                if (raw_base / "surface_probe").is_dir()
                else None
            )
            trans_rel = (
                str((raw_base / "transitions.json").relative_to(repo_root()))
                if (raw_base / "transitions.json").is_file()
                else None
            )
            meth_rel = (
                str((raw_base / "website_exposure").relative_to(repo_root()))
                if (raw_base / "website_exposure").is_dir()
                else None
            )
            artifacts = ArtifactIndex(
                connect_log=str((run_root / "raw" / "connect.log").relative_to(repo_root())),
                ip_check_json=str((raw_base / "ip-check.json").relative_to(repo_root())),
                dnsleak_dir=str((raw_base / "dnsleak").relative_to(repo_root())),
                webrtc_dir=str((raw_base / "webrtc").relative_to(repo_root())),
                ipv6_dir=str((raw_base / "ipv6").relative_to(repo_root())),
                fingerprint_dir=str((raw_base / "fingerprint").relative_to(repo_root())),
                attribution_json=str((raw_base / "attribution.json").relative_to(repo_root())),
                asn_prefixes_json=asn_pf_rel,
                exit_dns_json=exit_dns_rel,
                policy_dir=str(policy_dir.relative_to(repo_root())),
                competitor_probe_dir=comp_rel,
                browserleaks_probe_dir=bl_rel,
                yourinfo_probe_dir=yi_rel,
                baseline_json=baseline_rel,
                surface_probe_dir=surf_rel,
                transitions_json=trans_rel,
                website_exposure_dir=meth_rel,
            )

            normalized = NormalizedRun(
                run_id=run_id,
                runner_env=RunnerEnv(
                    os=manifest.runner_env.os,
                    kernel=manifest.runner_env.kernel,
                    python=manifest.runner_env.python,
                    vpn_protocol=mode,
                ),
                vpn_provider=slug,
                vpn_location_id=loc_id,
                vpn_location_label=loc_label,
                connection_mode=mode,
                extra=loc_extra,
                exit_ip_v4=v4,
                exit_ip_v6=v6,
                exit_ip_sources=exit_sources,
                dns_servers_observed=dns_obs,
                dns_leak_flag=dns_flag,
                dns_leak_notes=dns_notes,
                webrtc_candidates=webrtc_cands,
                webrtc_leak_flag=webrtc_flag,
                webrtc_notes=webrtc_notes,
                ipv6_status=ipv6_status,
                ipv6_leak_flag=ipv6_flag,
                ipv6_notes=ipv6_notes,
                fingerprint_snapshot=fp,
                attribution=attribution,
                policies=policies,
                services_contacted=sorted(set(services_contacted)),
                artifacts=artifacts,
                competitor_surface=competitor_surface,
                yourinfo_snapshot=yourinfo_snapshot,
                browserleaks_snapshot=browserleaks_snapshot,
                website_exposure_methodology=web_exp,
            )
            run_progress.step("Write normalized.json + framework")
            if not args.no_framework:
                normalized = apply_framework(normalized)

            norm_path.parent.mkdir(parents=True, exist_ok=True)
            norm_path.write_text(normalized.model_dump_json(indent=2), encoding="utf-8")
            normalized_paths.append(norm_path)
            fresh_normalized_paths.append(norm_path)
            log(f"wrote {norm_path}")

        else:
            loop_completed_normally = True

        run_progress.clear_location()

        if capture_finalize_pending:
            run_progress.step("Finalize PCAP session")
            from vpn_leaks.capture.finalize_bundle import finalize_capture_and_merge

            finalize_capture_and_merge(
                run_root=run_root,
                fresh_norm_paths=fresh_normalized_paths,
                log=log,
            )
    except BaseException:
        if capture_finalize_pending and (
            getattr(args, "with_pcap", False) or not loop_completed_normally
        ):
            try:
                from vpn_leaks.capture.finalize_bundle import finalize_capture_and_merge

                log("Finalize PCAP session (after early exit)")
                finalize_capture_and_merge(
                    run_root=run_root,
                    fresh_norm_paths=fresh_normalized_paths,
                    log=log,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"PCAP finalize error: {exc}", file=sys.stderr)
        raise
    finally:
        log_fp.close()

    try:
        run_progress.step("Writing run summary")
        write_run_summary(run_root, normalized_paths)
    finally:
        run_progress.close()

    print(f"Run complete: {run_root}", file=sys.stderr)
    return 0


def cmd_graph_export(args: argparse.Namespace) -> int:
    out = (
        Path(args.output).resolve()
        if args.output
        else repo_root() / "exposure-graph.json"
    )
    slug: str | None = args.provider
    write_exposure_graph(out, provider_slug=slug)
    print(str(out))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    try:
        slug = normalize_provider_slug(args.provider)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    cfg_path = repo_root() / "configs" / "vpns" / f"{slug}.yaml"
    missing_cfg = not cfg_path.is_file()
    vpn_config = load_vpn_config(slug, create_if_missing=True)
    if missing_cfg:
        print(f"Created default VPN config: {cfg_path}", file=sys.stderr)
    name = vpn_config.get("provider_name") or slug
    total_steps = 11 + (3 if args.asn else 0)
    report_progress = RunProgress(total_steps, no_progress=args.no_progress)
    try:
        p = generate_vpn_report(slug, vpn_name=str(name), progress_step=report_progress.step)
        if args.asn:
            p2 = generate_provider_report(
                int(args.asn),
                title=args.asn_title,
                progress_step=report_progress.step,
            )
    finally:
        report_progress.close()

    print(str(p))
    print(str(p.with_suffix(".html")))
    if args.asn:
        print(str(p2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vpn-leaks")
    sub = p.add_subparsers(dest="command", required=True)

    pr = sub.add_parser("run", help="Run leak tests for a provider")
    pr.add_argument("--provider", required=True, help="VPN slug (configs/vpns/<slug>.yaml)")
    pr.add_argument(
        "--locations",
        nargs="*",
        default=None,
        metavar="ID",
        help="Explicit location ids; omit for auto-detect from exit IP + geo (ipwho.is)",
    )
    pr.add_argument(
        "--no-auto-location",
        action="store_false",
        dest="auto_location",
        help="Require --locations (disables auto-detect from exit IP + ipwho.is)",
    )
    pr.add_argument(
        "--location-label",
        default=None,
        help="Human-readable label when exactly one --locations id is used (default: id as label)",
    )
    pr.add_argument(
        "--no-persist-locations",
        action="store_true",
        help="Do not append new location ids to the provider YAML",
    )
    pr.add_argument("--run-id", help="Existing run id folder under runs/")
    pr.add_argument("--resume", action="store_true", help="Continue using --run-id")
    pr.add_argument(
        "--force",
        action="store_true",
        help="Re-run even if this exit IP was benchmarked before; overwrite normalized.json",
    )
    pr.add_argument("--dry-run", action="store_true", help="Skip VPN connect/disconnect")
    pr.add_argument("--skip-vpn", action="store_true", help="Alias for --dry-run")
    pr.add_argument(
        "--skip-competitor-dns",
        action="store_true",
        help="Skip competitor_probe provider DNS (NS/A/AAAA) lookups",
    )
    pr.add_argument(
        "--skip-competitor-web",
        action="store_true",
        help="Skip competitor_probe Playwright web/HAR probes",
    )
    pr.add_argument(
        "--skip-competitor-portal",
        action="store_true",
        help="Skip competitor_probe portal DNS + HTTPS checks",
    )
    pr.add_argument(
        "--skip-competitor-transit",
        action="store_true",
        help="Skip competitor_probe traceroute toward exit IP",
    )
    pr.add_argument(
        "--skip-competitor-stray-json",
        action="store_true",
        help="Skip competitor_probe stray JSON path GETs",
    )
    pr.add_argument(
        "--skip-yourinfo",
        action="store_true",
        help="Skip loading yourinfo.ai benchmark (Playwright HAR + excerpt)",
    )
    pr.add_argument(
        "--skip-browserleaks",
        action="store_true",
        help="Skip pinned browserleaks.com pages (Playwright HAR + excerpts)",
    )
    pr.add_argument(
        "--no-framework",
        action="store_true",
        help="Skip SPEC framework synthesis (findings, coverage, risk in normalized.json)",
    )
    pr.add_argument(
        "--capture-baseline",
        action="store_true",
        help=(
            "Write raw/baseline.json at run start; disconnect VPN first for a true ISP baseline"
        ),
    )
    pr.add_argument(
        "--attach-capture",
        action="store_true",
        help=(
            "After the run: stop tcpdump from `vpn-leaks capture start`, "
            "write PCAP under runs/.../raw/<loc>/capture/, merge pcap_summary into normalized.json"
        ),
    )
    pr.add_argument(
        "--with-pcap",
        action="store_true",
        help=(
            "Start tcpdump when the harness starts (same session envelope as competitive capture); "
            "finalize PCAP + merge at end (mutually exclusive with --attach-capture)"
        ),
    )
    pr.add_argument(
        "--transition-tests",
        action="store_true",
        help="After probes, poll exit IP across disconnect/reconnect (non-manual_gui only)",
    )
    pr.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable tqdm bar; still print phase lines to stderr",
    )
    pr.set_defaults(func=cmd_run, auto_location=True)

    rep = sub.add_parser("report", help="Regenerate markdown reports")
    rep.add_argument("--provider", required=True)
    rep.add_argument("--asn", help="Also emit PROVIDERS/AS<asn>.md")
    rep.add_argument("--asn-title", default=None)
    rep.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable tqdm bar; still print phase lines to stderr",
    )
    rep.set_defaults(func=cmd_report)

    gx = sub.add_parser(
        "graph-export",
        help="Export exposure graph JSON (nodes/edges) from normalized runs",
    )
    gx.add_argument(
        "--provider",
        default=None,
        metavar="SLUG",
        help="Limit to one VPN slug; omit to include all providers under runs/",
    )
    gx.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output file (default: exposure-graph.json in repo root)",
    )
    gx.set_defaults(func=cmd_graph_export)

    cap_root = sub.add_parser(
        "capture",
        help="Long-lived PCAP session (tcpdump). No Wireshark/tshark/mitmproxy.",
    )
    csub = cap_root.add_subparsers(dest="cap_cmd", required=True)

    pst = csub.add_parser("start", help="Start tcpdump (often requires sudo)")
    pst.add_argument(
        "-i",
        "--interface",
        default=None,
        metavar="IFACE",
        help="Network interface (default: $VPN_LEAKS_CAPTURE_INTERFACE or en0)",
    )
    pst.add_argument(
        "--bpf",
        default=None,
        metavar="EXPR",
        help="Optional tcpdump filter expression",
    )

    pst2 = csub.add_parser("status", help="Show active capture session")

    pst3 = csub.add_parser("abort", help="Stop tcpdump and clear session descriptor")
    pst3.add_argument(
        "--keep-pcap",
        action="store_true",
        help="Keep partial PCAP file in cache (default: delete alongside abort)",
    )

    pst4 = csub.add_parser(
        "idle",
        help="Capture VPN-app telemetry BEFORE the tunnel is connected (TASK-10; requires sudo)",
    )
    pst4.add_argument("--provider", required=True, help="VPN provider slug (e.g. nordvpn)")
    pst4.add_argument("--duration", type=int, default=120, help="Seconds to capture (default: 120)")
    pst4.add_argument("-i", "--interface", default=None, metavar="IFACE",
                      help="Network interface (default: $VPN_LEAKS_CAPTURE_INTERFACE or en0)")
    pst4.add_argument("--bpf", default=None, metavar="EXPR", help="Optional tcpdump filter")
    pst4.add_argument("-o", "--output", default=None,
                      help="Output JSON path (default: runs/idle_telemetry/<provider>-<ts>.json)")

    for leaf in (pst, pst2, pst3, pst4):
        leaf.set_defaults(func=cmd_capture)

    psum = sub.add_parser(
        "pcap-summarize",
        help="Emit pcap_summary.json next to a .pcap (Python/dpkt only)",
    )
    psum.add_argument("pcap", help="Path to .pcap file")
    psum.add_argument("-o", "--output", default=None, help="Output JSON path")
    psum.set_defaults(func=cmd_pcap_summarize)

    bgp = sub.add_parser(
        "bgp-update",
        help="Download latest Route Views MRT RIB and rebuild .cache/vpn_leaks/bgp_prefixes.db",
    )
    bgp.add_argument("--url", default=None, help="Override RIB .bz2 URL")
    bgp.add_argument(
        "--rib-file", default=None, metavar="PATH",
        help="Use local .bz2 file instead of downloading",
    )
    bgp.add_argument("--db", default=None, metavar="PATH", help="Output DB path (default: auto)")
    bgp.set_defaults(func=cmd_bgp_update)

    return p


def cmd_capture(args: argparse.Namespace) -> int:
    from vpn_leaks.capture.session import abort as cap_abort
    from vpn_leaks.capture.session import start as cap_start
    from vpn_leaks.capture.session import status as cap_status

    iface_default = os.environ.get("VPN_LEAKS_CAPTURE_INTERFACE", "en0")

    cmd = getattr(args, "cap_cmd", "")
    if cmd == "start":
        iface = args.interface or iface_default
        desc, err = cap_start(interface=str(iface), bpf=getattr(args, "bpf", None))
        if err or desc is None:
            print(err or "capture start failed", file=sys.stderr)
            return 1
        print(
            json.dumps(
                {"ok": True, "session_id": desc.session_id, **desc.to_json()},
                indent=2,
            ),
        )
        return 0

    if cmd == "status":
        desc, info = cap_status()
        payload: dict[str, object] = {"active": desc is not None, "details": info}
        if desc is not None:
            payload["descriptor"] = desc.to_json()
        print(json.dumps(payload, indent=2))
        return 0

    if cmd == "abort":
        ok, msg = cap_abort(discard_pcap=not bool(getattr(args, "keep_pcap", False)))
        print(msg, file=sys.stderr)
        return 0 if ok else 1

    if cmd == "idle":
        from vpn_leaks.checks.idle_telemetry import run_idle_capture

        iface = args.interface or iface_default
        try:
            slug = normalize_provider_slug(args.provider)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
        try:
            result = run_idle_capture(
                provider=slug,
                duration=int(args.duration),
                interface=str(iface),
                output=getattr(args, "output", None),
                bpf=getattr(args, "bpf", None),
            )
        except Exception as e:
            print(f"capture idle failed: {e}", file=sys.stderr)
            return 1
        print(json.dumps({
            "provider": result["provider"],
            "duration_seconds": result["duration_seconds"],
            "captured_at": result["captured_at"],
            "summary": result["summary"],
            "output_path": result.get("output_path"),
        }, indent=2))
        return 0

    print(f"Unknown capture command: {cmd}", file=sys.stderr)
    return 2


def cmd_pcap_summarize(args: argparse.Namespace) -> int:
    from vpn_leaks.checks.pcap_summarize import write_pcap_summary_json

    pc = Path(args.pcap).resolve()
    outp = Path(args.output).resolve() if args.output else pc.parent / "pcap_summary.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    write_pcap_summary_json(pc, outp)
    print(str(outp))
    return 0


def cmd_bgp_update(args: argparse.Namespace) -> int:
    from vpn_leaks.attribution.bgp_build import build_bgp_db
    from vpn_leaks.attribution.bgp_lookup import _default_db_path

    db_path = Path(args.db).resolve() if args.db else _default_db_path()
    rib_file = Path(args.rib_file).resolve() if args.rib_file else None
    try:
        result = build_bgp_db(db_path, rib_url=args.url, rib_file=rib_file, progress=True)
        print(
            f"prefixes={result['prefix_count']:,}  db={result['db_path']}  "
            f"size={result['db_size_mb']:.0f}MB  elapsed={result['elapsed_s']:.0f}s"
        )
        return 0
    except Exception as e:
        print(f"bgp-update failed: {e}", file=sys.stderr)
        return 1


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))
