# VPN Leaks — agent handoff

This document orients future AI coding agents (and humans) to the **vpn-leaks** repository: what it does, where code lives, what has been built, and what is out of scope. For a chronological decision log and benchmark snapshots, see **[progress.md](progress.md)**. For users, start with **[README.md](README.md)**.

_Last updated: 2026-04-17 (SPEC **FP-001**: `answered` when fingerprint/BrowserLeaks evidence exists; MD/HTML coverage blurb for **DYNAMIC_PARTIAL** vs desk interpretation; plus prior: website exposure in reports, NordVPN `surface_urls`, transition-tests; desk pass Phases 8–9)._

---

## What this project is

**VPN Leaks** is a Python **CLI harness** for repeatable, **client-observable** VPN benchmarking: exit IP, DNS leaks (local + external HTML), IPv6 exposure, WebRTC candidates, optional browser fingerprint, **public routing attribution** (RIPEstat, Team Cymru, PeeringDB), **privacy policy** fetch with SHA-256 and heuristic keyword summaries, **always-on yourinfo.ai** capture (third-party benchmark page: HAR + text excerpt; **`--skip-yourinfo`** to omit), optional **competitor-surface** probes (provider apex DNS, Playwright web/HAR + CDN headers, HTTPS portal checks, traceroute toward exit, bounded stray JSON GETs)—driven by `competitor_probe` in each provider YAML—and optional **`surface_urls`** (tagged Playwright loads → **`surface_probe/`**, e.g. pricing/signup/checkout pages for SPEC web/signup inventory).

- **Package name:** `vpn-leaks` (import: `vpn_leaks`).
- **Python:** 3.12+ ([pyproject.toml](pyproject.toml)).
- **Entry point:** `vpn-leaks` → `vpn_leaks.cli:main`.
- **Key deps:** httpx, pydantic, PyYAML, Jinja2, Playwright (Chromium for WebRTC, policy fallback, and web probes), **dnspython** (authoritative DNS for competitor domains).

It does **not** prove what a VPN stores on its servers or automate vendor desktop apps beyond optional adapters; for NordVPN the expected workflow is **manual connect in the app**, then `vpn-leaks run --provider nordvpn --skip-vpn`.

---

## Repository layout (engineering)

| Area | Path | Role |
|------|------|------|
| CLI / orchestration | [vpn_leaks/cli.py](vpn_leaks/cli.py) | `run`, `report`, `graph-export`, preflight, duplicate guard, per-location suite |
| Models / schema | [vpn_leaks/models.py](vpn_leaks/models.py) | `NormalizedRun` (1.3 default; 1.2: `yourinfo_snapshot`; 1.1: `competitor_surface`), policies, attribution, artifacts index |
| Config loading | [vpn_leaks/config_loader.py](vpn_leaks/config_loader.py) | Repo root, YAML loading |
| VPN YAML + locations | [vpn_leaks/vpn_config_locations.py](vpn_leaks/vpn_config_locations.py), [configs/vpns/](configs/vpns/) | Provider slugs, `manual_gui`, `policy_urls`, location list |
| Auto location (ipwho) | [vpn_leaks/auto_connection.py](vpn_leaks/auto_connection.py) | When `--locations` omitted: build `location_id` / label, optional YAML persist |
| Leak checks | [vpn_leaks/checks/](vpn_leaks/checks/) | `ip_check`, `dns`, `ipv6`, `webrtc`, `fingerprint`, `yourinfo_probe`, `competitor_probes`, `surface_probe` (`surface_urls` in YAML) |
| Attribution | [vpn_leaks/attribution/](vpn_leaks/attribution/) | merge, RIPEstat, Cymru, PeeringDB, optional GeoLite |
| Policy | [vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py), [summarize_policy.py](vpn_leaks/policy/summarize_policy.py) | Fetch HTML, hash, keyword bullets |
| Reporting | [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py), [html_dashboard.py](vpn_leaks/reporting/html_dashboard.py), [web_exposure.py](vpn_leaks/reporting/web_exposure.py) (HAR + provider DNS + surface matrix rollups for reports), [exposure_graph.py](vpn_leaks/reporting/exposure_graph.py), Jinja templates, [static/](vpn_leaks/reporting/static/) (CSS + isotype) | `VPNs/<SLUG>.md` + **`VPNs/<SLUG>.html`** (visual-first dashboard; **Website and DNS surface** section from harness data; full markdown in collapsible appendix), `PROVIDERS/AS<n>.md`, `graph-export` JSON |
| SPEC framework | [vpn_leaks/framework/](vpn_leaks/framework/), [configs/framework/](configs/framework/) | Question bank, coverage, findings, risk scores embedded as `normalized.json` → `framework` (skip with `--no-framework`); see [docs/framework.md](docs/framework.md). Aggregated report **“Next steps”** copy is driven by [configs/framework/report_hints.yaml](configs/framework/report_hints.yaml) plus per-run notes from [coverage.py](vpn_leaks/framework/coverage.py) ([coverage_rollup.py](vpn_leaks/reporting/coverage_rollup.py) merge). |
| Viewer | [viewer/](viewer/) | 3D graph of `graph-export` output (static HTML + CDN) |
| Adapters | [vpn_leaks/adapters/](vpn_leaks/adapters/) | `manual`, `wireguard`, registry |
| Tests | [tests/](tests/) | pytest, mocks for network where applicable |

