# Run steps: `vpn-leaks run --provider nordvpn --skip-vpn --force`

This document walks through what the harness does for that command. **Defaults assumed:** `--locations` omitted (auto location from exit IP + geo), `--auto-location` on (default), locations **persisted** into `configs/vpns/nordvpn.yaml` unless you pass `--no-persist-locations`.

---

## 1. CLI parsing

**Input (argv)**

```text
vpn-leaks run --provider nordvpn --skip-vpn --force
```

**Effect**

| Flag | Meaning |
|------|---------|
| `--provider nordvpn` | Load `configs/vpns/nordvpn.yaml` (slug `nordvpn`). |
| `--skip-vpn` | Same as `--dry-run`: do **not** call `adapter.connect` / `adapter.disconnect`. |
| `--force` | (a) Do **not** exit early when this exit IPv4 was already benchmarked for `nordvpn`. (b) If `normalized.json` for a location already exists in this run, **re-run** and overwrite it instead of skipping. |

**Output**

- No stdout yet; later steps log to **stderr** and append to `runs/<run_id>/raw/connect.log`.

---

## 2. Load configuration files

**Inputs (on disk)**

| Path | Role |
|------|------|
| `configs/vpns/nordvpn.yaml` | Provider name, `connection_mode`, `locations`, policy URLs, `competitor_probe`, etc. |
| `configs/tools/leak-tests.yaml` | `stabilize_seconds`, `ip_endpoints`, DNS/WebRTC/IPv6/browser probe settings. |
| `configs/tools/attribution.yaml` | Attribution merge settings (RIPE / Cymru / etc.). |

**Example (`nordvpn.yaml` excerpt)**

```yaml
provider_name: NordVPN
slug: nordvpn
connection_mode: manual_gui
locations:
  - id: us-california-santa-clara-157
    label: Santa Clara, California, United States
policy_urls:
  - https://my.nordaccount.com/legal/privacy-policy/
```

**Example (`leak-tests.yaml` excerpt)**

```yaml
stabilize_seconds: 3
ip_endpoints:
  - url: "https://api.ipify.org"
    format: text
```

**Output**

- In-memory dicts used for preflight IP, probes, and merge behavior.

---

## 3. Preflight: discover exit IPv4

**What runs**

- `quick_exit_ip(leak_cfg)` uses **only the first** `ip_endpoints` entry (here `https://api.ipify.org`) in a temp directory and records which service was contacted.

**Example HTTP behavior**

- GET `https://api.ipify.org` → response body is a plain IPv4 string, e.g. `203.0.113.42`.

**Example output (tuple)**

```text
("203.0.113.42", ["https://api.ipify.org"])
```

**Failure**

- If no IPv4 is obtained, stderr prints `Preflight failed: could not determine exit IPv4.` and the process exits with code `1`.

---

## 4. Duplicate-run guard (skipped because of `--force`)

**Without `--force`**

- `find_prior_run_with_same_exit(vpn_provider="nordvpn", exit_ip_v4=<v4>)` scans `runs/*/locations/*/normalized.json`.
- If any prior row has `vpn_provider == "nordvpn"` and `exit_ip_v4` equal to the preflight IP, the run **stops** with stderr like:

```text
Skipping: this exit IPv4 (203.0.113.42) was already benchmarked for provider 'nordvpn'.
Prior result: runs/nordvpn-20260414T120000Z-a1b2c3d4/locations/us-west-1/normalized.json
Use --force to run the full suite again anyway.
```

(exit code `0` — intentional “no-op success”.)

**With `--force` (your command)**

- This check is **not** performed; execution continues.

---

## 5. Resolve location(s) — auto mode

**Input**

- No `--locations` → **auto** mode (`args.locations is None`).
- Requires `auto_location` true (default).

**Steps**

