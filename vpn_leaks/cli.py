"""CLI entry: `vpn-leaks run` and `vpn-leaks report`."""

from __future__ import annotations

import argparse
import json
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
from vpn_leaks.checks.competitor_probes import run_competitor_probes
from vpn_leaks.checks.dns import run_dns_checks_sync
from vpn_leaks.checks.fingerprint import run_fingerprint_snapshot
from vpn_leaks.checks.ip_check import run_ip_check_sync
from vpn_leaks.checks.ipv6 import run_ipv6_checks_sync
from vpn_leaks.checks.surface_probe import run_surface_probes
from vpn_leaks.checks.transition_tests import run_transition_tests
from vpn_leaks.checks.webrtc import run_webrtc_check
from vpn_leaks.checks.yourinfo_probe import run_yourinfo_probe
from vpn_leaks.config_loader import (
    load_attribution_config,
    load_leak_tests_config,
    load_vpn_config,
    repo_root,
)
from vpn_leaks.framework import apply_framework
from vpn_leaks.models import ArtifactIndex, NormalizedRun, RunnerEnv
from vpn_leaks.policy.fetch_policy import fetch_policies
from vpn_leaks.reporting.exposure_graph import write_exposure_graph
from vpn_leaks.reporting.generate_reports import (
    generate_provider_report,
    generate_vpn_report,
    write_run_summary,
)
from vpn_leaks.run_manifest import build_manifest, manifest_to_json
from vpn_leaks.vpn_config_locations import append_location_if_missing, resolve_run_locations


def _utc_run_id(slug: str) -> str:
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return f"{slug}-{ts}-{uuid.uuid4().hex[:8]}"


def cmd_run(args: argparse.Namespace) -> int:
    slug = args.provider
    vpn_config = load_vpn_config(slug)
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

    connect_log = run_root / "raw" / "connect.log"
    connect_log.parent.mkdir(parents=True, exist_ok=True)
    log_fp = connect_log.open("a", encoding="utf-8")

    def log(msg: str) -> None:
        log_fp.write(msg + "\n")
        log_fp.flush()
        print(msg, file=sys.stderr)

    preflight_ip = v4
    try:
        for loc in locations:
            loc_id = str(loc.get("id") or "default")
            loc_label = str(loc.get("label") or loc_id)
            norm_path = run_root / "locations" / loc_id / "normalized.json"
            if norm_path.is_file() and not args.force:
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

            mode = str(vpn_config.get("connection_mode") or "manual_gui")

            if not skip_vpn:
                log(f"connect: {loc_id} ({loc_label}) mode={mode}")
                adapter.connect(loc)
            else:
                log("skip_vpn: not invoking adapter.connect")

            time.sleep(stabilize)

            endpoints = leak_cfg.get("ip_endpoints") or [
                {"url": "https://api.ipify.org", "format": "text"},
            ]
            exit_sources, v4, v6 = run_ip_check_sync(
                raw_dir=raw_base,
                endpoints=endpoints,
                services_contacted=services_contacted,
            )

            dns_obs, dns_flag, dns_notes = run_dns_checks_sync(
                raw_dir=raw_base / "dnsleak",
                leak_cfg=leak_cfg,
                exit_ip_v4=v4,
                services_contacted=services_contacted,
            )

            ipv6_status, ipv6_flag, ipv6_notes = run_ipv6_checks_sync(
                raw_dir=raw_base / "ipv6",
                leak_cfg=leak_cfg,
                exit_ip_v6=v6,
                services_contacted=services_contacted,
            )

            webrtc_cands, webrtc_flag, webrtc_notes = run_webrtc_check(
                raw_dir=raw_base / "webrtc",
                leak_cfg=leak_cfg,
                exit_ip_v4=v4,
                services_contacted=services_contacted,
            )

            fp = run_fingerprint_snapshot(
                raw_dir=raw_base / "fingerprint",
                leak_cfg=leak_cfg,
                services_contacted=services_contacted,
            )

            attribution = merge_attribution(
                exit_ip_v4=v4,
                attr_cfg=attr_cfg,
                raw_dir=raw_base,
            )

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

            yourinfo_snapshot = run_yourinfo_probe(
                raw_dir=raw_base,
                services_contacted=services_contacted,
                skip=args.skip_yourinfo,
            )

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
            surface_data = run_surface_probes(
                vpn_config,
                raw_base=raw_base,
                services_contacted=services_contacted,
            )
            if surface_data:
                loc_extra["surface_probe"] = surface_data

            if args.transition_tests and not skip_vpn:
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
            artifacts = ArtifactIndex(
                connect_log=str((run_root / "raw" / "connect.log").relative_to(repo_root())),
                ip_check_json=str((raw_base / "ip-check.json").relative_to(repo_root())),
                dnsleak_dir=str((raw_base / "dnsleak").relative_to(repo_root())),
                webrtc_dir=str((raw_base / "webrtc").relative_to(repo_root())),
                ipv6_dir=str((raw_base / "ipv6").relative_to(repo_root())),
                fingerprint_dir=str((raw_base / "fingerprint").relative_to(repo_root())),
                attribution_json=str((raw_base / "attribution.json").relative_to(repo_root())),
                policy_dir=str(policy_dir.relative_to(repo_root())),
                competitor_probe_dir=comp_rel,
                yourinfo_probe_dir=yi_rel,
                baseline_json=baseline_rel,
                surface_probe_dir=surf_rel,
                transitions_json=trans_rel,
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
            )
            if not args.no_framework:
                normalized = apply_framework(normalized)

            norm_path.parent.mkdir(parents=True, exist_ok=True)
            norm_path.write_text(normalized.model_dump_json(indent=2), encoding="utf-8")
            normalized_paths.append(norm_path)
            log(f"wrote {norm_path}")
    finally:
        log_fp.close()

    write_run_summary(run_root, normalized_paths)
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
    slug = args.provider
    vpn_config = load_vpn_config(slug)
    name = vpn_config.get("provider_name") or slug
    p = generate_vpn_report(slug, vpn_name=str(name))
    print(str(p))
    if args.asn:
        p2 = generate_provider_report(int(args.asn), title=args.asn_title)
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
        "--transition-tests",
        action="store_true",
        help="After probes, poll exit IP across disconnect/reconnect (non-manual_gui only)",
    )
    pr.set_defaults(func=cmd_run, auto_location=True)

    rep = sub.add_parser("report", help="Regenerate markdown reports")
    rep.add_argument("--provider", required=True)
    rep.add_argument("--asn", help="Also emit PROVIDERS/AS<asn>.md")
    rep.add_argument("--asn-title", default=None)
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

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))
