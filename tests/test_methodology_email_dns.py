"""Unit tests for methodology email/DNS TXT parsing."""

from __future__ import annotations

from dns.exception import DNSException
from dns.rdatatype import RdataType

from vpn_leaks.checks.methodology_email_dns import (
    parse_dmarc_aggregate_record,
    summarize_spf_mechanisms,
)
from vpn_leaks.checks.website_exposure_methodology import _walk_spf_includes


class _TxtRR:
    def __init__(self, s: str) -> None:
        self.strings = (s.encode("utf-8"),)


class _FakeResolverIncludes:
    def __init__(self, txt_by_domain: dict[str, list[str]]) -> None:
        self._txt_by_domain = {k.lower().rstrip("."): v for k, v in txt_by_domain.items()}

    def resolve(self, domain: str, rdtype):  # noqa: ANN001
        if rdtype != RdataType.TXT:
            raise DNSException(f"unsupported {rdtype}")
        key = str(domain).lower().rstrip(".")
        blobs = self._txt_by_domain.get(key)
        if blobs is None:
            raise DNSException(f"nx {key}")
        return [_TxtRR(x) for x in blobs]


def test_parse_dmarc_basic() -> None:
    txt = 'v=DMARC1;p=reject;rua=mailto:dmarc@test.invalid;pct=100'
    r = parse_dmarc_aggregate_record(txt)
    assert r["p"] == "reject"
    assert r["pct"] == "100"
    assert r["rua"] == "mailto:dmarc@test.invalid"


def test_parse_dmarc_no_version() -> None:
    assert parse_dmarc_aggregate_record("p=none")["p"] is None


def test_summarize_spf_includes_redirect() -> None:
    s = "v=spf1 include:_spf.vendor.test redirect=spf.mail.test -all"
    m = summarize_spf_mechanisms(s)
    assert "_spf.vendor.test" in m["include"]
    assert "spf.mail.test" in m["redirect"]


def test_walk_spf_expand_chain() -> None:
    tbl = {
        "apex.test": ["v=spf1 include:include1.apex.test -all"],
        "include1.apex.test": ["v=spf1 include:include2.apex.test -all"],
        "include2.apex.test": ["v=spf1 ip4:192.0.2.10 -all"],
    }
    res = _FakeResolverIncludes(tbl)
    services: list[str] = []
    inc, errs = _walk_spf_includes(
        res,
        "apex.test",
        seen=set(),
        depth=0,
        services_contacted=services,
    )
    assert "include1.apex.test" in inc and "include2.apex.test" in inc
    assert not errs


def test_walk_spf_recursion_cap() -> None:
    """Circular include stops via `seen`; no stack blowup."""
    tbl = {
        "loop.test": ["v=spf1 include:loop.test -all"],
    }
    res = _FakeResolverIncludes(tbl)
    inc, errs = _walk_spf_includes(res, "loop.test", seen=set(), depth=0, services_contacted=[])
    assert "loop.test" in inc
    assert not errs


def test_walk_spf_respects_max_depth() -> None:
    tbl = {
        "a.maxd.test": ["v=spf1 include:b.maxd.test -all"],
        "b.maxd.test": ["v=spf1 include:c.maxd.test -all"],
        "c.maxd.test": ["v=spf1 ip4:203.0.113.77 -all"],
    }
    res = _FakeResolverIncludes(tbl)
    shallow, _e = _walk_spf_includes(
        res,
        "a.maxd.test",
        seen=set(),
        depth=0,
        services_contacted=[],
        max_depth=0,
    )
    assert "b.maxd.test" in shallow
    assert "c.maxd.test" not in shallow

