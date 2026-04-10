import textwrap

from vpn_leaks.config_loader import load_yaml
from vpn_leaks.vpn_config_locations import resolve_run_locations


def test_resolve_unknown_persists(monkeypatch, tmp_path):
    monkeypatch.setattr("vpn_leaks.vpn_config_locations.repo_root", lambda: tmp_path)
    cfg_dir = tmp_path / "configs" / "vpns"
    cfg_dir.mkdir(parents=True)
    ypath = cfg_dir / "nordvpn.yaml"
    ypath.write_text(
        textwrap.dedent(
            """
            provider_name: "NordVPN"
            slug: nordvpn
            locations:
              - id: sf-usa
                label: "SF"
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    vpn_config = load_yaml(ypath)

    out = resolve_run_locations(
        slug="nordvpn",
        vpn_config=vpn_config,
        requested_ids=["uk"],
        location_label="United Kingdom",
        persist=True,
    )
    assert len(out) == 1
    assert out[0]["id"] == "uk"
    assert out[0]["label"] == "United Kingdom"

    text = ypath.read_text(encoding="utf-8")
    assert "uk" in text
    assert "United Kingdom" in text


def test_resolve_existing_no_write(monkeypatch, tmp_path):
    monkeypatch.setattr("vpn_leaks.vpn_config_locations.repo_root", lambda: tmp_path)
    cfg_dir = tmp_path / "configs" / "vpns"
    cfg_dir.mkdir(parents=True)
    ypath = cfg_dir / "nordvpn.yaml"
    original = "provider_name: X\nslug: nordvpn\nlocations:\n  - id: a\n    label: A\n"
    ypath.write_text(original, encoding="utf-8")
    vpn_config = load_yaml(ypath)

    out = resolve_run_locations(
        slug="nordvpn",
        vpn_config=vpn_config,
        requested_ids=["a"],
        location_label="ignored",
        persist=True,
    )
    assert out[0]["label"] == "A"
    assert ypath.read_text(encoding="utf-8") == original

