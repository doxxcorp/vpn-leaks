# VPN Leaks — agent handoff

This document orients future AI coding agents (and humans) to the **vpn-leaks** repository: what it does, where code lives, what has been built, and what is out of scope. For a chronological decision log and benchmark snapshots, see **[progress.md](progress.md)**. For users, start with **[README.md](README.md)**.

_Last updated: 2026-05-05 — **Protection gap coverage** (12-task batch from [docs/protection-gap-coverage-plan.md](docs/protection-gap-coverage-plan.md)): the IP table now exposes BGP **AS Path** (TASK-01), **Flows** count (TASK-02), and a **Role** badge (TASK-03; `vpn-control` / `vpn-data` / `provider-analytics` / `dns-resolver` / `routing-infra` / `unknown`) computed from canonical-company match against the provider slug + a 16-pattern analytics-vendor list. New `_resolve_dns_operators()` (TASK-04, dnspython, 4 s timeout, on-disk cache) attributes every PCAP-observed DNS hostname to its authoritative-NS operator and renders a "DNS operators" `<details>` Tier 3 section. The ASN topology DAG (TASK-05) now renders **multi-hop transit nodes** at negative layers when `ip.as_path` has ≥ 3 hops, with dynamic LY computation and barycenter sweeps over the actual layer set. A new **role-split KPI tile** (TASK-06, magenta border) summarizes contacts by role next to the existing organization counts. NordVPN's YAML now carries `surface_urls` + `competitor_probe` (TASK-07) so the rest of the new pre-registration phase can target the right pages. New `analyze_signup_exposure()` (TASK-08) deep-scans HARs for `signup|checkout|pricing|order` page types, returning third-party domains (categorized analytics/advertising/cdn/payment), cross-origin POST endpoints, and analytics-event requests; `fingerprint_payment_processors()` (TASK-09; 12-pattern dict) detects Stripe/PayPal/Adyen/etc. and renders payment-card tiles with hardcoded data-exposure descriptions. Brand-new `vpn-leaks capture idle` subcommand (TASK-10) starts tcpdump for ``--duration`` seconds (default 120 s), summarizes the resulting pcap, runs full attribution + role classification, and writes ``runs/idle_telemetry/<provider>-<ts>.json``; report renders an "App idle telemetry" Tier 3 section with a warning callout for any third-party contact captured before the tunnel is up. `IdleTelemetryResult` Pydantic model added; `NormalizedRun.schema_version` bumped **1.5 → 1.6**. New `vpn_leaks/checks/tls_probe.py` (TASK-11; stdlib `ssl` for the handshake, `cryptography>=42.0` to parse the leaf DER because `getpeercert(binary_form=False)` returns `{}` under `verify_mode=CERT_NONE`) writes leaf-issuer + OCSP URL into `__tls_chains__` cache; the IP table renders a `CA: <issuer_o>` line under reverse DNS for any peer IP that resolves from a probed SNI hostname. `_SDK_ENDPOINT_PATTERNS` (TASK-12; 15-entry dict, Amplitude/Segment/Firebase/Sentry/etc.) flags known analytics-SDK endpoints discovered via PCAP and renders a magenta `SDK · <name>` badge that overrides the role badge plus a top-of-section ⚠ callout. `cryptography>=42.0` added to `pyproject.toml`. New tests: `tests/test_classify_contact_role.py` (9 cases). Prior: **Interactive ASN topology DAG**: the Network Intelligence section shows a full-width SVG DAG above the company cluster list. Upstream transit providers (top row, purple) connect to contacted companies (bottom row, teal); click a company to expand its ASN child nodes (magenta stroke), click an ASN to open a floating IP details panel, click an upstream to highlight its downstream companies. Layout uses a **static Sugiyama barycenter algorithm** (4 alternating top-down/bottom-up sweeps, per-component proportional horizontal zones, pure `placeRow` with no force simulation) for crossing-minimized, deterministic rendering. Pan by dragging empty SVG space; the graph resizes and re-lays-out on window resize with a 200 ms D3 transition. Implemented entirely in `vpn_report_document.html.j2` + `report.css`; no Python changes. Prior: **Upstream transit org name in IP table**: the Network Intelligence IP table has an **Upstream** column showing the transit provider's company name resolved via `_cymru_asn_names_bulk` and cached in `ip_intel.json/__upstream_asns__`. Prior: **Offline BGP prefix lookup**: `vpn-leaks bgp-update` downloads the latest Route Views MRT RIB (~73 MB compressed) and builds `.cache/vpn_leaks/bgp_prefixes.db` (SQLite, 1.09M IPv4 prefixes, integer-range LPM index). `bgp_lookup.lookup_ip(ip)` returns `{asn, upstream_asn, prefix, as_path}` in sub-milliseconds; integrated into `pcap_host_intelligence` and `attribution/merge.py`. Prior: capture-first HTML report redesign, persistent IP intel cache, Cymru bulk ASN lookup, heuristic + LLM org-name normalization._