---

## CLI commands (short reference)

```bash
pip install -e ".[dev]"
playwright install chromium

# After VPN is connected (manual app) — auto location via ipwho.is:
vpn-leaks run --provider nordvpn --skip-vpn

# Optional desk pass (not CLI): Phases 8–9 from docs/website-exposure-methodology.md — MX/SPF/DMARC/DKIM/TXT/CNAME inventory; archive transcript under research/ or appendix. Then:
# Aggregated markdown + HTML dashboard from all runs for that provider under runs/:
vpn-leaks report --provider nordvpn

# Transition-phase artifact: for manual_gui, writes transitions.json (skipped stub) even with --skip-vpn:
vpn-leaks run --provider nordvpn --skip-vpn --transition-tests

# Per-ASN underlay report:
vpn-leaks report --provider nordvpn --asn <asn_integer>

# Exposure graph JSON (all runs or one provider); open viewer/index.html via local HTTP server:
vpn-leaks graph-export --provider nordvpn -o exposure-graph.json
```

**Preflight:** resolves exit IPv4; **skips** a full run if that IPv4 was already recorded for the same `--provider` in any `runs/*/locations/*/normalized.json` unless **`--force`**.

**Locations:** Omitting `--locations` triggers **auto** `location_id` / label (ipwho.is) and can append to `configs/vpns/<slug>.yaml` unless `--no-persist-locations`.

**YourInfo:** After policy fetch, **`vpn-leaks run`** loads **https://yourinfo.ai/** in Playwright (unless **`--skip-yourinfo`**).

**Competitor probes:** If `competitor_probe` is set in the provider YAML, `vpn-leaks run` performs those phases after YourInfo (same VPN session). Skip flags: `--skip-competitor-dns`, `--skip-competitor-web`, `--skip-competitor-portal`, `--skip-competitor-transit`, `--skip-competitor-stray-json`.

---

## Artifacts and reports

