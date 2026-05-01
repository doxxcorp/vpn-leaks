<p align="center">
  <img src="vpn-leaks.png" alt="VPN Leaks" width="320" />
</p>

# VPN Leaks

Repeatable client-side benchmarking for VPN services: exit IP, DNS leaks, IPv6, WebRTC, underlay ASN attribution, policy capture, always-on **yourinfo.ai** load (Playwright HAR + excerpt; skip with `--skip-yourinfo`), and optional **competitor-surface** probes (provider DNS, web/CDN/HAR, portals, transit, stray JSON) via `competitor_probe` in `configs/vpns/<slug>.yaml`. The **`vpn-leaks report`** rollup mirrors normalized fields per run (large JSON may be truncated; see each `normalized.json` for full fidelity).

- **Operational overview:** [docs/spec.md](docs/spec.md)  
- **SPEC framework (question bank, coverage):** [docs/framework.md](docs/framework.md)  
- **Run order & methodology:** [docs/methodology.md](docs/methodology.md)  
- **Website third-party exposure analysis:** [docs/website-exposure-methodology.md](docs/website-exposure-methodology.md)  
- **Competitive capture (UTM, `capture start` → `run --attach-capture`, PCAP plan):** [docs/competitive-capture-playbook.md](docs/competitive-capture-playbook.md)  
- **Research questions, evidence map, desk playbook, FD graphs:** [docs/research-questions-and-evidence.md](docs/research-questions-and-evidence.md)  
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
| **[viewer/](viewer/)** | Static **3D exposure graph** (loads JSON from `vpn-leaks graph-export`); see [viewer/README.md](viewer/README.md). |

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

## Purpose

This project measures **client-observable** privacy exposure—leaks, attribution, policy text—to assess how far competitor VPN offerings can be trusted with user traffic. It is normal security and competitive benchmarking: observe what the tunnel and related surfaces reveal, not attacks on vendor systems.

## Security

- **Never commit VPN credentials.** Use environment variables or an encrypted secrets store.
- **Packet capture is optional** (`capture start` + `run --attach-capture`, or `run --with-pcap`). Treat PCAP as sensitive operational data (tokens, IPs, endpoints).
- Third-party leak-test sites may log your exit IP and user agent; the harness records which endpoints were contacted.

## Setup

```bash
cd /path/to/vpn-leaks
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# Optional placeholder extra for future PCAP fingerprint addons (currently empty; core parsing uses dpkt):
# pip install -e ".[dev,pcap]"
playwright install chromium
```

Copy `.env.example` to `.env` and set variables referenced by your VPN config (credential env var names only in YAML).

## Configuration

- `configs/vpns/<slug>.yaml` — provider, connection mode, credential env names (see `example.yaml`). If the file is missing, **`vpn-leaks run`** and **`vpn-leaks report`** create a minimal default YAML (slug must be `a-z0-9`, hyphens, underscores; lowercased for the filename) so you can edit and re-run.
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
- **`--skip-yourinfo`** skips the third-party yourinfo.ai benchmark (saves time if the page is slow).

### Packet capture (tcpdump → `pcap_derived`)

PCAP stays **outside** Wireshark/`tshark`/mitmproxy on the supported path—summarization is **Python/`dpkt`** (`pcap_summary.json`). Default interface is **`en0`** or override with **`VPN_LEAKS_CAPTURE_INTERFACE`**. **`tcpdump`** usually needs **sudo** on macOS: run **`sudo vpn-leaks capture start`** and **`sudo vpn-leaks run … --attach-capture`** from the **repo root** so BPF access and finalize (tcpdump teardown) run as the same user (see [docs/competitive-capture-playbook.md](docs/competitive-capture-playbook.md) § *tcpdump privileges*, [HANDOFF.md](HANDOFF.md)).

| Mode | When | Commands |
|------|------|-----------|
| **Competitive** (signup / install / marketing in PCAP) | Default competitive story — start PCAP *before* browser/app work | **`vpn-leaks capture start`** (`-i`/ `--interface iface`, optional `--bpf` filter) … then on-VPN **`vpn-leaks run --provider <slug> --skip-vpn --attach-capture`** |
| **Harness window only** | No prior `capture start`; PCAP covers the harness run only | **`vpn-leaks run --provider <slug> --skip-vpn --with-pcap`** (**mutually exclusive** with **`--attach-capture`**; no other active **`capture`** session) |
| **Standalone repair / inspection** | Re-emit **`pcap_summary.json`** next to an existing PCAP | **`vpn-leaks pcap-summarize <file.pcap> [-o out.json]`** |