---

## What this project is

**VPN Leaks** is a Python **CLI harness** for repeatable, **client-observable** VPN benchmarking: exit IP, DNS leaks (local + external HTML), IPv6 exposure, WebRTC candidates, optional fingerprint, pinned **browserleaks** pages (unless **`--skip-browserleaks`** / disabled in config), **public routing attribution** (RIPEstat, Team Cymru, PeeringDB), **privacy policy** fetch with SHA-256 and heuristic keyword summaries, **always-on yourinfo.ai** capture (HAR + excerpt; **`--skip-yourinfo`** to omit), optional **competitor-surface** probes (**`competitor_probe`** in YAML), optional **`surface_urls`** → **`surface_probe/`**, and **automated website-exposure methodology** (**`website_exposure_methodology`** in **`normalized.json`**, Phases **1–9** desk projection; fail-soft). Optional **PCAP**: **`capture start`** + **`run --attach-capture`**, or **`run --with-pcap`**, summarized with **dpkt** only.

- **Package name:** `vpn-leaks` (import: `vpn_leaks`).
- **Python:** 3.12+ ([pyproject.toml](pyproject.toml)).
- **Entry point:** `vpn-leaks` → `vpn_leaks.cli:main`.
- **Key deps:** httpx, pydantic, PyYAML, Jinja2, Playwright (Chromium for WebRTC, policy fallback, and web probes), **dnspython** (authoritative DNS for competitor domains), **dpkt** (PCAP summarization; no tshark), **tqdm** (terminal progress for `vpn-leaks run`).

It does **not** prove what a VPN stores on its servers or automate vendor desktop apps beyond optional adapters; for NordVPN the expected workflow is **manual connect in the app**, then `vpn-leaks run --provider nordvpn --skip-vpn`.

---

## Repository layout (engineering)

