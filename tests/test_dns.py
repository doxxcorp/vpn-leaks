from vpn_leaks.checks.dns import _infer_dns_leak
from vpn_leaks.models import DnsObservation


def test_dns_leak_public_resolver():
    obs = [
        DnsObservation(tier="external", detail="t", servers=["8.8.8.8"]),
    ]
    flag, _notes = _infer_dns_leak(obs, "1.2.3.4")
    assert flag is True


def test_dns_no_external():
    obs = [DnsObservation(tier="local", detail="r", servers=["127.0.0.53"])]
    flag, notes = _infer_dns_leak(obs, None)
    assert flag is None
    assert notes is not None
