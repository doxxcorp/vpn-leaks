# Nordvpn (nordvpn)

- **Report generated:** 2026-04-16T00:42:51.283224+00:00
- **Runs included:** nordvpn-20260415T232536Z-488a1217, nordvpn-20260416T003526Z-f5ad2e99
- **Normalized locations:** 2

> **How to read this report**
>
> - The **Matrix**, **Leak summary**, and **Underlay (ASNs)** sections below are a **high-level rollup only**.
> - **Per-location benchmarks** (exit IP, DNS, WebRTC, IPv6, fingerprint, attribution, policies, services, artifacts, YourInfo, competitor probes, and the full JSON record) are in **`## Detailed runs`** — they are **not omitted**; scroll or open this file as plain text if the preview shows only the first screen.
> - The **canonical** machine-readable record for each location is always `runs/<run_id>/locations/<location_id>/normalized.json` (paths are repeated under each run). For very large JSON, use your editor or a JSON viewer rather than Markdown preview alone.

## Matrix

| Field | Value |
|-------|-------|
| Connection modes observed | manual_gui |
| Locations covered | 2 |

## Executive summary (SPEC framework)


- **Rollup severity (max across runs):** `LOW`
- **Question coverage (merged across locations, one row per SPEC ID):** counts below sum to **42** question(s) in the bank (42 total). Status for each ID is the **strictest** across benchmark rows: unanswered > partially answered > answered > not testable dynamically.
  - answered: 7
  - partially answered: 23
  - unanswered: 8
  - not testable dynamically: 4

**Top severity findings (HIGH/CRITICAL)**


- *None flagged in this rollup.*


## SPEC question coverage (full table)

| ID | Status | Category | Question | Summary | Next steps |
|----|--------|----------|----------|---------|------------|
| `IDENTITY-001` | `partially_answered` | identity_correlation | What identifiers are assigned to the user, app install, browser session, and device? | Browser/session signals captured via fingerprint and optional YourInfo probe. | Run with fingerprint + YourInfo probes enabled; compare `fingerprint_snapshot` and `yourinfo_snapshot` in normalized.json. See RUN-STEPS.md (benchmark phases). |
| `IDENTITY-006` | `partially_answered` | identity_correlation | Are there long-lived client identifiers transmitted during auth or app startup? | Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints). | Browser `services_contacted` is partial; for app auth traffic use external capture or vendor docs (D). |
| `IDENTITY-009` | `partially_answered` | identity_correlation | Is the browser fingerprinting surface strong enough to re-identify the same user across sessions? | BrowserLeaks probe data available for re-identification risk assessment. | Enable fingerprint capture; without it re-ID risk stays unassessed. |
| `SIGNUP-001` | `partially_answered` | signup_payment | What third parties are involved during signup? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Set `competitor_probe` + `surface_urls` for signup/checkout in the provider YAML; re-run `vpn-leaks run`. |
| `SIGNUP-004` | `partially_answered` | signup_payment | Are analytics or marketing scripts loaded during signup or checkout? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Same as signup surface — competitor web HAR and `har_summary.json`. |
| `SIGNUP-010` | `partially_answered` | signup_payment | Are these surfaces behind a CDN/WAF? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Enable competitor web probes; check `cdn_headers` / `web_probes` in competitor_surface. |
| `WEB-001` | `unanswered` | website_portal | Where is the marketing site hosted (DNS/routing level)? |  | Configure competitor_probe.provider_domains. — Set `competitor_probe.provider_domains` (and related probes); for desk truth use `dig apex NS` + glue WHOIS (see docs/research-questions-and-evidence.md §H). |
| `WEB-004` | `unanswered` | website_portal | What CDN/WAF is used? |  | No web probes in run. — Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed. |
| `WEB-008` | `partially_answered` | website_portal | Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs? | Review web probe headers, redirects, and HAR for origin leaks. | Enable competitor probes and review HAR / redirects in raw artifacts. |
| `DNS-001` | `answered` | dns | Which DNS resolvers are used while connected? | Resolver tiers observed (local + external). | — |
| `DNS-002` | `partially_answered` | dns | Are DNS requests tunneled (consistent with VPN exit)? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Compare resolver IPs to exit; read `dns_leak_notes` (heuristic). Capture baseline off-VPN if comparing. |
| `DNS-003` | `partially_answered` | dns | Is there DNS fallback to ISP/router/public resolvers? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Same as DNS-002; transition tests help — run with `--transition-tests` when supported. |
| `DNS-004` | `partially_answered` | dns | Does DNS leak during connect/disconnect/reconnect? | Connect/disconnect DNS not sampled; use --transition-tests when supported. | Run `vpn-leaks run` with `--transition-tests` (see RUN-STEPS.md). |
| `DNS-009` | `partially_answered` | dns | Are DoH or DoT endpoints used? | DoH/DoT not isolated from resolver snapshot; inspect raw captures. | Inspect raw DNS captures / resolver lists; DoH/DoT may not be isolated in summary alone. |
| `DNS-011` | `partially_answered` | dns | Are resolvers first-party or third-party? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Attribute resolver IPs (O); compare to exit ASN (I/D). |
| `IP-001` | `answered` | real_ip_leak | Is the real public IPv4 exposed while connected? | Exit IPv4 185.187.168.67; leak flags dns=False webrtc=False ipv6=False. | — |
| `IP-002` | `partially_answered` | real_ip_leak | Is the real public IPv6 exposed while connected? | No IPv6 exit or IPv6 not returned by endpoints. | Enable IPv6 path in environment; check `ipv6/` artifacts when present. |
| `IP-006` | `answered` | real_ip_leak | Is the real IP exposed through WebRTC? | WebRTC candidates captured; leak flag=False. | — |
| `IP-007` | `partially_answered` | real_ip_leak | Is the local LAN IP exposed through WebRTC or browser APIs? | Inspect host candidates vs LAN; see webrtc_notes. | Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`. |
| `IP-014` | `partially_answered` | real_ip_leak | Do leak-check sites disagree about observed IP identity? | Multiple IP echo endpoints; compare exit_ip_sources for disagreement. | Compare `exit_ip_sources` entries for disagreement. |
| `CTRL-002` | `partially_answered` | control_plane | Which domains and IPs are contacted after the tunnel is up? | Post-harness service list captured. | Expand `services_contacted` via full harness; list is harness-visible URLs only. |
| `CTRL-003` | `not_testable_dynamically` | control_plane | Which control-plane endpoints are used for auth/config/session management? | Auth/control-plane inventory requires internal docs or app instrumentation. | DOCUMENT_RESEARCH: vendor docs, app MITM, or support (D). |
| `CTRL-004` | `partially_answered` | control_plane | Which telemetry endpoints are contacted during connection? | Infer from services_contacted and classified endpoints. | Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*). |
| `CTRL-009` | `unanswered` | control_plane | Is the control plane behind a CDN/WAF? |  | No web probes. — Enable portal/web probes (`portal_probes`); check `https_cdn_headers`. |
| `EXIT-001` | `answered` | exit_infrastructure | What exit IP is assigned for each region? | Exit IPv4 185.187.168.67 for location us-california-san-francisco-67. | — |
| `EXIT-002` | `answered` | exit_infrastructure | What ASN announces the exit IP? | ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-003` | `answered` | exit_infrastructure | What organization owns the IP range? | ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-004` | `partially_answered` | exit_infrastructure | What reverse DNS exists for the exit node? | PTR lookup errors: ptr_v4: The resolution lifetime expired after 10.202 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out. | Check raw `exit_dns.json` / attribution for rDNS when stored. |
| `EXIT-005` | `partially_answered` | exit_infrastructure | Does the observed geolocation match the advertised location? | Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States'). | Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate. |
| `THIRDWEB-001` | `unanswered` | third_party_web | What external JS files are loaded on the site? |  | Enable competitor_probe or surface_urls. — Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`. |
| `THIRDWEB-003` | `unanswered` | third_party_web | What analytics providers are present? |  | Enable competitor_probe or surface_urls. — HAR + `har_summary.json` tracker_candidates when competitor probes run. |
| `THIRDWEB-012` | `unanswered` | third_party_web | What cookies are set by first-party and third-party scripts? |  | Enable competitor_probe or surface_urls. — Review HAR for Set-Cookie; summary may be partial. |
| `FP-001` | `unanswered` | browser_tracking | Does the site attempt browser fingerprinting? |  | No fingerprint data. — Enable browserleaks / fingerprint phase; without data FP questions stay open. |
| `FP-011` | `answered` | browser_tracking | Does WebRTC run on provider pages? | WebRTC exercised by harness on leak-test pages. | — |
| `TELEM-001` | `not_testable_dynamically` | telemetry_app | Does the app talk to telemetry vendors? | App telemetry requires traffic capture or binary analysis; not proven by this harness alone. | INTERNAL_UNVERIFIABLE in harness; use binary/network analysis or vendor disclosures (D). |
| `TELEM-004` | `not_testable_dynamically` | telemetry_app | Does the app send connection events to telemetry systems? | App telemetry requires traffic capture or binary analysis; not proven by this harness alone. | Same as TELEM-001. |
| `OS-001` | `partially_answered` | os_specific | On macOS/Windows/Linux, do helper processes bypass the tunnel? | OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run. | Process-level bypass not in default harness; external tooling or manual checks. |
| `FAIL-001` | `partially_answered` | failure_state | What leaks during initial connection? | Not sampled; optional --transition-tests or manual observation. | Use `--transition-tests` for connect-phase leaks when supported. |
| `FAIL-003` | `partially_answered` | failure_state | What leaks during reconnect? | Not sampled; optional --transition-tests or manual observation. | Use `--transition-tests` for reconnect leaks when supported. |
| `FAIL-004` | `not_testable_dynamically` | failure_state | What leaks if the VPN app crashes? | Crash/kill leak tests not run in this harness by default. | Crash/kill scenarios not in default harness; fault injection or manual test. |
| `LOG-001` | `partially_answered` | logging_retention | What is the provider likely able to log based on observed traffic? | Infer logging surface from observable endpoints and services_contacted. | Review `services_contacted` + endpoint classifications; pair with policy/audit (D). |
| `LOG-005` | `unanswered` | logging_retention | Are there contradictions between observed traffic and no-logs marketing claims? |  | No policy fetch or failed fetch. — Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md. |

## How to close gaps

Questions still **unanswered** or only **partially answered** (merged status). Use **Next steps** above; this list is the same IDs in short form.



- **`IDENTITY-001`** (`partially_answered`): Run with fingerprint + YourInfo probes enabled; compare `fingerprint_snapshot` and `yourinfo_snapshot` in normalized.json. See RUN-STEPS.md (benchmark phases).