| Output | Location |
|--------|----------|
| Per run | `runs/<run_id>/` — `run.json`, `summary.md`, `raw/preflight.json`, `locations/<location_id>/normalized.json`, `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy, **yourinfo_probe/**, optional **competitor_probe/**, optional **surface_probe/** including **`har_summary.json`** when HARs exist, optional **transitions.json** when `--transition-tests`) |
| Per-provider rollup | `vpn-leaks report --provider <slug>` → **`VPNs/<SLUG>.md`** (full narrative + **Website and DNS surface** rollup + per-location summary; links [docs/website-exposure-methodology.md](docs/website-exposure-methodology.md)) and **`VPNs/<SLUG>.html`** (dashboard: risk strip, location cards, **website/DNS surface** tables + HAR-derived lists, SPEC by category, coverage bar, embedded 3D exposure graph; slug uppercased, `-` → `_`) |
| Per-ASN rollup | `PROVIDERS/AS<n>.md` |

**Viewing `VPNs/<SLUG>.html`:** Prefer the **HTML** file for a **visual-first** read: severity, leak chips, **per-location cards** (CSS **subgrid** aligns rows across cards; **Exit IPv4/IPv6** both listed; leak **badges** are harness outcomes, not the same as “has IPv6 exit”), **Website and DNS surface** panel when `competitor_probe` / `surface_urls` produced data (merged HAR hints, apex DNS table, surface URL matrix, CDN/tracker lists), SPEC accordions (when multiple locations exist, copy explains **strictest merged** status per question ID), coverage visualization, and the **embedded 3D exposure graph** (same data as `graph-export`; **node labels on load** via `three-spritetext`). The complete markdown-derived report lives in a **collapsed** section (“Full narrative export”). Styles and logo ship from [`vpn_leaks/reporting/static/`](vpn_leaks/reporting/static/) (embedded at render time; aligned with the org **style** repo / doxx design tokens).

**Viewing `VPNs/<SLUG>.md`:** The markdown file opens with **How to read** (rollup vs **Detailed runs**), then a **numbered index** of runs. The bulk of the data is under **`## Detailed runs`**. If a JSON excerpt is capped, a **note** at the top of that run lists what was shortened; **on-disk `normalized.json` is always complete**. In **Markdown preview**, still **scroll** or open as **plain text** for very large sections.

**`normalized.json`** is the canonical structured record for tooling and reports; see [docs/data-dictionary.md](docs/data-dictionary.md).

---

## Policy fetching (important)

- **NordVPN** ([configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml)): `policy_urls` lists both **`https://nordvpn.com/privacy-policy/`** and **`https://my.nordaccount.com/legal/privacy-policy/`** (account legal is the reliable capture for Playwright/httpx; the marketing URL often returns **403** or Cloudflare interstitials to simple HTTP clients).
- Implementation: browser-like **httpx** headers; **Playwright** fallback for Cloudflare challenges or thin SPA shells (e.g. Nord Account). Successful runs add `policy:playwright_chromium` to `services_contacted`.
- **Older runs (2026-04-10)** may still show `fetch error: 403` in `policies` for the *previous* URL; new runs after the config change should have `sha256` and summary bullets. Re-run benchmarks if you need on-disk policy HTML under `raw/.../policy/`.

---

## SPEC coverage and `framework` rows

[`vpn_leaks/framework/coverage.py`](vpn_leaks/framework/coverage.py) maps the question bank to per-run **answer_status** / summaries. Recent alignment work: **portal** and **web** probes both count for WEB/CTRL/SIGNUP/THIRDWEB-style questions; **BrowserLeaks** snapshots count toward fingerprint-style IDs; **EXIT-004** / **EXIT-005** / **IP-014** use structured summaries from `exit_dns.json`, `extra.exit_geo`, and `exit_ip_sources` when present. Provider YAML example with **`competitor_probe`** and **`policy_urls`**: [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml).

**FP-001 (browser fingerprinting):** When **`fingerprint_snapshot`** or **`browserleaks_snapshot`** has real content, coverage marks **`answered`** (harness baseline captured; summaries explicitly **do not** claim proof of provider-side fingerprinting—use THIRDWEB / HAR rows for script-level evidence). If neither is present, the row stays **`unanswered`**; [configs/framework/report_hints.yaml](configs/framework/report_hints.yaml) drives gap **Next steps**. Aggregated MD/HTML reports add a short note that for some **`DYNAMIC_PARTIAL`** IDs, **`answered`** means the harness captured the intended evidence class, not a fully settled desk answer—see [vpn_leaks/reporting/templates/vpn_report_document.html.j2](vpn_leaks/reporting/templates/vpn_report_document.html.j2) / [vpn_report.md.j2](vpn_leaks/reporting/templates/vpn_report.md.j2). **`vpn-leaks report`** merged **`gap_rows`** use the strictest status across locations (unchanged).

---

## NordVPN: completed benchmark snapshot

Historical **NordVPN** runs (one exit per connect session) used **`vpn-leaks run --provider nordvpn --skip-vpn`** with **auto location** after switching the **NordVPN macOS client** per destination. **No** DNS / WebRTC / IPv6 leak flags were set in the 2026-04-10 campaign (per harness heuristics). The **[progress.md](progress.md)** table lists those run ids; newer gap-closure runs (surface probes, transition stubs) are summarized in the **“NordVPN gap-closure plan”** section there—update **progress.md** when you add material runs.

