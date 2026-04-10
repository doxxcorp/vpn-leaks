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
from vpn_leaks.checks.dns import run_dns_checks_sync
from vpn_leaks.checks.fingerprint import run_fingerprint_snapshot
from vpn_leaks.checks.ip_check import run_ip_check_sync
from vpn_leaks.checks.ipv6 import run_ipv6_checks_sync
from vpn_leaks.checks.webrtc import run_webrtc_check
from vpn_leaks.config_loader import (
    load_attribution_config,
    load_leak_tests_config,
    load_vpn_config,
    repo_root,
)
from vpn_leaks.models import ArtifactIndex, NormalizedRun, RunnerEnv
from vpn_leaks.policy.fetch_policy import fetch_policies
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

            if not skip_vpn:
                log(f"disconnect: {loc_id}")
                adapter.disconnect()
            else:
                log("skip_vpn: not invoking adapter.disconnect")

            artifacts = ArtifactIndex(
                connect_log=str((run_root / "raw" / "connect.log").relative_to(repo_root())),
                ip_check_json=str((raw_base / "ip-check.json").relative_to(repo_root())),
                dnsleak_dir=str((raw_base / "dnsleak").relative_to(repo_root())),
                webrtc_dir=str((raw_base / "webrtc").relative_to(repo_root())),
                ipv6_dir=str((raw_base / "ipv6").relative_to(repo_root())),
                fingerprint_dir=str((raw_base / "fingerprint").relative_to(repo_root())),
                attribution_json=str((raw_base / "attribution.json").relative_to(repo_root())),
                policy_dir=str(policy_dir.relative_to(repo_root())),
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
                extra=dict(run_extra),
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
            )

            norm_path.parent.mkdir(parents=True, exist_ok=True)
            norm_path.write_text(normalized.model_dump_json(indent=2), encoding="utf-8")
            normalized_paths.append(norm_path)
            log(f"wrote {norm_path}")
    finally:
        log_fp.close()

    write_run_summary(run_root, normalized_paths)
    print(f"Run complete: {run_root}", file=sys.stderr)
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
    pr.set_defaults(func=cmd_run, auto_location=True)

    rep = sub.add_parser("report", help="Regenerate markdown reports")
    rep.add_argument("--provider", required=True)
    rep.add_argument("--asn", help="Also emit PROVIDERS/AS<asn>.md")
    rep.add_argument("--asn-title", default=None)
    rep.set_defaults(func=cmd_report)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))