- **`IDENTITY-006`** (`partially_answered`): Browser `services_contacted` is partial; for app auth traffic use external capture or vendor docs (D).

- **`IDENTITY-009`** (`partially_answered`): Enable fingerprint capture; without it re-ID risk stays unassessed.

- **`SIGNUP-001`** (`partially_answered`): Set `competitor_probe` + `surface_urls` for signup/checkout in the provider YAML; re-run `vpn-leaks run`.

- **`SIGNUP-004`** (`partially_answered`): Same as signup surface — competitor web HAR and `har_summary.json`.

- **`SIGNUP-010`** (`partially_answered`): Enable competitor web probes; check `cdn_headers` / `web_probes` in competitor_surface.

- **`WEB-001`** (`unanswered`): Configure competitor_probe.provider_domains. — Set `competitor_probe.provider_domains` (and related probes); for desk truth use `dig apex NS` + glue WHOIS (see docs/research-questions-and-evidence.md §H).

- **`WEB-004`** (`unanswered`): No web probes in run. — Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed.

- **`WEB-008`** (`partially_answered`): Enable competitor probes and review HAR / redirects in raw artifacts.

- **`DNS-002`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Compare resolver IPs to exit; read `dns_leak_notes` (heuristic). Capture baseline off-VPN if comparing.

- **`DNS-003`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Same as DNS-002; transition tests help — run with `--transition-tests` when supported.

- **`DNS-004`** (`partially_answered`): Run `vpn-leaks run` with `--transition-tests` (see RUN-STEPS.md).

- **`DNS-009`** (`partially_answered`): Inspect raw DNS captures / resolver lists; DoH/DoT may not be isolated in summary alone.

- **`DNS-011`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Attribute resolver IPs (O); compare to exit ASN (I/D).

- **`IP-002`** (`partially_answered`): Enable IPv6 path in environment; check `ipv6/` artifacts when present.

- **`IP-007`** (`partially_answered`): Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`.

- **`IP-014`** (`partially_answered`): Compare `exit_ip_sources` entries for disagreement.

- **`CTRL-002`** (`partially_answered`): Expand `services_contacted` via full harness; list is harness-visible URLs only.

- **`CTRL-004`** (`partially_answered`): Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*).

- **`CTRL-009`** (`unanswered`): No web probes. — Enable portal/web probes (`portal_probes`); check `https_cdn_headers`.

- **`EXIT-004`** (`partially_answered`): Check raw `exit_dns.json` / attribution for rDNS when stored.

- **`EXIT-005`** (`partially_answered`): Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate.

- **`THIRDWEB-001`** (`unanswered`): Enable competitor_probe or surface_urls. — Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`.

- **`THIRDWEB-003`** (`unanswered`): Enable competitor_probe or surface_urls. — HAR + `har_summary.json` tracker_candidates when competitor probes run.

- **`THIRDWEB-012`** (`unanswered`): Enable competitor_probe or surface_urls. — Review HAR for Set-Cookie; summary may be partial.

- **`FP-001`** (`unanswered`): No fingerprint data. — Enable browserleaks / fingerprint phase; without data FP questions stay open.

- **`OS-001`** (`partially_answered`): Process-level bypass not in default harness; external tooling or manual checks.

- **`FAIL-001`** (`partially_answered`): Use `--transition-tests` for connect-phase leaks when supported.

- **`FAIL-003`** (`partially_answered`): Use `--transition-tests` for reconnect leaks when supported.

- **`LOG-001`** (`partially_answered`): Review `services_contacted` + endpoint classifications; pair with policy/audit (D).

- **`LOG-005`** (`unanswered`): No policy fetch or failed fetch. — Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md.



## Analysis of collected evidence

### Scope

- **Benchmark rows in this report:** 2 (one row per `normalized.json` location).
- **Merge rule:** For each SPEC question ID, the status shown in the table is the **strictest** across rows: unanswered > partially_answered > answered > not_testable_dynamically.

### Risk and findings

- **Rollup severity (max across runs):** `LOW`
- **HIGH / CRITICAL framework findings:** none in this rollup.

### By category (merged coverage)

#### browser_tracking

- **FP-001** (unanswered): No fingerprint data.
- **FP-011** (answered): WebRTC exercised by harness on leak-test pages.

#### control_plane

- **CTRL-002** (partial): Post-harness service list captured.
- **CTRL-003** (`not_testable_dynamically`): Auth/control-plane inventory requires internal docs or app instrumentation.
- **CTRL-004** (partial): Infer from services_contacted and classified endpoints.
- **CTRL-009** (unanswered): No web probes.

#### dns

- **DNS-001** (answered): Resolver tiers observed (local + external).
- **DNS-002** (partial): Leak flag=False; see notes.
- **DNS-003** (partial): Leak flag=False; see notes.
- **DNS-004** (partial): Connect/disconnect DNS not sampled; use --transition-tests when supported.
- **DNS-009** (partial): DoH/DoT not isolated from resolver snapshot; inspect raw captures.
- **DNS-011** (partial): Leak flag=False; see notes.

#### exit_infrastructure

- **EXIT-001** (answered): Exit IPv4 185.187.168.67 for location us-california-san-francisco-67.
- **EXIT-002** (answered): ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-003** (answered): ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-004** (partial): PTR lookup errors: ptr_v4: The resolution lifetime expired after 10.202 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.
- **EXIT-005** (partial): Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States').

#### failure_state

- **FAIL-001** (partial): Not sampled; optional --transition-tests or manual observation.
- **FAIL-003** (partial): Not sampled; optional --transition-tests or manual observation.
- **FAIL-004** (`not_testable_dynamically`): Crash/kill leak tests not run in this harness by default.

#### identity_correlation

- **IDENTITY-001** (partial): Browser/session signals captured via fingerprint and optional YourInfo probe.
- **IDENTITY-006** (partial): Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).
- **IDENTITY-009** (partial): BrowserLeaks probe data available for re-identification risk assessment.

#### logging_retention

- **LOG-001** (partial): Infer logging surface from observable endpoints and services_contacted.
- **LOG-005** (unanswered): No policy fetch or failed fetch.

#### os_specific

- **OS-001** (partial): OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.

#### real_ip_leak

- **IP-001** (answered): Exit IPv4 185.187.168.67; leak flags dns=False webrtc=False ipv6=False.
- **IP-002** (partial): No IPv6 exit or IPv6 not returned by endpoints.
- **IP-006** (answered): WebRTC candidates captured; leak flag=False.
- **IP-007** (partial): Inspect host candidates vs LAN; see webrtc_notes.
- **IP-014** (partial): Multiple IP echo endpoints; compare exit_ip_sources for disagreement.

#### signup_payment

- **SIGNUP-001** (partial): No competitor web HAR in this run; configure competitor_probe and surface_urls.
- **SIGNUP-004** (partial): No competitor web HAR in this run; configure competitor_probe and surface_urls.
- **SIGNUP-010** (partial): No competitor web HAR in this run; configure competitor_probe and surface_urls.

#### telemetry_app

- **TELEM-001** (`not_testable_dynamically`): App telemetry requires traffic capture or binary analysis; not proven by this harness alone.
- **TELEM-004** (`not_testable_dynamically`): App telemetry requires traffic capture or binary analysis; not proven by this harness alone.

#### third_party_web

- **THIRDWEB-001** (unanswered): Enable competitor_probe or surface_urls.
- **THIRDWEB-003** (unanswered): Enable competitor_probe or surface_urls.
- **THIRDWEB-012** (unanswered): Enable competitor_probe or surface_urls.

#### website_portal

- **WEB-001** (unanswered): Configure competitor_probe.provider_domains.
- **WEB-004** (unanswered): No web probes in run.
- **WEB-008** (partial): Review web probe headers, redirects, and HAR for origin leaks.

### Limitations

- Leak flags and DNS notes are **heuristic / harness-defined**; read raw `runs/.../raw/` artifacts for full context.
- **Observed leak flags (any location):** DNS=False, WebRTC=False, IPv6=False.
- **App telemetry (TELEM-001, TELEM-004)** and some control-plane details are **not** proven by browser-only harness paths; use **D** (documents) or external traffic studies where applicable.
- **Desk research (S)** (e.g. apex `dig`, glue WHOIS) is not auto-merged into this report; compare to `competitor_probe` / provider DNS when both exist.




## Leak summary

| Location | DNS leak | WebRTC leak | IPv6 leak |
|----------|----------|-------------|-----------|
| Albuquerque, New Mexico, United States | False | False | False |
| San Francisco, California, United States | False | False | False |


## Underlay (ASNs)


- **AS136787:** PACKETHUBSA-AS-AP PacketHub S.A.

- **AS212238:** CDNEXT - Datacamp Limited


---

## Detailed runs

**Included in this report** (each subsection below mirrors one `normalized.json`):


1. `nordvpn-20260415T232536Z-488a1217` / `us-new-mexico-albuquerque-20` — `runs/nordvpn-20260415T232536Z-488a1217/locations/us-new-mexico-albuquerque-20/normalized.json`

2. `nordvpn-20260416T003526Z-f5ad2e99` / `us-california-san-francisco-67` — `runs/nordvpn-20260416T003526Z-f5ad2e99/locations/us-california-san-francisco-67/normalized.json`


Large JSON fields use size caps in this markdown file; when an excerpt hits a cap, a **note** appears at the start of that run’s section listing what was capped. **On-disk `normalized.json` is always complete.**



### nordvpn-20260415T232536Z-488a1217 / us-new-mexico-albuquerque-20



- **vpn_provider:** nordvpn
- **Label:** Albuquerque, New Mexico, United States
- **Path:** `runs/nordvpn-20260415T232536Z-488a1217/locations/us-new-mexico-albuquerque-20/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-15T23:27:00.502329+00:00
- **connection_mode:** manual_gui

#### Runner environment

```json
{
  "os": "Darwin 25.4.0",
  "kernel": "25.4.0",
  "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
  "browser": null,
  "vpn_protocol": "manual_gui",
  "vpn_client": null
}
```

#### Exit IP

| Field | Value |
|-------|-------|
| exit_ip_v4 | 66.179.156.20 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "66.179.156.20",
    "ipv6": null,
    "raw_excerpt": "66.179.156.20",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "66.179.156.20",
    "ipv6": null,
    "raw_excerpt": "66.179.156.20",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "66.179.156.20",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"66.179.156.20\"}",
    "error": null
  }
]
```

#### DNS

| Field | Value |
|-------|-------|
| dns_leak_flag | False |
| dns_leak_notes | Heuristic: no obvious public resolver IPs parsed from external page |

**dns_servers_observed**

