"""WebRTC ICE gathering via Playwright (Chromium)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vpn_leaks.models import WebRtcCandidate

ICE_GATHER_JS = """
async (opts) => {
  const stunUrls = opts.stunUrls || [];
  const timeoutMs = opts.timeoutMs || 12000;
  const servers = stunUrls.map(u => ({ urls: u }));
  const defStun = [{ urls: 'stun:stun.l.google.com:19302' }];
  const pc = new RTCPeerConnection({ iceServers: servers.length ? servers : defStun });
  const candidates = [];
  pc.onicecandidate = (e) => {
    if (e.candidate) {
      const c = e.candidate;
      candidates.push({
        candidate_type: c.type || null,
        protocol: c.protocol || null,
        address: c.address || null,
        port: c.port || null,
        raw: c.candidate,
      });
    }
  };
  pc.createDataChannel('vpn-leaks-probe');
  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);
  await new Promise((resolve) => setTimeout(resolve, timeoutMs));
  try { pc.close(); } catch (e) {}
  return candidates;
}
"""


def run_webrtc_check(
    *,
    raw_dir: Path,
    leak_cfg: dict[str, Any],
    exit_ip_v4: str | None,
    services_contacted: list[str],
) -> tuple[list[WebRtcCandidate], bool | None, str | None]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    wcfg = leak_cfg.get("webrtc") or {}
    timeout_ms = int(wcfg.get("gather_timeout_ms") or 12000)
    stun = wcfg.get("stun_servers") or [{"urls": "stun:stun.l.google.com:19302"}]
    stun_urls = [s.get("urls") for s in stun if isinstance(s, dict) and s.get("urls")]
    services_contacted.append("webrtc:local_playwright_chromium")

    from playwright.sync_api import sync_playwright

    candidates: list[WebRtcCandidate] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            gathered = page.evaluate(
                ICE_GATHER_JS,
                {"stunUrls": stun_urls, "timeoutMs": timeout_ms},
            )
            for g in gathered or []:
                candidates.append(
                    WebRtcCandidate(
                        candidate_type=g.get("candidate_type"),
                        protocol=g.get("protocol"),
                        address=g.get("address"),
                        port=g.get("port"),
                        raw=g.get("raw"),
                    ),
                )
        finally:
            browser.close()

    (raw_dir / "webrtc_candidates.json").write_text(
        json.dumps([c.model_dump(mode="json") for c in candidates], indent=2),
        encoding="utf-8",
    )

    leak_flag, notes = _infer_webrtc_leak(candidates, exit_ip_v4)
    return candidates, leak_flag, notes


def _infer_webrtc_leak(
    candidates: list[WebRtcCandidate],
    exit_ip_v4: str | None,
) -> tuple[bool | None, str | None]:
    if not candidates:
        return None, "No ICE candidates gathered"
    addrs = [c.address for c in candidates if c.address]
    if not exit_ip_v4:
        return None, "No exit IPv4 to compare; review candidates manually"
    # srflx/host that match exit are often OK; leak if we see a different public IP in host/srflx
    public_like = [a for a in addrs if a and not a.startswith(("192.168.", "10.", "172.16."))]
    if exit_ip_v4 in public_like:
        return False, "Exit IP appears in candidate set (expected for tunneled public)"
    if public_like:
        return True, f"Public-like candidate IPs differ from exit_ip_v4: {public_like[:5]}"
    return False, "Only local/private candidates or no public comparison possible"