Session state lives under **`.vpn-leaks/capture/`** (ignored by git); finalized bundles land at **`runs/<run_id>/raw/<location_id>/capture/`**. See **[docs/data-dictionary.md](docs/data-dictionary.md)** for **`pcap_derived`**, **`capture_finalize`**, **`artifacts.capture_dir`**.

### Website-exposure methodology (automated)

Every full run can populate **`normalized.json`** → **`website_exposure_methodology`** (desk automation tier — **not** the same interpretation as **`dns_servers_observed`** / DNS leak flags). Prerequisites in **`configs/vpns/<slug>.yaml`**:

- **`competitor_probe.provider_domains`** — Apex domains driving Phase **8–9** depth; empty domains skip most of automation (CLI prints **hints** on stderr).
- **`surface_urls`** — Optional; broadens host inventory from HAR/surface matrix.
- **`policy_urls`** — Optional but recommended; empty list skips policy HTML fetch (hint on stderr).

Reports add a **methodology + PCAP** subsection when data exists. Evidence tiers (**O** vs desk automation vs manual **S**): [docs/research-questions-and-evidence.md](docs/research-questions-and-evidence.md). Full manual workflow and phase definitions: [docs/website-exposure-methodology.md](docs/website-exposure-methodology.md). Run order detail: [docs/methodology.md](docs/methodology.md).

### NordVPN (macOS app or other GUI)

Connect in the **NordVPN app** first, then run with **`--skip-vpn`** so the harness does not drive the adapter. Prefer **omitting `--locations`** so the active server is reflected via **geo + exit IP** in the config and report.

**Manual ids:** You can still pass **`--locations <id>`**; new ids are **appended** to the YAML by default (**`--no-persist-locations`** to skip). YAML rewrites may drop comments (PyYAML).

Artifacts: `runs/<run_id>/` (gitignored), including `raw/preflight.json`.

## Reports

- Per-run: `runs/<run_id>/summary.md`, `locations/<id>/normalized.json`
- Aggregated: `VPNs/<COMPANY>.md`, `PROVIDERS/AS<asn>.md` (via `vpn-leaks report`)

| Report | Command |
|--------|---------|
| Per-VPN rollup | `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md` and **`VPNs/<SLUG>.html`** (HTML includes SPEC framework coverage bars, embedded **3D exposure graph** from the same data as `graph-export`, plus the full markdown body). For reliable loading of the graph script, serve the folder over HTTP (e.g. `python3 -m http.server` in `VPNs/`) instead of opening the file directly via `file:`. |
| Underlay (ASN) | `vpn-leaks report --provider <slug> --asn <n>` → `PROVIDERS/AS<n>.md` |
| Exposure graph (nodes/edges JSON) | `vpn-leaks graph-export [--provider <slug>] [-o exposure-graph.json]` — then open [viewer/](viewer/) (see [viewer/README.md](viewer/README.md)). When runs include **`pcap_derived`**, export **graph_schema 1.1** may add PCAP-derived edges (see [docs/data-dictionary.md](docs/data-dictionary.md)). |

### GitHub Pages (github.io)

For a **project site** in this repository, the published base URL is typically:

`https://<owner>.github.io/<repo>/`

- **Landing:** `https://<owner>.github.io/<repo>/` — index listing all `VPNs/*.html` reports.
- **Example report:** `https://<owner>.github.io/<repo>/VPNs/NORDVPN.html` (replace `<owner>`, `<repo>`, and filename with yours).

**One-time setup:** In the GitHub repo, open **Settings → Pages → Build and deployment** and set **Source** to **GitHub Actions** (not “Deploy from a branch”). The workflow [`.github/workflows/pages.yml`](.github/workflows/pages.yml) stages `VPNs/`, `style/icons/` (needed for SPEC category icons in HTML), and a generated `index.html`, then deploys. You can also run **Actions → Pages → Run workflow** to redeploy without a commit.

**Notes:** Publishing exposes whatever is committed under `VPNs/` (exit IPs and benchmark detail). Confirm that is acceptable. Private repositories may need a paid GitHub plan for **private** Pages visibility. To preview locally: `python3 scripts/build_github_pages_site.py` then serve the `site/` directory over HTTP.

Add `runs/` (and optionally `VPNs/` / `PROVIDERS/`) to `.gitignore` if you do not want local reports or run artifacts in version control.

## Development

```bash
ruff check vpn_leaks tests
pytest tests -q
```

[`.github/workflows/pages.yml`](.github/workflows/pages.yml) deploys reports to GitHub Pages. Lint/test CI is still optional: copy [docs/github-actions-ci.yml.example](docs/github-actions-ci.yml.example) to `.github/workflows/ci.yml` locally if it is not present (GitHub OAuth may require the `workflow` scope to push workflow files; `gh auth refresh -s workflow`). That workflow runs lint and tests without a live VPN (mocks only).
