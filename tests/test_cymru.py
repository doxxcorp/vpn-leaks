"""Team Cymru DNS attribution (dig)."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from vpn_leaks.attribution.cymru import cymru_asn_lookup


def test_cymru_asn_lookup_timeout_returns_error_dict():
    with patch("vpn_leaks.attribution.cymru.subprocess.run") as run_mock:
        run_mock.side_effect = subprocess.TimeoutExpired(cmd=["dig"], timeout=15)
        out = cymru_asn_lookup("8.8.8.8")
    assert "error" in out
    assert "timed out" in out["error"]
    assert out.get("disclaimer")
