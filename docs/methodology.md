# Methodology

## Order of operations (`vpn-leaks run`)

The live harness runs steps in this order (see [`vpn_leaks/cli.py`](../vpn_leaks/cli.py)):

1. **Preflight** — Resolve exit IPv4 once using the first endpoint in [`configs/tools/leak-tests.yaml`](../configs/tools/leak-tests.yaml) (same machinery as the full IP check, minimal disk use). Record summary under `runs/<run_id>/raw/preflight.json` after the run directory is created (see below).

2. **Duplicate guard** — Search all existing `runs/*/locations/*/normalized.json` for the same `vpn_provider` slug. If any row has the same `exit_ip_v4` as preflight, **stop** (exit 0) unless **`--force`**. This avoids re-benchmarking the same tunnel exit without meaning to.

3. **Location resolution**
   - **Auto (default):** If **`--locations` is omitted**, call **ipwho.is** for the preflight IP, derive `vpn_location_id` (e.g. `cc-region-city-lastOctet`) and label, optionally **append** to `configs/vpns/<slug>.yaml` (unless `--no-persist-locations`). Snapshot stored in **`extra.exit_geo`** on `normalized.json`.
   - **Manual:** If **`--locations id …`** is passed, use entries from YAML (and append unknown ids when persisting), or require **`--no-auto-location`** when you must not use auto-detect.

4. **Run directory** — Create `runs/<run_id>/`, write `run.json`, then `raw/preflight.json`, then proceed per location.

5. **Per location (tunnel must already match your intent)**  
   - **Connect** — Unless **`--skip-vpn` / `--dry-run`**, adapter connect (or manual GUI prompt).  
   - **Stabilize** — Cooldown from config.  
   - **Exit IP** — Full multi-endpoint capture to `raw/<location_id>/ip-check.json`.  
   - **Leak suite** — DNS, IPv6, WebRTC, optional fingerprint.  
   - **Attribution** — RIPEstat, Team Cymru, PeeringDB, optional GeoLite.  
   - **Policy** — Fetch VPN (and optional underlay) URLs; hash + store HTML.  
   - **Disconnect** — Unless skipped.  
   - **Write** — `locations/<location_id>/normalized.json`.

6. **Repeat** — Next location in the resolved list (often one location per run when using auto + GUI VPN).

7. **Summary** — `runs/<run_id>/summary.md`.

For **vendor GUI only** (e.g. NordVPN macOS app), connect **before** running and use **`--skip-vpn`** so the harness does not prompt for connect/disconnect; preflight still reflects the active tunnel.

## Standard run loop (conceptual — one location)

Aligned with [vpn-leaks.md](../vpn-leaks.md): account ready → connect → stabilize → exit IP → leak suite → attribution → policy → disconnect → repeat. The numbered sequence above is how the **implemented** CLI orders work, including preflight and duplicate detection before heavy I/O.

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
5. **Optional** — `competitor_surface` (apex DNS, NS glue attribution, web/CDN, HAR summary, portals, transit) when `competitor_probe` is configured. See [competitor-probe-checklist.md](competitor-probe-checklist.md) for YAML fields.
6. **Optional** — `yourinfo_snapshot` unless `--skip-yourinfo`.

### Reproducibility

- **Code state:** `run.json` should record `git_sha` when available.
- **Environment:** `runner_env` (OS, kernel, Python, VPN mode).
- **Canonical record:** `runs/<run_id>/locations/<location_id>/normalized.json` is the single structured artifact for tooling and reports.

### Interpretation

- Leak flags are **heuristics** from client-observable tests; **“no leak”** means the harness did not flag an issue under those conditions, not a proof of privacy against all adversaries or all traffic paths.
- Provider apex DNS and **NS glue** attribution (see [data-dictionary](data-dictionary.md)) describe **public DNS/routing relationships**, not VPN tunnel contents.

### Aggregates and graphs

- Rollup markdown: `vpn-leaks report --provider <slug>` → `VPNs/<SLUG>.md`.
- Exposure graph export (nodes/edges for analysis or 3D viewer): `vpn-leaks graph-export` — see [README](../README.md).
