"""Generate markdown reports from normalized run JSON files."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from vpn_leaks.config_loader import repo_root
from vpn_leaks.reporting.benchmark_location import format_benchmark_location_display
from vpn_leaks.reporting.coverage_rollup import build_framework_rollup_payload
from vpn_leaks.reporting.html_dashboard import build_html_dashboard_context
from vpn_leaks.reporting.web_exposure import (
    methodology_and_pcap_sections,
    per_location_web_exposure,
    rollup_web_exposure,
)

# Default cap for medium-sized fenced JSON (DNS, exit sources, policies, artifacts).
REPORT_JSON_BLOCK_MAX = 120_000
# Attribution / competitor payloads include large API `raw` blobs — use high caps.
REPORT_ATTRIBUTION_JSON_MAX = 500_000
REPORT_COMPETITOR_JSON_MAX = 500_000
# Full copy of each normalized.json at end of each detailed section (safety cap ~2 MiB).
REPORT_FULL_NORMALIZED_MAX = 2_000_000
REPORT_YOURINFO_TEXT_MAX = 3500
WEBRTC_CANDIDATES_MAX = 20
SERVICES_CONTACTED_MAX = 250
WEBRTC_RAW_CELL_MAX = 200
REPORT_FRAMEWORK_JSON_MAX = 400_000
ProgressStep = Callable[[str], None]


def _jinja_env() -> Environment:
    tpl_dir = Path(__file__).resolve().parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(tpl_dir)),
        autoescape=select_autoescape(enabled_extensions=(".html",)),
    )


def _load_report_static_file(name: str) -> str:
    p = Path(__file__).resolve().parent / "static" / name
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8")


def _markdown_extensions() -> list[str]:
    return [
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
    ]


def markdown_to_html_body(text: str) -> str:
    """Convert markdown report text to HTML (tables + fenced code)."""
    md = markdown.Markdown(extensions=_markdown_extensions())
    return md.convert(text)


def _json_for_html_script(obj: Any) -> str:
    """Serialize JSON for embedding in <script type=\"application/json\"> (escape < for HTML)."""
    return json.dumps(obj, ensure_ascii=False).replace("<", r"\u003c")


def collect_normalized_runs(
    provider_slug: str | None = None,
) -> list[tuple[str, Path, dict[str, Any]]]:
    """Return (run_id, path, data) for each normalized.json under runs/.

    Filter by provider slug or include all.
    """
    runs = repo_root() / "runs"
    if not runs.is_dir():
        return []
    out: list[tuple[str, Path, dict[str, Any]]] = []
    for run_dir in sorted(runs.iterdir()):
        if not run_dir.is_dir():
            continue
        loc_root = run_dir / "locations"
        if not loc_root.is_dir():
            continue
        for loc_dir in sorted(loc_root.iterdir()):
            p = loc_dir / "normalized.json"
            if not p.is_file():
                continue
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if provider_slug is not None and data.get("vpn_provider") != provider_slug:
                continue
            out.append((run_dir.name, p, data))
    return out


def collect_normalized_for_provider(provider_slug: str) -> list[tuple[str, Path, dict[str, Any]]]:
    """Return list of (run_id, path, data) for all normalized.json under runs/ for one provider."""
    return collect_normalized_runs(provider_slug)


