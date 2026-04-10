import json

from vpn_leaks.auto_connection import build_location_from_geo, find_prior_run_with_same_exit


def test_find_prior_run(tmp_path):
    runs = tmp_path / "runs"
    loc = runs / "r1" / "locations" / "x"
    loc.mkdir(parents=True)
    norm = loc / "normalized.json"
    norm.write_text(
        json.dumps({"vpn_provider": "nordvpn", "exit_ip_v4": "203.0.113.50"}),
        encoding="utf-8",
    )
    found = find_prior_run_with_same_exit(
        vpn_provider="nordvpn",
        exit_ip_v4="203.0.113.50",
        runs_root=runs,
    )
    assert found == norm

    assert (
        find_prior_run_with_same_exit(
            vpn_provider="nordvpn",
            exit_ip_v4="198.51.100.1",
            runs_root=runs,
        )
        is None
    )


def test_build_location_from_geo():
    lid, label, snap = build_location_from_geo(
        {
            "success": True,
            "country_code": "US",
            "region": "California",
            "city": "San Francisco",
        },
        "203.0.113.10",
    )
    assert "us" in lid
    assert "san-francisco" in lid
    assert "10" in lid
    assert "San Francisco" in label
    assert snap["location_id"] == lid
