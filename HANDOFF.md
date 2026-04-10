# VPN Leaks — agent handoff

This document orients future AI coding agents (and humans) to the **vpn-leaks** repository: what it does, where code lives, what has been built, and what is out of scope. For a chronological decision log and benchmark snapshots, see **[progress.md](progress.md)**. For users, start with **[README.md](README.md)**.

_Last updated: 2026-04-10._

---

## What this project is

**VPN Leaks** is a Python **CLI harness** for repeatable, **client-observable** VPN benchmarking: exit IP, DNS leaks (local + external HTML), IPv6 exposure, WebRTC candidates, optional browser fingerprint, **public routing attribution** (RIPEstat, Team Cymru, PeeringDB), **privacy policy** fetch with SHA-256 and heuristic keyword summaries, and optional **competitor-surface** probes (provider apex DNS, Playwright web/HAR + CDN headers, HTTPS portal checks, traceroute toward exit, bounded stray JSON GETs)—driven by `competitor_probe` in each provider YAML.

- **Package name:** `vpn-leaks` (import: `vpn_leaks`).
- **Python:** 3.12+ ([pyproject.toml](pyproject.toml)).
- **Entry point:** `vpn-leaks` → `vpn_leaks.cli:main`.
- **Key deps:** httpx, pydantic, PyYAML, Jinja2, Playwright (Chromium for WebRTC, policy fallback, and web probes), **dnspython** (authoritative DNS for competitor domains).

It does **not** prove what a VPN stores on its servers or automate vendor desktop apps beyond optional adapters; for NordVPN the expected workflow is **manual connect in the app**, then `vpn-leaks run --provider nordvpn --skip-vpn`.

---

## Repository layout (engineering)

| Area | Path | Role |
|------|------|------|
| CLI / orchestration | [vpn_leaks/cli.py](vpn_leaks/cli.py) | `run`, `report`, preflight, duplicate guard, per-location suite |
| Models / schema | [vpn_leaks/models.py](vpn_leaks/models.py) | `NormalizedRun` (`schema_version` 1.1+ adds `competitor_surface`), policies, attribution, artifacts index |
| Config loading | [vpn_leaks/config_loader.py](vpn_leaks/config_loader.py) | Repo root, YAML loading |
| VPN YAML + locations | [vpn_leaks/vpn_config_locations.py](vpn_leaks/vpn_config_locations.py), [configs/vpns/](configs/vpns/) | Provider slugs, `manual_gui`, `policy_urls`, location list |
| Auto location (ipwho) | [vpn_leaks/auto_connection.py](vpn_leaks/auto_connection.py) | When `--locations` omitted: build `location_id` / label, optional YAML persist |
| Leak checks | [vpn_leaks/checks/](vpn_leaks/checks/) | `ip_check`, `dns`, `ipv6`, `webrtc`, `fingerprint`, `competitor_probes` |
| Attribution | [vpn_leaks/attribution/](vpn_leaks/attribution/) | merge, RIPEstat, Cymru, PeeringDB, optional GeoLite |
| Policy | [vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py), [summarize_policy.py](vpn_leaks/policy/summarize_policy.py) | Fetch HTML, hash, keyword bullets |
| Reporting | [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py), Jinja templates under `vpn_leaks/reporting/templates/` | `VPNs/<SLUG>.md`, `PROVIDERS/AS<n>.md` |
| Adapters | [vpn_leaks/adapters/](vpn_leaks/adapters/) | `manual`, `wireguard`, registry |
| Tests | [tests/](tests/) | pytest, mocks for network where applicable |

---

## CLI commands (short reference)

```bash
pip install -e ".[dev]"
playwright install chromium

# After VPN is connected (manual app) — auto location via ipwho.is:
vpn-leaks run --provider nordvpn --skip-vpn

# Aggregated markdown from all runs for that provider under runs/:
vpn-leaks report --provider nordvpn

# Per-ASN underlay report:
vpn-leaks report --provider nordvpn --asn <asn_integer>
```

**Preflight:** resolves exit IPv4; **skips** a full run if that IPv4 was already recorded for the same `--provider` in any `runs/*/locations/*/normalized.json` unless **`--force`**.

**Locations:** Omitting `--locations` triggers **auto** `location_id` / label (ipwho.is) and can append to `configs/vpns/<slug>.yaml` unless `--no-persist-locations`.

