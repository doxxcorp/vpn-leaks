# Methodology

## Order of operations (`vpn-leaks run`)

The live harness runs steps in this order (see [`vpn_leaks/cli.py`](../vpn_leaks/cli.py)):

1. **Preflight** — Resolve exit IPv4 once using the first endpoint in [`configs/tools/leak-tests.yaml`](../configs/tools/leak-tests.yaml) (same machinery as the full IP check, minimal disk use). Record summary under `runs/<run_id>/raw/preflight.json` after the run directory is created (see below).

2. **Duplicate guard** — Search all existing `runs/*/locations/*/normalized.json` for the same `vpn_provider` slug. If any row has the same `exit_ip_v4` as preflight, **stop** (exit 0) unless **`--force`**. This avoids re-benchmarking the same tunnel exit without meaning to.

3. **Location resolution**
   - **Auto (default):** If **`--locations` is omitted**, call **ipwho.is** for the preflight IP, derive `vpn_location_id` (e.g. `cc-region-city-lastOctet`) and label, optionally **append** to `configs/vpns/<slug>.yaml` (unless `--no-persist-locations`). Snapshot stored in **`extra.exit_geo`** on `normalized.json`.
   - **Manual:** If **`--locations id …`** is passed, use entries from YAML (and append unknown ids when persisting), or require **`--no-auto-location`** when you must not use auto-detect.

4. **Run directory** — Create `runs/<run_id>/`, write `run.json`, then `raw/preflight.json`, then proceed per location.

5. **Per location (tunnel must already match your intent)** — executed in order (same as [`vpn_leaks/cli.py`](../vpn_leaks/cli.py)):

   1. **Connect** — Unless **`--skip-vpn` / `--dry-run`**, adapter connect (or manual GUI prompt).  
   2. **Stabilize** — Cooldown from `leak-tests.yaml`.  
   3. **Exit IP** — Full multi-endpoint capture → `raw/<location_id>/ip-check.json`.  
   4. **Leak suite** — DNS leaks, IPv6, WebRTC, optional fingerprint snapshots.  
   5. **Attribution** — RIPEstat, Team Cymru, PeeringDB, optional GeoLite → `attribution.json` (etc.).  
   6. **Privacy policies** — Fetch URLs from `policy_urls` / optional `underlay_policy_urls`; hash HTML + excerpts.  
   7. **yourinfo.ai** — Playwright HAR + excerpt (unless **`--skip-yourinfo`**).  
   8. **BrowserLeaks** — Pinned pages (unless **`--skip-browserleaks`** / disabled in config).  
   9. **Competitor probes** — When `competitor_probe` is set in provider YAML: apex DNS, web/HAR, portals, transit, stray JSON (individual phases skippable with **`--skip-competitor-*`**).  
   10. **Surface probes** — When `surface_urls` is configured: tagged Playwright loads + HAR (`surface_probe/`).  
   11. **Transition tests** — Optional (**`--transition-tests`**); reconnect polling where the adapter applies.  
   12. **Website exposure methodology** — Automated desk bundle (**Phases 1–9 projection**) into **`normalized.json.website_exposure_methodology`** and `raw/<location_id>/website_exposure/`; fail-soft per phase. Prerequisites: principally **`competitor_probe.provider_domains`** (stderr **hints** from `methodology_config_hints` when incomplete). Runs **before** disconnect in the harness.  
   13. **Disconnect** — Unless **`--skip-vpn`**.  
   14. **Write** — Apply SPEC framework (**`--no-framework`** to skip) → **`locations/<location_id>/normalized.json`**.

6. **Repeat** — Next location in the resolved list (often one location per run when using auto + GUI VPN).

