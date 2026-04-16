# VPN Leaks — project progress

_Last updated: 2026-04-16._

## 2026-04-16 — VPN HTML report UX (location cards, exposure graph, SPEC hints)

- **[`vpn_report_document.html.j2`](vpn_leaks/reporting/templates/vpn_report_document.html.j2):** Benchmark **location cards** use **CSS subgrid** so rows line up across cards; **Exit IPv6** always shown; short hint distinguishes exit addresses vs leak-test **badges**. **Coverage** blurb states **strictest merge** rule; **SPEC** section adds the same when **multiple locations** exist. **Exposure graph** blurb explains VPN → exit IP → ASN / policies / DNS glue; **3d-force-graph** uses **`three-spritetext`** + **`nodeThreeObjectExtend`** so **labels render on load** (pinned `three@0.160.0` via esm.sh).
- **[`report.css`](vpn_leaks/reporting/static/report.css):** Subgrid + `@supports` fallback (`min-height` on ASN row).
- **[`configs/framework/report_hints.yaml`](configs/framework/report_hints.yaml):** Clearer **FP-001** and **CTRL-002** next-step copy (harness knobs, `services_contacted` scope, multi-location merge).
- **[`coverage.py`](vpn_leaks/framework/coverage.py):** FP-001 unanswered rows omit redundant empty **notes** (hints carry guidance).
- **[HANDOFF.md](HANDOFF.md):** Reporting table and **Viewing `VPNs/<SLUG>.html`** updated for subgrid cards, IPv4/IPv6/badges copy, on-load graph labels, merged SPEC semantics, and pointers to **`report_hints.yaml`** / **`coverage_rollup`**.

## 2026-04-15 — GitHub Pages (doxxcorp.github.io/vpn-leaks)

- **[`.github/workflows/pages.yml`](.github/workflows/pages.yml):** Build job runs [`scripts/build_github_pages_site.py`](scripts/build_github_pages_site.py) to stage `site/` (`VPNs/`, `style/icons/` for SPEC category icon URLs in HTML, `.nojekyll`, generated `index.html` listing `VPNs/*.html`), then `upload-pages-artifact` + `deploy-pages`. Triggers: `push` to `main`/`master` with `paths` on `VPNs/**`, `style/icons/**`, workflow/script, or **workflow_dispatch**.
- **[README.md](README.md):** “GitHub Pages (github.io)” under Reports — URL pattern, Settings note, privacy/plan caveats, local preview via the script.
- **`.gitignore`:** `site/` (local staging output).
- **Public URL:** `https://doxxcorp.github.io/vpn-leaks/` (reports under `/VPNs/<SLUG>.html`).

## 2026-04-15 — HANDOFF.md refresh

- **[HANDOFF.md](HANDOFF.md):** Updated for the **HTML dashboard** (`VPNs/<SLUG>.html`), [`html_dashboard.py`](vpn_leaks/reporting/html_dashboard.py), [`reporting/static/`](vpn_leaks/reporting/static/), **SPEC coverage** alignment notes, and the reporting table / CLI blurbs.

## 2026-04-15 — VPN HTML report dashboard (visual-first)

- **`vpn_report_document.html.j2`:** Replaced the single long markdown article with a **dashboard**: header + isotype, **risk strip** (rollup severity, leak chips), **location cards** (exit IP, ASN, resolver summary, flags), **third-party panel** when competitor data exists, **SPEC accordions** by category, existing **coverage bar** + **3D exposure graph**, and the full markdown HTML under **`<details class="report-appendix">`**.
- **Static bundle:** [`vpn_leaks/reporting/static/report.css`](vpn_leaks/reporting/static/report.css) (doxx-aligned tokens, Syne + JetBrains Mono), [`logo-isotype.svg`](vpn_leaks/reporting/static/logo-isotype.svg) from the org style repo; CSS/logo embedded at render time via [`generate_reports.py`](vpn_leaks/reporting/generate_reports.py).
- **Context:** [`vpn_leaks/reporting/html_dashboard.py`](vpn_leaks/reporting/html_dashboard.py) — `build_html_dashboard_context` for template props.
- **Docs:** [docs/framework.md](docs/framework.md) HTML subsection; [RUN-STEPS.md](RUN-STEPS.md) aggregated report bullet.

