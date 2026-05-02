"""Tests for PCAP host intelligence report payload."""

from __future__ import annotations

from vpn_leaks.reporting import web_exposure


def test_pcap_host_intelligence_scope_and_merge(monkeypatch) -> None:
    def fake_run_cmd(args: list[str], timeout_s: int) -> tuple[str, str | None]:
        if args[0] == "dig" and args[1:3] == ["+short", "-x"]:
            return "ptr.peer.example.\n", None
        if args[0] == "dig" and args[-1] == "A":
            return "8.8.8.8\n10.0.0.2\n", None
        if args[0] == "dig" and args[-1] == "AAAA":
            return "", None
        if args[0] == "dig" and args[-1] == "CNAME":
            return "", None
        if args[0] == "dig" and args[-1] == "MX":
            return "", None
        if args[0] == "dig" and args[-1] == "TXT":
            return '"v=spf1 -all"\n', None
        if args[0] == "whois":
            return "OrgName: Test Org\norigin: AS15169\nCountry: US\n", None
        return "", None

    monkeypatch.setattr(web_exposure, "_run_cmd", fake_run_cmd)
    monkeypatch.setattr(
        web_exposure.socket,
        "gethostbyaddr",
        lambda ip: (f"ptr-{ip}.example", [], []),
    )

    payload = web_exposure.pcap_host_intelligence(
        {
            "pcap_derived": {
                "flows_sample": [
                    {"key": ["ip4", "08080808", "0a000001", "443", "12345"], "bytes": 100},
                    {"key": ["ip4", "01010101", "08080808", "443", "54321"], "bytes": 200},
                ],
                "top_inet_pairs_sample": [
                    {"src": "8.8.8.8", "dst": "1.1.1.1", "bytes": 10},
                    {"src": "10.0.0.1", "dst": "8.8.8.8", "bytes": 10},
                ],
                "dns_hostnames_unique": ["api.example.com", "api.example.com"],
                "tls_clienthello_snis_unique": ["api.example.com", "sni.example.net"],
            },
        },
    )

    assert payload["has_inventory"] is True
    rows = payload["rows"]
    row_hosts = {r["host"] for r in rows}
    assert "8.8.8.8" in row_hosts
    assert "1.1.1.1" in row_hosts
    assert "10.0.0.1" not in row_hosts
    assert "api.example.com" in row_hosts
    api_row = next(r for r in rows if r["host"] == "api.example.com")
    assert api_row["source"] == "pcap_dns+pcap_sni"
    assert "8.8.8.8" in api_row["ips"]


def test_pcap_host_intelligence_failsoft(monkeypatch) -> None:
    def fake_run_cmd(args: list[str], timeout_s: int) -> tuple[str, str | None]:
        if args[0] == "dig":
            return "", "timeout:dig"
        if args[0] == "whois":
            return "", "timeout:whois"
        return "", "error"

    monkeypatch.setattr(web_exposure, "_run_cmd", fake_run_cmd)
    monkeypatch.setattr(
        web_exposure.socket,
        "gethostbyaddr",
        lambda ip: (_ for _ in ()).throw(OSError("boom")),
    )
    # Cymru uses a raw socket connection, not _run_cmd — stub it out too
    monkeypatch.setattr(web_exposure, "_cymru_asn_bulk", lambda ips: {})
    # Isolate from any on-disk cache that could supply pre-resolved ASNs
    monkeypatch.setattr(web_exposure, "_load_ip_intel_cache", lambda: {})
    monkeypatch.setattr(web_exposure, "_save_ip_intel_cache", lambda: None)

    payload = web_exposure.pcap_host_intelligence(
        {
            "pcap_derived": {
                "top_inet_pairs_sample": [{"src": "8.8.8.8", "dst": "1.1.1.1", "bytes": 10}],
                "dns_hostnames_unique": ["api.example.com"],
                "tls_clienthello_snis_unique": [],
            },
        },
    )
    assert payload["has_inventory"] is True
    row = next(r for r in payload["rows"] if r["host"] == "8.8.8.8")
    assert row["asn"] == "—"
    assert row["owner"] == "—"
    assert "reverse_dns_failed" in row["lookup_errors_text"]
