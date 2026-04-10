"""Unit tests for policy fetch helpers."""

from __future__ import annotations

from vpn_leaks.policy.fetch_policy import (
    _looks_like_cloudflare_challenge,
    _needs_playwright_for_spa,
)


def test_cloudflare_challenge_detection() -> None:
    html = b'<!DOCTYPE html><html><head><title>Just a moment...</title></head></html>'
    assert _looks_like_cloudflare_challenge(html) is True
    assert _looks_like_cloudflare_challenge(b"<html>Privacy Policy</html>") is False


def test_nord_account_spa_shell_triggers_playwright() -> None:
    url = "https://my.nordaccount.com/legal/privacy-policy/"
    small = b"<html>" + b"x" * 1000
    big = b"<html>" + b"x" * 100_000
    assert _needs_playwright_for_spa(url, small) is True
    assert _needs_playwright_for_spa(url, big) is False
    assert _needs_playwright_for_spa("https://nordvpn.com/privacy-policy/", small) is False