## 2026-04-15 — SPEC coverage parity and NordVPN example config

- **`coverage.py`:** Question handlers align with **`scoring.py`**: **WEB-004**, **CTRL-009**, **SIGNUP-***, and **THIRDWEB-*** treat **`portal_probes`** like **`web_probes`**. **FP-001** / **IDENTITY-001** / **IDENTITY-009** count **`browserleaks_snapshot`** as fingerprint-class evidence. **EXIT-004** reads **`exit_dns.json`** via **`artifacts.exit_dns_json`** (PTR present → `answered`; empty/error → explicit partial summaries). **EXIT-005** and **IP-014** emit deterministic comparison text from **`extra.exit_geo`** / **`exit_ip_sources`**.
- **`configs/vpns/nordvpn.yaml`:** **`policy_urls`**, **`competitor_probe`** (`provider_domains`, `probe_urls`, `portal_hosts`), and a comment pointing to **`--transition-tests`** for transition-phase questions.
- **Tests:** [`tests/test_framework.py`](tests/test_framework.py) covers portal-only WEB-004, BrowserLeaks-only FP-001, IP-014 agreement, EXIT-005 consistency, EXIT-004 fixture read; [`tests/fixtures/exit_dns_no_ptr.json`](tests/fixtures/exit_dns_no_ptr.json).

## 2026-04-12 — SPEC framework (question bank, coverage, findings)

- **`schema_version` 1.4:** optional **`framework`** on `normalized.json` (findings, per-question coverage, risk scores, classified hosts). Synthesis in [`vpn_leaks/framework/`](vpn_leaks/framework/); config in [`configs/framework/`](configs/framework/). Opt out: **`--no-framework`**.
- **CLI:** `--capture-baseline` writes `raw/baseline.json`; **`--transition-tests`** writes `raw/<loc>/transitions.json` (skipped for `manual_gui`). Provider YAML may define **`surface_urls`** for extra HAR under `surface_probe/` ([`vpn_leaks/checks/surface_probe.py`](vpn_leaks/checks/surface_probe.py)).
- **Reports:** [`vpn_report.md.j2`](vpn_leaks/reporting/templates/vpn_report.md.j2) adds an **Executive summary (SPEC framework)** rollup; per-run **SPEC framework** subsection. Docs: [docs/framework.md](docs/framework.md).

## 2026-04-10 — Systematic methodology, NS glue attribution, exposure graph

- **Docs:** [docs/methodology.md](docs/methodology.md) adds a **systematic research** section (dimensions, probe checklist, reproducibility, interpretation). [docs/data-dictionary.md](docs/data-dictionary.md) documents **`schema_version` 1.3** and `provider_dns.ns_hosts` with per-IP **`ip_attribution`** (NS glue).
- **DNS:** [`run_provider_dns`](vpn_leaks/checks/competitor_probes.py) resolves each NS hostname’s A/AAAA and runs [`merge_attribution_for_ip`](vpn_leaks/attribution/merge.py) (refactored `collect_attribution_sources`; IPv6 skips Team Cymru TXT). **`services_contacted`** includes `dns:ns_glue:` and `attribution:ns_glue:` entries; ~250 ms between uncached glue IPs to reduce API pressure.
- **CLI:** `vpn-leaks graph-export [--provider SLUG] [-o file]` writes nodes/edges JSON via [`exposure_graph.py`](vpn_leaks/reporting/exposure_graph.py).
- **Viewer:** [viewer/](viewer/) — static **3D** page (3d-force-graph via CDN) + [viewer/README.md](viewer/README.md).

## 2026-04-10 — VPN rollup report readability

- **Templates / code:** [`vpn_report.md.j2`](vpn_leaks/reporting/templates/vpn_report.md.j2) now starts with a **How to read** block, lists each included run **before** **Detailed runs**, and shows a **blockquote** of `truncation_notes` when any fenced JSON or list is size-capped ([`generate_reports.py`](vpn_leaks/reporting/generate_reports.py): `_fence_json` returns `(fence, truncated)`; `competitor_surface` gets `absent` / `null` / `empty` / `data`). Empty sections use explanatory text instead of bare `*(none)*`. Each run’s `summary.md` (via `write_run_summary`) includes pointers to `VPNs/<SLUG>.md` and canonical `normalized.json`.

