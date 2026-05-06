"""Tests for classify_contact_role() in web_exposure (TASK-03)."""

from __future__ import annotations

from vpn_leaks.reporting.web_exposure import classify_contact_role


def test_dns_resolver_when_only_pcap_dns_source() -> None:
    role = classify_contact_role(
        owner="Cloudflare, Inc.",
        canonical_company="Cloudflare",
        provider_name="nordvpn",
        sources="pcap_dns",
    )
    assert role == "dns-resolver"


def test_dns_resolver_takes_priority_over_company_match() -> None:
    role = classify_contact_role(
        owner="NordVPN S.A.",
        canonical_company="NordVPN",
        provider_name="nordvpn",
        sources="pcap_dns",
    )
    assert role == "dns-resolver"


def test_vpn_control_when_company_matches_provider_name() -> None:
    role = classify_contact_role(
        owner="NordVPN S.A.",
        canonical_company="NordVPN",
        provider_name="nordvpn",
        sources="pcap_peer_ip",
    )
    assert role == "vpn-control"


def test_vpn_control_with_hyphen_in_provider_name() -> None:
    role = classify_contact_role(
        owner="ExpressVPN Limited",
        canonical_company="ExpressVPN",
        provider_name="express-vpn",
        sources="pcap_peer_ip",
    )
    assert role == "vpn-control"


def test_provider_analytics_amplitude() -> None:
    role = classify_contact_role(
        owner="Amplitude, Inc.",
        canonical_company="Amplitude",
        provider_name="nordvpn",
        sources="pcap_peer_ip+pcap_sni",
    )
    assert role == "provider-analytics"


def test_provider_analytics_sentry() -> None:
    role = classify_contact_role(
        owner="Functional Software, Inc. dba Sentry",
        canonical_company="Sentry",
        provider_name="nordvpn",
        sources="pcap_peer_ip",
    )
    assert role == "provider-analytics"


def test_unknown_fallback_for_random_org() -> None:
    role = classify_contact_role(
        owner="Random Hosting Co",
        canonical_company="Random Hosting",
        provider_name="nordvpn",
        sources="pcap_peer_ip",
    )
    assert role == "unknown"


def test_unknown_when_all_inputs_empty() -> None:
    role = classify_contact_role(
        owner="",
        canonical_company="",
        provider_name="",
        sources="",
    )
    assert role == "unknown"


def test_dns_with_peer_ip_is_not_resolver() -> None:
    """If pcap_peer_ip is present alongside pcap_dns, the contact is real wire traffic."""
    role = classify_contact_role(
        owner="Cloudflare, Inc.",
        canonical_company="Cloudflare",
        provider_name="nordvpn",
        sources="pcap_peer_ip+pcap_dns",
    )
    assert role != "dns-resolver"
