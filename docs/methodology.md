# Methodology

## Standard run loop (one location)

1. Account ready (credentials via env/secrets; not stored in repo).
2. Connect — vendor client, WireGuard/OpenVPN config, or official CLI; or manual GUI with orchestrator prompts.
3. Stabilize — short cooldown; optional route/interface checks (logged).
4. Exit IP — multiple independent endpoints; store all responses.
5. Leak suite — DNS (local + external), WebRTC (Playwright ICE gather), IPv6 (local + external), optional fingerprint.
6. Underlay attribution — RIPEstat primary; Team Cymru cross-check; PeeringDB + optional GeoLite ASN; confidence and sources stored.
7. Policy fetch — VPN URL + underlay URLs when known; raw HTML + SHA-256 hash.
8. Disconnect — adapter disconnect; DNS flush best-effort; close browser contexts.
9. Repeat for each location.

## Isolation and reproducibility

- Prefer a dedicated VM or clean network namespace for comparable runs.
- Record OS, kernel, browser, and VPN client versions in `run.json` / `runner_env`.
- Use multi-source checks; disagreement between attribution sources lowers confidence.

## DNS and WebRTC reliability

- **DNS:** Tier A — OS resolver snapshot + controlled queries; Tier B — external leak-test pages (pinned URLs, timeouts, saved HTML). Compare baseline vs VPN state; encode platform quirks in reports when relevant.
- **WebRTC:** Controlled Playwright session with configurable STUN servers, time-bounded ICE gathering, candidate classification vs expected exit IP; retries and raw artifacts on failure.

## Manual vs automated boundaries

- Signup/payment: manual by default.
- GUI: use **prompted manual connect** when configs/CLI are unavailable; do not rely on brittle GUI scripting for MVP.
- ToS-risk automation (scraping): explicit config opt-in only.