**Competitor probes:** If `competitor_probe` is set in the provider YAML, `vpn-leaks run` performs those phases after policy fetch (same VPN session). Skip flags: `--skip-competitor-dns`, `--skip-competitor-web`, `--skip-competitor-portal`, `--skip-competitor-transit`, `--skip-competitor-stray-json`.

---

## Artifacts and reports

| Output | Location |
|--------|----------|
| Per run | `runs/<run_id>/` — `run.json`, `summary.md`, `raw/preflight.json`, `locations/<location_id>/normalized.json`, `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy, optional **competitor_probe/**) |
| Per-provider rollup | `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md` (slug uppercased, `-` → `_`) |
| Per-ASN rollup | `PROVIDERS/AS<n>.md` |

**`normalized.json`** is the canonical structured record for tooling and reports; see [docs/data-dictionary.md](docs/data-dictionary.md).

---

## Policy fetching (important)

- **NordVPN** ([configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml)): `policy_urls` points at **`https://my.nordaccount.com/legal/privacy-policy/`** because the marketing site `https://nordvpn.com/privacy-policy/` often returns **403** or Cloudflare interstitials to simple HTTP clients.
- Implementation: browser-like **httpx** headers; **Playwright** fallback for Cloudflare challenges or thin SPA shells (e.g. Nord Account). Successful runs add `policy:playwright_chromium` to `services_contacted`.
- **Older runs (2026-04-10)** may still show `fetch error: 403` in `policies` for the *previous* URL; new runs after the config change should have `sha256` and summary bullets. Re-run benchmarks if you need on-disk policy HTML under `raw/.../policy/`.

---

## NordVPN: completed benchmark snapshot

Five **NordVPN** runs were collected (one exit per run) using **`vpn-leaks run --provider nordvpn --skip-vpn`** with **auto location** after switching the **NordVPN macOS client** per destination. **No** DNS / WebRTC / IPv6 leak flags were set in those runs (per harness heuristics). Full table (run ids, locations, exit IPs, ASNs) is in **[progress.md](progress.md)** — do not duplicate that table here; update **progress.md** when new runs are added.

**Config:** [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml) lists location entries including the five auto-derived ids.

---

## Documentation map

| Doc | Use |
|-----|-----|
| [README.md](README.md) | Setup, commands, ethics, directory index |
| [vpn-leaks.md](vpn-leaks.md) | Long-form product / research spec |
| [docs/spec.md](docs/spec.md) | Operational spec |
| [docs/methodology.md](docs/methodology.md) | Run order |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Fields in `normalized.json` |
| [progress.md](progress.md) | Project progress, Nord run table, policy notes |

---

## CI / GitHub

- Workflow is **not** committed under `.github/workflows/` (OAuth `workflow` scope can block pushes). Copy **[docs/github-actions-ci.yml.example](docs/github-actions-ci.yml.example)** to `.github/workflows/ci.yml` locally or after `gh auth refresh -s workflow`.
- Remote repo: **doxxcorp/vpn-leaks** on GitHub. Commit authorship is **g4lr0n &lt;g4lr0n@doxx.net&gt;**; local repo `user.name` / `user.email` should match for new commits.

---

## Ethics and security (do not weaken)

- Only test services the operator is entitled to use; do not bypass controls or load-test third parties.
- **Never commit** VPN credentials; use env vars / secrets.
- `runs/` may contain sensitive exit-IP and test artifacts; **add `runs/` to `.gitignore`** if clones should not ship local benchmarks (README mentions this).

---

## Suggested next steps for future agents

1. Read **[progress.md](progress.md)** for the latest benchmark and policy decisions.
2. Before changing behavior, skim **docs/spec.md** and **data-dictionary.md** so JSON fields stay consistent.
3. After edits, run **`ruff check vpn_leaks tests`** and **`pytest tests -q`**.
4. **Policy / fetch changes:** touch [vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py) and consider Nord + one generic provider in tests.
5. **Reporting changes:** [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py) and templates under `vpn_leaks/reporting/templates/`.

---

## Update this file

When you make **significant** architectural or workflow changes, add a short subsection here or extend **[progress.md](progress.md)** so the next agent inherits accurate context.