```json
[
  {
    "tier": "local",
    "detail": "resolv.conf nameserver lines (Unix)",
    "servers": [
      "100.64.0.2"
    ]
  },
  {
    "tier": "local",
    "detail": "getaddrinfo('whoami.akamai.net')",
    "servers": [
      "66.179.156.21"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "66.179.156.20"
    ]
  }
]
```

#### WebRTC

| Field | Value |
|-------|-------|
| webrtc_leak_flag | False |
| webrtc_notes | Exit IP appears in candidate set (expected for tunneled public) |



| type | protocol | address | port | raw (may be shortened in table) |
|------|----------|---------|------|--------------------------------|
| host | udp | 6efa4629-8271-4005-b72f-c1d94cb5e569.local | 64439 | `candidate:1558097308 1 udp 2113937151 6efa4629-8271-4005-b72f-c1d94cb5e569.local 64439 typ host generation 0 ufrag 07ZN network-cost 999` |
| srflx | udp | 66.179.156.20 | 38073 | `candidate:1230998428 1 udp 1677729535 66.179.156.20 38073 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag 07ZN network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


*No fingerprint snapshot in this run (fingerprint check disabled, skipped, or empty capture).*


#### Attribution

```json
{
  "asn": 136787,
  "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [136787]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 136787,
      "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (66.179.156.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260415232554-f01efe29-6372-46fc-b0ca-2e8cbc70724e",
          "process_time": 101,
          "server_id": "app179",
          "build_version": "v0.9.7-thriftpy2-2026.04.10",
          "pipeline": "1223136",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-15T23:25:54.587521",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 136787,
                "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
              }
            ],
            "related_prefixes": [],
            "resource": "66.179.156.0/24",
            "type": "prefix",
            "block": {
              "resource": "66.0.0.0/8",
              "desc": "ARIN (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-04-15T16:00:00",
            "num_filtered_out": 0
          }
        }
      }
    },
    {
      "name": "team_cymru",
      "asn": null,
      "holder": null,
      "country": null,
      "raw": {
        "error": "dig timed out after 15s",
        "disclaimer": [
          "Team Cymru DNS lookup timed out; cross-check skipped."
        ]
      }
    },
    {
      "name": "peeringdb",
      "asn": null,
      "holder": null,
      "country": null,
      "raw": {
        "error": "Client error '404 Not Found' for url 'https://www.peeringdb.com/api/net?asn=136787'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
      }
    }
  ],
  "disclaimers": [
    "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
    "Team Cymru DNS lookup timed out; cross-check skipped."
  ]
}
```

#### Policies

```json
[]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/66.179.156.20`

- `https://test-ipv6.com/`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260415T232536Z-488a1217/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/webrtc",
  "ipv6_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/fingerprint",
  "attribution_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/policy",
  "competitor_probe_dir": null,
  "browserleaks_probe_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": null,
  "transitions_json": null
}
```

#### YourInfo (yourinfo.ai benchmark)


```json
{
  "url": "https://yourinfo.ai/",
  "final_url": "https://yourinfo.ai/",
  "status": 200,
  "title": "YourInfo.ai",
  "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
  "text_excerpt_truncated": false,
  "har_path": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/yourinfo_probe/yourinfo.har",
  "cdn_headers": {},
  "error": null
}
```

**Visible text excerpt** (length may be capped in this report):

~~~
RESEARCHING YOUR INFORMATION...
20
Querying intelligence databases...

Concerned about your digital privacy?

doxx.net - Secure networking for humans
 
~~~




#### SPEC framework (findings, coverage, risk)


Overall **LOW** · leak **INFO** · third-party **LOW** · correlation **MEDIUM**

```json
{
  "question_bank_version": "1",
  "test_matrix_version": "1",
  "findings": [
    {
      "id": "finding-yourinfo-97b79e7d",
      "category": "third_party_web",
      "title": "Third-party benchmark page loaded (yourinfo.ai)",
      "description": "HAR and page excerpt captured for competitive benchmark; third parties may observe exit IP and browser metadata.",
      "severity": "LOW",
      "confidence": "HIGH",
      "kind": "inferred",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "yourinfo_snapshot",
          "note": null
        }
      ],
      "affected_data_types": [
        "public_ip",
        "user_agent",
        "browser_fingerprint"
      ],
      "recipients": [
        "yourinfo.ai",
        "asset_hosts"
      ],
      "test_conditions": "connected_state_benchmark",
      "reproducibility_notes": null
    }
  ],
  "question_coverage": [
    {
      "question_id": "IDENTITY-001",
      "question_text": "What identifiers are assigned to the user, app install, browser session, and device?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Browser/session signals captured via fingerprint and optional YourInfo probe.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "fingerprint_snapshot",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "yourinfo_snapshot",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IDENTITY-006",
      "question_text": "Are there long-lived client identifiers transmitted during auth or app startup?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IDENTITY-009",
      "question_text": "Is the browser fingerprinting surface strong enough to re-identify the same user across sessions?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Fingerprint snapshot available for re-identification risk assessment.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "fingerprint_snapshot",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "SIGNUP-001",
      "question_text": "What third parties are involved during signup?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
      "evidence_refs": [],
      "notes": ""
    },
    {
      "question_id": "SIGNUP-004",
      "question_text": "Are analytics or marketing scripts loaded during signup or checkout?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
      "evidence_refs": [],
      "notes": ""
    },
    {
      "question_id": "SIGNUP-010",
      "question_text": "Are these surfaces behind a CDN/WAF?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
      "evidence_refs": [],
      "notes": ""
    },
    {
      "question_id": "WEB-001",
      "question_text": "Where is the marketing site hosted (DNS/routing level)?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "Configure competitor_probe.provider_domains."
    },
    {
      "question_id": "WEB-004",
      "question_text": "What CDN/WAF is used?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "No web probes in run."
    },
    {
      "question_id": "WEB-008",
      "question_text": "Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Review web probe headers, redirects, and HAR for origin leaks.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-001",
      "question_text": "Which DNS resolvers are used while connected?",
      "category": "dns",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Resolver tiers observed (local + external).",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-002",
      "question_text": "Are DNS requests tunneled (consistent with VPN exit)?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "DNS-003",
      "question_text": "Is there DNS fallback to ISP/router/public resolvers?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "DNS-004",
      "question_text": "Does DNS leak during connect/disconnect/reconnect?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Connect/disconnect DNS not sampled; use --transition-tests when supported.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "DNS-009",
      "question_text": "Are DoH or DoT endpoints used?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "DoH/DoT not isolated from resolver snapshot; inspect raw captures.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-011",
      "question_text": "Are resolvers first-party or third-party?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "IP-001",
      "question_text": "Is the real public IPv4 exposed while connected?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 66.179.156.20; leak flags dns=False webrtc=False ipv6=False.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_v4",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IP-002",
      "question_text": "Is the real public IPv6 exposed while connected?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "partially_answered",
      "answer_summary": "No IPv6 exit or IPv6 not returned by endpoints.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IP-006",
      "question_text": "Is the real IP exposed through WebRTC?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "WebRTC candidates captured; leak flag=False.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_leak_flag",
          "note": null
        }
      ],
      "notes": "Exit IP appears in candidate set (expected for tunneled public)"
    },
    {
      "question_id": "IP-007",
      "question_text": "Is the local LAN IP exposed through WebRTC or browser APIs?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "partially_answered",
      "answer_summary": "Inspect host candidates vs LAN; see webrtc_notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        }
      ],
      "notes": "Exit IP appears in candidate set (expected for tunneled public)"
    },
    {
      "question_id": "IP-014",
      "question_text": "Do leak-check sites disagree about observed IP identity?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Multiple IP echo endpoints; compare exit_ip_sources for disagreement.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-002",
      "question_text": "Which domains and IPs are contacted after the tunnel is up?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Post-harness service list captured.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-003",
      "question_text": "Which control-plane endpoints are used for auth/config/session management?",
      "category": "control_plane",
      "testability": "DOCUMENT_RESEARCH",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "Auth/control-plane inventory requires internal docs or app instrumentation.",
      "evidence_refs": [],
      "notes": "DOCUMENT_RESEARCH"
    },
    {
      "question_id": "CTRL-004",
      "question_text": "Which telemetry endpoints are contacted during connection?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Infer from services_contacted and classified endpoints.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-009",
      "question_text": "Is the control plane behind a CDN/WAF?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "No web probes."
    },
    {
      "question_id": "EXIT-001",
      "question_text": "What exit IP is assigned for each region?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 66.179.156.20 for location us-new-mexico-albuquerque-20.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_v4",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-002",
      "question_text": "What ASN announces the exit IP?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "attribution",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-003",
      "question_text": "What organization owns the IP range?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "attribution",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-004",
      "question_text": "What reverse DNS exists for the exit node?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "rDNS not always in merge; see raw attribution JSON if present.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "attribution",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-005",
      "question_text": "Does the observed geolocation match the advertised location?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Compare extra.exit_geo to advertised location label.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "extra.exit_geo",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "THIRDWEB-001",
      "question_text": "What external JS files are loaded on the site?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "Enable competitor_probe or surface_urls."
    },
    {
      "question_id": "THIRDWEB-003",
      "question_text": "What analytics providers are present?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "Enable competitor_probe or surface_urls."
    },
    {
      "question_id": "THIRDWEB-012",
      "question_text": "What cookies are set by first-party and third-party scripts?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "Enable competitor_probe or surface_urls."
    },
    {
      "question_id": "FP-001",
      "question_text": "Does the site attempt browser fingerprinting?",
      "category": "browser_tracking",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "No fingerprint data."
    },
    {
      "question_id": "FP-011",
      "question_text": "Does WebRTC run on provider pages?",
      "category": "browser_tracking",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "WebRTC exercised by harness on leak-test pages.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "TELEM-001",
      "question_text": "Does the app talk to telemetry vendors?",
      "category": "telemetry_app",
      "testability": "INTERNAL_UNVERIFIABLE",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
      "evidence_refs": [],
      "notes": "INTERNAL_UNVERIFIABLE"
    },
    {
      "question_id": "TELEM-004",
      "question_text": "Does the app send connection events to telemetry systems?",
      "category": "telemetry_app",
      "testability": "INTERNAL_UNVERIFIABLE",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
      "evidence_refs": [],
      "notes": "INTERNAL_UNVERIFIABLE"
    },
    {
      "question_id": "OS-001",
      "question_text": "On macOS/Windows/Linux, do helper processes bypass the tunnel?",
      "category": "os_specific",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "runner_env",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "FAIL-001",
      "question_text": "What leaks during initial connection?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "FAIL-003",
      "question_text": "What leaks during reconnect?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "FAIL-004",
      "question_text": "What leaks if the VPN app crashes?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "Crash/kill leak tests not run in this harness by default.",
      "evidence_refs": [],
      "notes": "DYNAMIC_PARTIAL"
    },
    {
      "question_id": "LOG-001",
      "question_text": "What is the provider likely able to log based on observed traffic?",
      "category": "logging_retention",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Infer logging surface from observable endpoints and services_contacted.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "LOG-005",
      "question_text": "Are there contradictions between observed traffic and no-logs marketing claims?",
      "category": "logging_retention",
      "testability": "DOCUMENT_RESEARCH",
      "answer_status": "unanswered",
      "answer_summary": "",
      "evidence_refs": [],
      "notes": "No policy fetch or failed fetch."
    }
  ],
  "risk_scores": {
    "overall_severity": "LOW",
    "leak_severity": "INFO",
    "correlation_risk": "MEDIUM",
    "third_party_exposure": "LOW",
    "notes": []
  },
  "observed_endpoints": [
    {
      "host": "api.ipify.org",
      "classification": "third_party_analytics",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "api64.ipify.org",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "browserleaks.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "ipleak.net",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "ipwho.is",
      "classification": "unknown",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "test-ipv6.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "webrtc",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "yourinfo.ai",
      "classification": "unknown",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    }
  ]
}
```


#### Competitor surface (provider YAML probes)


*`competitor_surface` is null; no competitor data for this run.*


#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "66.179.156.20",
    "country_code": "US",
    "region": "New Mexico",
    "city": "Albuquerque",
    "connection": {
      "asn": 136787,
      "org": "Core Ip Solutions LLC",
      "isp": "Packethub S.A.",
      "domain": "packethub.net"
    },
    "location_id": "us-new-mexico-albuquerque-20",
    "location_label": "Albuquerque, New Mexico, United States"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260415T232536Z-488a1217",
  "timestamp_utc": "2026-04-15T23:27:00.502329+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-new-mexico-albuquerque-20",
  "vpn_location_label": "Albuquerque, New Mexico, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "66.179.156.20",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "66.179.156.20",
      "ipv6": null,
      "raw_excerpt": "66.179.156.20",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "66.179.156.20",
      "ipv6": null,
      "raw_excerpt": "66.179.156.20",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "66.179.156.20",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"66.179.156.20\"}",
      "error": null
    }
  ],
  "dns_servers_observed": [
    {
      "tier": "local",
      "detail": "resolv.conf nameserver lines (Unix)",
      "servers": [
        "100.64.0.2"
      ]
    },
    {
      "tier": "local",
      "detail": "getaddrinfo('whoami.akamai.net')",
      "servers": [
        "66.179.156.21"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "66.179.156.20"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "6efa4629-8271-4005-b72f-c1d94cb5e569.local",
      "port": 64439,
      "raw": "candidate:1558097308 1 udp 2113937151 6efa4629-8271-4005-b72f-c1d94cb5e569.local 64439 typ host generation 0 ufrag 07ZN network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "66.179.156.20",
      "port": 38073,
      "raw": "candidate:1230998428 1 udp 1677729535 66.179.156.20 38073 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag 07ZN network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {},
  "attribution": {
    "asn": 136787,
    "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [136787]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 136787,
        "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (66.179.156.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260415232554-f01efe29-6372-46fc-b0ca-2e8cbc70724e",
            "process_time": 101,
            "server_id": "app179",
            "build_version": "v0.9.7-thriftpy2-2026.04.10",
            "pipeline": "1223136",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-15T23:25:54.587521",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 136787,
                  "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
                }
              ],
              "related_prefixes": [],
              "resource": "66.179.156.0/24",
              "type": "prefix",
              "block": {
                "resource": "66.0.0.0/8",
                "desc": "ARIN (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-04-15T16:00:00",
              "num_filtered_out": 0
            }
          }
        }
      },
      {
        "name": "team_cymru",
        "asn": null,
        "holder": null,
        "country": null,
        "raw": {
          "error": "dig timed out after 15s",
          "disclaimer": [
            "Team Cymru DNS lookup timed out; cross-check skipped."
          ]
        }
      },
      {
        "name": "peeringdb",
        "asn": null,
        "holder": null,
        "country": null,
        "raw": {
          "error": "Client error '404 Not Found' for url 'https://www.peeringdb.com/api/net?asn=136787'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
        }
      }
    ],
    "disclaimers": [
      "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
      "Team Cymru DNS lookup timed out; cross-check skipped."
    ]
  },
  "policies": [],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/66.179.156.20",
    "https://test-ipv6.com/",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260415T232536Z-488a1217/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/webrtc",
    "ipv6_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/fingerprint",
    "attribution_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/policy",
    "competitor_probe_dir": null,
    "browserleaks_probe_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": null,
    "transitions_json": null
  },
  "competitor_surface": null,
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/yourinfo_probe/yourinfo.har",
    "cdn_headers": {},
    "error": null
  },
  "browserleaks_snapshot": {
    "pages": [
      {
        "url": "https://browserleaks.com/ip",
        "final_url": "https://browserleaks.com/ip",
        "status": 200,
        "title": "My IP Address - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t66.179.156.20\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tNew Mexico\nCity\tAlbuquerque\nISP\tPacketHub S.A.\nOrganization\tCore IP Solutions LLC\nNetwork\tAS136787 PacketHub S.A. (VPN, VPSH, ANYCAST)\nUsage Type\tCorporate / Business\nTimezone\tAmerica/Denver (MDT)\nLocal Time\tWed, 15 Apr 2026 17:26:27 -0600\nCoordinates\t35.0844,-106.6500\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t66.179.156.20\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t12 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t2cfd29165ede506a4d04aa0bbf91bf63\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t66.179.156.0 - 66.179.156.255\nCIDR\t66.179.156.0/24\nName\tUS-COREIP4-20011009\nHandle\t66.179.156.0 - 66.179.156.255\nParent Handle\t0.0.0.0 - 255.255.255.255\nNet Type\tALLOCATED PA\nCountry\tUnited States\nRegistration\tWed, 07 Jan 2026 15:25:27 GMT\nLast Changed\tMon, 19 Jan 2026 14:00:35 GMT\nDescription\tPacketHub United States\nFull Name\tNetwork Operations\nHandle\tNO1983-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tPANAMA\nPanama City\n0801\nOffice 76, Plaza 2000, 50th Street and Marbella, Bella Vista\nFull Name\tCore IP Solutions LLC\nHandle\tORG-CISL14-RIPE\nEntity Roles\tRegistrant\nTelephone\t+40733131313\nAddress\t16192 Coastal Highway\n19958\nLewes, Delaware\nUNITED STATES\nFull Name\tRIPE-NCC-HM-MNT\nHandle\tRIPE-NCC-HM-MNT\nEntity Roles\tRegistrant\nOrganization\tORG-NCC1-RIPE\nFull Name\tUs-coreip-1-mnt\nHandle\tUs-coreip-1-mnt\nEntity Roles\tRegistrant\nFull Name\tAbuse-C Role\nHandle\tAR67868-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tPANAMA\nPanama City\n0801\nOffice 76, Plaza 2000, 50th Street and Marbella, Bella Vista\nFull Name\tLir-pa-packethub-1-MNT\nHandle\tLir-pa-packethub-1-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
        "text_excerpt_truncated": false,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/dns",
        "final_url": "https://browserleaks.com/dns",
        "status": 200,
        "title": "DNS Leak Test - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t66.179.156.20\nISP\tPacketHub S.A.\nLocation\tUnited States, Albuquerque\nDNS Leak Test\nTest Results\tFound 10 Servers, 2 ISP, 2 Locations\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n66.179.156.13\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.14\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.15\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.16\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.17\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.18\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.19\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.20\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.21\tPacketHub S.A.\tUnited States, Albuquerque\n173.219.119.98\tSuddenlink Communications\tUnited States, Fortuna\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
        "text_excerpt_truncated": false,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/webrtc",
        "final_url": "https://browserleaks.com/webrtc",
        "status": 200,
        "title": "WebRTC Leak Test - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t66.179.156.20\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t66.179.156.20\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (217)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
        "text_excerpt_truncated": false,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/tls",
        "final_url": "https://browserleaks.com/tls",
        "status": 200,
        "title": "TLS Client Test - TLS Fingerprinting - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_50d132a891d9\nJA3\t8007c26a16ca4700908f5714807f4e7a\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x1A1A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0xFAFA\nGREASE\n\n\n0x000B\nec_point_formats\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x0033\nkey_share\n\n\n0x0017\nextended_main_secret\n\n\n0x000D\nsignature_algorithms\n\n\n0x002B\nsupported_versions\n\n\n0x0023\nsession_ticket\n\n\n0x0005\nstatus_request\n\n\n0x000A\nsupported_groups\n\n\n0xFF01\nrenegotiation_info\n\n\n0x001B\ncompress_certificate\n\n\n0x0000\nserver_name\n\n\n0x44CD\napplication_settings\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x1A1A\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t185\nenc_length\t32\npayload_length\t144\nkey_share\nclient_shares\t\n0x1A1A\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brow",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260415T232536Z-488a1217/raw/us-new-mexico-albuquerque-20/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-97b79e7d",
        "category": "third_party_web",
        "title": "Third-party benchmark page loaded (yourinfo.ai)",
        "description": "HAR and page excerpt captured for competitive benchmark; third parties may observe exit IP and browser metadata.",
        "severity": "LOW",
        "confidence": "HIGH",
        "kind": "inferred",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "yourinfo_snapshot",
            "note": null
          }
        ],
        "affected_data_types": [
          "public_ip",
          "user_agent",
          "browser_fingerprint"
        ],
        "recipients": [
          "yourinfo.ai",
          "asset_hosts"
        ],
        "test_conditions": "connected_state_benchmark",
        "reproducibility_notes": null
      }
    ],
    "question_coverage": [
      {
        "question_id": "IDENTITY-001",
        "question_text": "What identifiers are assigned to the user, app install, browser session, and device?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Browser/session signals captured via fingerprint and optional YourInfo probe.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "fingerprint_snapshot",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "yourinfo_snapshot",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IDENTITY-006",
        "question_text": "Are there long-lived client identifiers transmitted during auth or app startup?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IDENTITY-009",
        "question_text": "Is the browser fingerprinting surface strong enough to re-identify the same user across sessions?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Fingerprint snapshot available for re-identification risk assessment.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "fingerprint_snapshot",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "SIGNUP-001",
        "question_text": "What third parties are involved during signup?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
        "evidence_refs": [],
        "notes": ""
      },
      {
        "question_id": "SIGNUP-004",
        "question_text": "Are analytics or marketing scripts loaded during signup or checkout?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
        "evidence_refs": [],
        "notes": ""
      },
      {
        "question_id": "SIGNUP-010",
        "question_text": "Are these surfaces behind a CDN/WAF?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "No competitor web HAR in this run; configure competitor_probe and surface_urls.",
        "evidence_refs": [],
        "notes": ""
      },
      {
        "question_id": "WEB-001",
        "question_text": "Where is the marketing site hosted (DNS/routing level)?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "Configure competitor_probe.provider_domains."
      },
      {
        "question_id": "WEB-004",
        "question_text": "What CDN/WAF is used?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "No web probes in run."
      },
      {
        "question_id": "WEB-008",
        "question_text": "Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Review web probe headers, redirects, and HAR for origin leaks.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-001",
        "question_text": "Which DNS resolvers are used while connected?",
        "category": "dns",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Resolver tiers observed (local + external).",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-002",
        "question_text": "Are DNS requests tunneled (consistent with VPN exit)?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "DNS-003",
        "question_text": "Is there DNS fallback to ISP/router/public resolvers?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "DNS-004",
        "question_text": "Does DNS leak during connect/disconnect/reconnect?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Connect/disconnect DNS not sampled; use --transition-tests when supported.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "DNS-009",
        "question_text": "Are DoH or DoT endpoints used?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "DoH/DoT not isolated from resolver snapshot; inspect raw captures.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-011",
        "question_text": "Are resolvers first-party or third-party?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "IP-001",
        "question_text": "Is the real public IPv4 exposed while connected?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 66.179.156.20; leak flags dns=False webrtc=False ipv6=False.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_v4",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IP-002",
        "question_text": "Is the real public IPv6 exposed while connected?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "partially_answered",
        "answer_summary": "No IPv6 exit or IPv6 not returned by endpoints.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IP-006",
        "question_text": "Is the real IP exposed through WebRTC?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "WebRTC candidates captured; leak flag=False.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_leak_flag",
            "note": null
          }
        ],
        "notes": "Exit IP appears in candidate set (expected for tunneled public)"
      },
      {
        "question_id": "IP-007",
        "question_text": "Is the local LAN IP exposed through WebRTC or browser APIs?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "partially_answered",
        "answer_summary": "Inspect host candidates vs LAN; see webrtc_notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          }
        ],
        "notes": "Exit IP appears in candidate set (expected for tunneled public)"
      },
      {
        "question_id": "IP-014",
        "question_text": "Do leak-check sites disagree about observed IP identity?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Multiple IP echo endpoints; compare exit_ip_sources for disagreement.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-002",
        "question_text": "Which domains and IPs are contacted after the tunnel is up?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Post-harness service list captured.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-003",
        "question_text": "Which control-plane endpoints are used for auth/config/session management?",
        "category": "control_plane",
        "testability": "DOCUMENT_RESEARCH",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "Auth/control-plane inventory requires internal docs or app instrumentation.",
        "evidence_refs": [],
        "notes": "DOCUMENT_RESEARCH"
      },
      {
        "question_id": "CTRL-004",
        "question_text": "Which telemetry endpoints are contacted during connection?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Infer from services_contacted and classified endpoints.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-009",
        "question_text": "Is the control plane behind a CDN/WAF?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "No web probes."
      },
      {
        "question_id": "EXIT-001",
        "question_text": "What exit IP is assigned for each region?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 66.179.156.20 for location us-new-mexico-albuquerque-20.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_v4",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-002",
        "question_text": "What ASN announces the exit IP?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "attribution",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-003",
        "question_text": "What organization owns the IP range?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "attribution",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-004",
        "question_text": "What reverse DNS exists for the exit node?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "rDNS not always in merge; see raw attribution JSON if present.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "attribution",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-005",
        "question_text": "Does the observed geolocation match the advertised location?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Compare extra.exit_geo to advertised location label.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "extra.exit_geo",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "THIRDWEB-001",
        "question_text": "What external JS files are loaded on the site?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "Enable competitor_probe or surface_urls."
      },
      {
        "question_id": "THIRDWEB-003",
        "question_text": "What analytics providers are present?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "Enable competitor_probe or surface_urls."
      },
      {
        "question_id": "THIRDWEB-012",
        "question_text": "What cookies are set by first-party and third-party scripts?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "Enable competitor_probe or surface_urls."
      },
      {
        "question_id": "FP-001",
        "question_text": "Does the site attempt browser fingerprinting?",
        "category": "browser_tracking",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "No fingerprint data."
      },
      {
        "question_id": "FP-011",
        "question_text": "Does WebRTC run on provider pages?",
        "category": "browser_tracking",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "WebRTC exercised by harness on leak-test pages.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "TELEM-001",
        "question_text": "Does the app talk to telemetry vendors?",
        "category": "telemetry_app",
        "testability": "INTERNAL_UNVERIFIABLE",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
        "evidence_refs": [],
        "notes": "INTERNAL_UNVERIFIABLE"
      },
      {
        "question_id": "TELEM-004",
        "question_text": "Does the app send connection events to telemetry systems?",
        "category": "telemetry_app",
        "testability": "INTERNAL_UNVERIFIABLE",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
        "evidence_refs": [],
        "notes": "INTERNAL_UNVERIFIABLE"
      },
      {
        "question_id": "OS-001",
        "question_text": "On macOS/Windows/Linux, do helper processes bypass the tunnel?",
        "category": "os_specific",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "runner_env",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "FAIL-001",
        "question_text": "What leaks during initial connection?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "FAIL-003",
        "question_text": "What leaks during reconnect?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "FAIL-004",
        "question_text": "What leaks if the VPN app crashes?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "Crash/kill leak tests not run in this harness by default.",
        "evidence_refs": [],
        "notes": "DYNAMIC_PARTIAL"
      },
      {
        "question_id": "LOG-001",
        "question_text": "What is the provider likely able to log based on observed traffic?",
        "category": "logging_retention",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Infer logging surface from observable endpoints and services_contacted.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "LOG-005",
        "question_text": "Are there contradictions between observed traffic and no-logs marketing claims?",
        "category": "logging_retention",
        "testability": "DOCUMENT_RESEARCH",
        "answer_status": "unanswered",
        "answer_summary": "",
        "evidence_refs": [],
        "notes": "No policy fetch or failed fetch."
      }
    ],
    "risk_scores": {
      "overall_severity": "LOW",
      "leak_severity": "INFO",
      "correlation_risk": "MEDIUM",
      "third_party_exposure": "LOW",
      "notes": []
    },
    "observed_endpoints": [
      {
        "host": "api.ipify.org",
        "classification": "third_party_analytics",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "api64.ipify.org",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "browserleaks.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "ipleak.net",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "ipwho.is",
        "classification": "unknown",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "test-ipv6.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "webrtc",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "yourinfo.ai",
        "classification": "unknown",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      }
    ]
  },
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "66.179.156.20",
      "country_code": "US",
      "region": "New Mexico",
      "city": "Albuquerque",
      "connection": {
        "asn": 136787,
        "org": "Core Ip Solutions LLC",
        "isp": "Packethub S.A.",
        "domain": "packethub.net"
      },
      "location_id": "us-new-mexico-albuquerque-20",
      "location_label": "Albuquerque, New Mexico, United States"
    }
  }
}
```

