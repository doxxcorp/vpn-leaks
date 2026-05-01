"""Tests for exposure graph export."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vpn_leaks.reporting.exposure_graph import build_exposure_graph


def _patch_repo(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr("vpn_leaks.reporting.generate_reports.repo_root", lambda: tmp_path)
    monkeypatch.setattr("vpn_leaks.reporting.exposure_graph.repo_root", lambda: tmp_path)


def test_build_exposure_graph_empty(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / "runs").mkdir()
    _patch_repo(monkeypatch, tmp_path)
    g = build_exposure_graph()
    assert g["nodes"] == []
    assert g["edges"] == []


def test_build_exposure_graph_exit_and_policy(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    loc = tmp_path / "runs" / "run-a" / "locations" / "loc1"
    loc.mkdir(parents=True)
    norm = {
        "vpn_provider": "example",
        "vpn_location_id": "loc1",
        "exit_ip_v4": "203.0.113.1",
        "attribution": {"asn": 64496, "holder": "Example"},
        "policies": [{"url": "https://example.com/privacy", "role": "vpn"}],
    }
    (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")
    _patch_repo(monkeypatch, tmp_path)
    g = build_exposure_graph()
    ids = {n["id"] for n in g["nodes"]}
    assert "vpn:example" in ids
    assert "ip:203.0.113.1" in ids
    assert "asn:64496" in ids
    rels = {e["relation"] for e in g["edges"]}
    assert "exit_ip" in rels
    assert "attributed_as" in rels
    assert "policy_document" in rels


def test_build_exposure_graph_provider_filter(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    for slug, rid in [("a", "r1"), ("b", "r2")]:
        loc = tmp_path / "runs" / rid / "locations" / "loc"
        loc.mkdir(parents=True)
        ip = "198.51.100.1" if slug == "a" else "198.51.100.2"
        norm = {
            "vpn_provider": slug,
            "vpn_location_id": "loc",
            "exit_ip_v4": ip,
            "attribution": {},
        }
        (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")
    _patch_repo(monkeypatch, tmp_path)
    g = build_exposure_graph("a")
    ids = {n["id"] for n in g["nodes"]}
    assert "vpn:a" in ids
    assert "vpn:b" not in ids


def test_build_exposure_graph_pcap_edges(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    loc = tmp_path / "runs" / "run-p" / "locations" / "loc1"
    loc.mkdir(parents=True)
    norm = {
        "vpn_provider": "example",
        "vpn_location_id": "loc1",
        "exit_ip_v4": "203.0.113.45",
        "attribution": {},
        "competitor_surface": None,
        "pcap_derived": {
            "top_inet_pairs_sample": [{"src": "10.1.2.3", "dst": "8.8.8.8", "bytes": 42}],
            "tls_clienthello_snis_unique": ["api.vendor.example"],
        },
    }
    (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")
    _patch_repo(monkeypatch, tmp_path)
    g = build_exposure_graph()
    relations = [e["relation"] for e in g["edges"]]
    assert "pcap_ip_flow" in relations
    assert "tls_sni_observed" in relations
    assert any(n["type"] == "tls_sni" for n in g["nodes"])
