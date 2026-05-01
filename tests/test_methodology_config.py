"""Website-exposure methodology config hints."""

from __future__ import annotations

from vpn_leaks.checks.website_exposure_methodology import _collect_hosts_inventory
from vpn_leaks.config_loader import methodology_config_hints


def test_methodology_hints_empty_domains_warn() -> None:
    msgs = methodology_config_hints({})
    assert any("provider_domains" in m for m in msgs)


def test_methodology_hints_policy_urls() -> None:
    msgs = methodology_config_hints({"competitor_probe": {"provider_domains": ["x.example"]}})
    assert any("policy_urls" in m for m in msgs)


def test_collect_hosts_inventory_merges_surface() -> None:
    cfg = {
        "surface_urls": [{"page_type": "home", "url": "https://www.vendor.test/price"}],
        "competitor_probe": {"probe_urls": ["https://acct.vendor.test/"], "provider_domains": []},
    }
    har = {"har_summary": {"merged_unique_hosts": ["tracker.vendor.test"]}}
    inv = _collect_hosts_inventory(cfg, None, har)
    hosts = inv.get("unique_hosts") or []
    assert "www.vendor.test" in hosts or "acct.vendor.test" in hosts
    assert "tracker.vendor.test" in hosts
