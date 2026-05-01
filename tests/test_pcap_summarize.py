"""PCAP summarizer unit tests."""

from __future__ import annotations

import json
from pathlib import Path

import dpkt

from vpn_leaks.checks.pcap_summarize import summarize_pcap_file, write_pcap_summary_json


def test_summarize_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "nope.pcap"
    row = summarize_pcap_file(missing)
    assert row["schema_version"] == "1.0"
    assert "pcap_not_found" in (row.get("errors") or [])


def test_write_pcap_dns_roundtrip(tmp_path: Path) -> None:
    pcap = tmp_path / "mini.pcap"
    with pcap.open("wb") as f:
        pw = dpkt.pcap.Writer(f)
        udp = dpkt.udp.UDP(sport=53, dport=53)

        dns = dpkt.dns.DNS(
            id=123,
            qd=[
                dpkt.dns.DNS.Q(
                    name="vpn.example.invalid",
                    type=dpkt.dns.DNS_A,
                    cls=dpkt.dns.DNS_IN,
                ),
            ],
        )
        udp.data = bytes(dns)
        udp.ulen += len(udp.data)
        ip = dpkt.ip.IP(dst=b"\x08\x08\x08\x08", src=b"\xc0\xa8\x01\x05", p=17, data=udp, len=20)

        udp.sum = 0
        ip.len = ip.len + udp.ulen + 8
        eth = dpkt.ethernet.Ethernet(dst=b"\xff" * 6, src=b"\x02" * 6, type=2048, data=ip)

        pw.writepkt(eth.pack(), ts=1000)

    outp = tmp_path / "out.json"
    write_pcap_summary_json(pcap, outp)
    blob = json.loads(outp.read_text(encoding="utf-8"))
    assert "vpn.example.invalid" in " ".join(blob.get("dns_hostnames_unique") or [])