1. `fetch_geo_sync(v4)` → GET `https://ipwho.is/<exit_ip>` (async via httpx).
2. `build_location_from_geo(geo, v4)` → `(location_id, label, geo_snapshot)`.
3. If geo fails, stderr may show `Geo lookup failed (...); using exit-IP fallback for location id.` and id becomes like `auto-ip-42`.

**Example geo response (illustrative)**

```json
{
  "success": true,
  "ip": "203.0.113.42",
  "country_code": "US",
  "region": "California",
  "city": "Santa Clara"
}
```

**Example derived location**

```text
id:    us-california-santa-clara-42
label: Santa Clara, California, US
```

(Exact id depends on slugging and last octet; see `vpn_leaks/auto_connection.py`.)

**Persistence**

- Unless `--no-persist-locations`, `append_location_if_missing` may append `{"id": ..., "label": ...}` to `configs/vpns/nordvpn.yaml` if that id is new.

**Output**

- `locations = [{"id": "<loc_id>", "label": "<label>"}]` (one entry in default auto mode).
- `run_extra["exit_geo"]` gets the geo snapshot for later `normalized.json` `extra`.

---

## 6. Allocate run directory and id

**Input**

- No `--run-id` → new id from `_utc_run_id("nordvpn")`.

**Example run id**

```text
nordvpn-20260415T143022Z-8f3a9c1d
```

**Paths created**

```text
runs/nordvpn-20260415T143022Z-8f3a9c1d/
  run.json
  raw/
    preflight.json
    connect.log
```

**Example `run.json` (illustrative)**

```json
{
  "run_id": "nordvpn-20260415T143022Z-8f3a9c1d",
  "created_utc": "2026-04-15T14:30:22.123456+00:00",
  "git_sha": "a1b2c3d4e5f6...",
  "vpn_provider": "nordvpn",
  "tool_versions": { "python": "3.12.x" },
  "runner_env": {
    "os": "Darwin 24.x.x",
    "kernel": "24.x.x",
    "python": "3.12.x (...)"
  }
}
```

**Example `raw/preflight.json`**

```json
{
  "exit_ip_v4": "203.0.113.42",
  "preflight_services": ["https://api.ipify.org"],
  "auto_location": true
}
```

---

## 7. Adapter and logging setup

**Input**

- `get_adapter("nordvpn", vpn_config)` — CLI adapter for scripted VPNs; for NordVPN with `manual_gui` it still constructs the adapter but **will not connect** when `--skip-vpn` is set.

**Output**

- `runs/.../raw/connect.log` opened for append; each `log(...)` line goes to **stderr** and this file.

**Early log lines (example)**

```text
skip_vpn: not invoking adapter.connect
```

---

## 8. Per location: skip existing artifact? (`--force` matters again)

For each selected location, target normalized path:

```text
runs/<run_id>/locations/<loc_id>/normalized.json
```

**Without `--force`**, if that file already exists:

```text
skip (exists): runs/.../locations/us-california-santa-clara-42/normalized.json
```

**With `--force`**, that skip is **not** taken; the suite runs and **overwrites** `normalized.json`.

---

## 9. Per location: stabilize, then probes (order fixed)

**Input**

- `stabilize_seconds` from leak-tests config (default `3`).
- `--skip-vpn` → `skip_vpn = true`.

**Sequence (each step writes under `runs/<run_id>/raw/<loc_id>/`)**

| Step | Function | Example artifacts |
|------|----------|-------------------|
| Sleep | `time.sleep(3)` | — |
| Exit IPs | `run_ip_check_sync` | `ip-check.json` |
| DNS | `run_dns_checks_sync` | `dnsleak/` (e.g. `dns_summary.json`, HTML captures) |
| IPv6 | `run_ipv6_checks_sync` | `ipv6/` |
| WebRTC | `run_webrtc_check` | `webrtc/` |
| Fingerprint | `run_fingerprint_snapshot` | `fingerprint/` (may be minimal if disabled in YAML) |
| Attribution | `merge_attribution` | `attribution.json`, optional `asn_prefixes.json` |
| Policies | `fetch_policies` | `policy/*.html`, hashes in normalized output |
| YourInfo | `run_yourinfo_probe` | `yourinfo_probe/` |
| BrowserLeaks | `run_browserleaks_probe` | `browserleaks_probe/` |
| Competitor | `run_competitor_probes` | `competitor_probe/` |
| Surface | `run_surface_probes` | `surface_probe/` (if any) |

