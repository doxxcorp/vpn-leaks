<p align="center">
  <img src="vpn-leaks.png" alt="VPN Leaks" width="320" />
</p>

# VPN Leaks

Repeatable client-side benchmarking for VPN services: exit IP, DNS leaks, IPv6, WebRTC, underlay ASN attribution, policy capture, and optional **competitor-surface** probes (provider DNS, web/CDN/HAR, portals, traceroute transit, stray JSON paths) configured per provider in `configs/vpns/<slug>.yaml` under `competitor_probe`.

- **Operational overview:** [docs/spec.md](docs/spec.md)  
- **Run order & methodology:** [docs/methodology.md](docs/methodology.md)  
- **Fields & paths:** [docs/data-dictionary.md](docs/data-dictionary.md)  
- **Full product spec:** [vpn-leaks.md](vpn-leaks.md)
- **Agent handoff (context for AI/humans):** [HANDOFF.md](HANDOFF.md)

## Directory index

Generated and local benchmark data live under three top-level folders (each may be empty until you run reports or benchmarks):

| Directory | Purpose |
|-----------|---------|
| **[VPNs/](VPNs/)** | Aggregated per-provider markdown from `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md` (slug uppercased; `-` → `_`). |
| **[PROVIDERS/](PROVIDERS/)** | Per-underlay ASN markdown from `vpn-leaks report --provider <slug> --asn <n>` → `PROVIDERS/AS<n>.md`. |
| **[runs/](runs/)** | One directory per `vpn-leaks run` (gitignored if you add `runs/` to `.gitignore`; contains raw captures and `normalized.json`). |

**VPNs** (checked in when present):

- [NORDVPN.md](VPNs/NORDVPN.md)

**PROVIDERS** (example path once generated):

- `PROVIDERS/AS<n>.md` — replace `<n>` with the ASN you pass to `--asn`.

**runs** (local benchmark folders; structure is identical for each run id):

- [nordvpn-20260410T014115Z-192ddf81](runs/nordvpn-20260410T014115Z-192ddf81/)
- [nordvpn-20260410T020850Z-06046ac5](runs/nordvpn-20260410T020850Z-06046ac5/)
- [nordvpn-20260410T020935Z-8559f9bc](runs/nordvpn-20260410T020935Z-8559f9bc/)
- [nordvpn-20260410T021013Z-3db4d1ec](runs/nordvpn-20260410T021013Z-3db4d1ec/)
- [nordvpn-20260410T021116Z-5cf8e0dc](runs/nordvpn-20260410T021116Z-5cf8e0dc/)

Inside each run: `run.json`, `summary.md`, `raw/preflight.json`, `locations/<location_id>/normalized.json`, and `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy).

## Ethics and legal

- Only test services you have paid access to.
- Do not bypass access controls, exploit vulnerabilities, or load-test infrastructure.
- Automated signups and vendor API scraping are **opt-in** (ToS risk).

## Security

- **Never commit VPN credentials.** Use environment variables or an encrypted secrets store.
- **Packet capture is off by default** (`--pcap` if added later); test traffic can still contain sensitive data.
- Third-party leak-test sites may log your exit IP and user agent; the harness records which endpoints were contacted.

## Setup

```bash
cd /path/to/vpn-leaks
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
```

Copy `.env.example` to `.env` and set variables referenced by your VPN config (credential env var names only in YAML).

## Configuration

- `configs/vpns/<slug>.yaml` — provider, connection mode, credential env names (see `nordvpn.yaml` for GUI-app workflow).
- `configs/tools/leak-tests.yaml` — endpoints, timeouts, STUN servers for WebRTC.
- `configs/tools/attribution.yaml` — RIPEstat, Team Cymru, PeeringDB, optional GeoLite path.

## Run

Every `run` starts with a **preflight** check (quick exit IPv4):

1. **Duplicate guard:** If that IPv4 was already recorded in any prior `runs/*/locations/*/normalized.json` for this **same `--provider`**, the command **exits without running tests** (no new run folder). Use **`--force`** to run the full suite anyway (also overwrites an existing `normalized.json` in the current run when reusing a run id).
2. **Location:** If you **omit `--locations`**, the tool calls **ipwho.is** on your exit IP, builds a **`location_id`** (country/region/city + last octet) and **label**, appends them to `configs/vpns/<slug>.yaml` (unless **`--no-persist-locations`**), and stores geo metadata under **`extra.exit_geo`** in `normalized.json`. Pass **`--locations id ...`** for manual ids instead (**`--no-auto-location`** requires explicit locations).

```bash
# Auto location (default): connect VPN, then:
vpn-leaks run --provider nordvpn --skip-vpn
vpn-leaks report --provider nordvpn

# Manual location id (still runs preflight + duplicate check):
vpn-leaks run --provider nordvpn --skip-vpn --locations uk --location-label "United Kingdom"

# Repeat benchmark on same exit IP (e.g. second dry run):
vpn-leaks run --provider example --dry-run --force
```

- Adapters with `manual_gui` pause for connect/disconnect unless you use **`--skip-vpn`**.

### NordVPN (macOS app or other GUI)

Connect in the **NordVPN app** first, then run with **`--skip-vpn`** so the harness does not drive the adapter. Prefer **omitting `--locations`** so the active server is reflected via **geo + exit IP** in the config and report.

**Manual ids:** You can still pass **`--locations <id>`**; new ids are **appended** to the YAML by default (**`--no-persist-locations`** to skip). YAML rewrites may drop comments (PyYAML).

Artifacts: `runs/<run_id>/` (gitignored), including `raw/preflight.json`.

## Reports

- Per-run: `runs/<run_id>/summary.md`, `locations/<id>/normalized.json`
- Aggregated: `VPNs/<COMPANY>.md`, `PROVIDERS/AS<asn>.md` (via `vpn-leaks report`)

| Report | Command |
|--------|---------|
| Per-VPN rollup | `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md` |
| Underlay (ASN) | `vpn-leaks report --provider <slug> --asn <n>` → `PROVIDERS/AS<n>.md` |

Add `runs/` (and optionally `VPNs/` / `PROVIDERS/`) to `.gitignore` if you do not want local reports or run artifacts in version control.

## Development

```bash
ruff check vpn_leaks tests
pytest tests -q
```

CI is not checked in under `.github/workflows/` (GitHub OAuth requires the `workflow` scope to push workflow files). Copy [docs/github-actions-ci.yml.example](docs/github-actions-ci.yml.example) to `.github/workflows/ci.yml` locally or after refreshing `gh auth refresh -s workflow`. It runs lint and tests without a live VPN (mocks only).
