# Data dictionary

## `runs/<run_id>/run.json`

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | string | Unique run identifier |
| `created_utc` | ISO-8601 | Manifest creation time |
| `git_sha` | string? | `git rev-parse HEAD` when available |
| `vpn_provider` | string | Slug from config |
| `tool_versions` | object | e.g. Python version |
| `runner_env` | object | OS, kernel, python |

## `runs/<run_id>/raw/` layout

Top-level files under `raw/`:

| Path | Content |
|------|---------|
| `preflight.json` | Preflight exit IPv4, `preflight_services`, `auto_location` (whether ids came from ipwho auto-detect) |
| `baseline.json` | Optional; when `--capture-baseline`: snapshot IP + optional `scutil --dns` (macOS) |
| `connect.log` | Adapter / orchestrator log |

Per **location** (under `raw/<location_id>/`):

| Path | Content |
|------|---------|
| `ip-check.json` | Raw multi-source IP responses |
| `dnsleak/` | Resolver snapshots, external test HTML |
| `webrtc/` | ICE candidate JSON |
| `ipv6/` | curl output, external page HTML |
| `fingerprint/` | Optional fingerprint JSON |
| `pcap/` | Optional (gated) |
| `attribution.json` | Raw RIPEstat/Cymru/PeeringDB responses |
| `asn_prefixes.json` | RIPEstat **announced-prefixes** for merged exit ASN (slim list + cache metadata) |
| `exit_dns.json` | **PTR** lookups for exit IPv4/IPv6 |
| `policy/` | `vpn_policy_*.html`, underlay HTML |
| `competitor_probe/` | If `competitor_probe` is set in `configs/vpns/<slug>.yaml`: `provider_dns.json` (apex NS/A/AAAA/**TXT/MX/CAA** plus **`ns_hosts`** glue + attribution), `transit.json`, `web_probes.json`, `har/*.har`, **`har_summary.json`** (aggregated HAR hosts + tracker/CDN hints), `portal_probes.json`, `stray_json.json` |
| `yourinfo_probe/` | Always-on unless `--skip-yourinfo`: `yourinfo.json`, `yourinfo.har` (third-party benchmark page) |
| `browserleaks_probe/` | Unless `--skip-browserleaks` and `browserleaks_probe` enabled in `leak-tests.yaml`: `browserleaks.json`, `browserleaks.har` (pinned `/ip`, `/dns`, `/webrtc`, `/tls` pages) |
| `surface_probe/` | Optional; when `surface_urls` in provider YAML: `web_probes.json`, `har/*.har` per page |
| `transitions.json` | Optional; when `--transition-tests`: IP poll samples across disconnect/reconnect |

## `runs/<run_id>/locations/<location_id>/normalized.json`

Aligned with `vpn_leaks.models.NormalizedRun` (`schema_version`).

| Field | Notes |
|-------|--------|
| `schema_version` | **1.5** (current): adds **`website_exposure_methodology`** (automated Phases 1–9 desk bundle), **`pcap_derived`** (PCAP summary blob, `schema_version` inside), **`capture_finalize`** (attach-capture audit). Previous **1.4** added **`framework`**. Older: `1.1`–`1.3` as before (`competitor_surface`, `yourinfo_snapshot`, `ns_hosts`, etc.) |
| `run_id` | Parent run |
| `timestamp_utc` | Location run start/end |
| `runner_env` | OS, kernel, browser, vpn_protocol |
| `vpn_provider` | Provider slug |
| `vpn_location_id` / `vpn_location_label` | From YAML/adapter, **or** auto-detect (ipwho.is + derived id) |
| `extra` | Optional bag; **`extra.exit_geo`** when auto-location; **`extra.baseline_path`** when `--capture-baseline`; **`extra.surface_probe`**, **`extra.transition_tests`** when those phases run |
| `connection_mode` | e.g. `wireguard`, `manual_gui` |
| `exit_ip_v4` / `exit_ip_v6` | Best-effort canonical (full suite; may match preflight IPv4) |
| `exit_ip_sources` | List of `{url, ipv4, ipv6, error}` |
| `dns_servers_observed` | Tier local + external observations |
| `dns_leak_flag` | Boolean + `dns_leak_notes` |
| `webrtc_candidates` | ICE candidates |
| `webrtc_leak_flag` | vs expected exit / LAN |
| `ipv6_status` | Semantic status string |
| `ipv6_leak_flag` | |
| `fingerprint_snapshot` | Anonymous summary |
| `attribution` | ASN, holder, confidence, sources, disclaimers |
| `policies` | vpn + underlay policy records |
| `competitor_surface` | Optional summary: provider DNS, web/CDN probes, **`har_summary`** (merged HAR host/tag hints), portal probes, transit, stray JSON paths (`null` if no `competitor_probe` config). **`provider_dns`** includes `domains` (apex NS/A/AAAA/**TXT/MX/CAA** plus optional **`rr_errors`**) and **`ns_hosts`**: each NS hostname → `a`, `aaaa`, **`ip_attribution`** (map IP → `AttributionResult` JSON for DNS NS glue, same pipeline as exit attribution with `[provider_ns_glue]` notes on `confidence_notes`) |
| `yourinfo_snapshot` | Capture from **yourinfo.ai** (HAR path, headers, title, text excerpt); `null` if `--skip-yourinfo` |
| `browserleaks_snapshot` | Pinned **browserleaks.com** pages from `leak-tests.yaml`; `null` if `--skip-browserleaks` or disabled |
| `services_contacted` | Third-party URLs used in tests (includes preflight + ipwho when auto) |
| `artifacts` | Relative paths into `raw/` |
| `artifacts.competitor_probe_dir` | When present, `raw/<location_id>/competitor_probe/` |
| `artifacts.asn_prefixes_json` | When present, `raw/<location_id>/asn_prefixes.json` |
| `artifacts.exit_dns_json` | When present, `raw/<location_id>/exit_dns.json` |
| `artifacts.browserleaks_probe_dir` | When present, `raw/<location_id>/browserleaks_probe/` |
| `artifacts.yourinfo_probe_dir` | When present, `raw/<location_id>/yourinfo_probe/` |
| `artifacts.baseline_json` | When `--capture-baseline`, relative path to `raw/baseline.json` |
| `artifacts.surface_probe_dir` | When `surface_urls` configured, `raw/<location_id>/surface_probe/` |
| `artifacts.transitions_json` | When `--transition-tests` wrote a file, `raw/<location_id>/transitions.json` |
| `artifacts.website_exposure_dir` | When methodology ran, `raw/<location_id>/website_exposure/` (JSON artifacts) |
| `artifacts.capture_dir` | When **`--attach-capture`** or **`--with-pcap`** finalized, `raw/<location_id>/capture/` (PCAP + `pcap_summary.json`) |
| `framework` | SPEC synthesis: findings, `question_coverage`, `risk_scores`, `observed_endpoints` (omit with `--no-framework`) |
| `website_exposure_methodology` | Desk automation tier: host inventory, resolver sample, Phase 8 DNS audit pointer, Phase 9 third-party inventory — see [website-exposure-methodology.md](website-exposure-methodology.md) |
| `pcap_derived` | Metadata from Python/dpkt summarizer (flows sample, SNI, cleartext DNS, limits); not a substitute for full PCAP |
| `capture_finalize` | Session id, timestamps, errors from attach-capture teardown |

**Duplicate detection (operational):** The CLI compares the **preflight** IPv4 against all prior `normalized.json` files for the same `vpn_provider` before creating a new run. That logic is not stored as a single field; it prevents duplicate **runs** for the same exit IP unless `--force`.

Append-only: add fields with new `schema_version` rather than renaming.

## `vpn-leaks graph-export` (`exposure-graph.json`)

| Key | Notes |
|-----|--------|
| `graph_schema` | **1.1** — adds optional PCAP-derived observation edges (`pcap_ip_flow`, `pcap_neighbor_ip`, `tls_sni_observed`) when **`pcap_derived`** exists on merged runs |

Nodes may include `tls_sni` observations and additional `ip` nodes labeled from PCAP aggregates; tiering mirrors desk vs client-DNS disclaimers elsewhere.
