"""Resolve CLI location ids against VPN YAML; optionally persist new ids."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from vpn_leaks.config_loader import load_yaml, repo_root


def vpn_yaml_path(slug: str) -> Path:
    return repo_root() / "configs" / "vpns" / f"{slug}.yaml"


def _locations_from_config(vpn_config: dict[str, Any]) -> list[dict[str, Any]]:
    locs = vpn_config.get("locations") or []
    if not isinstance(locs, list):
        return []
    return [x for x in locs if isinstance(x, dict) and x.get("id") is not None]


def append_location_if_missing(slug: str, entry: dict[str, Any]) -> bool:
    """Append entry to locations in the provider YAML if id is new. Returns True if written."""
    path = vpn_yaml_path(slug)
    data = load_yaml(path)
    locs = data.get("locations")
    if not isinstance(locs, list):
        locs = []
        data["locations"] = locs
    eid = str(entry.get("id", ""))
    if not eid:
        return False
    if any(str(x.get("id")) == eid for x in locs if isinstance(x, dict)):
        return False
    locs.append({"id": entry["id"], "label": entry.get("label", eid)})
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=1000,
        )
    return True


def resolve_run_locations(
    *,
    slug: str,
    vpn_config: dict[str, Any],
    requested_ids: list[str] | None,
    location_label: str | None,
    persist: bool,
) -> list[dict[str, Any]]:
    """
    Build the ordered list of location dicts for this run.

    - If ``requested_ids`` is empty/None: all locations from config (original order).
    - If ``requested_ids`` is set: for each id, use the YAML entry if present; otherwise
      create ``{id, label}`` and optionally append to YAML when ``persist`` is True.
    """
    configured = _locations_from_config(vpn_config)
    by_id: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for x in configured:
        i = str(x["id"])
        if i not in by_id:
            order.append(i)
        by_id[i] = x

    if not requested_ids:
        return [by_id[i] for i in order]

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_id in requested_ids:
        loc_id = str(raw_id)
        if loc_id in seen:
            continue
        seen.add(loc_id)
        if loc_id in by_id:
            out.append(by_id[loc_id])
            continue
        label = (
            location_label
            if len(requested_ids) == 1 and location_label
            else loc_id
        )
        entry: dict[str, Any] = {"id": loc_id, "label": label}
        if persist:
            append_location_if_missing(slug, entry)
        out.append(entry)
    return out