---



### nordvpn-20260416T003526Z-f5ad2e99 / us-california-san-francisco-67



- **vpn_provider:** nordvpn
- **Label:** San Francisco, California, United States
- **Path:** `runs/nordvpn-20260416T003526Z-f5ad2e99/locations/us-california-san-francisco-67/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-16T00:40:23.612374+00:00
- **connection_mode:** manual_gui

#### Runner environment

```json
{
  "os": "Darwin 25.4.0",
  "kernel": "25.4.0",
  "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
  "browser": null,
  "vpn_protocol": "manual_gui",
  "vpn_client": null
}
```

#### Exit IP

| Field | Value |
|-------|-------|
| exit_ip_v4 | 185.187.168.67 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.187.168.67",
    "ipv6": null,
    "raw_excerpt": "185.187.168.67",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "185.187.168.67",
    "ipv6": null,
    "raw_excerpt": "185.187.168.67",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.187.168.67",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.187.168.67\"}",
    "error": null
  }
]
```

#### DNS

| Field | Value |
|-------|-------|
| dns_leak_flag | False |
| dns_leak_notes | Heuristic: no obvious public resolver IPs parsed from external page |

**dns_servers_observed**

```json
[
  {
    "tier": "local",
    "detail": "resolv.conf nameserver lines (Unix)",
    "servers": [
      "100.64.0.2"
    ]
  },
  {
    "tier": "local",
    "detail": "getaddrinfo('whoami.akamai.net')",
    "servers": [
      "185.187.168.73"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.187.168.67"
    ]
  }
]
```