## 2026-04-10 — YourInfo capture + comprehensive `VPNs/` reports

- **yourinfo.ai:** Each location run loads the third-party benchmark page in Playwright after policy fetch ([`vpn_leaks/checks/yourinfo_probe.py`](vpn_leaks/checks/yourinfo_probe.py)); writes `raw/<loc>/yourinfo_probe/yourinfo.json` + `yourinfo.har`; **`normalized.json` `schema_version` 1.2** adds `yourinfo_snapshot` and `artifacts.yourinfo_probe_dir`. Opt out: **`--skip-yourinfo`**.
- **Reports:** [`vpn_leaks/reporting/templates/vpn_report.md.j2`](vpn_leaks/reporting/templates/vpn_report.md.j2) now includes a **Detailed runs** section per `normalized.json` (exit, DNS, WebRTC, IPv6, fingerprint, attribution, policies, services, artifacts, YourInfo, competitor_surface, extra). Large JSON blocks are capped; verbatim data remains in `normalized.json`.

## 2026-04-10 — Competitor-surface probes in `vpn-leaks run`

- **Decision:** Fold competitive-intelligence probes into the same **`vpn-leaks run`** invocation (not a separate subcommand). Config lives under **`competitor_probe`** in [`configs/vpns/<slug>.yaml`](configs/vpns/nordvpn.yaml).
- **Implementation:** [`vpn_leaks/checks/competitor_probes.py`](vpn_leaks/checks/competitor_probes.py) — provider apex **NS/A/AAAA** (dnspython), **traceroute** toward exit IPv4, **Playwright** page loads with **HAR** + CDN-oriented response headers + script/image hosts (captcha heuristics), **HTTPS** probes for portal hosts, bounded **GET**s for stray JSON paths. Summaries go to **`normalized.json`** as `competitor_surface` (`schema_version` **1.1**); raw JSON under `raw/<location>/competitor_probe/`.
- **Dependency:** `dnspython` added in [pyproject.toml](pyproject.toml).
- **NordVPN** config includes example domains/URLs; older benchmark runs remain **`schema_version` 1.0** without `competitor_surface`.

## Where the project stands

The **VPN Leaks harness is implemented and usable end-to-end** in this repository:

- **CLI:** `vpn-leaks run` and `vpn-leaks report` (install with `pip install -e ".[dev]"`, Playwright Chromium for WebRTC and web probes).
- **Preflight:** Each run resolves exit IPv4 first, skips duplicate benchmarks for the same provider + exit IP unless `--force`, and (by default) **auto-detects** location id/label via ipwho.is when `--locations` is omitted.
- **Suite per location:** Multi-source exit IP, DNS (local + IPLeak HTML), IPv6 (curl + test-ipv6 page), WebRTC (Playwright ICE), optional fingerprint, **RIPEstat + Team Cymru + PeeringDB** attribution, **privacy policy** fetch + SHA-256 + keyword summary ([vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py): browser-like httpx headers; **Playwright** when the response is a Cloudflare interstitial or a thin JS shell such as Nord Account; Nord config uses [my.nordaccount.com legal privacy URL](https://my.nordaccount.com/legal/privacy-policy/) because `nordvpn.com/privacy-policy/` is often blocked for automated clients), and optional **competitor_probe** phases when configured (see section above).
- **Artifacts:** Under `runs/<run_id>/` (gitignored): `run.json`, `raw/preflight.json`, per-location `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy HTML, **yourinfo_probe**, optional **competitor_probe**), and `locations/<location_id>/normalized.json`.
- **Docs:** [README.md](README.md), [HANDOFF.md](HANDOFF.md) (full context for future agents), [docs/spec.md](docs/spec.md), [docs/methodology.md](docs/methodology.md), [docs/data-dictionary.md](docs/data-dictionary.md), canonical [vpn-leaks.md](vpn-leaks.md).

**Not in scope for the harness itself:** Proving what NordVPN stores on servers; automating the Nord macOS app (you connect manually, then `vpn-leaks run --provider nordvpn --skip-vpn`).

---

## NordVPN benchmark runs you collected

You ran **`vpn-leaks run --provider nordvpn --skip-vpn`** (auto location) after switching the **NordVPN macOS client** to each destination. That produced **five separate run directories** — one **location / exit** per run — listed **oldest to newest** below.

| # | Run id (folder under `runs/`) | Auto location id | Label (ipwho) | Exit IPv4 | Exit ASN | ASN holder (attribution) | DNS leak | WebRTC leak | IPv6 leak |
|---|------------------------------|------------------|-----------------|-----------|----------|---------------------------|----------|-------------|-----------|
| 1 | `nordvpn-20260410T014115Z-192ddf81` | `us-california-san-francisco-67` | San Francisco, California, United States | 185.187.168.67 | 212238 | CDNEXT - Datacamp Limited | false | false | false |
| 2 | `nordvpn-20260410T020850Z-06046ac5` | `gb-england-london-102` | London, England, United Kingdom | 2.58.73.102 | 62240 | CLOUVIDER - Clouvider Limited | false | false | false |
| 3 | `nordvpn-20260410T020935Z-8559f9bc` | `ca-british-columbia-vancouver-153` | Vancouver, British Columbia, Canada | 45.90.222.153 | 147049 | PACKETHUBSA-AS-AP PacketHub S.A. | false | false | false |
| 4 | `nordvpn-20260410T021013Z-3db4d1ec` | `de-hamburg-hamburg-127` | Hamburg, Hamburg, Germany | 185.161.202.127 | 207137 | PACKETHUBSA - PacketHub S.A. | false | false | false |
| 5 | `nordvpn-20260410T021116Z-5cf8e0dc` | `us-new-mexico-albuquerque-136` | Albuquerque, New Mexico, United States | 66.179.156.136 | 136787 | PACKETHUBSA-AS-AP PacketHub S.A. | false | false | false |

**What each run stored (per location):**

- **`normalized.json`:** Full structured record: `exit_ip_sources`, `dns_servers_observed`, WebRTC candidates, IPv6 status, `attribution` (confidence + sources), `policies` (Nord privacy URL + content hash + heuristic bullets), `services_contacted`, `extra.exit_geo` (ipwho snapshot when auto-location was used).
- **`raw/<location_id>/`:** `ip-check.json`, `dnsleak/` (e.g. `ipleak_dns.html`, `dns_summary.json`), `webrtc/webrtc_candidates.json`, `ipv6/` (curl output, test-ipv6 HTML, summary JSON), `attribution.json`, `policy/` (fetched HTML), optional **`competitor_probe/`** (DNS/transit/web/portal/stray JSON artifacts).
- **`raw/preflight.json`:** Preflight IPv4 and whether auto-location was used for that run.

**Config updated:** [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml) now lists the six location entries (including the older `sf-usa` placeholder) plus the five auto-derived ids above.

**Aggregated markdown reports:** Generate locally with `vpn-leaks report --provider nordvpn` (writes under `VPNs/`, gitignored by default). Underlay-specific report: `vpn-leaks report --provider nordvpn --asn <asn>` if you want a file per ASN.

**Historical note (2026-04-10 runs):** Those five `normalized.json` files record **`fetch error: 403`** for the old policy URL (`https://nordvpn.com/privacy-policy/`). New runs after the fetch + config change above should populate `policies[].sha256` and keyword bullets; re-run benchmarks if you need on-disk policy HTML under `raw/.../policy/` for Nord.

---

## Quick reference paths

```text
runs/nordvpn-20260410T014115Z-192ddf81/locations/us-california-san-francisco-67/normalized.json
runs/nordvpn-20260410T020850Z-06046ac5/locations/gb-england-london-102/normalized.json
runs/nordvpn-20260410T020935Z-8559f9bc/locations/ca-british-columbia-vancouver-153/normalized.json
runs/nordvpn-20260410T021013Z-3db4d1ec/locations/de-hamburg-hamburg-127/normalized.json
runs/nordvpn-20260410T021116Z-5cf8e0dc/locations/us-new-mexico-albuquerque-136/normalized.json
```

If you delete `runs/` later, this table is the snapshot of what was collected on **2026-04-10**; re-run the commands above to regenerate data.