**Example stderr + log**

```text
skip_vpn: not invoking adapter.connect
... (after probes) ...
skip_vpn: not invoking adapter.disconnect
wrote runs/nordvpn-20260415T143022Z-8f3a9c1d/locations/us-california-santa-clara-42/normalized.json
```

**`--transition-tests` with `--skip-vpn`**

- For **`manual_gui`**, transition tests **still run** and write `raw/<loc>/transitions.json` with `status: skipped` (no automated disconnect/reconnect). For scripted modes, full transition polling runs only when **`--skip-vpn` is not** set.

---

## 10. Build `normalized.json`

**Input**

- All probe results above, plus manifest, location id/label, `connection_mode` from YAML (`manual_gui` for NordVPN example).

**Processing**

- Construct `NormalizedRun` (Pydantic model).
- Unless `--no-framework`, `apply_framework(normalized)` adds SPEC framework fields (coverage, findings, risk scores).

**Example output path**

```text
runs/nordvpn-20260415T143022Z-8f3a9c1d/locations/us-california-santa-clara-42/normalized.json
```

**Example excerpt (illustrative)**

```json
{
  "run_id": "nordvpn-20260415T143022Z-8f3a9c1d",
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-santa-clara-42",
  "exit_ip_v4": "203.0.113.42",
  "connection_mode": "manual_gui",
  "dns_leak_flag": false,
  "framework": { "...": "..." }
}
```

---

## 11. Run summary

**Input**

- `run_root`, list of `normalized_paths` written this session.

**Output file**

```text
runs/<run_id>/summary.md
```

**Example `summary.md` excerpt**

```markdown
# Run summary

- Run directory: `.../runs/nordvpn-20260415T143022Z-8f3a9c1d`
- Locations: 1

- `runs/nordvpn-20260415T143022Z-8f3a9c1d/locations/us-california-santa-clara-42/normalized.json`

## Aggregated report

- Markdown rollup `VPNs/NORDVPN.md` and the **dashboard HTML** `VPNs/NORDVPN.html` (visual-first layout, full narrative in a collapsible section) — regenerate with `vpn-leaks report --provider nordvpn`
- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
```

---

## 12. Final stderr line

**Example**

```text
Run complete: /path/to/vpn-leaks/runs/nordvpn-20260415T143022Z-8f3a9c1d
```

**Exit code:** `0` on success.

---

## What this command does *not* do

- **Does not** run `vpn-leaks report` — `VPNs/NORDVPN.md` / `.html` are updated only when you run `vpn-leaks report --provider nordvpn` separately.
- **Does not** run `vpn-leaks graph-export` — exposure graph JSON is separate.
- **Does not** connect or disconnect the NordVPN app — you are expected to have the tunnel up already when using `--skip-vpn`.

---

## Quick reference: artifacts under `runs/<run_id>/`

| Path | Purpose |
|------|---------|
| `run.json` | Manifest (env, git sha, run id). |
| `raw/preflight.json` | Exit IPv4 from preflight + flags. |
| `raw/connect.log` | Timestamped log lines (includes `skip_vpn` messages). |
| `raw/<loc_id>/` | Raw probe outputs (ip-check, dnsleak, webrtc, ipv6, attribution, policy, probes, …). |
| `locations/<loc_id>/normalized.json` | Canonical structured result (+ framework if enabled). |
| `summary.md` | Pointers to this run’s JSON and the aggregated VPN report command. |