#### WebRTC

| Field | Value |
|-------|-------|
| webrtc_leak_flag | False |
| webrtc_notes | Exit IP appears in candidate set (expected for tunneled public) |



| type | protocol | address | port | raw (may be shortened in table) |
|------|----------|---------|------|--------------------------------|
| host | udp | 75152e19-12ff-477e-b68c-bb9128ff3691.local | 50289 | `candidate:3787496119 1 udp 2113937151 75152e19-12ff-477e-b68c-bb9128ff3691.local 50289 typ host generation 0 ufrag tMgR network-cost 999` |
| srflx | udp | 185.187.168.67 | 37309 | `candidate:3788839825 1 udp 1677729535 185.187.168.67 37309 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag tMgR network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


*No fingerprint snapshot in this run (fingerprint check disabled, skipped, or empty capture).*


#### Attribution

```json
{
  "asn": 212238,
  "holder": "CDNEXT - Datacamp Limited",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [212238]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 212238,
      "holder": "CDNEXT - Datacamp Limited",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (185.187.168.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260416003544-5e878819-fefe-48a0-8246-97ce15cbab46",
          "process_time": 52,
          "server_id": "app190",
          "build_version": "v0.9.7-2026.04.09",
          "pipeline": "1221926",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-16T00:35:45.035042",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 212238,
                "holder": "CDNEXT - Datacamp Limited"
              }
            ],
            "related_prefixes": [],
            "resource": "185.187.168.0/24",
            "type": "prefix",
            "block": {
              "resource": "185.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-04-15T16:00:00",
            "num_filtered_out": 0
          }
        }
      }
    },
    {
      "name": "team_cymru",
      "asn": null,
      "holder": null,
      "country": null,
      "raw": {
        "error": "dig timed out after 15s",
        "disclaimer": [
          "Team Cymru DNS lookup timed out; cross-check skipped."
        ]
      }
    },
    {
      "name": "peeringdb",
      "asn": null,
      "holder": null,
      "country": null,
      "raw": {
        "error": "Client error '404 Not Found' for url 'https://www.peeringdb.com/api/net?asn=212238'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
      }
    }
  ],
  "disclaimers": [
    "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
    "Team Cymru DNS lookup timed out; cross-check skipped."
  ]
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-16T00:36:50.435697+00:00",
    "sha256": "43ba36d39f4206a35c19946530ec5e355f3ce5dc2721a3f7c91fb8847a237e20",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  }
]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `competitor_probe:enabled`

