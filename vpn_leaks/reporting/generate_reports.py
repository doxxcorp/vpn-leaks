"""Generate markdown reports from normalized run JSON files."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from vpn_leaks.config_loader import repo_root


def _jinja_env() -> Environment:
    tpl_dir = Path(__file__).resolve().parent / "templates"
    return Environment(
        loader=FileSystemLoader(str(tpl_dir)),
        autoescape=select_autoescape(enabled_extensions=(".html",)),
    )


def collect_normalized_for_provider(provider_slug: str) -> list[tuple[str, Path, dict[str, Any]]]:
    """Return list of (run_id, path, data) for all normalized.json under runs/."""
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
            if data.get("vpn_provider") != provider_slug:
                continue
            out.append((run_dir.name, p, data))
    return out


def generate_vpn_report(provider_slug: str, *, vpn_name: str | None = None) -> Path:
    rows = collect_normalized_for_provider(provider_slug)
    if not rows:
        raise FileNotFoundError(f"No normalized runs for provider {provider_slug!r}")

    connection_modes = sorted({r[2].get("connection_mode") or "unknown" for r in rows})
    table_rows: list[dict[str, Any]] = []
    asn_notes: dict[int, str] = {}
    run_ids: list[str] = sorted({r[0] for r in rows})

    for _run_id, _path, data in rows:
        loc = data.get("vpn_location_label") or data.get("vpn_location_id")
        table_rows.append(
            {
                "label": str(loc),
                "dns": data.get("dns_leak_flag"),
                "webrtc": data.get("webrtc_leak_flag"),
                "ipv6": data.get("ipv6_leak_flag"),
            },
        )
        att = data.get("attribution") or {}
        asn = att.get("asn")
        if isinstance(asn, int):
            asn_notes.setdefault(asn, att.get("holder") or "")

    env = _jinja_env()
    tpl = env.get_template("vpn_report.md.j2")
    text = tpl.render(
        vpn_name=vpn_name or provider_slug,
        vpn_slug=provider_slug,
        generated_utc=datetime.now(UTC).isoformat(),
        run_ids=run_ids,
        connection_modes=connection_modes,
        locations=[r[2].get("vpn_location_id") for r in rows],
        table_rows=table_rows,
        asn_notes=[(a, asn_notes[a]) for a in sorted(asn_notes.keys())],
    )
    out_dir = repo_root() / "VPNs"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = provider_slug.upper().replace("-", "_")
    out_path = out_dir / f"{safe}.md"
    out_path.write_text(text, encoding="utf-8")
    return out_path


def generate_provider_report(asn: int, *, title: str | None = None) -> Path:
    """Aggregate markdown for an underlay ASN across VPNs."""
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
    text = tpl.render(
        provider_title=title or f"AS{asn}",
        generated_utc=datetime.now(UTC).isoformat(),
        evidence_blocks=evidence_blocks,
        policy_hashes=policy_hashes,
    )
    out_dir = repo_root() / "PROVIDERS"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"AS{asn}.md"
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
    out = run_root / "summary.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