| Area | Path | Role |
|------|------|------|
| CLI / orchestration | [vpn_leaks/cli.py](vpn_leaks/cli.py) | `run` (incl. **`--attach-capture`**, **`--with-pcap`**), **`capture`** `start|status|abort`, **`pcap-summarize`**, `report`, `graph-export`, **`bgp-update`** (build offline BGP prefix DB), preflight, duplicate guard |
| Run progress UI | [vpn_leaks/run_progress.py](vpn_leaks/run_progress.py) | `RunProgress`, `compute_run_total` — tqdm bar + phase descriptions on stderr; text-only lines when not a TTY or **`--no-progress`**. Reused by **`report`** with report-specific phase ticks |
| Models / schema | [vpn_leaks/models.py](vpn_leaks/models.py) | `NormalizedRun` (**1.6**: `idle_telemetry` (TASK-10); 1.5: `website_exposure_methodology`, `pcap_derived`, `capture_finalize`; 1.2: `yourinfo_snapshot`; 1.1: `competitor_surface`), `IdleTelemetryResult`, policies, attribution, `ArtifactIndex` (`website_exposure_dir`, `capture_dir`) |
| Config loading | [vpn_leaks/config_loader.py](vpn_leaks/config_loader.py) | Repo root, YAML loading; **`methodology_config_hints()`** for methodology/capture-related stderr reminders |
| VPN YAML + locations | [vpn_leaks/vpn_config_locations.py](vpn_leaks/vpn_config_locations.py), [configs/vpns/](configs/vpns/) | Provider slugs (`nordvpn`, `expressvpn`, `mullvad`, `example`, …), `manual_gui`, **`competitor_probe`**, **`surface_urls`**, `policy_urls`, location list |
| Auto location (ipwho) | [vpn_leaks/auto_connection.py](vpn_leaks/auto_connection.py) | When `--locations` omitted: build `location_id` / label, optional YAML persist |
| Leak checks | [vpn_leaks/checks/](vpn_leaks/checks/) | `ip_check`, `dns`, `ipv6`, `webrtc`, `fingerprint`, `yourinfo_probe`, `browserleaks_probe`, `competitor_probes`, `surface_probe`, **`website_exposure_methodology`**, **`methodology_email_dns`** (pure TXT parsers for tests/desk parity), **`pcap_summarize`** |
| Capture | [vpn_leaks/capture/](vpn_leaks/capture/) | Session JSON under repo **`.vpn-leaks/capture/`** (gitignored), `finalize_bundle` → `runs/.../raw/<loc>/capture/` |
| Attribution | [vpn_leaks/attribution/](vpn_leaks/attribution/) | merge, RIPEstat, Cymru, PeeringDB, optional GeoLite; **`bgp_lookup.py`** (offline Route Views prefix DB, `lookup_ip` → `{asn, upstream_asn, prefix, as_path}`), **`bgp_build.py`** (MRT download + SQLite build, called by `bgp-update` CLI), **`geolite_asn.lookup_city`** (GeoLite2-City) |
| Policy | [vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py), [summarize_policy.py](vpn_leaks/policy/summarize_policy.py) | Fetch HTML, hash, keyword bullets |
| Reporting | [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py), [html_dashboard.py](vpn_leaks/reporting/html_dashboard.py), [web_exposure.py](vpn_leaks/reporting/web_exposure.py) (`methodology_and_pcap_sections`, `pcap_host_intelligence`, `build_capture_workspace_rollup`, `_cymru_asn_bulk`, **`_cymru_asn_names_bulk`** (ASN→org name, cached in `ip_intel.json/__upstream_asns__`), `_heuristic_canonical`, `_normalize_org_names_llm`, **IP intel cache**), [exposure_graph.py](vpn_leaks/reporting/exposure_graph.py) (**`graph_schema` 1.1**), Jinja templates, [static/](vpn_leaks/reporting/static/) (CSS + isotype) | `VPNs/<SLUG>.md` + **`VPNs/<SLUG>.html`** (capture-first layout: PCAP workspace Tier 1 → benchmark run cards Tier 2 → SPEC/web/graph/narrative Tier 3 behind `<details>`), `PROVIDERS/AS<n>.md`, **`graph-export`** JSON |
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

# Competitive capture (PCAP spans signup → benchmark): start capture first, then on-VPN run:
#   vpn-leaks capture start [-i en0]   # default iface: VPN_LEAKS_CAPTURE_INTERFACE or en0
#   vpn-leaks run --provider nordvpn --skip-vpn --attach-capture
# Harness-window PCAP only (no prior capture start; mutually exclusive flags):
#   vpn-leaks run --provider nordvpn --skip-vpn --with-pcap
# Repair: vpn-leaks pcap-summarize path/to/file.pcap [-o pcap_summary.json]

# Aggregated markdown + HTML dashboard from all runs for that provider under runs/:
vpn-leaks report --provider nordvpn

# Transition-phase artifact: for manual_gui, writes transitions.json (skipped stub) even with --skip-vpn:
vpn-leaks run --provider nordvpn --skip-vpn --transition-tests

# Disable tqdm bar (still prints [n/total] phase lines to stderr):
vpn-leaks run --provider nordvpn --skip-vpn --no-progress
vpn-leaks report --provider nordvpn --no-progress

# Per-ASN underlay report:
vpn-leaks report --provider nordvpn --asn <asn_integer>

# Exposure graph JSON (all runs or one provider); open viewer/index.html via local HTTP server:
vpn-leaks graph-export --provider nordvpn -o exposure-graph.json