7. **PCAP finalize (optional)** — If **`--attach-capture`** (active session from `vpn-leaks capture start`) **or** **`--with-pcap`** (harness started tcpdump at run beginning): stop **tcpdump**, copy PCAP to **`runs/<run_id>/raw/<location_id>/capture/`**, write **`pcap_summary.json`** (Python/**dpkt**), merge **`pcap_derived`** and **`artifacts.capture_dir`** (+ **`capture_finalize`** audit fields) into each **newly written** location’s **`normalized.json`**. Mutually exclusive flags; **`--with-pcap`** conflicts with another active **`capture`** session ([competitive-capture-playbook.md](competitive-capture-playbook.md)).

8. **Summary** — `runs/<run_id>/summary.md`.

For **vendor GUI only** (e.g. NordVPN macOS app), connect **before** running and use **`--skip-vpn`** so the harness does not prompt for connect/disconnect; preflight still reflects the active tunnel.

## Standard run loop (conceptual — one location)

Aligned with [vpn-leaks.md](../vpn-leaks.md): connect → stabilize → exit IP → leak suite → attribution → policies → optional probes (yourinfo, browserleaks, competitor, surface) → optional transition tests → **website exposure methodology** → disconnect → write `normalized.json`. The numbered sequence above is how the **implemented** CLI orders work, including preflight and duplicate detection before heavy I/O.

## Isolation and reproducibility

- Prefer a dedicated VM or clean network namespace for comparable runs.
- Record OS, kernel, browser, and VPN client versions in `run.json` / `runner_env`.
- Use multi-source checks; disagreement between attribution sources lowers confidence.

## DNS and WebRTC reliability

- **DNS:** Tier A — OS resolver snapshot + controlled queries; Tier B — external leak-test pages (pinned URLs, timeouts, saved HTML). Compare baseline vs VPN state; encode platform quirks in reports when relevant.
- **WebRTC:** Controlled Playwright session with configurable STUN servers, time-bounded ICE gathering, candidate classification vs expected exit IP; retries and raw artifacts on failure.

## Manual vs automated boundaries

- Signup/payment: manual by default.
- GUI: **prompted manual connect** or **you connect first + `--skip-vpn`** when the vendor app cannot be scripted.
- Vendor scraping / API automation: explicit config opt-in only.

## Third-party services (auto location)

Auto mode uses **ipwho.is** (and records it in `services_contacted`). That implies an HTTP request from your machine; see [README](../README.md) security notes.

## Systematic research (matrix and checklist)

Use this when comparing providers or publishing results so benchmarks are **comparable** and **reproducible**.

**Full mapping:** Every framework question with primary artifact paths, evidence tiers (**O** / **S** / **D** / **I**), systematic `dig`/WHOIS playbook, example answer shapes, Mermaid FD graphs, and how this relates to `graph-export` / the 3D viewer — see [research-questions-and-evidence.md](research-questions-and-evidence.md).

### Dimensions

Each benchmark is a point in a space you should record explicitly:

| Dimension | Where it lives |
|-----------|----------------|
| VPN provider | `vpn_provider` (slug), `configs/vpns/<slug>.yaml` |
| Exit / location | `vpn_location_id`, `vpn_location_label`, `extra.exit_geo` when auto |
| Run identity | `run_id`, folder `runs/<run_id>/` |
| Time | `timestamp_utc`, `run.json` `created_utc` |

### Minimum probe set (typical “full” run)

Align questions to probes; not every question needs every probe.

1. **Tunnel / exit** — `exit_ip_v4` / `exit_ip_v6`, `exit_ip_sources` (multi-endpoint).
2. **Leak heuristics** — DNS (`dns_servers_observed`, `dns_leak_flag`), WebRTC, IPv6.
3. **Exit attribution** — `attribution` (RIPEstat, Team Cymru, PeeringDB, optional GeoLite).
4. **Policies** — `policies` (VPN + optional underlay URLs), hashes and summaries.
5. **Optional** — `competitor_surface` when `competitor_probe` is configured ([competitor-probe-checklist.md](competitor-probe-checklist.md)).
6. **Optional** — `surface_probe` / **`extra.surface_probe`** when `surface_urls` is set.
7. **Optional** — `yourinfo_snapshot` unless **`--skip-yourinfo`**.
8. **Optional** — `browserleaks_snapshot` unless skipped.
9. **Optional** — `website_exposure_methodology` desk-automation tier when apex domains (**`provider_domains`**) allow Phase 8–9 projection ([data-dictionary](data-dictionary.md), [website-exposure-methodology §10](website-exposure-methodology.md)).
10. **Optional** — `pcap_derived` + `artifacts.capture_dir` after **`--attach-capture`** or **`--with-pcap`** finalize.

### Reproducibility

- **Code state:** `run.json` should record `git_sha` when available.
- **Environment:** `runner_env` (OS, kernel, Python, VPN mode).
- **Canonical record:** `runs/<run_id>/locations/<location_id>/normalized.json` is the single structured artifact for tooling and reports.

### Interpretation

- Leak flags are **heuristics** from client-observable tests; **“no leak”** means the harness did not flag an issue under those conditions, not a proof of privacy against all adversaries or all traffic paths.
- Provider apex DNS and **NS glue** attribution (see [data-dictionary](data-dictionary.md)) describe **public DNS/routing relationships**, not VPN tunnel contents.

### Website third-party exposure — automated vs manual deepening

**During `vpn-leaks run` (automated — first-class in `normalized.json`):**

- The harness merges **OBSERVED (O)** signals from **`competitor_probe`** (apex DNS/`provider_dns.json`, web/HAR, portals, transit) and optional **`surface_urls`** / **`surface_probe`** into **`competitor_surface`** / **`extra.surface_probe`**.
- It additionally runs **`website_exposure_methodology`**: compact Phases **1–9 projection** — including SPF include walk, DMARC/DKIM/TXT probing, subdomain CNAME scan, and **`phase9_third_party_inventory`** with **`evidence_tier: desk_automation`** and an explicit **`evidence_tier_note`** (desk automation, **not** the same tier as client DNS-leak probes). Raw JSON lives under **`raw/<location_id>/website_exposure/`** when populated.
- On **stderr**, **`methodology_config_hints`** reminds you if **`competitor_probe.provider_domains`** is empty (Phase 8–9 automation largely skipped), **`surface_urls`** is empty (weaker host inventory), or **`policy_urls`** is empty (no marketing policy HTML fetched). Mapping table: [website-exposure-methodology.md §10](website-exposure-methodology.md).

**Optional manual deepening (S / narrative archival):**

Use when you need **full `dig`/transcript archival**, narrative-only evidence tiers, or edge cases (**SPF permerror**, blocked resolvers). Same day as the run — record which resolver you used:

1. Follow [website-exposure-methodology.md](website-exposure-methodology.md) for manual Phases **8–9** transcripts per apex ([research-questions-and-evidence.md](research-questions-and-evidence.md) §H pattern).
2. Archive (e.g. `research/desk-<date>-<apex>.txt`) or use [scripts/desk_dns_audit.sh](../scripts/desk_dns_audit.sh) for a Phase-8-style `dig` bundle (stdout paste-friendly).

When writing **`vpn-leaks report`** narrative, keep **desk / automation** apex and email infra separate from **`dnsleak/`** tunnel resolver evidence (**DNS-001**). See evidence tiers in [research-questions-and-evidence.md](research-questions-and-evidence.md).

### Aggregates and graphs

- Rollup markdown + HTML dashboard: **`vpn-leaks report --provider <slug>`** → **`VPNs/<SLUG>.md`** and **`VPNs/<SLUG>.html`** (includes **website-exposure methodology** and **PCAP-derived** subsections when `normalized.json` carries those blocks).
- Exposure graph (`vpn_leaks/reporting/exposure_graph.py`): **`vpn-leaks graph-export`** emits **`graph_schema` 1.1** payloads that can add PCAP-derived observation edges (**`pcap_ip_flow`**, **`tls_sni_observed`**, etc.) whenever **`pcap_derived`** is present on merged runs — see [data-dictionary § graph-export](data-dictionary.md) and [viewer/README](../viewer/README.md).
