"""Tests for VPN config loading and auto-creation."""

from __future__ import annotations

import pytest

from vpn_leaks.config_loader import load_vpn_config, normalize_provider_slug


def test_normalize_provider_slug() -> None:
    assert normalize_provider_slug("NordVPN") == "nordvpn"
    assert normalize_provider_slug("my-provider") == "my-provider"
    assert normalize_provider_slug("  foo_bar  ") == "foo_bar"


def test_normalize_provider_slug_rejects_invalid() -> None:
    with pytest.raises(ValueError, match="Provider slug"):
        normalize_provider_slug("")
    with pytest.raises(ValueError, match="Provider slug"):
        normalize_provider_slug("../etc/passwd")
    with pytest.raises(ValueError, match="Provider slug"):
        normalize_provider_slug("a" * 64)


def test_load_vpn_config_missing_raises(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", lambda: tmp_path)
    (tmp_path / "configs" / "vpns").mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        load_vpn_config("nordvpn", create_if_missing=False)


def test_load_vpn_config_create_if_missing(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", lambda: tmp_path)
    p = tmp_path / "configs" / "vpns" / "newvpn.yaml"
    assert not p.is_file()
    data = load_vpn_config("NewVPN", create_if_missing=True)
    assert p.is_file()
    assert data.get("slug") == "newvpn"
    assert data.get("connection_mode") == "manual_gui"
    assert data.get("provider_name") == "Newvpn"
    assert data.get("policy_urls") == []


def test_load_vpn_config_existing_unchanged(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", lambda: tmp_path)
    (tmp_path / "configs" / "vpns").mkdir(parents=True)
    p = tmp_path / "configs" / "vpns" / "x.yaml"
    p.write_text("provider_name: Custom\nslug: x\n", encoding="utf-8")
    data = load_vpn_config("x", create_if_missing=True)
    assert data.get("provider_name") == "Custom"