- `competitor_probe:har_summary`

- `dns:lookup:nordvpn.com`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/185.187.168.67`

- `https://my.nordaccount.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/webrtc",
  "ipv6_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/fingerprint",
  "attribution_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/policy",
  "competitor_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": null,
  "transitions_json": null
}
```

#### YourInfo (yourinfo.ai benchmark)


```json
{
  "url": "https://yourinfo.ai/",
  "final_url": "https://yourinfo.ai/",
  "status": 200,
  "title": "YourInfo.ai",
  "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
  "text_excerpt_truncated": false,
  "har_path": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/yourinfo_probe/yourinfo.har",
  "cdn_headers": {},
  "error": null
}
```

**Visible text excerpt** (length may be capped in this report):

~~~
RESEARCHING YOUR INFORMATION...
20
Querying intelligence databases...

Concerned about your digital privacy?

doxx.net - Secure networking for humans
 
~~~




#### SPEC framework (findings, coverage, risk)


Overall **LOW** · leak **INFO** · third-party **MEDIUM** · correlation **MEDIUM**

```json
{
  "question_bank_version": "1",
  "test_matrix_version": "1",
  "findings": [
    {
      "id": "finding-yourinfo-ba1b751f",
      "category": "third_party_web",
      "title": "Third-party benchmark page loaded (yourinfo.ai)",
      "description": "HAR and page excerpt captured for competitive benchmark; third parties may observe exit IP and browser metadata.",
      "severity": "LOW",
      "confidence": "HIGH",
      "kind": "inferred",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "yourinfo_snapshot",
          "note": null
        }
      ],
      "affected_data_types": [
        "public_ip",
        "user_agent",
        "browser_fingerprint"
      ],
      "recipients": [
        "yourinfo.ai",
        "asset_hosts"
      ],
      "test_conditions": "connected_state_benchmark",
      "reproducibility_notes": null
    }
  ],
  "question_coverage": [
    {
      "question_id": "IDENTITY-001",
      "question_text": "What identifiers are assigned to the user, app install, browser session, and device?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Browser/session signals captured via fingerprint and optional YourInfo probe.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "fingerprint_snapshot",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "yourinfo_snapshot",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "browserleaks_snapshot",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IDENTITY-006",
      "question_text": "Are there long-lived client identifiers transmitted during auth or app startup?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IDENTITY-009",
      "question_text": "Is the browser fingerprinting surface strong enough to re-identify the same user across sessions?",
      "category": "identity_correlation",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "BrowserLeaks probe data available for re-identification risk assessment.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "fingerprint_snapshot",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "browserleaks_snapshot",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "SIGNUP-001",
      "question_text": "What third parties are involved during signup?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "SIGNUP-004",
      "question_text": "Are analytics or marketing scripts loaded during signup or checkout?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "SIGNUP-010",
      "question_text": "Are these surfaces behind a CDN/WAF?",
      "category": "signup_payment",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "WEB-001",
      "question_text": "Where is the marketing site hosted (DNS/routing level)?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Apex DNS/NS data recorded for configured provider domains.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface.provider_dns",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "WEB-004",
      "question_text": "What CDN/WAF is used?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Response headers / CDN signatures captured in web probes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface.web_probes",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "WEB-008",
      "question_text": "Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs?",
      "category": "website_portal",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Review web probe headers, redirects, and HAR for origin leaks.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-001",
      "question_text": "Which DNS resolvers are used while connected?",
      "category": "dns",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Resolver tiers observed (local + external).",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-002",
      "question_text": "Are DNS requests tunneled (consistent with VPN exit)?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "DNS-003",
      "question_text": "Is there DNS fallback to ISP/router/public resolvers?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "DNS-004",
      "question_text": "Does DNS leak during connect/disconnect/reconnect?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Connect/disconnect DNS not sampled; use --transition-tests when supported.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "DNS-009",
      "question_text": "Are DoH or DoT endpoints used?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "DoH/DoT not isolated from resolver snapshot; inspect raw captures.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "DNS-011",
      "question_text": "Are resolvers first-party or third-party?",
      "category": "dns",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Leak flag=False; see notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "dns_servers_observed",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "dns_leak_notes",
          "note": null
        }
      ],
      "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
    },
    {
      "question_id": "IP-001",
      "question_text": "Is the real public IPv4 exposed while connected?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 185.187.168.67; leak flags dns=False webrtc=False ipv6=False.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_v4",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IP-002",
      "question_text": "Is the real public IPv6 exposed while connected?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "partially_answered",
      "answer_summary": "No IPv6 exit or IPv6 not returned by endpoints.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "IP-006",
      "question_text": "Is the real IP exposed through WebRTC?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "WebRTC candidates captured; leak flag=False.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_leak_flag",
          "note": null
        }
      ],
      "notes": "Exit IP appears in candidate set (expected for tunneled public)"
    },
    {
      "question_id": "IP-007",
      "question_text": "Is the local LAN IP exposed through WebRTC or browser APIs?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_FULL",
      "answer_status": "partially_answered",
      "answer_summary": "Inspect host candidates vs LAN; see webrtc_notes.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        }
      ],
      "notes": "Exit IP appears in candidate set (expected for tunneled public)"
    },
    {
      "question_id": "IP-014",
      "question_text": "Do leak-check sites disagree about observed IP identity?",
      "category": "real_ip_leak",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "All 3 echo endpoints agree on IPv4 185.187.168.67.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_sources",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-002",
      "question_text": "Which domains and IPs are contacted after the tunnel is up?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Post-harness service list captured.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-003",
      "question_text": "Which control-plane endpoints are used for auth/config/session management?",
      "category": "control_plane",
      "testability": "DOCUMENT_RESEARCH",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "Auth/control-plane inventory requires internal docs or app instrumentation.",
      "evidence_refs": [],
      "notes": "DOCUMENT_RESEARCH"
    },
    {
      "question_id": "CTRL-004",
      "question_text": "Which telemetry endpoints are contacted during connection?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Infer from services_contacted and classified endpoints.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "CTRL-009",
      "question_text": "Is the control plane behind a CDN/WAF?",
      "category": "control_plane",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "CDN/WAF hints from web headers.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface.web_probes",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-001",
      "question_text": "What exit IP is assigned for each region?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 185.187.168.67 for location us-california-san-francisco-67.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "exit_ip_v4",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-002",
      "question_text": "What ASN announces the exit IP?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "ASN 212238 — CDNEXT - Datacamp Limited",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "attribution",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-003",
      "question_text": "What organization owns the IP range?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "ASN 212238 — CDNEXT - Datacamp Limited",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "attribution",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-004",
      "question_text": "What reverse DNS exists for the exit node?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "PTR lookup errors: ptr_v4: The resolution lifetime expired after 10.202 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "artifacts.exit_dns_json",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "EXIT-005",
      "question_text": "Does the observed geolocation match the advertised location?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States').",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "extra.exit_geo",
          "note": null
        },
        {
          "artifact_path": null,
          "normalized_pointer": "vpn_location_label",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "THIRDWEB-001",
      "question_text": "What external JS files are loaded on the site?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "THIRDWEB-003",
      "question_text": "What analytics providers are present?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "THIRDWEB-012",
      "question_text": "What cookies are set by first-party and third-party scripts?",
      "category": "third_party_web",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "competitor_surface",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "FP-001",
      "question_text": "Does the site attempt browser fingerprinting?",
      "category": "browser_tracking",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "BrowserLeaks probe pages captured (canvas/WebGL/tls signals in raw excerpts).",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "browserleaks_snapshot",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "FP-011",
      "question_text": "Does WebRTC run on provider pages?",
      "category": "browser_tracking",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "WebRTC exercised by harness on leak-test pages.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "webrtc_candidates",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "TELEM-001",
      "question_text": "Does the app talk to telemetry vendors?",
      "category": "telemetry_app",
      "testability": "INTERNAL_UNVERIFIABLE",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
      "evidence_refs": [],
      "notes": "INTERNAL_UNVERIFIABLE"
    },
    {
      "question_id": "TELEM-004",
      "question_text": "Does the app send connection events to telemetry systems?",
      "category": "telemetry_app",
      "testability": "INTERNAL_UNVERIFIABLE",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
      "evidence_refs": [],
      "notes": "INTERNAL_UNVERIFIABLE"
    },
    {
      "question_id": "OS-001",
      "question_text": "On macOS/Windows/Linux, do helper processes bypass the tunnel?",
      "category": "os_specific",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "runner_env",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "FAIL-001",
      "question_text": "What leaks during initial connection?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "FAIL-003",
      "question_text": "What leaks during reconnect?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
      "evidence_refs": [],
      "notes": null
    },
    {
      "question_id": "FAIL-004",
      "question_text": "What leaks if the VPN app crashes?",
      "category": "failure_state",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "not_testable_dynamically",
      "answer_summary": "Crash/kill leak tests not run in this harness by default.",
      "evidence_refs": [],
      "notes": "DYNAMIC_PARTIAL"
    },
    {
      "question_id": "LOG-001",
      "question_text": "What is the provider likely able to log based on observed traffic?",
      "category": "logging_retention",
      "testability": "DYNAMIC_PARTIAL",
      "answer_status": "partially_answered",
      "answer_summary": "Infer logging surface from observable endpoints and services_contacted.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ],
      "notes": null
    },
    {
      "question_id": "LOG-005",
      "question_text": "Are there contradictions between observed traffic and no-logs marketing claims?",
      "category": "logging_retention",
      "testability": "DOCUMENT_RESEARCH",
      "answer_status": "partially_answered",
      "answer_summary": "Policy text captured; compare claims to observed traffic manually.",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "policies",
          "note": null
        }
      ],
      "notes": null
    }
  ],
  "risk_scores": {
    "overall_severity": "LOW",
    "leak_severity": "INFO",
    "correlation_risk": "MEDIUM",
    "third_party_exposure": "MEDIUM",
    "notes": [
      "Competitor web/portal probes executed."
    ]
  },
  "observed_endpoints": [
    {
      "host": "api.ipify.org",
      "classification": "third_party_analytics",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "api64.ipify.org",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "browserleaks.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "competitor_probe",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "dns",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "ipleak.net",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "ipwho.is",
      "classification": "unknown",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "my.nordaccount.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "nordvpn.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "policy",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "test-ipv6.com",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "transit",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "webrtc",
      "classification": "unknown",
      "confidence": 0.4,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    },
    {
      "host": "yourinfo.ai",
      "classification": "unknown",
      "confidence": 0.95,
      "source": "services_contacted",
      "evidence_refs": [
        {
          "artifact_path": null,
          "normalized_pointer": "services_contacted",
          "note": null
        }
      ]
    }
  ]
}
```


#### Competitor surface (provider YAML probes)


```json
{
  "provider_dns": {
    "domains": {
      "nordvpn.com": {
        "ns": [],
        "a": [],
        "aaaa": [],
        "error": "NS: The resolution lifetime expired after 10.206 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
        "txt": [],
        "mx": [],
        "caa": [],
        "rr_errors": {
          "txt": "The resolution lifetime expired after 10.206 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
          "mx": "The resolution lifetime expired after 10.205 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
          "caa": "The resolution lifetime expired after 10.207 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out."
        }
      }
    },
    "ns_hosts": {}
  },
  "web_probes": [
    {
      "url": "https://nordvpn.com/",
      "error": null,
      "status": 403,
      "final_url": "https://nordvpn.com/",
      "cdn_headers": {
        "server": "cloudflare",
        "cf-ray": "9ecf22e9dbe738ce-SJC"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ecf22e9dbe738ce"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe/har/d945f098fbd5bb50.har",
        "entry_count": 3,
        "unique_hosts": [
          "nordvpn.com"
        ],
        "unique_schemes": [
          "https"
        ],
        "tracker_candidates": [],
        "cdn_candidates": [],
        "error": null
      }
    ],
    "merged_unique_hosts": [
      "nordvpn.com"
    ],
    "merged_tracker_candidates": [],
    "merged_cdn_candidates": []
  },
  "portal_probes": [
    {
      "host": "my.nordaccount.com",
      "a": [],
      "aaaa": [],
      "https_status": 200,
      "https_cdn_headers": {
        "server": "cloudflare",
        "cf-ray": "9ecf236aab7b679b-SJC"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "185.187.168.67",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "185.187.168.67"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 185.187.168.67 (185.187.168.67), 15 hops max, 40 byte packets\n",
    "hops": [],
    "returncode": 0
  },
  "stray_json": [],
  "errors": []
}
```



#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "185.187.168.67",
    "country_code": "US",
    "region": "California",
    "city": "San Francisco",
    "connection": {
      "asn": 212238,
      "org": "Packethub S.A.",
      "isp": "Datacamp Limited",
      "domain": "packethub.net"
    },
    "location_id": "us-california-san-francisco-67",
    "location_label": "San Francisco, California, United States"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260416T003526Z-f5ad2e99",
  "timestamp_utc": "2026-04-16T00:40:23.612374+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-san-francisco-67",
  "vpn_location_label": "San Francisco, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.187.168.67",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.187.168.67",
      "ipv6": null,
      "raw_excerpt": "185.187.168.67",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "185.187.168.67",
      "ipv6": null,
      "raw_excerpt": "185.187.168.67",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.187.168.67",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.187.168.67\"}",
      "error": null
    }
  ],
  "dns_servers_observed": [
    {
      "tier": "local",
      "detail": "resolv.conf nameserver lines (Unix)",
      "servers": [
        "100.64.0.2"
      ]
    },
    {
      "tier": "local",
      "detail": "getaddrinfo('whoami.akamai.net')",
      "servers": [
        "185.187.168.73"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.187.168.67"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "75152e19-12ff-477e-b68c-bb9128ff3691.local",
      "port": 50289,
      "raw": "candidate:3787496119 1 udp 2113937151 75152e19-12ff-477e-b68c-bb9128ff3691.local 50289 typ host generation 0 ufrag tMgR network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.187.168.67",
      "port": 37309,
      "raw": "candidate:3788839825 1 udp 1677729535 185.187.168.67 37309 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag tMgR network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {},
  "attribution": {
    "asn": 212238,
    "holder": "CDNEXT - Datacamp Limited",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [212238]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 212238,
        "holder": "CDNEXT - Datacamp Limited",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (185.187.168.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260416003544-5e878819-fefe-48a0-8246-97ce15cbab46",
            "process_time": 52,
            "server_id": "app190",
            "build_version": "v0.9.7-2026.04.09",
            "pipeline": "1221926",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-16T00:35:45.035042",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 212238,
                  "holder": "CDNEXT - Datacamp Limited"
                }
              ],
              "related_prefixes": [],
              "resource": "185.187.168.0/24",
              "type": "prefix",
              "block": {
                "resource": "185.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-04-15T16:00:00",
              "num_filtered_out": 0
            }
          }
        }
      },
      {
        "name": "team_cymru",
        "asn": null,
        "holder": null,
        "country": null,
        "raw": {
          "error": "dig timed out after 15s",
          "disclaimer": [
            "Team Cymru DNS lookup timed out; cross-check skipped."
          ]
        }
      },
      {
        "name": "peeringdb",
        "asn": null,
        "holder": null,
        "country": null,
        "raw": {
          "error": "Client error '404 Not Found' for url 'https://www.peeringdb.com/api/net?asn=212238'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
        }
      }
    ],
    "disclaimers": [
      "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
      "Team Cymru DNS lookup timed out; cross-check skipped."
    ]
  },
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-16T00:36:50.435697+00:00",
      "sha256": "43ba36d39f4206a35c19946530ec5e355f3ce5dc2721a3f7c91fb8847a237e20",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    }
  ],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "competitor_probe:enabled",
    "competitor_probe:har_summary",
    "dns:lookup:nordvpn.com",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/185.187.168.67",
    "https://my.nordaccount.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/webrtc",
    "ipv6_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/fingerprint",
    "attribution_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/policy",
    "competitor_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": null,
    "transitions_json": null
  },
  "competitor_surface": {
    "provider_dns": {
      "domains": {
        "nordvpn.com": {
          "ns": [],
          "a": [],
          "aaaa": [],
          "error": "NS: The resolution lifetime expired after 10.206 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
          "txt": [],
          "mx": [],
          "caa": [],
          "rr_errors": {
            "txt": "The resolution lifetime expired after 10.206 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
            "mx": "The resolution lifetime expired after 10.205 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
            "caa": "The resolution lifetime expired after 10.207 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out."
          }
        }
      },
      "ns_hosts": {}
    },
    "web_probes": [
      {
        "url": "https://nordvpn.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ecf22e9dbe738ce-SJC"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ecf22e9dbe738ce"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/competitor_probe/har/d945f098fbd5bb50.har",
          "entry_count": 3,
          "unique_hosts": [
            "nordvpn.com"
          ],
          "unique_schemes": [
            "https"
          ],
          "tracker_candidates": [],
          "cdn_candidates": [],
          "error": null
        }
      ],
      "merged_unique_hosts": [
        "nordvpn.com"
      ],
      "merged_tracker_candidates": [],
      "merged_cdn_candidates": []
    },
    "portal_probes": [
      {
        "host": "my.nordaccount.com",
        "a": [],
        "aaaa": [],
        "https_status": 200,
        "https_cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ecf236aab7b679b-SJC"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "185.187.168.67",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "185.187.168.67"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 185.187.168.67 (185.187.168.67), 15 hops max, 40 byte packets\n",
      "hops": [],
      "returncode": 0
    },
    "stray_json": [],
    "errors": []
  },
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/yourinfo_probe/yourinfo.har",
    "cdn_headers": {},
    "error": null
  },
  "browserleaks_snapshot": {
    "pages": [
      {
        "url": "https://browserleaks.com/ip",
        "final_url": "https://browserleaks.com/ip",
        "status": 200,
        "title": "My IP Address - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.187.168.67\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tCalifornia\nCity\tSan Francisco\nISP\tDatacamp Limited\nOrganization\tPackethub S.A\nNetwork\tAS212238 Datacamp Limited (VPN, VPSH, TOR, ANYCAST, CONTENT)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Los_Angeles (PDT)\nLocal Time\tWed, 15 Apr 2026 17:36:57 -0700\nCoordinates\t37.7749,-122.4190\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.187.168.67\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t17 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t00768b5eb7d62fa09f7fb6772e03048f\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.187.168.0 - 185.187.168.255\nCIDR\t185.187.168.0/24\nName\tPACKETHUB-20221011\nHandle\t185.187.168.0 - 185.187.168.255\nParent Handle\t185.187.168.0 - 185.187.171.255\nNet Type\tASSIGNED PA\nCountry\tUnited States\nRegistration\tTue, 11 Oct 2022 14:07:42 GMT\nLast Changed\tTue, 11 Oct 2022 14:07:42 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
        "text_excerpt_truncated": false,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/dns",
        "final_url": "https://browserleaks.com/dns",
        "status": 200,
        "title": "DNS Leak Test - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.187.168.67\nISP\tDatacamp Limited\nLocation\tUnited States, San Francisco\nDNS Leak Test\nTest Results\tFound 48 Servers, 2 ISP, 3 Locations\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.187.168.62\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.63\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.64\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.65\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.66\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.67\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.68\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.69\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.70\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.71\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.72\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.73\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.74\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.75\tDatacamp Limited\tUnited States, San Francisco\n2607:f8b0:4004:1000::124\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1000::127\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1000::128\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1000::12d\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1001::125\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1001::12a\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1002::128\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1002::12b\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1002::12c\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1002::12d\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1002::12e\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1007::121\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1007::128\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1007::12a\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1007::12d\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1009::12c\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:1009::12e\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:100d::128\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:4004:100d::12d\tGoogle LLC\tUnited States, Los Angeles\n2607:f8b0:400e:c05::121\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c06::124\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c06::129\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c06::12c\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c08::126\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c09::123\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c09::125\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c09::127\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c0a::124\tGoogle LLC\tUnited States, The Dalles\n2607:f8b0:400e:c0c::122\tGoogle LLC\tUn",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/webrtc",
        "final_url": "https://browserleaks.com/webrtc",
        "status": 200,
        "title": "WebRTC Leak Test - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.187.168.67\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.187.168.67\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (217)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
        "text_excerpt_truncated": false,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      },
      {
        "url": "https://browserleaks.com/tls",
        "final_url": "https://browserleaks.com/tls",
        "status": 200,
        "title": "TLS Client Test - TLS Fingerprinting - BrowserLeaks",
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_7c2e8ce9f131\nJA3\t2a419027380130b22d33481c7ee93d92\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x4A4A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0xAAAA\nGREASE\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x000A\nsupported_groups\n\n\n0xFF01\nrenegotiation_info\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x0023\nsession_ticket\n\n\n0x000B\nec_point_formats\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x44CD\napplication_settings\n\n\n0x002B\nsupported_versions\n\n\n0x0005\nstatus_request\n\n\n0x0017\nextended_main_secret\n\n\n0x0000\nserver_name\n\n\n0x0033\nkey_share\n\n\n0x001B\ncompress_certificate\n\n\n0x000D\nsignature_algorithms\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0xBABA\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t59\nenc_length\t32\npayload_length\t240\nkey_share\nclient_shares\t\n0xAAAA\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brows",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260416T003526Z-f5ad2e99/raw/us-california-san-francisco-67/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-ba1b751f",
        "category": "third_party_web",
        "title": "Third-party benchmark page loaded (yourinfo.ai)",
        "description": "HAR and page excerpt captured for competitive benchmark; third parties may observe exit IP and browser metadata.",
        "severity": "LOW",
        "confidence": "HIGH",
        "kind": "inferred",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "yourinfo_snapshot",
            "note": null
          }
        ],
        "affected_data_types": [
          "public_ip",
          "user_agent",
          "browser_fingerprint"
        ],
        "recipients": [
          "yourinfo.ai",
          "asset_hosts"
        ],
        "test_conditions": "connected_state_benchmark",
        "reproducibility_notes": null
      }
    ],
    "question_coverage": [
      {
        "question_id": "IDENTITY-001",
        "question_text": "What identifiers are assigned to the user, app install, browser session, and device?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Browser/session signals captured via fingerprint and optional YourInfo probe.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "fingerprint_snapshot",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "yourinfo_snapshot",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "browserleaks_snapshot",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IDENTITY-006",
        "question_text": "Are there long-lived client identifiers transmitted during auth or app startup?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IDENTITY-009",
        "question_text": "Is the browser fingerprinting surface strong enough to re-identify the same user across sessions?",
        "category": "identity_correlation",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "BrowserLeaks probe data available for re-identification risk assessment.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "fingerprint_snapshot",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "browserleaks_snapshot",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "SIGNUP-001",
        "question_text": "What third parties are involved during signup?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "SIGNUP-004",
        "question_text": "Are analytics or marketing scripts loaded during signup or checkout?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "SIGNUP-010",
        "question_text": "Are these surfaces behind a CDN/WAF?",
        "category": "signup_payment",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Third-party/CDN signals may appear in competitor web probes and HAR artifacts.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "WEB-001",
        "question_text": "Where is the marketing site hosted (DNS/routing level)?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Apex DNS/NS data recorded for configured provider domains.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface.provider_dns",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "WEB-004",
        "question_text": "What CDN/WAF is used?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Response headers / CDN signatures captured in web probes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface.web_probes",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "WEB-008",
        "question_text": "Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs?",
        "category": "website_portal",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Review web probe headers, redirects, and HAR for origin leaks.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-001",
        "question_text": "Which DNS resolvers are used while connected?",
        "category": "dns",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Resolver tiers observed (local + external).",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-002",
        "question_text": "Are DNS requests tunneled (consistent with VPN exit)?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "DNS-003",
        "question_text": "Is there DNS fallback to ISP/router/public resolvers?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "DNS-004",
        "question_text": "Does DNS leak during connect/disconnect/reconnect?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Connect/disconnect DNS not sampled; use --transition-tests when supported.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "DNS-009",
        "question_text": "Are DoH or DoT endpoints used?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "DoH/DoT not isolated from resolver snapshot; inspect raw captures.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "DNS-011",
        "question_text": "Are resolvers first-party or third-party?",
        "category": "dns",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Leak flag=False; see notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "dns_servers_observed",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "dns_leak_notes",
            "note": null
          }
        ],
        "notes": "Heuristic: no obvious public resolver IPs parsed from external page"
      },
      {
        "question_id": "IP-001",
        "question_text": "Is the real public IPv4 exposed while connected?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 185.187.168.67; leak flags dns=False webrtc=False ipv6=False.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_v4",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IP-002",
        "question_text": "Is the real public IPv6 exposed while connected?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "partially_answered",
        "answer_summary": "No IPv6 exit or IPv6 not returned by endpoints.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "IP-006",
        "question_text": "Is the real IP exposed through WebRTC?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "WebRTC candidates captured; leak flag=False.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_leak_flag",
            "note": null
          }
        ],
        "notes": "Exit IP appears in candidate set (expected for tunneled public)"
      },
      {
        "question_id": "IP-007",
        "question_text": "Is the local LAN IP exposed through WebRTC or browser APIs?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_FULL",
        "answer_status": "partially_answered",
        "answer_summary": "Inspect host candidates vs LAN; see webrtc_notes.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          }
        ],
        "notes": "Exit IP appears in candidate set (expected for tunneled public)"
      },
      {
        "question_id": "IP-014",
        "question_text": "Do leak-check sites disagree about observed IP identity?",
        "category": "real_ip_leak",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "All 3 echo endpoints agree on IPv4 185.187.168.67.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_sources",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-002",
        "question_text": "Which domains and IPs are contacted after the tunnel is up?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Post-harness service list captured.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-003",
        "question_text": "Which control-plane endpoints are used for auth/config/session management?",
        "category": "control_plane",
        "testability": "DOCUMENT_RESEARCH",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "Auth/control-plane inventory requires internal docs or app instrumentation.",
        "evidence_refs": [],
        "notes": "DOCUMENT_RESEARCH"
      },
      {
        "question_id": "CTRL-004",
        "question_text": "Which telemetry endpoints are contacted during connection?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Infer from services_contacted and classified endpoints.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "CTRL-009",
        "question_text": "Is the control plane behind a CDN/WAF?",
        "category": "control_plane",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "CDN/WAF hints from web headers.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface.web_probes",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-001",
        "question_text": "What exit IP is assigned for each region?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 185.187.168.67 for location us-california-san-francisco-67.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "exit_ip_v4",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-002",
        "question_text": "What ASN announces the exit IP?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "ASN 212238 — CDNEXT - Datacamp Limited",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "attribution",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-003",
        "question_text": "What organization owns the IP range?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "ASN 212238 — CDNEXT - Datacamp Limited",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "attribution",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-004",
        "question_text": "What reverse DNS exists for the exit node?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "PTR lookup errors: ptr_v4: The resolution lifetime expired after 10.202 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "artifacts.exit_dns_json",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "EXIT-005",
        "question_text": "Does the observed geolocation match the advertised location?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States').",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "extra.exit_geo",
            "note": null
          },
          {
            "artifact_path": null,
            "normalized_pointer": "vpn_location_label",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "THIRDWEB-001",
        "question_text": "What external JS files are loaded on the site?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "THIRDWEB-003",
        "question_text": "What analytics providers are present?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "THIRDWEB-012",
        "question_text": "What cookies are set by first-party and third-party scripts?",
        "category": "third_party_web",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "See web HAR + competitor_surface for external scripts/analytics.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "competitor_surface",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "FP-001",
        "question_text": "Does the site attempt browser fingerprinting?",
        "category": "browser_tracking",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "BrowserLeaks probe pages captured (canvas/WebGL/tls signals in raw excerpts).",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "browserleaks_snapshot",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "FP-011",
        "question_text": "Does WebRTC run on provider pages?",
        "category": "browser_tracking",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "WebRTC exercised by harness on leak-test pages.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "webrtc_candidates",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "TELEM-001",
        "question_text": "Does the app talk to telemetry vendors?",
        "category": "telemetry_app",
        "testability": "INTERNAL_UNVERIFIABLE",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
        "evidence_refs": [],
        "notes": "INTERNAL_UNVERIFIABLE"
      },
      {
        "question_id": "TELEM-004",
        "question_text": "Does the app send connection events to telemetry systems?",
        "category": "telemetry_app",
        "testability": "INTERNAL_UNVERIFIABLE",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "App telemetry requires traffic capture or binary analysis; not proven by this harness alone.",
        "evidence_refs": [],
        "notes": "INTERNAL_UNVERIFIABLE"
      },
      {
        "question_id": "OS-001",
        "question_text": "On macOS/Windows/Linux, do helper processes bypass the tunnel?",
        "category": "os_specific",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "runner_env",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "FAIL-001",
        "question_text": "What leaks during initial connection?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "FAIL-003",
        "question_text": "What leaks during reconnect?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Not sampled; optional --transition-tests or manual observation.",
        "evidence_refs": [],
        "notes": null
      },
      {
        "question_id": "FAIL-004",
        "question_text": "What leaks if the VPN app crashes?",
        "category": "failure_state",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "not_testable_dynamically",
        "answer_summary": "Crash/kill leak tests not run in this harness by default.",
        "evidence_refs": [],
        "notes": "DYNAMIC_PARTIAL"
      },
      {
        "question_id": "LOG-001",
        "question_text": "What is the provider likely able to log based on observed traffic?",
        "category": "logging_retention",
        "testability": "DYNAMIC_PARTIAL",
        "answer_status": "partially_answered",
        "answer_summary": "Infer logging surface from observable endpoints and services_contacted.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ],
        "notes": null
      },
      {
        "question_id": "LOG-005",
        "question_text": "Are there contradictions between observed traffic and no-logs marketing claims?",
        "category": "logging_retention",
        "testability": "DOCUMENT_RESEARCH",
        "answer_status": "partially_answered",
        "answer_summary": "Policy text captured; compare claims to observed traffic manually.",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "policies",
            "note": null
          }
        ],
        "notes": null
      }
    ],
    "risk_scores": {
      "overall_severity": "LOW",
      "leak_severity": "INFO",
      "correlation_risk": "MEDIUM",
      "third_party_exposure": "MEDIUM",
      "notes": [
        "Competitor web/portal probes executed."
      ]
    },
    "observed_endpoints": [
      {
        "host": "api.ipify.org",
        "classification": "third_party_analytics",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "api64.ipify.org",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "browserleaks.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "competitor_probe",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "dns",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "ipleak.net",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "ipwho.is",
        "classification": "unknown",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "my.nordaccount.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "nordvpn.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "policy",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "test-ipv6.com",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "transit",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "webrtc",
        "classification": "unknown",
        "confidence": 0.4,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      },
      {
        "host": "yourinfo.ai",
        "classification": "unknown",
        "confidence": 0.95,
        "source": "services_contacted",
        "evidence_refs": [
          {
            "artifact_path": null,
            "normalized_pointer": "services_contacted",
            "note": null
          }
        ]
      }
    ]
  },
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "185.187.168.67",
      "country_code": "US",
      "region": "California",
      "city": "San Francisco",
      "connection": {
        "asn": 212238,
        "org": "Packethub S.A.",
        "isp": "Datacamp Limited",
        "domain": "packethub.net"
      },
      "location_id": "us-california-san-francisco-67",
      "location_label": "San Francisco, California, United States"
    }
  }
}
```

---



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`