# Build offline BGP prefix database from Route Views MRT RIB (run once, refresh periodically):
vpn-leaks bgp-update
# Override URL or use local file:
#   vpn-leaks bgp-update --url https://archive.routeviews.org/.../rib.YYYYMMDD.HHMM.bz2
#   vpn-leaks bgp-update --rib-file /path/to/rib.bz2
```

**Preflight:** resolves exit IPv4; **skips** a full run if that IPv4 was already recorded for the same `--provider` in any `runs/*/locations/*/normalized.json` unless **`--force`**.

**Locations:** Omitting `--locations` triggers **auto** `location_id` / label (ipwho.is) and can append to `configs/vpns/<slug>.yaml` unless `--no-persist-locations`.

**YourInfo:** After policies, **`vpn-leaks run`** loads **https://yourinfo.ai/** in Playwright (unless **`--skip-yourinfo`**).

**BrowserLeaks:** After YourInfo unless **`--skip-browserleaks`** (or probe disabled in config).

**Competitor / surface / methodology (order):** With tunnel up: **competitor_probe** → **`surface_urls`** surface_probe → optional **`--transition-tests`** → **`website_exposure_methodology`** (before disconnect). Skip flags: `--skip-competitor-*`. Empty **`competitor_probe.provider_domains`** yields sparse methodology; watch stderr **hints** from **`methodology_config_hints`**.

**PCAP finalize:** After all locations, if **`--attach-capture`** or **`--with-pcap`**: [vpn_leaks/capture/finalize_bundle.py](vpn_leaks/capture/finalize_bundle.py) stops tcpdump, writes **`raw/<loc>/capture/`**, merges **`pcap_derived`** into each new **`normalized.json`**.

---

## Artifacts and reports

| Output | Location |
|--------|----------|
| Per run | `runs/<run_id>/` — `run.json`, `summary.md`, `raw/preflight.json`, `locations/<location_id>/normalized.json`, `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy, **yourinfo_probe/**, **browserleaks_probe/** when run, optional **competitor_probe/**, optional **surface_probe/** + **`har_summary.json`**, optional **`website_exposure/`**, optional **`capture/`** `.pcap` + **`pcap_summary.json`**, optional **transitions.json** (`--transition-tests`)) |
| Per-provider rollup | `vpn-leaks report --provider <slug>` → **`VPNs/<SLUG>.md`** / **`.html`** (per-location **Automated website-exposure methodology & PCAP** when `website_exposure_methodology` / `pcap_derived` present; **Website and DNS surface**; methodology doc link; embedded 3D graph; slug uppercased, `-` → `_`) |
| Per-ASN rollup | `PROVIDERS/AS<n>.md` |

**Viewing `VPNs/<SLUG>.html`:** Prefer the **HTML** file for a **visual-first** read. The page opens on a **Network Intelligence** workspace (Tier 1, always visible): a KPI row (organizations / WHOIS handles / peer IPs / SNI+DNS names), provenance note, a live filter bar, an **interactive ASN topology DAG** (upstream transit providers → contacted companies; click company to expand ASNs, click ASN for IP panel, click upstream to highlight connected companies; drag to pan), and **company clusters** — each an expandable `<details>` showing per-ASN IP tables with IP, source badge (`PCAP·WIRE` / `PCAP·DNS` etc.), reverse DNS, ASN pill (hover for tooltip showing org name and covering prefix), **Upstream** (transit provider company name, resolved via `_cymru_asn_names_bulk` and cached in `ip_intel.json/__upstream_asns__`), bytes, and run IDs. Company names are normalized from raw WHOIS handles via rDNS suffix + prefix heuristics (and Claude Opus when `ANTHROPIC_API_KEY` is set). Below the fold: **Benchmark runs** (Tier 2, per-location cards; CSS subgrid; Exit IPv4/IPv6; leak badges). All other panels — Findings, SPEC framework, Website & DNS surface, Exposure graph, and Full narrative — are **Tier 3 `<details>`**, collapsed by default. Styles and logo embed from [`vpn_leaks/reporting/static/`](vpn_leaks/reporting/static/) (doxx design tokens: `#14141F` bg, Acumin + JetBrains Mono, teal/magenta/red/yellow palette).

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

Historical **NordVPN** runs (one exit per connect session) used **`vpn-leaks run --provider nordvpn --skip-vpn`** with **auto location** after switching the **NordVPN macOS client** per destination. **No** DNS / WebRTC / IPv6 leak flags were set in the 2026-04-10 campaign (per harness heuristics). The **[progress.md](progress.md)** table lists committed run ids (including **2026-04-17** Vancouver + Hamburg runs); the **“NordVPN gap-closure plan”** section there has the 2026-04-16 artifact review—update **progress.md** when you add material runs.

**Config:** [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml) includes **`competitor_probe`**, dual **`policy_urls`**, optional **`surface_urls`** (pricing/signup/checkout → **`surface_probe/`**), and multiple declared **`locations`** (merge **strictest** SPEC status across all runs included in `vpn-leaks report`).

---

## Documentation map

| Doc | Use |
|-----|-----|
| [README.md](README.md) | Setup, commands, purpose, directory index |
| [vpn-leaks.md](vpn-leaks.md) | Long-form product / research spec |
| [docs/spec.md](docs/spec.md) | Operational spec |
| [docs/methodology.md](docs/methodology.md) | Full **`vpn-leaks run`** phase order, PCAP finalize, automated vs manual desk |
| [docs/website-exposure-methodology.md](docs/website-exposure-methodology.md) | Website third-party exposure methodology; **harness automates** Phases **1–9** into `normalized.json` (`website_exposure_methodology`); manual desk scripts remain optional for edge cases |
| [docs/competitive-capture-playbook.md](docs/competitive-capture-playbook.md) | UTM golden VM, **`attach-capture` vs `with-pcap`**, tcpdump/sudo, **dpkt** summarization (**no Wireshark**/mitmproxy), remaining optional backlog |
| [docs/data-dictionary.md](docs/data-dictionary.md) | `normalized.json` fields + **`graph-export`** overview |
| [docs/framework.md](docs/framework.md) | Question bank, CLI flags (`--capture-baseline`, `--transition-tests`), `framework` object |
| [RUN-STEPS.md](RUN-STEPS.md) | Nord-oriented step-through; see header callout for methodology + PCAP (README / **docs/methodology.md**) |
| [progress.md](progress.md) | Project progress, Nord run table, gap-closure notes, policy notes |
| [docs/competitor-probe-checklist.md](docs/competitor-probe-checklist.md) | Filling **`competitor_probe`** YAML; **`provider_dns` (O)** vs **`website_exposure_methodology`** (desk automation) vs manual **S** |
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
5. **Reporting changes:** [vpn_leaks/reporting/generate_reports.py](vpn_leaks/reporting/generate_reports.py), [html_dashboard.py](vpn_leaks/reporting/html_dashboard.py), [web_exposure.py](vpn_leaks/reporting/web_exposure.py), [exposure_graph.py](vpn_leaks/reporting/exposure_graph.py), [static/report.css](vpn_leaks/reporting/static/report.css), templates (`vpn_report.md.j2`, `vpn_report_document.html.j2`), and—when changing rollup “Next steps”—[configs/framework/report_hints.yaml](configs/framework/report_hints.yaml) with [coverage.py](vpn_leaks/framework/coverage.py) / [coverage_rollup.py](vpn_leaks/reporting/coverage_rollup.py).
6. **Capture / methodology:** [vpn_leaks/capture/](vpn_leaks/capture/), [finalize_bundle.py](vpn_leaks/capture/finalize_bundle.py), [vpn_leaks/cli.py](vpn_leaks/cli.py) (`--attach-capture`, `--with-pcap`), [website_exposure_methodology.py](vpn_leaks/checks/website_exposure_methodology.py), [pcap_summarize.py](vpn_leaks/checks/pcap_summarize.py), [config_loader.py](vpn_leaks/config_loader.py) hints—keep [docs/methodology.md](docs/methodology.md), [README Run](README.md), and this file in sync.

---

## Update this file

When you make **significant** architectural or workflow changes, add a short subsection here or extend **[progress.md](progress.md)** so the next agent inherits accurate context.
