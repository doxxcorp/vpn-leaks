# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium    # Required for WebRTC checks and policy fetch fallback

# Lint & test
ruff check vpn_leaks tests     # E, F, I, UP rules; 100-char line length
pytest tests -q                # All tests
pytest tests/test_dns.py -v    # Single test file

# CLI
vpn-leaks run --provider nordvpn --skip-vpn      # Run all leak checks (skip VPN connection)
vpn-leaks report --provider nordvpn              # Generate MD + HTML reports
vpn-leaks capture start [-i en0]                 # Start background PCAP (tcpdump, needs sudo)
vpn-leaks pcap-summarize <file.pcap>             # Repair/regenerate pcap_summary.json
vpn-leaks graph-export [--provider slug]         # Export 3D graph JSON

# GitHub Pages
python3 scripts/build_github_pages_site.py       # Stage site/ for deployment
```

## Architecture

The harness runs a sequential pipeline per VPN location:

1. **Config loading** (`config_loader.py`) — reads `configs/vpns/<slug>.yaml` (provider/locations/policy URLs), `configs/tools/leak-tests.yaml` (endpoints, timeouts), and `configs/tools/attribution.yaml` (RIPEstat/Cymru/PeeringDB).

2. **Checks** (`checks/`) — exit IP detection, DNS leak, IPv6, WebRTC (via Playwright), browser fingerprint, optional competitor/surface/yourinfo probes. Each check writes a raw JSON file under `runs/<run_id>/raw/<location_id>/`.

3. **Attribution** (`attribution/`) — enriches exit IPs via RIPEstat API, Team Cymru whois, and PeeringDB. Results are merged into a confidence-scored `AttributionResult`.

4. **Policy fetch** (`policy/`) — fetches privacy policy HTML via httpx with Playwright fallback for Cloudflare-protected pages. Hashes content (SHA-256) and extracts keyword bullets.

5. **Website exposure methodology** (`checks/website_exposure_methodology.py`) — automated Phases 1–9: DNS probes, HAR capture via Playwright, third-party domain classification, and CDN/tracker inventory from HAR (`checks/har_summary.py`).

6. **PCAP finalize** (`capture/finalize_bundle.py`) — stops tcpdump, moves `.pcap` to the run folder, runs dpkt-based summarization (`checks/pcap_summarize.py`). No Wireshark/tshark dependency.

7. **Normalize** (`models.py`) — all check outputs are assembled into a `NormalizedRun` Pydantic model (schema v1.5) and written to `runs/<run_id>/locations/<location_id>/normalized.json`.

8. **Framework** (`framework/`) — maps observations to a SPEC question bank (YAML), scores risk levels, and synthesizes findings.

9. **Reports** (`reporting/`) — Jinja2 templates render per-provider rollup (`VPNs/<SLUG>.md` + `.html`) and per-ASN underlay (`PROVIDERS/AS<n>.md`) from all normalized.json files for a provider.

## Key Conventions

**Adding a new check:** Implement in `checks/`, write raw JSON to `runs/.../raw/`, add a field to `NormalizedRun` in `models.py`, map it in the framework coverage (`framework/coverage.py`), and surface it in the report template.

**Adding a VPN provider:** Copy `configs/vpns/example.yaml`, set `slug` (lowercase, hyphens/underscores only), `connection_mode` (`manual_gui` or `wireguard`), and `locations`. Provider config is auto-created with defaults if missing on first `run`.

**`--skip-vpn`:** Skips `adapter.connect()` entirely — useful for testing the harness logic without an active tunnel. The exit IP will be your real IP.

**PCAP capture modes:**
- `capture start` → background tcpdump session tracked in `.vpn-leaks/capture/`
- `--attach-capture` → the `run` command starts/stops tcpdump around the test window
- `--with-pcap <file>` → supply an existing PCAP for summarization only

**Progress output:** `tqdm` on TTY, plain `[n/total] phase` lines on stderr when not a TTY (CI-friendly). The `RunProgress` wrapper in `run_progress.py` handles both.

**Artifact paths** are relative to the run root and tracked in `ArtifactIndex` within `NormalizedRun.artifacts`. Always use these paths when referencing files in reports rather than constructing paths manually.
