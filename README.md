# VPN Leaks

Repeatable client-side benchmarking for VPN services: exit IP, DNS leaks, IPv6, WebRTC, underlay ASN attribution, and policy capture. See [docs/spec.md](docs/spec.md) and the full [vpn-leaks.md](vpn-leaks.md) specification.

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

- `configs/vpns/<slug>.yaml` — provider, connection mode, credential env names.
- `configs/tools/leak-tests.yaml` — endpoints, timeouts, STUN servers for WebRTC.
- `configs/tools/attribution.yaml` — RIPEstat, Team Cymru, PeeringDB, optional GeoLite path.

## Run

```bash
vpn-leaks run --provider example --locations us-east
vpn-leaks run --provider example --resume
vpn-leaks report --provider example
```

- **`--force`**: re-run locations even if outputs exist.
- Adapters with `manual_gui` pause for you to connect in the vendor app before tests proceed.

Artifacts are written under `runs/<run_id>/` (gitignored).

## Reports

- Per-run: `runs/<run_id>/summary.md`, `locations/<id>/normalized.json`
- Aggregated: `VPNs/<COMPANY>.md`, `PROVIDERS/AS<asn>.md` (via `vpn-leaks report`)

| Report | Command |
|--------|---------|
| Per-VPN rollup | `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md` |
| Underlay (ASN) | `vpn-leaks report --provider <slug> --asn <n>` → `PROVIDERS/AS<n>.md` |

## Development

```bash
ruff check vpn_leaks tests
pytest tests -q
```

CI runs lint and tests without a live VPN (mocks only).
