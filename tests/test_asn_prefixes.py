"""RIPEstat announced-prefixes flattening."""

from __future__ import annotations

from vpn_leaks.attribution.ripestat import announced_prefix_strings


def test_announced_prefix_strings() -> None:
    raw = {
        "data": {
            "prefixes": [
                {"prefix": "192.0.2.0/24", "timelines": []},
                {"prefix": "2001:db8::/32", "timelines": []},
            ],
        },
    }
    ps = announced_prefix_strings(raw)
    assert "192.0.2.0/24" in ps
    assert "2001:db8::/32" in ps