**Config:** [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml) includes **`competitor_probe`**, dual **`policy_urls`**, optional **`surface_urls`** (pricing/signup/checkout → **`surface_probe/`**), and multiple declared **`locations`** (merge **strictest** SPEC status across all runs included in `vpn-leaks report`).

---

## Documentation map

| Doc | Use |
|-----|-----|
| [README.md](README.md) | Setup, commands, purpose, directory index |
| [vpn-leaks.md](vpn-leaks.md) | Long-form product / research spec |
| [docs/spec.md](docs/spec.md) | Operational spec |
| [docs/methodology.md](docs/methodology.md) | Run order |
| [docs/website-exposure-methodology.md](docs/website-exposure-methodology.md) | Manual website third-party exposure analysis (curl, DNS, WHOIS, classification); **after run**, Phases **8–9** + [scripts/desk_dns_audit.sh](scripts/desk_dns_audit.sh), [research/desk-exposure-template.md](research/desk-exposure-template.md) |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Fields in `normalized.json` |
| [docs/framework.md](docs/framework.md) | Question bank, CLI flags (`--capture-baseline`, `--transition-tests`), `framework` object |
| [RUN-STEPS.md](RUN-STEPS.md) | Step-by-step walkthrough of `vpn-leaks run` (including transition tests vs `skip_vpn`) |
| [progress.md](progress.md) | Project progress, Nord run table, gap-closure notes, policy notes |
| [HANDOFF.md](HANDOFF.md) | This file: repo map, CLI, artifacts, agent next steps |

---

## CI / GitHub

- **Remote:** **github.com/doxxcorp/vpn-leaks**. Commit authorship is **g4lr0n &lt;g4lr0n@doxx.net&gt;**; local repo `user.name` / `user.email` should match for new commits.
- **GitHub Pages:** [`.github/workflows/pages.yml`](.github/workflows/pages.yml) deploys a static site (copies **`VPNs/`** and **`style/icons/`**, generates **`index.html`** via [`scripts/build_github_pages_site.py`](scripts/build_github_pages_site.py)) on pushes that touch those paths or on **workflow_dispatch**. **One-time:** repo **Settings → Pages → Source: GitHub Actions**. Public URL (project site): **`https://doxxcorp.github.io/vpn-leaks/`** (e.g. **`https://doxxcorp.github.io/vpn-leaks/VPNs/NORDVPN.html`**). Pushing workflow files may require OAuth **`workflow`** scope (`gh auth refresh -s workflow`) or a credential that is allowed to update `.github/workflows/`.
- **Lint/test CI (optional):** Not required for Pages. Copy **[docs/github-actions-ci.yml.example](docs/github-actions-ci.yml.example)** to `.github/workflows/ci.yml` if you want Ruff + pytest in Actions.

---

## Suggested next steps for future agents

1. Read **[progress.md](progress.md)** for the latest benchmark and policy decisions.
2. Before changing behavior, skim **docs/spec.md** and **data-dictionary.md** so JSON fields stay consistent.
3. After edits, run **`ruff check vpn_leaks tests`** and **`pytest tests -q`**.
4. **Policy / fetch changes:** touch [vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py) and consider Nord + one generic provider in tests.
5. **Reporting changes:** [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py), [html_dashboard.py](vpn_leaks/reporting/html_dashboard.py), [web_exposure.py](vpn_leaks/reporting/web_exposure.py), [static/report.css](vpn_leaks/reporting/static/report.css), templates under `vpn_leaks/reporting/templates/` (especially `vpn_report.md.j2` and `vpn_report_document.html.j2`), and—when changing rollup “Next steps”—[configs/framework/report_hints.yaml](configs/framework/report_hints.yaml) with [coverage.py](vpn_leaks/framework/coverage.py) / [coverage_rollup.py](vpn_leaks/reporting/coverage_rollup.py).

---

## Update this file

When you make **significant** architectural or workflow changes, add a short subsection here or extend **[progress.md](progress.md)** so the next agent inherits accurate context.