def load_idle_telemetry_latest(provider_slug: str) -> dict[str, Any] | None:
    """Return the most recent ``runs/idle_telemetry/<provider>-*.json`` payload, if any.

    TASK-10: rendered as a Tier 3 section in the HTML report so operators can
    see app telemetry captured before the VPN tunnel was established.
    """
    idle_dir = repo_root() / "runs" / "idle_telemetry"
    if not idle_dir.is_dir():
        return None
    candidates = sorted(idle_dir.glob(f"{provider_slug}-*.json"))
    if not candidates:
        return None
    latest = candidates[-1]
    try:
        return json.loads(latest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _fence_json(
    label: str, obj: Any, max_chars: int = REPORT_JSON_BLOCK_MAX
) -> tuple[str, bool]:
    """Return fenced markdown and whether the JSON was truncated to max_chars."""
    body = json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    truncated = len(body) > max_chars
    if truncated:
        body = body[:max_chars] + "\n…"
    return f"```{label}\n{body}\n```", truncated


def build_framework_rollup(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Aggregate SPEC framework coverage and risk across runs (merged per question ID)."""
    return build_framework_rollup_payload(rows)


def build_detailed_runs(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> list[dict[str, Any]]:
    """Per-location sections for the VPN markdown report."""
    detailed: list[dict[str, Any]] = []
    root = repo_root()
    for run_id, path, data in rows:
        rel = path.relative_to(root)
        loc_id = data.get("vpn_location_id") or ""
        label = data.get("vpn_location_label") or loc_id

        exit_sources = data.get("exit_ip_sources") or []
        dns_obs = data.get("dns_servers_observed") or []
        webrtc = data.get("webrtc_candidates") or []
        webrtc_show = webrtc[:WEBRTC_CANDIDATES_MAX]
        webrtc_more = max(0, len(webrtc) - len(webrtc_show))

        svc = data.get("services_contacted") or []
        if isinstance(svc, list) and len(svc) > SERVICES_CONTACTED_MAX:
            svc_trim = svc[:SERVICES_CONTACTED_MAX]
            svc_note = f"+ {len(svc) - SERVICES_CONTACTED_MAX} more (see normalized.json)"
        else:
            svc_trim = svc
            svc_note = None

        yi = data.get("yourinfo_snapshot")
        yi_text_report = None
        yi_trunc = False
        if isinstance(yi, dict) and yi.get("text_excerpt"):
            t = str(yi["text_excerpt"])
            if len(t) > REPORT_YOURINFO_TEXT_MAX:
                yi_text_report = t[:REPORT_YOURINFO_TEXT_MAX] + "…"
                yi_trunc = True
            else:
                yi_text_report = t

        cs_raw = data.get("competitor_surface")
        cs_trunc = False
        if "competitor_surface" not in data:
            competitor_surface_kind = "absent"
            competitor_surface_block: str | None = None
        elif cs_raw is None:
            competitor_surface_kind = "null"
            competitor_surface_block = None
        else:
            cs = cs_raw
            competitor_surface_block, cs_trunc = _fence_json(
                "json", cs, max_chars=REPORT_COMPETITOR_JSON_MAX
            )
            if isinstance(cs, dict) and len(cs) == 0:
                competitor_surface_kind = "empty"
            else:
                competitor_surface_kind = "data"

        fp = data.get("fingerprint_snapshot") or {}
        if fp:
            fingerprint_block, fp_trunc = _fence_json("json", fp)
        else:
            fingerprint_block = None
            fp_trunc = False

        webrtc_show_rows: list[dict[str, Any]] = []
        for c in webrtc_show:
            if not isinstance(c, dict):
                continue
            raw = c.get("raw")
            raw_s = str(raw) if raw is not None else ""
            if len(raw_s) > WEBRTC_RAW_CELL_MAX:
                raw_s = raw_s[:WEBRTC_RAW_CELL_MAX] + "…"
            webrtc_show_rows.append({**c, "raw_cell": raw_s})

        truncation_notes: list[str] = []

        runner_env_block, t = _fence_json(
            "json", data.get("runner_env") or {}, max_chars=20_000
        )
        if t:
            truncation_notes.append(
                "`runner_env` excerpt exceeded size cap; full object in `normalized.json`."
            )

        exit_ip_sources_block, t = _fence_json("json", exit_sources)
        if t:
            truncation_notes.append(
                "`exit_ip_sources` excerpt exceeded size cap; full array in `normalized.json`."
            )

        dns_servers_observed_block, t = _fence_json("json", dns_obs)
        if t:
            truncation_notes.append(
                "`dns_servers_observed` excerpt exceeded size cap; full array in `normalized.json`."
            )

        if fp and fp_trunc:
            truncation_notes.append(
                "`fingerprint_snapshot` excerpt exceeded size cap; "
                "full object in `normalized.json`."
            )

        attribution_block, t = _fence_json(
            "json",
            data.get("attribution") or {},
            max_chars=REPORT_ATTRIBUTION_JSON_MAX,
        )
        if t:
            truncation_notes.append(
                "`attribution` excerpt exceeded size cap (large API `raw` blobs); "
                "full object in `normalized.json`."
            )

        policies_block, t = _fence_json("json", data.get("policies") or [])
        if t:
            truncation_notes.append(
                "`policies` excerpt exceeded size cap; full array in `normalized.json`."
            )

        artifacts_block, t = _fence_json("json", data.get("artifacts") or {})
        if t:
            truncation_notes.append(
                "`artifacts` excerpt exceeded size cap; full object in `normalized.json`."
            )

        if cs_trunc:
            truncation_notes.append(
                "`competitor_surface` excerpt exceeded size cap; full object in `normalized.json`."
            )

        extra_block, t = _fence_json("json", data.get("extra") or {})
        if t:
            truncation_notes.append(
                "`extra` excerpt exceeded size cap; full object in `normalized.json`."
            )

        yourinfo_snapshot_block: str | None
        if yi:
            yourinfo_snapshot_block, t = _fence_json(
                "json", yi, max_chars=REPORT_JSON_BLOCK_MAX
            )
            if t:
                truncation_notes.append(
                    "`yourinfo_snapshot` JSON excerpt exceeded size cap; "
                    "full object in `normalized.json`."
                )
        else:
            yourinfo_snapshot_block = None

        if yi_trunc or (
            isinstance(yi, dict) and yi.get("text_excerpt_truncated")
        ):
            truncation_notes.append(
                "YourInfo **visible text excerpt** below is length-capped; "
                "full text in raw `yourinfo_probe/` and `normalized.json`."
            )

        fw_raw = data.get("framework")
        framework_block: str | None = None
        framework_risk_line = ""
        if fw_raw:
            framework_block, fw_t = _fence_json(
                "json",
                fw_raw,
                max_chars=REPORT_FRAMEWORK_JSON_MAX,
            )
            if fw_t:
                truncation_notes.append(
                    "`framework` excerpt exceeded size cap; full object in `normalized.json`."
                )
            rs_fw = fw_raw.get("risk_scores") or {}
            if isinstance(rs_fw, dict):
                o = rs_fw.get("overall_severity", "—")
                lk = rs_fw.get("leak_severity", "—")
                tp = rs_fw.get("third_party_exposure", "—")
                cr = rs_fw.get("correlation_risk", "—")
                framework_risk_line = (
                    f"Overall **{o}** · leak **{lk}** · third-party **{tp}** · correlation **{cr}**"
                )

        full_normalized_block, t = _fence_json(
            "json", data, max_chars=REPORT_FULL_NORMALIZED_MAX
        )
        if t:
            truncation_notes.append(
                "**Complete normalized record** below exceeded ~2 MiB cap; "
                "open `normalized.json` on disk for the full file."
            )

        if svc_note:
            truncation_notes.append(
                "`services_contacted` list shows the first "
                f"{SERVICES_CONTACTED_MAX} entries; full list in `normalized.json`."
            )

        if webrtc_more > 0:
            truncation_notes.append(
                f"WebRTC table lists {len(webrtc_show_rows)} of "
                f"{len(webrtc_show_rows) + webrtc_more} candidates; remainder in `normalized.json`."
            )

        detailed.append(
            {
                "run_id": run_id,
                "location_id": loc_id,
                "location_label": label,
                "vpn_provider": data.get("vpn_provider"),
                "normalized_path": str(rel),
                "timestamp_utc": data.get("timestamp_utc"),
                "schema_version": data.get("schema_version"),
                "runner_env_block": runner_env_block,
                "connection_mode": data.get("connection_mode"),
                "exit_ip_v4": data.get("exit_ip_v4"),
                "exit_ip_v6": data.get("exit_ip_v6"),
                "exit_ip_sources_block": exit_ip_sources_block,
                "dns_servers_observed_block": dns_servers_observed_block,
                "dns_leak_flag": data.get("dns_leak_flag"),
                "dns_leak_notes": data.get("dns_leak_notes"),
                "webrtc_leak_flag": data.get("webrtc_leak_flag"),
                "webrtc_notes": data.get("webrtc_notes"),
                "webrtc_candidates_show": webrtc_show_rows,
                "webrtc_candidates_more": webrtc_more,
                "ipv6_status": data.get("ipv6_status"),
                "ipv6_leak_flag": data.get("ipv6_leak_flag"),
                "ipv6_notes": data.get("ipv6_notes"),
                "fingerprint_block": fingerprint_block,
                "attribution_block": attribution_block,
                "policies_block": policies_block,
                "services_contacted": svc_trim,
                "services_contacted_note": svc_note,
                "artifacts_block": artifacts_block,
                "competitor_surface_block": competitor_surface_block,
                "competitor_surface_kind": competitor_surface_kind,
                "extra_block": extra_block,
                "yourinfo_snapshot_block": yourinfo_snapshot_block,
                "yourinfo_text_report": yi_text_report,
                "yourinfo_text_truncated": yi_trunc or bool(
                    isinstance(yi, dict) and yi.get("text_excerpt_truncated"),
                ),
                "framework_block": framework_block,
                "framework_risk_line": framework_risk_line,
                "has_framework": bool(fw_raw),
                "full_normalized_block": full_normalized_block,
                "truncation_notes": truncation_notes,
                "has_truncated_blocks": bool(truncation_notes),
                "web_exposure": per_location_web_exposure(data),
                "methodology_pcap": methodology_and_pcap_sections(data),
            },
        )
    return detailed


def generate_vpn_report(
    provider_slug: str,
    *,
    vpn_name: str | None = None,
    progress_step: ProgressStep | None = None,
) -> Path:
    if progress_step is not None:
        progress_step("Report: collect normalized runs")
    rows = collect_normalized_for_provider(provider_slug)
    if not rows:
        runs = repo_root() / "runs"
        hint = (
            f"No files matched runs/*/locations/*/normalized.json with "
            f'vpn_provider={provider_slug!r}. '
            f"Run a benchmark first: "
            f"`vpn-leaks run --provider {provider_slug} --skip-vpn` "
            f"(only `run` accepts --skip-vpn; then use "
            f"`vpn-leaks report --provider {provider_slug}`). "
            f"Add --force on run if this exit IP was already captured. "
            f"Runs directory: {runs}"
        )
        raise FileNotFoundError(hint)

    if progress_step is not None:
        progress_step("Report: build location matrix")
    connection_modes = sorted({r[2].get("connection_mode") or "unknown" for r in rows})
    table_rows: list[dict[str, Any]] = []
    asn_notes: dict[int, str] = {}
    run_ids: list[str] = sorted({r[0] for r in rows})

    for _run_id, _path, data in rows:
        loc = data.get("vpn_location_label") or data.get("vpn_location_id")
        display = format_benchmark_location_display(data) or str(loc)
        table_rows.append(
            {
                "label": display,
                "dns": data.get("dns_leak_flag"),
                "webrtc": data.get("webrtc_leak_flag"),
                "ipv6": data.get("ipv6_leak_flag"),
            },
        )
        att = data.get("attribution") or {}
        asn = att.get("asn")
        if isinstance(asn, int):
            asn_notes.setdefault(asn, att.get("holder") or "")

    if progress_step is not None:
        progress_step("Report: build detailed sections")
    detailed_runs = build_detailed_runs(rows)
    pcap_intel_per_run = {
        d["run_id"]: d["methodology_pcap"]["pcap_hosts"]
        for d in detailed_runs
    }
    if progress_step is not None:
        progress_step("Report: framework rollup")
    framework_rollup = build_framework_rollup(rows)
    if progress_step is not None:
        progress_step("Report: web exposure rollup")
    web_exposure = rollup_web_exposure(rows)
    generated_utc = datetime.now(UTC).isoformat()

    env = _jinja_env()
    tpl = env.get_template("vpn_report.md.j2")
    if progress_step is not None:
        progress_step("Report: render markdown")
    text = tpl.render(
        vpn_name=vpn_name or provider_slug,
        vpn_slug=provider_slug,
        generated_utc=generated_utc,
        run_ids=run_ids,
        connection_modes=connection_modes,
        locations=[r[2].get("vpn_location_id") for r in rows],
        table_rows=table_rows,
        asn_notes=[(a, asn_notes[a]) for a in sorted(asn_notes.keys())],
        detailed_runs=detailed_runs,
        run_count=len(rows),
        framework_rollup=framework_rollup,
        web_exposure=web_exposure,
    )
    out_dir = repo_root() / "VPNs"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = provider_slug.upper().replace("-", "_")
    out_path = out_dir / f"{safe}.md"
    if progress_step is not None:
        progress_step("Report: write markdown")
    out_path.write_text(text, encoding="utf-8")

    display_name = vpn_name or provider_slug
    from vpn_leaks.reporting.exposure_graph import build_exposure_graph

    if progress_step is not None:
        progress_step("Report: build exposure graph")
    exposure_payload = build_exposure_graph(provider_slug)
    html_tpl = env.get_template("vpn_report_document.html.j2")
    report_css = _load_report_static_file("report.css")
    logo_raw = _load_report_static_file("logo-isotype.svg")
    if progress_step is not None:
        progress_step("Report: build HTML dashboard")
    idle_telemetry = load_idle_telemetry_latest(provider_slug)
    dashboard = build_html_dashboard_context(
        rows,
        framework_rollup,
        markdown_basename=f"{safe}.md",
        pcap_intel_per_run=pcap_intel_per_run,
        idle_telemetry=idle_telemetry,
    )
    if progress_step is not None:
        progress_step("Report: render HTML")
    html_doc = html_tpl.render(
        document_title=f"{display_name} ({provider_slug})",
        generated_utc=generated_utc,
        vpn_slug=provider_slug,
        framework_rollup=framework_rollup,
        exposure_graph_json=_json_for_html_script(exposure_payload),
        report_html=Markup(markdown_to_html_body(text)),
        report_css=Markup(report_css) if report_css else Markup(""),
        logo_svg=Markup(logo_raw) if logo_raw else Markup(""),
        dashboard=dashboard,
    )
    html_path = out_dir / f"{safe}.html"
    if progress_step is not None:
        progress_step("Report: write HTML")
    html_path.write_text(html_doc, encoding="utf-8")

    return out_path


def generate_provider_report(
    asn: int,
    *,
    title: str | None = None,
    progress_step: ProgressStep | None = None,
) -> Path:
    """Aggregate markdown for an underlay ASN across VPNs."""
    if progress_step is not None:
        progress_step("Provider report: collect evidence")
    runs = repo_root() / "runs"
    evidence_blocks: list[dict[str, str]] = []
    policy_hashes: list[dict[str, Any]] = []

    if runs.is_dir():
        for run_dir in sorted(runs.iterdir()):
            loc_root = run_dir / "locations"
            loc_dirs = list(loc_root.glob("*")) if loc_root.is_dir() else []
            for loc_dir in loc_dirs:
                p = loc_dir / "normalized.json"
                if not p.is_file():
                    continue
                data = json.loads(p.read_text(encoding="utf-8"))
                att = data.get("attribution") or {}
                if att.get("asn") != asn:
                    continue
                raw_path = run_dir / "raw" / loc_dir.name / "attribution.json"
                body = ""
                if raw_path.is_file():
                    body = raw_path.read_text(encoding="utf-8", errors="replace")[:8000]
                evidence_blocks.append(
                    {
                        "title": f"{run_dir.name} / {loc_dir.name}",
                        "body": body or json.dumps(att, indent=2),
                    },
                )
                for pol in data.get("policies") or []:
                    if pol.get("sha256") and pol.get("url"):
                        policy_hashes.append(
                            {
                                "url": pol["url"],
                                "sha256": pol["sha256"],
                                "fetched_at": pol.get("fetched_at_utc"),
                            },
                        )

    env = _jinja_env()
    tpl = env.get_template("provider_report.md.j2")
    if progress_step is not None:
        progress_step("Provider report: render markdown")
    text = tpl.render(
        provider_title=title or f"AS{asn}",
        generated_utc=datetime.now(UTC).isoformat(),
        evidence_blocks=evidence_blocks,
        policy_hashes=policy_hashes,
    )
    out_dir = repo_root() / "PROVIDERS"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"AS{asn}.md"
    if progress_step is not None:
        progress_step("Provider report: write markdown")
    out_path.write_text(text, encoding="utf-8")
    return out_path


def write_run_summary(run_root: Path, normalized_paths: list[Path]) -> Path:
    lines = [
        "# Run summary",
        "",
        f"- Run directory: `{run_root}`",
        f"- Locations: {len(normalized_paths)}",
        "",
    ]
    for p in normalized_paths:
        lines.append(f"- `{p.relative_to(repo_root())}`")

    slug: str | None = None
    if normalized_paths:
        try:
            first = json.loads(normalized_paths[0].read_text(encoding="utf-8"))
            slug = first.get("vpn_provider")
        except (OSError, json.JSONDecodeError, TypeError):
            slug = None

    if slug:
        safe = slug.upper().replace("-", "_")
        rollup = (
            f"- Markdown rollup (matrix plus **Detailed runs** per location): "
            f"`VPNs/{safe}.md` — regenerate with `vpn-leaks report --provider {slug}`"
        )
        canon = (
            "- Canonical JSON per location: "
            "`runs/<run_id>/locations/<location_id>/normalized.json` (paths above)."
        )
        lines.extend(["", "## Aggregated report", "", rollup, canon])

    out = run_root / "summary.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
