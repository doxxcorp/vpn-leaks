# Nordvpn (nordvpn)

- **Report generated:** 2026-04-16T04:52:33.739087+00:00
- **Runs included:** nordvpn-20260416T042117Z-7bbf2d88, nordvpn-20260416T042749Z-00a43d39, nordvpn-20260416T044817Z-976afdc6
- **Normalized locations:** 3

> **How to read this report**
>
> - The **Matrix**, **Leak summary**, and **Underlay (ASNs)** sections below are a **high-level rollup only**.
> - **Per-location benchmarks** (exit IP, DNS, WebRTC, IPv6, fingerprint, attribution, policies, services, artifacts, YourInfo, competitor probes, and the full JSON record) are in **`## Detailed runs`** — they are **not omitted**; scroll or open this file as plain text if the preview shows only the first screen.
> - The **canonical** machine-readable record for each location is always `runs/<run_id>/locations/<location_id>/normalized.json` (paths are repeated under each run). For very large JSON, use your editor or a JSON viewer rather than Markdown preview alone.

## Matrix

| Field | Value |
|-------|-------|
| Connection modes observed | manual_gui |
| Locations covered | 3 |

## Executive summary (SPEC framework)


- **Rollup severity (max across runs):** `LOW`
- **Question coverage (merged across locations, one row per SPEC ID):** counts below sum to **42** question(s) in the bank (42 total). Status for each ID is the **strictest** across benchmark rows: unanswered > partially answered > answered > not testable dynamically.
  - answered: 7
  - partially answered: 31
  - unanswered: 0
  - not testable dynamically: 4

**Top severity findings (HIGH/CRITICAL)**


- *None flagged in this rollup.*


## SPEC question coverage (full table)

| ID | Status | Category | Question | Summary | Next steps |
|----|--------|----------|----------|---------|------------|
| `IDENTITY-001` | `partially_answered` | identity_correlation | What identifiers are assigned to the user, app install, browser session, and device? | Browser/session signals captured via fingerprint and optional YourInfo probe. | Run with fingerprint + YourInfo probes enabled; compare `fingerprint_snapshot` and `yourinfo_snapshot` in normalized.json. See RUN-STEPS.md (benchmark phases). |
| `IDENTITY-006` | `partially_answered` | identity_correlation | Are there long-lived client identifiers transmitted during auth or app startup? | Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints). | Browser `services_contacted` is partial; for app auth traffic use external capture or vendor docs (D). |
| `IDENTITY-009` | `partially_answered` | identity_correlation | Is the browser fingerprinting surface strong enough to re-identify the same user across sessions? | Fingerprint and BrowserLeaks captures present for re-identification risk assessment. | Enable fingerprint capture; without it re-ID risk stays unassessed. |
| `SIGNUP-001` | `partially_answered` | signup_payment | What third parties are involved during signup? | Third-party/CDN signals may appear in competitor web probes and HAR artifacts. | Set `competitor_probe` + `surface_urls` for signup/checkout in the provider YAML; re-run `vpn-leaks run`. |
| `SIGNUP-004` | `partially_answered` | signup_payment | Are analytics or marketing scripts loaded during signup or checkout? | Third-party/CDN signals may appear in competitor web probes and HAR artifacts. | Same as signup surface — competitor web HAR and `har_summary.json`. |
| `SIGNUP-010` | `partially_answered` | signup_payment | Are these surfaces behind a CDN/WAF? | Third-party/CDN signals may appear in competitor web probes and HAR artifacts. | Enable competitor web probes; check `cdn_headers` / `web_probes` in competitor_surface. |
| `WEB-001` | `partially_answered` | website_portal | Where is the marketing site hosted (DNS/routing level)? | Apex DNS/NS data recorded for configured provider domains. | Set `competitor_probe.provider_domains` (and related probes); for desk truth use `dig apex NS` + glue WHOIS (see docs/research-questions-and-evidence.md §H). |
| `WEB-004` | `partially_answered` | website_portal | What CDN/WAF is used? | Response headers / CDN signatures captured in web probes. | Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed. |
| `WEB-008` | `partially_answered` | website_portal | Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs? | Review web probe headers, redirects, and HAR for origin leaks. | Enable competitor probes and review HAR / redirects in raw artifacts. |
| `DNS-001` | `answered` | dns | Which DNS resolvers are used while connected? | Resolver tiers observed (local + external). | — |
| `DNS-002` | `partially_answered` | dns | Are DNS requests tunneled (consistent with VPN exit)? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Compare resolver IPs to exit; read `dns_leak_notes` (heuristic). Capture baseline off-VPN if comparing. |
| `DNS-003` | `partially_answered` | dns | Is there DNS fallback to ISP/router/public resolvers? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Same as DNS-002; transition tests help — run with `--transition-tests` when supported. |
| `DNS-004` | `partially_answered` | dns | Does DNS leak during connect/disconnect/reconnect? | Connect/disconnect DNS not sampled; use --transition-tests when supported. | Run `vpn-leaks run` with `--transition-tests` (see RUN-STEPS.md). |
| `DNS-009` | `partially_answered` | dns | Are DoH or DoT endpoints used? | DoH/DoT not isolated from resolver snapshot; inspect raw captures. | Inspect raw DNS captures / resolver lists; DoH/DoT may not be isolated in summary alone. |
| `DNS-011` | `partially_answered` | dns | Are resolvers first-party or third-party? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Attribute resolver IPs (O); compare to exit ASN (I/D). |
| `IP-001` | `answered` | real_ip_leak | Is the real public IPv4 exposed while connected? | Exit IPv4 185.161.202.238; leak flags dns=False webrtc=False ipv6=False. | — |
| `IP-002` | `partially_answered` | real_ip_leak | Is the real public IPv6 exposed while connected? | No IPv6 exit or IPv6 not returned by endpoints. | Enable IPv6 path in environment; check `ipv6/` artifacts when present. |
| `IP-006` | `answered` | real_ip_leak | Is the real IP exposed through WebRTC? | WebRTC candidates captured; leak flag=False. | — |
| `IP-007` | `partially_answered` | real_ip_leak | Is the local LAN IP exposed through WebRTC or browser APIs? | Inspect host candidates vs LAN; see webrtc_notes. | Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`. |
| `IP-014` | `partially_answered` | real_ip_leak | Do leak-check sites disagree about observed IP identity? | Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.238, 91.64.142.30. | Compare `exit_ip_sources` entries for disagreement. |
| `CTRL-002` | `partially_answered` | control_plane | Which domains and IPs are contacted after the tunnel is up? | Post-harness service list captured. | `services_contacted` in `normalized.json` lists only URLs and probes this harness actually ran (not full-device traffic). Run a fuller benchmark: avoid `--skip-browserleaks` and competitor skip flags where you need those surfaces; add `competitor_probe` / portal / `surface_urls` in the provider YAML per RUN-STEPS.md; add more locations for diversity. For VPN app background traffic, use external capture—see CTRL-003. |
| `CTRL-003` | `not_testable_dynamically` | control_plane | Which control-plane endpoints are used for auth/config/session management? | Auth/control-plane inventory requires internal docs or app instrumentation. | DOCUMENT_RESEARCH: vendor docs, app MITM, or support (D). |
| `CTRL-004` | `partially_answered` | control_plane | Which telemetry endpoints are contacted during connection? | Infer from services_contacted and classified endpoints. | Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*). |
| `CTRL-009` | `partially_answered` | control_plane | Is the control plane behind a CDN/WAF? | CDN/WAF hints from web headers. | Enable portal/web probes (`portal_probes`); check `https_cdn_headers`. |
| `EXIT-001` | `answered` | exit_infrastructure | What exit IP is assigned for each region? | Exit IPv4 185.187.168.64 for location us-california-san-francisco-64. | — |
| `EXIT-002` | `answered` | exit_infrastructure | What ASN announces the exit IP? | ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-003` | `answered` | exit_infrastructure | What organization owns the IP range? | ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-004` | `partially_answered` | exit_infrastructure | What reverse DNS exists for the exit node? | PTR lookup errors: ptr_v4: The DNS query name does not exist: 238.202.161.185.in-addr.arpa. | Check raw `exit_dns.json` / attribution for rDNS when stored. |
| `EXIT-005` | `partially_answered` | exit_infrastructure | Does the observed geolocation match the advertised location? | Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States'). | Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate. |
| `THIRDWEB-001` | `partially_answered` | third_party_web | What external JS files are loaded on the site? | See web HAR + competitor_surface for external scripts/analytics. | Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`. |
| `THIRDWEB-003` | `partially_answered` | third_party_web | What analytics providers are present? | See web HAR + competitor_surface for external scripts/analytics. | HAR + `har_summary.json` tracker_candidates when competitor probes run. |
| `THIRDWEB-012` | `partially_answered` | third_party_web | What cookies are set by first-party and third-party scripts? | See web HAR + competitor_surface for external scripts/analytics. | Review HAR for Set-Cookie; summary may be partial. |
| `FP-001` | `partially_answered` | browser_tracking | Does the site attempt browser fingerprinting? | Fingerprint snapshot present. | Per location, FP-001 is satisfied when `fingerprint_snapshot` and/or `browserleaks_snapshot` in `normalized.json` has real content: set `fingerprint.enabled: true` under `configs/tools/leak-tests.yaml` (optional Playwright navigator snapshot), re-run `vpn-leaks run` without `--skip-browserleaks`, and confirm `raw/<location>/browserleaks_probe/` exists. Merged report status is strictest across locations—if any location lacks that evidence, FP-001 can stay unanswered for the whole report; check each location under Detailed runs or `framework.question_coverage`. |
| `FP-011` | `answered` | browser_tracking | Does WebRTC run on provider pages? | WebRTC exercised by harness on leak-test pages. | — |
| `TELEM-001` | `not_testable_dynamically` | telemetry_app | Does the app talk to telemetry vendors? | App telemetry requires traffic capture or binary analysis; not proven by this harness alone. | INTERNAL_UNVERIFIABLE in harness; use binary/network analysis or vendor disclosures (D). |
| `TELEM-004` | `not_testable_dynamically` | telemetry_app | Does the app send connection events to telemetry systems? | App telemetry requires traffic capture or binary analysis; not proven by this harness alone. | Same as TELEM-001. |
| `OS-001` | `partially_answered` | os_specific | On macOS/Windows/Linux, do helper processes bypass the tunnel? | OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run. | Process-level bypass not in default harness; external tooling or manual checks. |
| `FAIL-001` | `partially_answered` | failure_state | What leaks during initial connection? | Not sampled; optional --transition-tests or manual observation. | Use `--transition-tests` for connect-phase leaks when supported. |
| `FAIL-003` | `partially_answered` | failure_state | What leaks during reconnect? | Not sampled; optional --transition-tests or manual observation. | Use `--transition-tests` for reconnect leaks when supported. |
| `FAIL-004` | `not_testable_dynamically` | failure_state | What leaks if the VPN app crashes? | Crash/kill leak tests not run in this harness by default. | Crash/kill scenarios not in default harness; fault injection or manual test. |
| `LOG-001` | `partially_answered` | logging_retention | What is the provider likely able to log based on observed traffic? | Infer logging surface from observable endpoints and services_contacted. | Review `services_contacted` + endpoint classifications; pair with policy/audit (D). |
| `LOG-005` | `partially_answered` | logging_retention | Are there contradictions between observed traffic and no-logs marketing claims? | Policy text captured; compare claims to observed traffic manually. | Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md. |

## How to close gaps

Questions still **unanswered** or only **partially answered** (merged status). Use **Next steps** above; this list is the same IDs in short form.



- **`IDENTITY-001`** (`partially_answered`): Run with fingerprint + YourInfo probes enabled; compare `fingerprint_snapshot` and `yourinfo_snapshot` in normalized.json. See RUN-STEPS.md (benchmark phases).

- **`IDENTITY-006`** (`partially_answered`): Browser `services_contacted` is partial; for app auth traffic use external capture or vendor docs (D).

- **`IDENTITY-009`** (`partially_answered`): Enable fingerprint capture; without it re-ID risk stays unassessed.

- **`SIGNUP-001`** (`partially_answered`): Set `competitor_probe` + `surface_urls` for signup/checkout in the provider YAML; re-run `vpn-leaks run`.

- **`SIGNUP-004`** (`partially_answered`): Same as signup surface — competitor web HAR and `har_summary.json`.

- **`SIGNUP-010`** (`partially_answered`): Enable competitor web probes; check `cdn_headers` / `web_probes` in competitor_surface.

- **`WEB-001`** (`partially_answered`): Set `competitor_probe.provider_domains` (and related probes); for desk truth use `dig apex NS` + glue WHOIS (see docs/research-questions-and-evidence.md §H).

- **`WEB-004`** (`partially_answered`): Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed.

- **`WEB-008`** (`partially_answered`): Enable competitor probes and review HAR / redirects in raw artifacts.

- **`DNS-002`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Compare resolver IPs to exit; read `dns_leak_notes` (heuristic). Capture baseline off-VPN if comparing.

- **`DNS-003`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Same as DNS-002; transition tests help — run with `--transition-tests` when supported.

- **`DNS-004`** (`partially_answered`): Run `vpn-leaks run` with `--transition-tests` (see RUN-STEPS.md).

- **`DNS-009`** (`partially_answered`): Inspect raw DNS captures / resolver lists; DoH/DoT may not be isolated in summary alone.

- **`DNS-011`** (`partially_answered`): Heuristic: no obvious public resolver IPs parsed from external page — Attribute resolver IPs (O); compare to exit ASN (I/D).

- **`IP-002`** (`partially_answered`): Enable IPv6 path in environment; check `ipv6/` artifacts when present.

- **`IP-007`** (`partially_answered`): Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`.

- **`IP-014`** (`partially_answered`): Compare `exit_ip_sources` entries for disagreement.

- **`CTRL-002`** (`partially_answered`): `services_contacted` in `normalized.json` lists only URLs and probes this harness actually ran (not full-device traffic). Run a fuller benchmark: avoid `--skip-browserleaks` and competitor skip flags where you need those surfaces; add `competitor_probe` / portal / `surface_urls` in the provider YAML per RUN-STEPS.md; add more locations for diversity. For VPN app background traffic, use external capture—see CTRL-003.

- **`CTRL-004`** (`partially_answered`): Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*).

- **`CTRL-009`** (`partially_answered`): Enable portal/web probes (`portal_probes`); check `https_cdn_headers`.

- **`EXIT-004`** (`partially_answered`): Check raw `exit_dns.json` / attribution for rDNS when stored.

- **`EXIT-005`** (`partially_answered`): Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate.

- **`THIRDWEB-001`** (`partially_answered`): Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`.

- **`THIRDWEB-003`** (`partially_answered`): HAR + `har_summary.json` tracker_candidates when competitor probes run.

- **`THIRDWEB-012`** (`partially_answered`): Review HAR for Set-Cookie; summary may be partial.

- **`FP-001`** (`partially_answered`): Per location, FP-001 is satisfied when `fingerprint_snapshot` and/or `browserleaks_snapshot` in `normalized.json` has real content: set `fingerprint.enabled: true` under `configs/tools/leak-tests.yaml` (optional Playwright navigator snapshot), re-run `vpn-leaks run` without `--skip-browserleaks`, and confirm `raw/<location>/browserleaks_probe/` exists. Merged report status is strictest across locations—if any location lacks that evidence, FP-001 can stay unanswered for the whole report; check each location under Detailed runs or `framework.question_coverage`.

- **`OS-001`** (`partially_answered`): Process-level bypass not in default harness; external tooling or manual checks.

- **`FAIL-001`** (`partially_answered`): Use `--transition-tests` for connect-phase leaks when supported.

- **`FAIL-003`** (`partially_answered`): Use `--transition-tests` for reconnect leaks when supported.

- **`LOG-001`** (`partially_answered`): Review `services_contacted` + endpoint classifications; pair with policy/audit (D).

- **`LOG-005`** (`partially_answered`): Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md.



## Analysis of collected evidence

### Scope

- **Benchmark rows in this report:** 3 (one row per `normalized.json` location).
- **Merge rule:** For each SPEC question ID, the status shown in the table is the **strictest** across rows: unanswered > partially_answered > answered > not_testable_dynamically.

### Risk and findings

- **Rollup severity (max across runs):** `LOW`
- **HIGH / CRITICAL framework findings:** none in this rollup.

### By category (merged coverage)

#### browser_tracking

- **FP-001** (partial): Fingerprint snapshot present.
- **FP-011** (answered): WebRTC exercised by harness on leak-test pages.

#### control_plane

- **CTRL-002** (partial): Post-harness service list captured.
- **CTRL-003** (`not_testable_dynamically`): Auth/control-plane inventory requires internal docs or app instrumentation.
- **CTRL-004** (partial): Infer from services_contacted and classified endpoints.
- **CTRL-009** (partial): CDN/WAF hints from web headers.

#### dns

- **DNS-001** (answered): Resolver tiers observed (local + external).
- **DNS-002** (partial): Leak flag=False; see notes.
- **DNS-003** (partial): Leak flag=False; see notes.
- **DNS-004** (partial): Connect/disconnect DNS not sampled; use --transition-tests when supported.
- **DNS-009** (partial): DoH/DoT not isolated from resolver snapshot; inspect raw captures.
- **DNS-011** (partial): Leak flag=False; see notes.

#### exit_infrastructure

- **EXIT-001** (answered): Exit IPv4 185.187.168.64 for location us-california-san-francisco-64.
- **EXIT-002** (answered): ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-003** (answered): ASN 136787 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-004** (partial): PTR lookup errors: ptr_v4: The DNS query name does not exist: 238.202.161.185.in-addr.arpa.
- **EXIT-005** (partial): Consistent: exit_geo.location_label matches vpn_location_label ('San Francisco, California, United States').

#### failure_state

- **FAIL-001** (partial): Not sampled; optional --transition-tests or manual observation.
- **FAIL-003** (partial): Not sampled; optional --transition-tests or manual observation.
- **FAIL-004** (`not_testable_dynamically`): Crash/kill leak tests not run in this harness by default.

#### identity_correlation

- **IDENTITY-001** (partial): Browser/session signals captured via fingerprint and optional YourInfo probe.
- **IDENTITY-006** (partial): Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints).
- **IDENTITY-009** (partial): Fingerprint and BrowserLeaks captures present for re-identification risk assessment.

#### logging_retention

- **LOG-001** (partial): Infer logging surface from observable endpoints and services_contacted.
- **LOG-005** (partial): Policy text captured; compare claims to observed traffic manually.

#### os_specific

- **OS-001** (partial): OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.

#### real_ip_leak

- **IP-001** (answered): Exit IPv4 185.161.202.238; leak flags dns=False webrtc=False ipv6=False.
- **IP-002** (partial): No IPv6 exit or IPv6 not returned by endpoints.
- **IP-006** (answered): WebRTC candidates captured; leak flag=False.
- **IP-007** (partial): Inspect host candidates vs LAN; see webrtc_notes.
- **IP-014** (partial): Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.238, 91.64.142.30.

#### signup_payment

- **SIGNUP-001** (partial): Third-party/CDN signals may appear in competitor web probes and HAR artifacts.
- **SIGNUP-004** (partial): Third-party/CDN signals may appear in competitor web probes and HAR artifacts.
- **SIGNUP-010** (partial): Third-party/CDN signals may appear in competitor web probes and HAR artifacts.

#### telemetry_app

- **TELEM-001** (`not_testable_dynamically`): App telemetry requires traffic capture or binary analysis; not proven by this harness alone.
- **TELEM-004** (`not_testable_dynamically`): App telemetry requires traffic capture or binary analysis; not proven by this harness alone.

#### third_party_web

- **THIRDWEB-001** (partial): See web HAR + competitor_surface for external scripts/analytics.
- **THIRDWEB-003** (partial): See web HAR + competitor_surface for external scripts/analytics.
- **THIRDWEB-012** (partial): See web HAR + competitor_surface for external scripts/analytics.

#### website_portal

- **WEB-001** (partial): Apex DNS/NS data recorded for configured provider domains.
- **WEB-004** (partial): Response headers / CDN signatures captured in web probes.
- **WEB-008** (partial): Review web probe headers, redirects, and HAR for origin leaks.

### Limitations

- Leak flags and DNS notes are **heuristic / harness-defined**; read raw `runs/.../raw/` artifacts for full context.
- **Observed leak flags (any location):** DNS=False, WebRTC=False, IPv6=False.
- **App telemetry (TELEM-001, TELEM-004)** and some control-plane details are **not** proven by browser-only harness paths; use **D** (documents) or external traffic studies where applicable.
- **Desk research (S)** (e.g. apex `dig`, glue WHOIS) is not auto-merged into this report; compare to `competitor_probe` / provider DNS when both exist.




## Leak summary

| Location | DNS leak | WebRTC leak | IPv6 leak |
|----------|----------|-------------|-----------|
| San Francisco, CA, USA | False | False | False |
| Albuquerque, NM, USA | False | False | False |
| Hamburg, HA, DEU | False | False | False |


## Underlay (ASNs)


- **AS136787:** PACKETHUBSA-AS-AP PacketHub S.A.

- **AS207137:** PACKETHUBSA - PacketHub S.A.

- **AS212238:** CDNEXT - Datacamp Limited


---

## Detailed runs

**Included in this report** (each subsection below mirrors one `normalized.json`):


1. `nordvpn-20260416T042117Z-7bbf2d88` / `us-california-san-francisco-64` — `runs/nordvpn-20260416T042117Z-7bbf2d88/locations/us-california-san-francisco-64/normalized.json`

2. `nordvpn-20260416T042749Z-00a43d39` / `us-new-mexico-albuquerque-105` — `runs/nordvpn-20260416T042749Z-00a43d39/locations/us-new-mexico-albuquerque-105/normalized.json`

3. `nordvpn-20260416T044817Z-976afdc6` / `de-hamburg-hamburg-238` — `runs/nordvpn-20260416T044817Z-976afdc6/locations/de-hamburg-hamburg-238/normalized.json`


Large JSON fields use size caps in this markdown file; when an excerpt hits a cap, a **note** appears at the start of that run’s section listing what was capped. **On-disk `normalized.json` is always complete.**



### nordvpn-20260416T042117Z-7bbf2d88 / us-california-san-francisco-64



- **vpn_provider:** nordvpn
- **Label:** San Francisco, California, United States
- **Path:** `runs/nordvpn-20260416T042117Z-7bbf2d88/locations/us-california-san-francisco-64/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-16T04:24:50.894371+00:00
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
| exit_ip_v4 | 185.187.168.64 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.187.168.64",
    "ipv6": null,
    "raw_excerpt": "185.187.168.64",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "185.187.168.64",
    "ipv6": null,
    "raw_excerpt": "185.187.168.64",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.187.168.64",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.187.168.64\"}",
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
      "185.187.168.66"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.187.168.64"
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
| host | udp | f6081914-5fd9-499c-975e-3991d769a321.local | 59115 | `candidate:1654439336 1 udp 2113937151 f6081914-5fd9-499c-975e-3991d769a321.local 59115 typ host generation 0 ufrag De7T network-cost 999` |
| srflx | udp | 185.187.168.64 | 53197 | `candidate:1998429096 1 udp 1677729535 185.187.168.64 53197 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag De7T network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


```json
{
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
  "language": "en-US",
  "hardwareConcurrency": 16,
  "platform": "MacIntel"
}
```


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
          "query_id": "20260416042136-e301b79c-fb25-4e0f-aa4b-368ccc31fcea",
          "process_time": 52,
          "server_id": "app188",
          "build_version": "v0.9.7-2026.04.09",
          "pipeline": "1221926",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-16T04:21:36.755018",
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
      "asn": 212238,
      "holder": null,
      "country": null,
      "raw": {
        "asn": 212238,
        "raw_line": "212238 | 185.187.168.0/24 | DE | ripencc | 2017-01-27",
        "parts": [
          "212238",
          "185.187.168.0/24",
          "DE",
          "ripencc",
          "2017-01-27"
        ],
        "disclaimer": [
          "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
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
    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
  ]
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:22:17.214432+00:00",
    "sha256": "a02374b5f44f77895e1d8adcda2f3e403f68034aa978074fa12c75e3114136ab",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  },
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:22:21.449340+00:00",
    "sha256": "0f63d0050f0884d2eb72d5b5aec4a9ebe01382d9339a615b98e1a0ae34dad9fe",
    "summary_bullets": [
      "Mentions retention (keyword hit; review source)",
      "Mentions logging (keyword hit; review source)",
      "Mentions law enforcement (keyword hit; review source)",
      "Mentions third parties (keyword hit; review source)",
      "Mentions telemetry (keyword hit; review source)"
    ]
  }
]
```

#### Services contacted




- `attribution:ns_glue:108.162.192.130`

- `attribution:ns_glue:108.162.193.142`

- `attribution:ns_glue:172.64.32.130`

- `attribution:ns_glue:172.64.33.142`

- `attribution:ns_glue:173.245.58.130`

- `attribution:ns_glue:173.245.59.142`

- `attribution:ns_glue:2606:4700:50::adf5:3a82`

- `attribution:ns_glue:2606:4700:58::adf5:3b8e`

- `attribution:ns_glue:2803:f800:50::6ca2:c082`

- `attribution:ns_glue:2803:f800:50::6ca2:c18e`

- `attribution:ns_glue:2a06:98c1:50::ac40:2082`

- `attribution:ns_glue:2a06:98c1:50::ac40:218e`

- `browserleaks.com:playwright_chromium`

- `competitor_probe:enabled`

- `competitor_probe:har_summary`

- `dns:lookup:nordvpn.com`

- `dns:ns_glue:lily.ns.cloudflare.com`

- `dns:ns_glue:seth.ns.cloudflare.com`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/185.187.168.64`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordcheckout.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/pricing/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/webrtc",
  "ipv6_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/fingerprint",
  "attribution_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/policy",
  "competitor_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe",
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
  "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-33b378c6",
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
      "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
      "answer_summary": "Exit IPv4 185.187.168.64; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 185.187.168.64.",
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
      "answer_summary": "Exit IPv4 185.187.168.64 for location us-california-san-francisco-64.",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 64.168.187.185.in-addr.arpa.",
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
      "answer_summary": "Fingerprint snapshot present.",
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
      "Competitor web/portal probes executed.",
      "Large services_contacted list."
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
      "host": "attribution",
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
      "host": "fingerprint",
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
      "host": "nordcheckout.com",
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
        "ns": [
          "lily.ns.cloudflare.com",
          "seth.ns.cloudflare.com"
        ],
        "a": [
          "104.16.208.203",
          "104.19.159.190"
        ],
        "aaaa": [],
        "error": null,
        "txt": [
          "MS=ms41624661",
          "MS=ms60989570",
          "MS=ms69824556",
          "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
          "oneuptime=2fYJpBXRQsmY3Py",
          "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
          "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13"
        ],
        "mx": [
          "1 aspmx.l.google.com",
          "5 alt1.aspmx.l.google.com",
          "5 alt2.aspmx.l.google.com",
          "10 alt3.aspmx.l.google.com",
          "10 alt4.aspmx.l.google.com"
        ],
        "caa": [],
        "rr_errors": {
          "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
        }
      }
    },
    "ns_hosts": {
      "lily.ns.cloudflare.com": {
        "a": [
          "108.162.192.130",
          "172.64.32.130",
          "173.245.58.130"
        ],
        "aaaa": [
          "2606:4700:50::adf5:3a82",
          "2803:f800:50::6ca2:c082",
          "2a06:98c1:50::ac40:2082"
        ],
        "ip_attribution": {
          "108.162.192.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (108.162.192.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "108.162.192.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042253-20615932-1f20-4a42-ace1-63e767a569ee",
                    "process_time": 68,
                    "server_id": "app175",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:22:53.763171",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "108.162.192.0/20"
                      ],
                      "resource": "108.162.192.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "108.0.0.0/8",
                        "desc": "ARIN (Status: ALLOCATED)",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 108.162.192.0/20 | US | arin | 2011-10-28",
                  "parts": [
                    "13335",
                    "108.162.192.0/20",
                    "US",
                    "arin",
                    "2011-10-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "data": [
                    {
                      "id": 4224,
                      "org_id": 4715,
                      "name": "Cloudflare",
                      "aka": "",
                      "name_long": "",
                      "website": "https://www.cloudflare.com",
                      "social_media": [
                        {
                          "service": "website",
                          "identifier": "https://www.cloudflare.com"
                        }
                      ],
                      "asn": 13335,
                      "looking_glass": "",
                      "route_server": "",
                      "irr_as_set": "AS13335:AS-CLOUDFLARE",
                      "info_type": "Content",
                      "info_types": [
                        "Content"
                      ],
                      "info_prefixes4": 80000,
                      "info_prefixes6": 30000,
                      "info_traffic": "",
                      "info_ratio": "Mostly Outbound",
                      "info_scope": "Global",
                      "info_unicast": true,
                      "info_multicast": false,
                      "info_ipv6": true,
                      "info_never_via_route_servers": false,
                      "ix_count": 349,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-02T19:21:39Z",
                      "netfac_updated": "2026-04-01T18:35:35Z",
                      "poc_updated": "2025-12-04T21:15:09Z",
                      "policy_url": "https://www.cloudflare.com/peering-policy/",
                      "policy_general": "Open",
                      "policy_locations": "Preferred",
                      "policy_ratio": false,
                      "policy_contracts": "Not Required",
                      "allow_ixp_update": false,
                      "status_dashboard": "https://www.cloudflarestatus.com/",
                      "rir_status": "ok",
                      "rir_status_updated": "2024-06-26T04:47:55Z",
                      "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                      "created": "2011-09-06T19:40:05Z",
                      "updated": "2026-04-02T10:08:34Z",
                      "status": "ok"
                    }
                  ],
                  "meta": {}
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "172.64.32.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (172.64.32.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "172.64.32.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042256-86fffc52-15c9-48d8-9d9e-00588d0c4fdd",
                    "process_time": 70,
                    "server_id": "app185",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:22:56.088177",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "172.64.32.0/20"
                      ],
                      "resource": "172.64.32.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "172.0.0.0/8",
                        "desc": "Administered by ARIN",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 172.64.32.0/24 | US | arin | 2015-02-25",
                  "parts": [
                    "13335",
                    "172.64.32.0/24",
                    "US",
                    "arin",
                    "2015-02-25"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "data": [
                    {
                      "id": 4224,
                      "org_id": 4715,
                      "name": "Cloudflare",
                      "aka": "",
                      "name_long": "",
                      "website": "https://www.cloudflare.com",
                      "social_media": [
                        {
                          "service": "website",
                          "identifier": "https://www.cloudflare.com"
                        }
                      ],
                      "asn": 13335,
                      "looking_glass": "",
                      "route_server": "",
                      "irr_as_set": "AS13335:AS-CLOUDFLARE",
                      "info_type": "Content",
                      "info_types": [
                        "Content"
                      ],
                      "info_prefixes4": 80000,
                      "info_prefixes6": 30000,
                      "info_traffic": "",
                      "info_ratio": "Mostly Outbound",
                      "info_scope": "Global",
                      "info_unicast": true,
                      "info_multicast": false,
                      "info_ipv6": true,
                      "info_never_via_route_servers": false,
                      "ix_count": 349,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-02T19:21:39Z",
                      "netfac_updated": "2026-04-01T18:35:35Z",
                      "poc_updated": "2025-12-04T21:15:09Z",
                      "policy_url": "https://www.cloudflare.com/peering-policy/",
                      "policy_general": "Open",
                      "policy_locations": "Preferred",
                      "policy_ratio": false,
                      "policy_contracts": "Not Required",
                      "allow_ixp_update": false,
                      "status_dashboard": "https://www.cloudflarestatus.com/",
                      "rir_status": "ok",
                      "rir_status_updated": "2024-06-26T04:47:55Z",
                      "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                      "created": "2011-09-06T19:40:05Z",
                      "updated": "2026-04-02T10:08:34Z",
                      "status": "ok"
                    }
                  ],
                  "meta": {}
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "173.245.58.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (173.245.58.0/24)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042258-81cef06f-1822-4e08-9ce9-7845b97db5a6",
                    "process_time": 271,
                    "server_id": "app186",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:22:58.674915",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "173.245.58.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "173.0.0.0/8",
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
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 173.245.58.0/24 | US | arin | 2010-12-28",
                  "parts": [
                    "13335",
                    "173.245.58.0/24",
                    "US",
                    "arin",
                    "2010-12-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "2606:4700:50::adf5:3a82": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "2606:4700::/36"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042301-8fc860a0-4fbe-41b5-862a-c9dfa6cc559b",
                    "process_time": 53,
                    "server_id": "app167",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:01.606998",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "2606:4700::/36"
                      ],
                      "resource": "2606:4700:50::/44",
                      "type": "prefix",
                      "block": {
                        "resource": "2600::/12",
                        "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
                      },
                      "actual_num_related": 1,
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2803:f800:50::6ca2:c082": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042303-998d5cdf-72c6-49c6-b503-1cadd85c30d3",
                    "process_time": 94,
                    "server_id": "app192",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:03.220857",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2803:f800:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2800::/12",
                        "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2a06:98c1:50::ac40:2082": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042304-573f9201-f16e-42e6-9b08-8c5ed12e0328",
                    "process_time": 62,
                    "server_id": "app170",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:04.764940",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2a06:98c1:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2a00::/12",
                        "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          }
        },
        "error": null
      },
      "seth.ns.cloudflare.com": {
        "a": [
          "108.162.193.142",
          "172.64.33.142",
          "173.245.59.142"
        ],
        "aaaa": [
          "2606:4700:58::adf5:3b8e",
          "2803:f800:50::6ca2:c18e",
          "2a06:98c1:50::ac40:218e"
        ],
        "ip_attribution": {
          "108.162.193.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (108.162.193.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "108.162.192.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042306-87dfce9a-c6e3-420f-95ab-486af802ca13",
                    "process_time": 54,
                    "server_id": "app182",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:06.379321",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "108.162.192.0/20"
                      ],
                      "resource": "108.162.193.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "108.0.0.0/8",
                        "desc": "ARIN (Status: ALLOCATED)",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 108.162.193.0/24 | US | arin | 2011-10-28",
                  "parts": [
                    "13335",
                    "108.162.193.0/24",
                    "US",
                    "arin",
                    "2011-10-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "172.64.33.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (172.64.33.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "172.64.32.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042308-67923cb7-2677-4e2b-a933-cc276992f376",
                    "process_time": 47,
                    "server_id": "app162",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:08.286323",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "172.64.32.0/20"
                      ],
                      "resource": "172.64.33.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "172.0.0.0/8",
                        "desc": "Administered by ARIN",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 172.64.32.0/20 | US | arin | 2015-02-25",
                  "parts": [
                    "13335",
                    "172.64.32.0/20",
                    "US",
                    "arin",
                    "2015-02-25"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "173.245.59.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (173.245.59.0/24)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042310-91785296-9bf1-4421-a3b7-211d4602cb3c",
                    "process_time": 83,
                    "server_id": "app197",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:10.149748",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "173.245.59.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "173.0.0.0/8",
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
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 173.245.59.0/24 | US | arin | 2010-12-28",
                  "parts": [
                    "13335",
                    "173.245.59.0/24",
                    "US",
                    "arin",
                    "2010-12-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "2606:4700:58::adf5:3b8e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "2606:4700::/36"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042312-dc10e7d4-610f-4fca-9762-35d38229c641",
                    "process_time": 58,
                    "server_id": "app163",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:12.102644",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "2606:4700::/36"
                      ],
                      "resource": "2606:4700:50::/44",
                      "type": "prefix",
                      "block": {
                        "resource": "2600::/12",
                        "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
                      },
                      "actual_num_related": 1,
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2803:f800:50::6ca2:c18e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042313-4812c7c6-b175-42b8-8bd5-8725126a896d",
                    "process_time": 132,
                    "server_id": "app183",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:13.746248",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2803:f800:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2800::/12",
                        "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2a06:98c1:50::ac40:218e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042315-956527ca-ac7f-4079-b951-e9e760e76cb6",
                    "process_time": 57,
                    "server_id": "app174",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:23:15.288417",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2a06:98c1:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2a00::/12",
                        "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          }
        },
        "error": null
      }
    }
  },
  "web_probes": [
    {
      "url": "https://nordvpn.com/",
      "error": null,
      "status": 403,
      "final_url": "https://nordvpn.com/",
      "cdn_headers": {
        "cf-ray": "9ed06c1dabd35c21-SJC",
        "server": "cloudflare"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c1dabd35c21"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe/har/d945f098fbd5bb50.har",
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
      "a": [
        "104.18.42.225",
        "172.64.145.31"
      ],
      "aaaa": [
        "2a06:98c1:3101::6812:2ae1",
        "2a06:98c1:3107::ac40:911f"
      ],
      "https_status": 200,
      "https_cdn_headers": {
        "cf-ray": "9ed06c211fd6ed3f-SJC",
        "server": "cloudflare"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "185.187.168.64",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "185.187.168.64"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 185.187.168.64 (185.187.168.64), 15 hops max, 40 byte packets\n",
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
    "ip": "185.187.168.64",
    "country_code": "US",
    "region": "California",
    "city": "San Francisco",
    "connection": {
      "asn": 212238,
      "org": "Packethub S.A.",
      "isp": "Datacamp Limited",
      "domain": "packethub.net"
    },
    "location_id": "us-california-san-francisco-64",
    "location_label": "San Francisco, California, United States"
  },
  "surface_probe": {
    "probes": [
      {
        "url": "https://nordvpn.com/pricing/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing/",
        "cdn_headers": {
          "cf-ray": "9ed06c276fc5f9f1-SJC",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c276fc5f9f1"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/3cec43152ba057c5.har",
        "page_type": "pricing"
      },
      {
        "url": "https://my.nordaccount.com/",
        "error": null,
        "status": 200,
        "final_url": "https://my.nordaccount.com/",
        "cdn_headers": {
          "cf-ray": "9ed06c2a083667b5-SJC",
          "server": "cloudflare"
        },
        "scripts": [
          "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
          "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
          "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
          "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
          "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
          "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
          "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
          "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
          "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
          "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
          "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
          "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
          "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
          "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
          "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
          "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
          "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
          "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
          "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
          "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
          "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
          "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
          "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
          "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
          "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
          "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
          "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
          "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
          "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
          "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
          "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
          "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
          "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
          "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
          "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
          "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
          "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
          "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
          "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
          "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
          "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
          "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
          "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
          "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
          "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
          "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
          "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
          "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
          "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
          "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
          "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
          "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
          "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
          "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
          "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
          "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/0096221d6f12d382.har",
        "page_type": "signup"
      },
      {
        "url": "https://nordcheckout.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
        "cdn_headers": {
          "cf-ray": "9ed06c377e63235b-SJC",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c377e63235b"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/5c4416295d131e0b.har",
        "page_type": "checkout"
      }
    ],
    "surface_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260416T042117Z-7bbf2d88",
  "timestamp_utc": "2026-04-16T04:24:50.894371+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-san-francisco-64",
  "vpn_location_label": "San Francisco, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.187.168.64",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.187.168.64",
      "ipv6": null,
      "raw_excerpt": "185.187.168.64",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "185.187.168.64",
      "ipv6": null,
      "raw_excerpt": "185.187.168.64",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.187.168.64",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.187.168.64\"}",
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
        "185.187.168.66"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.187.168.64"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "f6081914-5fd9-499c-975e-3991d769a321.local",
      "port": 59115,
      "raw": "candidate:1654439336 1 udp 2113937151 f6081914-5fd9-499c-975e-3991d769a321.local 59115 typ host generation 0 ufrag De7T network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.187.168.64",
      "port": 53197,
      "raw": "candidate:1998429096 1 udp 1677729535 185.187.168.64 53197 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag De7T network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
    "language": "en-US",
    "hardwareConcurrency": 16,
    "platform": "MacIntel"
  },
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
            "query_id": "20260416042136-e301b79c-fb25-4e0f-aa4b-368ccc31fcea",
            "process_time": 52,
            "server_id": "app188",
            "build_version": "v0.9.7-2026.04.09",
            "pipeline": "1221926",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-16T04:21:36.755018",
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
        "asn": 212238,
        "holder": null,
        "country": null,
        "raw": {
          "asn": 212238,
          "raw_line": "212238 | 185.187.168.0/24 | DE | ripencc | 2017-01-27",
          "parts": [
            "212238",
            "185.187.168.0/24",
            "DE",
            "ripencc",
            "2017-01-27"
          ],
          "disclaimer": [
            "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
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
      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
    ]
  },
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:22:17.214432+00:00",
      "sha256": "a02374b5f44f77895e1d8adcda2f3e403f68034aa978074fa12c75e3114136ab",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    },
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:22:21.449340+00:00",
      "sha256": "0f63d0050f0884d2eb72d5b5aec4a9ebe01382d9339a615b98e1a0ae34dad9fe",
      "summary_bullets": [
        "Mentions retention (keyword hit; review source)",
        "Mentions logging (keyword hit; review source)",
        "Mentions law enforcement (keyword hit; review source)",
        "Mentions third parties (keyword hit; review source)",
        "Mentions telemetry (keyword hit; review source)"
      ]
    }
  ],
  "services_contacted": [
    "attribution:ns_glue:108.162.192.130",
    "attribution:ns_glue:108.162.193.142",
    "attribution:ns_glue:172.64.32.130",
    "attribution:ns_glue:172.64.33.142",
    "attribution:ns_glue:173.245.58.130",
    "attribution:ns_glue:173.245.59.142",
    "attribution:ns_glue:2606:4700:50::adf5:3a82",
    "attribution:ns_glue:2606:4700:58::adf5:3b8e",
    "attribution:ns_glue:2803:f800:50::6ca2:c082",
    "attribution:ns_glue:2803:f800:50::6ca2:c18e",
    "attribution:ns_glue:2a06:98c1:50::ac40:2082",
    "attribution:ns_glue:2a06:98c1:50::ac40:218e",
    "browserleaks.com:playwright_chromium",
    "competitor_probe:enabled",
    "competitor_probe:har_summary",
    "dns:lookup:nordvpn.com",
    "dns:ns_glue:lily.ns.cloudflare.com",
    "dns:ns_glue:seth.ns.cloudflare.com",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/185.187.168.64",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordcheckout.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/pricing/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/webrtc",
    "ipv6_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/fingerprint",
    "attribution_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/policy",
    "competitor_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe",
    "transitions_json": null
  },
  "competitor_surface": {
    "provider_dns": {
      "domains": {
        "nordvpn.com": {
          "ns": [
            "lily.ns.cloudflare.com",
            "seth.ns.cloudflare.com"
          ],
          "a": [
            "104.16.208.203",
            "104.19.159.190"
          ],
          "aaaa": [],
          "error": null,
          "txt": [
            "MS=ms41624661",
            "MS=ms60989570",
            "MS=ms69824556",
            "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
            "oneuptime=2fYJpBXRQsmY3Py",
            "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
            "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13"
          ],
          "mx": [
            "1 aspmx.l.google.com",
            "5 alt1.aspmx.l.google.com",
            "5 alt2.aspmx.l.google.com",
            "10 alt3.aspmx.l.google.com",
            "10 alt4.aspmx.l.google.com"
          ],
          "caa": [],
          "rr_errors": {
            "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
          }
        }
      },
      "ns_hosts": {
        "lily.ns.cloudflare.com": {
          "a": [
            "108.162.192.130",
            "172.64.32.130",
            "173.245.58.130"
          ],
          "aaaa": [
            "2606:4700:50::adf5:3a82",
            "2803:f800:50::6ca2:c082",
            "2a06:98c1:50::ac40:2082"
          ],
          "ip_attribution": {
            "108.162.192.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (108.162.192.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "108.162.192.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042253-20615932-1f20-4a42-ace1-63e767a569ee",
                      "process_time": 68,
                      "server_id": "app175",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:22:53.763171",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "108.162.192.0/20"
                        ],
                        "resource": "108.162.192.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "108.0.0.0/8",
                          "desc": "ARIN (Status: ALLOCATED)",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 108.162.192.0/20 | US | arin | 2011-10-28",
                    "parts": [
                      "13335",
                      "108.162.192.0/20",
                      "US",
                      "arin",
                      "2011-10-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "data": [
                      {
                        "id": 4224,
                        "org_id": 4715,
                        "name": "Cloudflare",
                        "aka": "",
                        "name_long": "",
                        "website": "https://www.cloudflare.com",
                        "social_media": [
                          {
                            "service": "website",
                            "identifier": "https://www.cloudflare.com"
                          }
                        ],
                        "asn": 13335,
                        "looking_glass": "",
                        "route_server": "",
                        "irr_as_set": "AS13335:AS-CLOUDFLARE",
                        "info_type": "Content",
                        "info_types": [
                          "Content"
                        ],
                        "info_prefixes4": 80000,
                        "info_prefixes6": 30000,
                        "info_traffic": "",
                        "info_ratio": "Mostly Outbound",
                        "info_scope": "Global",
                        "info_unicast": true,
                        "info_multicast": false,
                        "info_ipv6": true,
                        "info_never_via_route_servers": false,
                        "ix_count": 349,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-02T19:21:39Z",
                        "netfac_updated": "2026-04-01T18:35:35Z",
                        "poc_updated": "2025-12-04T21:15:09Z",
                        "policy_url": "https://www.cloudflare.com/peering-policy/",
                        "policy_general": "Open",
                        "policy_locations": "Preferred",
                        "policy_ratio": false,
                        "policy_contracts": "Not Required",
                        "allow_ixp_update": false,
                        "status_dashboard": "https://www.cloudflarestatus.com/",
                        "rir_status": "ok",
                        "rir_status_updated": "2024-06-26T04:47:55Z",
                        "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                        "created": "2011-09-06T19:40:05Z",
                        "updated": "2026-04-02T10:08:34Z",
                        "status": "ok"
                      }
                    ],
                    "meta": {}
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "172.64.32.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (172.64.32.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "172.64.32.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042256-86fffc52-15c9-48d8-9d9e-00588d0c4fdd",
                      "process_time": 70,
                      "server_id": "app185",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:22:56.088177",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "172.64.32.0/20"
                        ],
                        "resource": "172.64.32.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "172.0.0.0/8",
                          "desc": "Administered by ARIN",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 172.64.32.0/24 | US | arin | 2015-02-25",
                    "parts": [
                      "13335",
                      "172.64.32.0/24",
                      "US",
                      "arin",
                      "2015-02-25"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "data": [
                      {
                        "id": 4224,
                        "org_id": 4715,
                        "name": "Cloudflare",
                        "aka": "",
                        "name_long": "",
                        "website": "https://www.cloudflare.com",
                        "social_media": [
                          {
                            "service": "website",
                            "identifier": "https://www.cloudflare.com"
                          }
                        ],
                        "asn": 13335,
                        "looking_glass": "",
                        "route_server": "",
                        "irr_as_set": "AS13335:AS-CLOUDFLARE",
                        "info_type": "Content",
                        "info_types": [
                          "Content"
                        ],
                        "info_prefixes4": 80000,
                        "info_prefixes6": 30000,
                        "info_traffic": "",
                        "info_ratio": "Mostly Outbound",
                        "info_scope": "Global",
                        "info_unicast": true,
                        "info_multicast": false,
                        "info_ipv6": true,
                        "info_never_via_route_servers": false,
                        "ix_count": 349,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-02T19:21:39Z",
                        "netfac_updated": "2026-04-01T18:35:35Z",
                        "poc_updated": "2025-12-04T21:15:09Z",
                        "policy_url": "https://www.cloudflare.com/peering-policy/",
                        "policy_general": "Open",
                        "policy_locations": "Preferred",
                        "policy_ratio": false,
                        "policy_contracts": "Not Required",
                        "allow_ixp_update": false,
                        "status_dashboard": "https://www.cloudflarestatus.com/",
                        "rir_status": "ok",
                        "rir_status_updated": "2024-06-26T04:47:55Z",
                        "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                        "created": "2011-09-06T19:40:05Z",
                        "updated": "2026-04-02T10:08:34Z",
                        "status": "ok"
                      }
                    ],
                    "meta": {}
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "173.245.58.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (173.245.58.0/24)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042258-81cef06f-1822-4e08-9ce9-7845b97db5a6",
                      "process_time": 271,
                      "server_id": "app186",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:22:58.674915",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "173.245.58.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "173.0.0.0/8",
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
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 173.245.58.0/24 | US | arin | 2010-12-28",
                    "parts": [
                      "13335",
                      "173.245.58.0/24",
                      "US",
                      "arin",
                      "2010-12-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "2606:4700:50::adf5:3a82": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "2606:4700::/36"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042301-8fc860a0-4fbe-41b5-862a-c9dfa6cc559b",
                      "process_time": 53,
                      "server_id": "app167",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:01.606998",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "2606:4700::/36"
                        ],
                        "resource": "2606:4700:50::/44",
                        "type": "prefix",
                        "block": {
                          "resource": "2600::/12",
                          "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
                        },
                        "actual_num_related": 1,
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2803:f800:50::6ca2:c082": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042303-998d5cdf-72c6-49c6-b503-1cadd85c30d3",
                      "process_time": 94,
                      "server_id": "app192",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:03.220857",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2803:f800:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2800::/12",
                          "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2a06:98c1:50::ac40:2082": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042304-573f9201-f16e-42e6-9b08-8c5ed12e0328",
                      "process_time": 62,
                      "server_id": "app170",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:04.764940",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2a06:98c1:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2a00::/12",
                          "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            }
          },
          "error": null
        },
        "seth.ns.cloudflare.com": {
          "a": [
            "108.162.193.142",
            "172.64.33.142",
            "173.245.59.142"
          ],
          "aaaa": [
            "2606:4700:58::adf5:3b8e",
            "2803:f800:50::6ca2:c18e",
            "2a06:98c1:50::ac40:218e"
          ],
          "ip_attribution": {
            "108.162.193.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (108.162.193.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "108.162.192.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042306-87dfce9a-c6e3-420f-95ab-486af802ca13",
                      "process_time": 54,
                      "server_id": "app182",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:06.379321",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "108.162.192.0/20"
                        ],
                        "resource": "108.162.193.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "108.0.0.0/8",
                          "desc": "ARIN (Status: ALLOCATED)",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 108.162.193.0/24 | US | arin | 2011-10-28",
                    "parts": [
                      "13335",
                      "108.162.193.0/24",
                      "US",
                      "arin",
                      "2011-10-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "172.64.33.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (172.64.33.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "172.64.32.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042308-67923cb7-2677-4e2b-a933-cc276992f376",
                      "process_time": 47,
                      "server_id": "app162",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:08.286323",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "172.64.32.0/20"
                        ],
                        "resource": "172.64.33.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "172.0.0.0/8",
                          "desc": "Administered by ARIN",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 172.64.32.0/20 | US | arin | 2015-02-25",
                    "parts": [
                      "13335",
                      "172.64.32.0/20",
                      "US",
                      "arin",
                      "2015-02-25"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "173.245.59.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (173.245.59.0/24)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042310-91785296-9bf1-4421-a3b7-211d4602cb3c",
                      "process_time": 83,
                      "server_id": "app197",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:10.149748",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "173.245.59.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "173.0.0.0/8",
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
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 173.245.59.0/24 | US | arin | 2010-12-28",
                    "parts": [
                      "13335",
                      "173.245.59.0/24",
                      "US",
                      "arin",
                      "2010-12-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "2606:4700:58::adf5:3b8e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "2606:4700::/36"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042312-dc10e7d4-610f-4fca-9762-35d38229c641",
                      "process_time": 58,
                      "server_id": "app163",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:12.102644",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "2606:4700::/36"
                        ],
                        "resource": "2606:4700:50::/44",
                        "type": "prefix",
                        "block": {
                          "resource": "2600::/12",
                          "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
                        },
                        "actual_num_related": 1,
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2803:f800:50::6ca2:c18e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042313-4812c7c6-b175-42b8-8bd5-8725126a896d",
                      "process_time": 132,
                      "server_id": "app183",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:13.746248",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2803:f800:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2800::/12",
                          "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2a06:98c1:50::ac40:218e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042315-956527ca-ac7f-4079-b951-e9e760e76cb6",
                      "process_time": 57,
                      "server_id": "app174",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:23:15.288417",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2a06:98c1:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2a00::/12",
                          "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            }
          },
          "error": null
        }
      }
    },
    "web_probes": [
      {
        "url": "https://nordvpn.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/",
        "cdn_headers": {
          "cf-ray": "9ed06c1dabd35c21-SJC",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c1dabd35c21"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/competitor_probe/har/d945f098fbd5bb50.har",
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
        "a": [
          "104.18.42.225",
          "172.64.145.31"
        ],
        "aaaa": [
          "2a06:98c1:3101::6812:2ae1",
          "2a06:98c1:3107::ac40:911f"
        ],
        "https_status": 200,
        "https_cdn_headers": {
          "cf-ray": "9ed06c211fd6ed3f-SJC",
          "server": "cloudflare"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "185.187.168.64",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "185.187.168.64"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 185.187.168.64 (185.187.168.64), 15 hops max, 40 byte packets\n",
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
    "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.187.168.64\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tCalifornia\nCity\tSan Francisco\nISP\tDatacamp Limited\nOrganization\tPackethub S.A\nNetwork\tAS212238 Datacamp Limited (VPN, VPSH, TOR, ANYCAST, CONTENT)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Los_Angeles (PDT)\nLocal Time\tWed, 15 Apr 2026 21:22:28 -0700\nCoordinates\t37.7749,-122.4190\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.187.168.64\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t16 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\tebdd936b147224d67cc5b780b065eb27\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.187.168.0 - 185.187.168.255\nCIDR\t185.187.168.0/24\nName\tPACKETHUB-20221011\nHandle\t185.187.168.0 - 185.187.168.255\nParent Handle\t185.187.168.0 - 185.187.171.255\nNet Type\tASSIGNED PA\nCountry\tUnited States\nRegistration\tTue, 11 Oct 2022 14:07:42 GMT\nLast Changed\tTue, 11 Oct 2022 14:07:42 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.187.168.64\nISP\tDatacamp Limited\nLocation\tUnited States, San Francisco\nDNS Leak Test\nTest Results\tFound 14 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.187.168.62\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.63\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.64\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.65\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.66\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.67\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.68\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.69\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.70\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.71\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.72\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.73\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.74\tDatacamp Limited\tUnited States, San Francisco\n185.187.168.75\tDatacamp Limited\tUnited States, San Francisco\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.187.168.64\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.187.168.64\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (217)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_3fa8765f5a30\nJA3\t78a2c67d9da712ff1e543c7843ddf7f1\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x1A1A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x5A5A\nGREASE\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x000A\nsupported_groups\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0000\nserver_name\n\n\n0x000B\nec_point_formats\n\n\n0x002B\nsupported_versions\n\n\n0x0023\nsession_ticket\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x001B\ncompress_certificate\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x0017\nextended_main_secret\n\n\n0x0033\nkey_share\n\n\n0x000D\nsignature_algorithms\n\n\n0xFF01\nrenegotiation_info\n\n\n0x44CD\napplication_settings\n\n\n0x0005\nstatus_request\n\n\n0x6A6A\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t217\nenc_length\t32\npayload_length\t144\nkey_share\nclient_shares\t\n0x6A6A\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brow",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-33b378c6",
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
        "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
        "answer_summary": "Exit IPv4 185.187.168.64; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 185.187.168.64.",
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
        "answer_summary": "Exit IPv4 185.187.168.64 for location us-california-san-francisco-64.",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 64.168.187.185.in-addr.arpa.",
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
        "answer_summary": "Fingerprint snapshot present.",
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
        "Competitor web/portal probes executed.",
        "Large services_contacted list."
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
        "host": "attribution",
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
        "host": "fingerprint",
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
        "host": "nordcheckout.com",
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
      "ip": "185.187.168.64",
      "country_code": "US",
      "region": "California",
      "city": "San Francisco",
      "connection": {
        "asn": 212238,
        "org": "Packethub S.A.",
        "isp": "Datacamp Limited",
        "domain": "packethub.net"
      },
      "location_id": "us-california-san-francisco-64",
      "location_label": "San Francisco, California, United States"
    },
    "surface_probe": {
      "probes": [
        {
          "url": "https://nordvpn.com/pricing/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing/",
          "cdn_headers": {
            "cf-ray": "9ed06c276fc5f9f1-SJC",
            "server": "cloudflare"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c276fc5f9f1"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/3cec43152ba057c5.har",
          "page_type": "pricing"
        },
        {
          "url": "https://my.nordaccount.com/",
          "error": null,
          "status": 200,
          "final_url": "https://my.nordaccount.com/",
          "cdn_headers": {
            "cf-ray": "9ed06c2a083667b5-SJC",
            "server": "cloudflare"
          },
          "scripts": [
            "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
            "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
            "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
            "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
            "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
            "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
            "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
            "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
            "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
            "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
            "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
            "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
            "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
            "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
            "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
            "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
            "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
            "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
            "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
            "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
            "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
            "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
            "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
            "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
            "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
            "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
            "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
            "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
            "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
            "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
            "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
            "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
            "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
            "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
            "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
            "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
            "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
            "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
            "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
            "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
            "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
            "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
            "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
            "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
            "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
            "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
            "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
            "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
            "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
            "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
            "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
            "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
            "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
            "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
            "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
            "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/0096221d6f12d382.har",
          "page_type": "signup"
        },
        {
          "url": "https://nordcheckout.com/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
          "cdn_headers": {
            "cf-ray": "9ed06c377e63235b-SJC",
            "server": "cloudflare"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed06c377e63235b"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe/har/5c4416295d131e0b.har",
          "page_type": "checkout"
        }
      ],
      "surface_probe_dir": "runs/nordvpn-20260416T042117Z-7bbf2d88/raw/us-california-san-francisco-64/surface_probe"
    }
  }
}
```

---



### nordvpn-20260416T042749Z-00a43d39 / us-new-mexico-albuquerque-105



- **vpn_provider:** nordvpn
- **Label:** Albuquerque, New Mexico, United States
- **Path:** `runs/nordvpn-20260416T042749Z-00a43d39/locations/us-new-mexico-albuquerque-105/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-16T04:31:17.869704+00:00
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
| exit_ip_v4 | 66.179.156.105 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "66.179.156.105",
    "ipv6": null,
    "raw_excerpt": "66.179.156.105",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "66.179.156.105",
    "ipv6": null,
    "raw_excerpt": "66.179.156.105",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "66.179.156.105",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"66.179.156.105\"}",
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
      "66.179.156.104"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "66.179.156.105"
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
| host | udp | 06eee100-5210-423f-a4f0-2880ec116d15.local | 61767 | `candidate:213344460 1 udp 2113937151 06eee100-5210-423f-a4f0-2880ec116d15.local 61767 typ host generation 0 ufrag IQ13 network-cost 999` |
| srflx | udp | 66.179.156.105 | 35248 | `candidate:422987468 1 udp 1677729535 66.179.156.105 35248 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag IQ13 network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


```json
{
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
  "language": "en-US",
  "hardwareConcurrency": 16,
  "platform": "MacIntel"
}
```


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
          "query_id": "20260416042808-7d30177b-ee07-4ab8-90a3-cc2166729cfc",
          "process_time": 57,
          "server_id": "app195",
          "build_version": "v0.9.7-2026.04.09",
          "pipeline": "1221926",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-16T04:28:08.330841",
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
      "asn": 136787,
      "holder": null,
      "country": null,
      "raw": {
        "asn": 136787,
        "raw_line": "136787 | 66.179.156.0/24 | US | ripencc | 2001-10-09",
        "parts": [
          "136787",
          "66.179.156.0/24",
          "US",
          "ripencc",
          "2001-10-09"
        ],
        "disclaimer": [
          "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
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
    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
  ]
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:28:50.693189+00:00",
    "sha256": "6841c9a4a380c7ab8bec73b40f407d16485c0f8e1c76b681fdaa5c034e8b353d",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  },
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:28:54.031085+00:00",
    "sha256": "df36bf08c766f682b0b6e2653507445d372c63e638c42327d2914af5bfc236df",
    "summary_bullets": [
      "Mentions retention (keyword hit; review source)",
      "Mentions logging (keyword hit; review source)",
      "Mentions law enforcement (keyword hit; review source)",
      "Mentions third parties (keyword hit; review source)",
      "Mentions telemetry (keyword hit; review source)"
    ]
  }
]
```

#### Services contacted




- `attribution:ns_glue:108.162.192.130`

- `attribution:ns_glue:108.162.193.142`

- `attribution:ns_glue:172.64.32.130`

- `attribution:ns_glue:172.64.33.142`

- `attribution:ns_glue:173.245.58.130`

- `attribution:ns_glue:173.245.59.142`

- `attribution:ns_glue:2606:4700:50::adf5:3a82`

- `attribution:ns_glue:2606:4700:58::adf5:3b8e`

- `attribution:ns_glue:2803:f800:50::6ca2:c082`

- `attribution:ns_glue:2803:f800:50::6ca2:c18e`

- `attribution:ns_glue:2a06:98c1:50::ac40:2082`

- `attribution:ns_glue:2a06:98c1:50::ac40:218e`

- `browserleaks.com:playwright_chromium`

- `competitor_probe:enabled`

- `competitor_probe:har_summary`

- `dns:lookup:nordvpn.com`

- `dns:ns_glue:lily.ns.cloudflare.com`

- `dns:ns_glue:seth.ns.cloudflare.com`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/66.179.156.105`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordcheckout.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/pricing/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260416T042749Z-00a43d39/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/webrtc",
  "ipv6_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/fingerprint",
  "attribution_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/policy",
  "competitor_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe",
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
  "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-0f985c14",
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
      "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
      "answer_summary": "Exit IPv4 66.179.156.105; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 66.179.156.105.",
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
      "answer_summary": "Exit IPv4 66.179.156.105 for location us-new-mexico-albuquerque-105.",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 105.156.179.66.in-addr.arpa.",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Albuquerque, New Mexico, United States').",
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
      "answer_summary": "Fingerprint snapshot present.",
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
      "Competitor web/portal probes executed.",
      "Large services_contacted list."
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
      "host": "attribution",
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
      "host": "fingerprint",
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
      "host": "nordcheckout.com",
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
        "ns": [
          "lily.ns.cloudflare.com",
          "seth.ns.cloudflare.com"
        ],
        "a": [
          "104.16.208.203",
          "104.19.159.190"
        ],
        "aaaa": [],
        "error": null,
        "txt": [
          "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
          "MS=ms41624661",
          "MS=ms60989570",
          "MS=ms69824556",
          "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
          "oneuptime=2fYJpBXRQsmY3Py",
          "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all"
        ],
        "mx": [
          "1 aspmx.l.google.com",
          "5 alt1.aspmx.l.google.com",
          "5 alt2.aspmx.l.google.com",
          "10 alt3.aspmx.l.google.com",
          "10 alt4.aspmx.l.google.com"
        ],
        "caa": [],
        "rr_errors": {
          "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
        }
      }
    },
    "ns_hosts": {
      "lily.ns.cloudflare.com": {
        "a": [
          "108.162.192.130",
          "172.64.32.130",
          "173.245.58.130"
        ],
        "aaaa": [
          "2606:4700:50::adf5:3a82",
          "2803:f800:50::6ca2:c082",
          "2a06:98c1:50::ac40:2082"
        ],
        "ip_attribution": {
          "108.162.192.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (108.162.192.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "108.162.192.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042924-9764c17c-c253-4acb-9e8b-05760426c138",
                    "process_time": 70,
                    "server_id": "app187",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:25.059978",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "108.162.192.0/20"
                      ],
                      "resource": "108.162.192.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "108.0.0.0/8",
                        "desc": "ARIN (Status: ALLOCATED)",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 108.162.192.0/24 | US | arin | 2011-10-28",
                  "parts": [
                    "13335",
                    "108.162.192.0/24",
                    "US",
                    "arin",
                    "2011-10-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "data": [
                    {
                      "id": 4224,
                      "org_id": 4715,
                      "name": "Cloudflare",
                      "aka": "",
                      "name_long": "",
                      "website": "https://www.cloudflare.com",
                      "social_media": [
                        {
                          "service": "website",
                          "identifier": "https://www.cloudflare.com"
                        }
                      ],
                      "asn": 13335,
                      "looking_glass": "",
                      "route_server": "",
                      "irr_as_set": "AS13335:AS-CLOUDFLARE",
                      "info_type": "Content",
                      "info_types": [
                        "Content"
                      ],
                      "info_prefixes4": 80000,
                      "info_prefixes6": 30000,
                      "info_traffic": "",
                      "info_ratio": "Mostly Outbound",
                      "info_scope": "Global",
                      "info_unicast": true,
                      "info_multicast": false,
                      "info_ipv6": true,
                      "info_never_via_route_servers": false,
                      "ix_count": 349,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-02T19:21:39Z",
                      "netfac_updated": "2026-04-01T18:35:35Z",
                      "poc_updated": "2025-12-04T21:15:09Z",
                      "policy_url": "https://www.cloudflare.com/peering-policy/",
                      "policy_general": "Open",
                      "policy_locations": "Preferred",
                      "policy_ratio": false,
                      "policy_contracts": "Not Required",
                      "allow_ixp_update": false,
                      "status_dashboard": "https://www.cloudflarestatus.com/",
                      "rir_status": "ok",
                      "rir_status_updated": "2024-06-26T04:47:55Z",
                      "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                      "created": "2011-09-06T19:40:05Z",
                      "updated": "2026-04-02T10:08:34Z",
                      "status": "ok"
                    }
                  ],
                  "meta": {}
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "172.64.32.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (172.64.32.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "172.64.32.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042926-2fa8ea5d-8fb2-443c-ae0c-1ca62eb9929c",
                    "process_time": 72,
                    "server_id": "app187",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:27.016901",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "172.64.32.0/20"
                      ],
                      "resource": "172.64.32.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "172.0.0.0/8",
                        "desc": "Administered by ARIN",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 172.64.32.0/20 | US | arin | 2015-02-25",
                  "parts": [
                    "13335",
                    "172.64.32.0/20",
                    "US",
                    "arin",
                    "2015-02-25"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "data": [
                    {
                      "id": 4224,
                      "org_id": 4715,
                      "name": "Cloudflare",
                      "aka": "",
                      "name_long": "",
                      "website": "https://www.cloudflare.com",
                      "social_media": [
                        {
                          "service": "website",
                          "identifier": "https://www.cloudflare.com"
                        }
                      ],
                      "asn": 13335,
                      "looking_glass": "",
                      "route_server": "",
                      "irr_as_set": "AS13335:AS-CLOUDFLARE",
                      "info_type": "Content",
                      "info_types": [
                        "Content"
                      ],
                      "info_prefixes4": 80000,
                      "info_prefixes6": 30000,
                      "info_traffic": "",
                      "info_ratio": "Mostly Outbound",
                      "info_scope": "Global",
                      "info_unicast": true,
                      "info_multicast": false,
                      "info_ipv6": true,
                      "info_never_via_route_servers": false,
                      "ix_count": 349,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-02T19:21:39Z",
                      "netfac_updated": "2026-04-01T18:35:35Z",
                      "poc_updated": "2025-12-04T21:15:09Z",
                      "policy_url": "https://www.cloudflare.com/peering-policy/",
                      "policy_general": "Open",
                      "policy_locations": "Preferred",
                      "policy_ratio": false,
                      "policy_contracts": "Not Required",
                      "allow_ixp_update": false,
                      "status_dashboard": "https://www.cloudflarestatus.com/",
                      "rir_status": "ok",
                      "rir_status_updated": "2024-06-26T04:47:55Z",
                      "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                      "created": "2011-09-06T19:40:05Z",
                      "updated": "2026-04-02T10:08:34Z",
                      "status": "ok"
                    }
                  ],
                  "meta": {}
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "173.245.58.130": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (173.245.58.0/24)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042928-29199f4d-86d5-435a-94d2-5dbc6c85ca37",
                    "process_time": 57,
                    "server_id": "app179",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:28.809878",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "173.245.58.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "173.0.0.0/8",
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
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 173.245.58.0/24 | US | arin | 2010-12-28",
                  "parts": [
                    "13335",
                    "173.245.58.0/24",
                    "US",
                    "arin",
                    "2010-12-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "data": [
                    {
                      "id": 4224,
                      "org_id": 4715,
                      "name": "Cloudflare",
                      "aka": "",
                      "name_long": "",
                      "website": "https://www.cloudflare.com",
                      "social_media": [
                        {
                          "service": "website",
                          "identifier": "https://www.cloudflare.com"
                        }
                      ],
                      "asn": 13335,
                      "looking_glass": "",
                      "route_server": "",
                      "irr_as_set": "AS13335:AS-CLOUDFLARE",
                      "info_type": "Content",
                      "info_types": [
                        "Content"
                      ],
                      "info_prefixes4": 80000,
                      "info_prefixes6": 30000,
                      "info_traffic": "",
                      "info_ratio": "Mostly Outbound",
                      "info_scope": "Global",
                      "info_unicast": true,
                      "info_multicast": false,
                      "info_ipv6": true,
                      "info_never_via_route_servers": false,
                      "ix_count": 349,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-02T19:21:39Z",
                      "netfac_updated": "2026-04-01T18:35:35Z",
                      "poc_updated": "2025-12-04T21:15:09Z",
                      "policy_url": "https://www.cloudflare.com/peering-policy/",
                      "policy_general": "Open",
                      "policy_locations": "Preferred",
                      "policy_ratio": false,
                      "policy_contracts": "Not Required",
                      "allow_ixp_update": false,
                      "status_dashboard": "https://www.cloudflarestatus.com/",
                      "rir_status": "ok",
                      "rir_status_updated": "2024-06-26T04:47:55Z",
                      "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                      "created": "2011-09-06T19:40:05Z",
                      "updated": "2026-04-02T10:08:34Z",
                      "status": "ok"
                    }
                  ],
                  "meta": {}
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "2606:4700:50::adf5:3a82": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "2606:4700::/36"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042930-2505e0a2-954a-4e83-812a-e5bf0a13a68c",
                    "process_time": 69,
                    "server_id": "app172",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:30.675156",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "2606:4700::/36"
                      ],
                      "resource": "2606:4700:50::/44",
                      "type": "prefix",
                      "block": {
                        "resource": "2600::/12",
                        "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
                      },
                      "actual_num_related": 1,
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2803:f800:50::6ca2:c082": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042932-ebb91d78-4cf7-4627-954a-6e4cc54751c2",
                    "process_time": 45,
                    "server_id": "app166",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:32.052577",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2803:f800:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2800::/12",
                        "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2a06:98c1:50::ac40:2082": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042933-17da36eb-f550-42cb-b3c6-016ce821417f",
                    "process_time": 153,
                    "server_id": "app193",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:33.418283",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2a06:98c1:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2a00::/12",
                        "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          }
        },
        "error": null
      },
      "seth.ns.cloudflare.com": {
        "a": [
          "108.162.193.142",
          "172.64.33.142",
          "173.245.59.142"
        ],
        "aaaa": [
          "2606:4700:58::adf5:3b8e",
          "2803:f800:50::6ca2:c18e",
          "2a06:98c1:50::ac40:218e"
        ],
        "ip_attribution": {
          "108.162.193.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (108.162.193.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "108.162.192.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042934-9537a114-eb4f-4c86-9b28-aaf8794d2eaf",
                    "process_time": 66,
                    "server_id": "app161",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:34.853471",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "108.162.192.0/20"
                      ],
                      "resource": "108.162.193.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "108.0.0.0/8",
                        "desc": "ARIN (Status: ALLOCATED)",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 108.162.192.0/20 | US | arin | 2011-10-28",
                  "parts": [
                    "13335",
                    "108.162.192.0/20",
                    "US",
                    "arin",
                    "2011-10-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "172.64.33.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (172.64.33.0/24)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "172.64.32.0/20"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042937-8b518339-1ab8-43f7-a6b0-72f7611f60a1",
                    "process_time": 53,
                    "server_id": "app181",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:37.855490",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "172.64.32.0/20"
                      ],
                      "resource": "172.64.33.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "172.0.0.0/8",
                        "desc": "Administered by ARIN",
                        "name": "IANA IPv4 Address Space Registry"
                      },
                      "actual_num_related": 1,
                      "query_time": "2026-04-15T16:00:00",
                      "num_filtered_out": 0
                    }
                  }
                }
              },
              {
                "name": "team_cymru",
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 172.64.33.0/24 | US | arin | 2015-02-25",
                  "parts": [
                    "13335",
                    "172.64.33.0/24",
                    "US",
                    "arin",
                    "2015-02-25"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "173.245.59.142": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (173.245.59.0/24)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042939-b0848c02-abce-4e52-8bc2-52012eadcd68",
                    "process_time": 71,
                    "server_id": "app185",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:39.581488",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "173.245.59.0/24",
                      "type": "prefix",
                      "block": {
                        "resource": "173.0.0.0/8",
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
                "asn": 13335,
                "holder": null,
                "country": null,
                "raw": {
                  "asn": 13335,
                  "raw_line": "13335 | 173.245.59.0/24 | US | arin | 2010-12-28",
                  "parts": [
                    "13335",
                    "173.245.59.0/24",
                    "US",
                    "arin",
                    "2010-12-28"
                  ],
                  "disclaimer": [
                    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                  ]
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
              "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
            ]
          },
          "2606:4700:58::adf5:3b8e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                      ]
                    ],
                    "see_also": [
                      {
                        "relation": "less-specific",
                        "resource": "2606:4700::/36"
                      }
                    ],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042941-11ce0167-9624-4e46-a02b-9b6f3dd613df",
                    "process_time": 96,
                    "server_id": "app180",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:41.178890",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [
                        "2606:4700::/36"
                      ],
                      "resource": "2606:4700:50::/44",
                      "type": "prefix",
                      "block": {
                        "resource": "2600::/12",
                        "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
                      },
                      "actual_num_related": 1,
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2803:f800:50::6ca2:c18e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042942-f24c8108-d96f-469d-bfa6-feb06b6adb2e",
                    "process_time": 54,
                    "server_id": "app168",
                    "build_version": "v0.9.7-thriftpy2-2026.04.10",
                    "pipeline": "1223136",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:42.721423",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2803:f800:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2800::/12",
                        "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          },
          "2a06:98c1:50::ac40:218e": {
            "asn": 13335,
            "holder": "CLOUDFLARENET - Cloudflare",
            "country": null,
            "confidence": 0.7,
            "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
            "supporting_sources": [
              {
                "name": "ripestat",
                "asn": 13335,
                "holder": "CLOUDFLARENET - Cloudflare",
                "country": null,
                "raw": {
                  "prefix_overview": {
                    "messages": [
                      [
                        "warning",
                        "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                      ]
                    ],
                    "see_also": [],
                    "version": "1.3",
                    "data_call_name": "prefix-overview",
                    "data_call_status": "supported",
                    "cached": false,
                    "query_id": "20260416042943-bfd93e17-8525-46b5-876f-4cdbabd0657d",
                    "process_time": 137,
                    "server_id": "app185",
                    "build_version": "v0.9.7-2026.04.09",
                    "pipeline": "1221926",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-16T04:29:44.101463",
                    "data": {
                      "is_less_specific": true,
                      "announced": true,
                      "asns": [
                        {
                          "asn": 13335,
                          "holder": "CLOUDFLARENET - Cloudflare"
                        }
                      ],
                      "related_prefixes": [],
                      "resource": "2a06:98c1:50::/45",
                      "type": "prefix",
                      "block": {
                        "resource": "2a00::/12",
                        "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                        "name": "IANA IPv6 Global Unicast Address Assignments"
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
                  "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                }
              },
              {
                "name": "peeringdb",
                "asn": null,
                "holder": null,
                "country": null,
                "raw": {
                  "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                }
              }
            ],
            "disclaimers": [
              "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
            ]
          }
        },
        "error": null
      }
    }
  },
  "web_probes": [
    {
      "url": "https://nordvpn.com/",
      "error": null,
      "status": 403,
      "final_url": "https://nordvpn.com/",
      "cdn_headers": {
        "cf-ray": "9ed0759868df33f3-PHX",
        "server": "cloudflare"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0759868df33f3"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe/har/d945f098fbd5bb50.har",
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
      "a": [
        "104.18.42.225",
        "172.64.145.31"
      ],
      "aaaa": [
        "2a06:98c1:3101::6812:2ae1",
        "2a06:98c1:3107::ac40:911f"
      ],
      "https_status": 200,
      "https_cdn_headers": {
        "cf-ray": "9ed0759a9fe87244-PHX",
        "server": "cloudflare"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "66.179.156.105",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "66.179.156.105"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 66.179.156.105 (66.179.156.105), 15 hops max, 40 byte packets\n",
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
    "ip": "66.179.156.105",
    "country_code": "US",
    "region": "New Mexico",
    "city": "Albuquerque",
    "connection": {
      "asn": 136787,
      "org": "Core Ip Solutions LLC",
      "isp": "Packethub S.A.",
      "domain": "packethub.net"
    },
    "location_id": "us-new-mexico-albuquerque-105",
    "location_label": "Albuquerque, New Mexico, United States"
  },
  "surface_probe": {
    "probes": [
      {
        "url": "https://nordvpn.com/pricing/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing/",
        "cdn_headers": {
          "cf-ray": "9ed0759f9a839869-PHX",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0759f9a839869"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/3cec43152ba057c5.har",
        "page_type": "pricing"
      },
      {
        "url": "https://my.nordaccount.com/",
        "error": null,
        "status": 200,
        "final_url": "https://my.nordaccount.com/",
        "cdn_headers": {
          "cf-ray": "9ed075a11dcc9d47-PHX",
          "server": "cloudflare"
        },
        "scripts": [
          "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
          "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
          "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
          "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
          "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
          "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
          "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
          "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
          "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
          "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
          "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
          "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
          "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
          "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
          "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
          "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
          "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
          "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
          "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
          "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
          "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
          "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
          "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
          "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
          "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
          "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
          "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
          "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
          "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
          "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
          "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
          "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
          "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
          "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
          "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
          "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
          "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
          "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
          "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
          "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
          "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
          "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
          "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
          "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
          "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
          "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
          "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
          "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
          "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
          "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
          "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
          "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
          "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
          "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
          "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
          "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/0096221d6f12d382.har",
        "page_type": "signup"
      },
      {
        "url": "https://nordcheckout.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
        "cdn_headers": {
          "cf-ray": "9ed075aa5862f4de-PHX",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed075aa5862f4de"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/5c4416295d131e0b.har",
        "page_type": "checkout"
      }
    ],
    "surface_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260416T042749Z-00a43d39",
  "timestamp_utc": "2026-04-16T04:31:17.869704+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-new-mexico-albuquerque-105",
  "vpn_location_label": "Albuquerque, New Mexico, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "66.179.156.105",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "66.179.156.105",
      "ipv6": null,
      "raw_excerpt": "66.179.156.105",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "66.179.156.105",
      "ipv6": null,
      "raw_excerpt": "66.179.156.105",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "66.179.156.105",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"66.179.156.105\"}",
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
        "66.179.156.104"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "66.179.156.105"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "06eee100-5210-423f-a4f0-2880ec116d15.local",
      "port": 61767,
      "raw": "candidate:213344460 1 udp 2113937151 06eee100-5210-423f-a4f0-2880ec116d15.local 61767 typ host generation 0 ufrag IQ13 network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "66.179.156.105",
      "port": 35248,
      "raw": "candidate:422987468 1 udp 1677729535 66.179.156.105 35248 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag IQ13 network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
    "language": "en-US",
    "hardwareConcurrency": 16,
    "platform": "MacIntel"
  },
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
            "query_id": "20260416042808-7d30177b-ee07-4ab8-90a3-cc2166729cfc",
            "process_time": 57,
            "server_id": "app195",
            "build_version": "v0.9.7-2026.04.09",
            "pipeline": "1221926",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-16T04:28:08.330841",
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
        "asn": 136787,
        "holder": null,
        "country": null,
        "raw": {
          "asn": 136787,
          "raw_line": "136787 | 66.179.156.0/24 | US | ripencc | 2001-10-09",
          "parts": [
            "136787",
            "66.179.156.0/24",
            "US",
            "ripencc",
            "2001-10-09"
          ],
          "disclaimer": [
            "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
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
      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
    ]
  },
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:28:50.693189+00:00",
      "sha256": "6841c9a4a380c7ab8bec73b40f407d16485c0f8e1c76b681fdaa5c034e8b353d",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    },
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:28:54.031085+00:00",
      "sha256": "df36bf08c766f682b0b6e2653507445d372c63e638c42327d2914af5bfc236df",
      "summary_bullets": [
        "Mentions retention (keyword hit; review source)",
        "Mentions logging (keyword hit; review source)",
        "Mentions law enforcement (keyword hit; review source)",
        "Mentions third parties (keyword hit; review source)",
        "Mentions telemetry (keyword hit; review source)"
      ]
    }
  ],
  "services_contacted": [
    "attribution:ns_glue:108.162.192.130",
    "attribution:ns_glue:108.162.193.142",
    "attribution:ns_glue:172.64.32.130",
    "attribution:ns_glue:172.64.33.142",
    "attribution:ns_glue:173.245.58.130",
    "attribution:ns_glue:173.245.59.142",
    "attribution:ns_glue:2606:4700:50::adf5:3a82",
    "attribution:ns_glue:2606:4700:58::adf5:3b8e",
    "attribution:ns_glue:2803:f800:50::6ca2:c082",
    "attribution:ns_glue:2803:f800:50::6ca2:c18e",
    "attribution:ns_glue:2a06:98c1:50::ac40:2082",
    "attribution:ns_glue:2a06:98c1:50::ac40:218e",
    "browserleaks.com:playwright_chromium",
    "competitor_probe:enabled",
    "competitor_probe:har_summary",
    "dns:lookup:nordvpn.com",
    "dns:ns_glue:lily.ns.cloudflare.com",
    "dns:ns_glue:seth.ns.cloudflare.com",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/66.179.156.105",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordcheckout.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/pricing/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260416T042749Z-00a43d39/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/webrtc",
    "ipv6_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/fingerprint",
    "attribution_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/policy",
    "competitor_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe",
    "transitions_json": null
  },
  "competitor_surface": {
    "provider_dns": {
      "domains": {
        "nordvpn.com": {
          "ns": [
            "lily.ns.cloudflare.com",
            "seth.ns.cloudflare.com"
          ],
          "a": [
            "104.16.208.203",
            "104.19.159.190"
          ],
          "aaaa": [],
          "error": null,
          "txt": [
            "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
            "MS=ms41624661",
            "MS=ms60989570",
            "MS=ms69824556",
            "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
            "oneuptime=2fYJpBXRQsmY3Py",
            "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all"
          ],
          "mx": [
            "1 aspmx.l.google.com",
            "5 alt1.aspmx.l.google.com",
            "5 alt2.aspmx.l.google.com",
            "10 alt3.aspmx.l.google.com",
            "10 alt4.aspmx.l.google.com"
          ],
          "caa": [],
          "rr_errors": {
            "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
          }
        }
      },
      "ns_hosts": {
        "lily.ns.cloudflare.com": {
          "a": [
            "108.162.192.130",
            "172.64.32.130",
            "173.245.58.130"
          ],
          "aaaa": [
            "2606:4700:50::adf5:3a82",
            "2803:f800:50::6ca2:c082",
            "2a06:98c1:50::ac40:2082"
          ],
          "ip_attribution": {
            "108.162.192.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (108.162.192.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "108.162.192.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042924-9764c17c-c253-4acb-9e8b-05760426c138",
                      "process_time": 70,
                      "server_id": "app187",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:25.059978",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "108.162.192.0/20"
                        ],
                        "resource": "108.162.192.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "108.0.0.0/8",
                          "desc": "ARIN (Status: ALLOCATED)",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 108.162.192.0/24 | US | arin | 2011-10-28",
                    "parts": [
                      "13335",
                      "108.162.192.0/24",
                      "US",
                      "arin",
                      "2011-10-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "data": [
                      {
                        "id": 4224,
                        "org_id": 4715,
                        "name": "Cloudflare",
                        "aka": "",
                        "name_long": "",
                        "website": "https://www.cloudflare.com",
                        "social_media": [
                          {
                            "service": "website",
                            "identifier": "https://www.cloudflare.com"
                          }
                        ],
                        "asn": 13335,
                        "looking_glass": "",
                        "route_server": "",
                        "irr_as_set": "AS13335:AS-CLOUDFLARE",
                        "info_type": "Content",
                        "info_types": [
                          "Content"
                        ],
                        "info_prefixes4": 80000,
                        "info_prefixes6": 30000,
                        "info_traffic": "",
                        "info_ratio": "Mostly Outbound",
                        "info_scope": "Global",
                        "info_unicast": true,
                        "info_multicast": false,
                        "info_ipv6": true,
                        "info_never_via_route_servers": false,
                        "ix_count": 349,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-02T19:21:39Z",
                        "netfac_updated": "2026-04-01T18:35:35Z",
                        "poc_updated": "2025-12-04T21:15:09Z",
                        "policy_url": "https://www.cloudflare.com/peering-policy/",
                        "policy_general": "Open",
                        "policy_locations": "Preferred",
                        "policy_ratio": false,
                        "policy_contracts": "Not Required",
                        "allow_ixp_update": false,
                        "status_dashboard": "https://www.cloudflarestatus.com/",
                        "rir_status": "ok",
                        "rir_status_updated": "2024-06-26T04:47:55Z",
                        "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                        "created": "2011-09-06T19:40:05Z",
                        "updated": "2026-04-02T10:08:34Z",
                        "status": "ok"
                      }
                    ],
                    "meta": {}
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "172.64.32.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (172.64.32.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "172.64.32.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042926-2fa8ea5d-8fb2-443c-ae0c-1ca62eb9929c",
                      "process_time": 72,
                      "server_id": "app187",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:27.016901",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "172.64.32.0/20"
                        ],
                        "resource": "172.64.32.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "172.0.0.0/8",
                          "desc": "Administered by ARIN",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 172.64.32.0/20 | US | arin | 2015-02-25",
                    "parts": [
                      "13335",
                      "172.64.32.0/20",
                      "US",
                      "arin",
                      "2015-02-25"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "data": [
                      {
                        "id": 4224,
                        "org_id": 4715,
                        "name": "Cloudflare",
                        "aka": "",
                        "name_long": "",
                        "website": "https://www.cloudflare.com",
                        "social_media": [
                          {
                            "service": "website",
                            "identifier": "https://www.cloudflare.com"
                          }
                        ],
                        "asn": 13335,
                        "looking_glass": "",
                        "route_server": "",
                        "irr_as_set": "AS13335:AS-CLOUDFLARE",
                        "info_type": "Content",
                        "info_types": [
                          "Content"
                        ],
                        "info_prefixes4": 80000,
                        "info_prefixes6": 30000,
                        "info_traffic": "",
                        "info_ratio": "Mostly Outbound",
                        "info_scope": "Global",
                        "info_unicast": true,
                        "info_multicast": false,
                        "info_ipv6": true,
                        "info_never_via_route_servers": false,
                        "ix_count": 349,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-02T19:21:39Z",
                        "netfac_updated": "2026-04-01T18:35:35Z",
                        "poc_updated": "2025-12-04T21:15:09Z",
                        "policy_url": "https://www.cloudflare.com/peering-policy/",
                        "policy_general": "Open",
                        "policy_locations": "Preferred",
                        "policy_ratio": false,
                        "policy_contracts": "Not Required",
                        "allow_ixp_update": false,
                        "status_dashboard": "https://www.cloudflarestatus.com/",
                        "rir_status": "ok",
                        "rir_status_updated": "2024-06-26T04:47:55Z",
                        "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                        "created": "2011-09-06T19:40:05Z",
                        "updated": "2026-04-02T10:08:34Z",
                        "status": "ok"
                      }
                    ],
                    "meta": {}
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "173.245.58.130": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (173.245.58.0/24)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042928-29199f4d-86d5-435a-94d2-5dbc6c85ca37",
                      "process_time": 57,
                      "server_id": "app179",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:28.809878",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "173.245.58.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "173.0.0.0/8",
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
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 173.245.58.0/24 | US | arin | 2010-12-28",
                    "parts": [
                      "13335",
                      "173.245.58.0/24",
                      "US",
                      "arin",
                      "2010-12-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "data": [
                      {
                        "id": 4224,
                        "org_id": 4715,
                        "name": "Cloudflare",
                        "aka": "",
                        "name_long": "",
                        "website": "https://www.cloudflare.com",
                        "social_media": [
                          {
                            "service": "website",
                            "identifier": "https://www.cloudflare.com"
                          }
                        ],
                        "asn": 13335,
                        "looking_glass": "",
                        "route_server": "",
                        "irr_as_set": "AS13335:AS-CLOUDFLARE",
                        "info_type": "Content",
                        "info_types": [
                          "Content"
                        ],
                        "info_prefixes4": 80000,
                        "info_prefixes6": 30000,
                        "info_traffic": "",
                        "info_ratio": "Mostly Outbound",
                        "info_scope": "Global",
                        "info_unicast": true,
                        "info_multicast": false,
                        "info_ipv6": true,
                        "info_never_via_route_servers": false,
                        "ix_count": 349,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-02T19:21:39Z",
                        "netfac_updated": "2026-04-01T18:35:35Z",
                        "poc_updated": "2025-12-04T21:15:09Z",
                        "policy_url": "https://www.cloudflare.com/peering-policy/",
                        "policy_general": "Open",
                        "policy_locations": "Preferred",
                        "policy_ratio": false,
                        "policy_contracts": "Not Required",
                        "allow_ixp_update": false,
                        "status_dashboard": "https://www.cloudflarestatus.com/",
                        "rir_status": "ok",
                        "rir_status_updated": "2024-06-26T04:47:55Z",
                        "logo": "https://peeringdb-media-prod.s3.amazonaws.com/media/logos_user_supplied/network-4224-70070349.png",
                        "created": "2011-09-06T19:40:05Z",
                        "updated": "2026-04-02T10:08:34Z",
                        "status": "ok"
                      }
                    ],
                    "meta": {}
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "2606:4700:50::adf5:3a82": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "2606:4700::/36"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042930-2505e0a2-954a-4e83-812a-e5bf0a13a68c",
                      "process_time": 69,
                      "server_id": "app172",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:30.675156",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "2606:4700::/36"
                        ],
                        "resource": "2606:4700:50::/44",
                        "type": "prefix",
                        "block": {
                          "resource": "2600::/12",
                          "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
                        },
                        "actual_num_related": 1,
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2803:f800:50::6ca2:c082": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042932-ebb91d78-4cf7-4627-954a-6e4cc54751c2",
                      "process_time": 45,
                      "server_id": "app166",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:32.052577",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2803:f800:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2800::/12",
                          "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2a06:98c1:50::ac40:2082": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042933-17da36eb-f550-42cb-b3c6-016ce821417f",
                      "process_time": 153,
                      "server_id": "app193",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:33.418283",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2a06:98c1:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2a00::/12",
                          "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            }
          },
          "error": null
        },
        "seth.ns.cloudflare.com": {
          "a": [
            "108.162.193.142",
            "172.64.33.142",
            "173.245.59.142"
          ],
          "aaaa": [
            "2606:4700:58::adf5:3b8e",
            "2803:f800:50::6ca2:c18e",
            "2a06:98c1:50::ac40:218e"
          ],
          "ip_attribution": {
            "108.162.193.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (108.162.193.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "108.162.192.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042934-9537a114-eb4f-4c86-9b28-aaf8794d2eaf",
                      "process_time": 66,
                      "server_id": "app161",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:34.853471",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "108.162.192.0/20"
                        ],
                        "resource": "108.162.193.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "108.0.0.0/8",
                          "desc": "ARIN (Status: ALLOCATED)",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 108.162.192.0/20 | US | arin | 2011-10-28",
                    "parts": [
                      "13335",
                      "108.162.192.0/20",
                      "US",
                      "arin",
                      "2011-10-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "172.64.33.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (172.64.33.0/24)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "172.64.32.0/20"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042937-8b518339-1ab8-43f7-a6b0-72f7611f60a1",
                      "process_time": 53,
                      "server_id": "app181",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:37.855490",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "172.64.32.0/20"
                        ],
                        "resource": "172.64.33.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "172.0.0.0/8",
                          "desc": "Administered by ARIN",
                          "name": "IANA IPv4 Address Space Registry"
                        },
                        "actual_num_related": 1,
                        "query_time": "2026-04-15T16:00:00",
                        "num_filtered_out": 0
                      }
                    }
                  }
                },
                {
                  "name": "team_cymru",
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 172.64.33.0/24 | US | arin | 2015-02-25",
                    "parts": [
                      "13335",
                      "172.64.33.0/24",
                      "US",
                      "arin",
                      "2015-02-25"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "173.245.59.142": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (173.245.59.0/24)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042939-b0848c02-abce-4e52-8bc2-52012eadcd68",
                      "process_time": 71,
                      "server_id": "app185",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:39.581488",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "173.245.59.0/24",
                        "type": "prefix",
                        "block": {
                          "resource": "173.0.0.0/8",
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
                  "asn": 13335,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "asn": 13335,
                    "raw_line": "13335 | 173.245.59.0/24 | US | arin | 2010-12-28",
                    "parts": [
                      "13335",
                      "173.245.59.0/24",
                      "US",
                      "arin",
                      "2010-12-28"
                    ],
                    "disclaimer": [
                      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
                    ]
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
                "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
              ]
            },
            "2606:4700:58::adf5:3b8e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2606:4700:50::/44)."
                        ]
                      ],
                      "see_also": [
                        {
                          "relation": "less-specific",
                          "resource": "2606:4700::/36"
                        }
                      ],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042941-11ce0167-9624-4e46-a02b-9b6f3dd613df",
                      "process_time": 96,
                      "server_id": "app180",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:41.178890",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [
                          "2606:4700::/36"
                        ],
                        "resource": "2606:4700:50::/44",
                        "type": "prefix",
                        "block": {
                          "resource": "2600::/12",
                          "desc": "Designated to ARIN on 03 October 2006 (Status: allocated; Note: 2600::/22, 2604::/22, 2608::/22 and 260c::/22 were allocated on 2005-04-19. The more recent allocation (2006-10-03) incorporates all these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
                        },
                        "actual_num_related": 1,
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2803:f800:50::6ca2:c18e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2803:f800:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042942-f24c8108-d96f-469d-bfa6-feb06b6adb2e",
                      "process_time": 54,
                      "server_id": "app168",
                      "build_version": "v0.9.7-thriftpy2-2026.04.10",
                      "pipeline": "1223136",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:42.721423",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2803:f800:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2800::/12",
                          "desc": "Designated to LACNIC on 03 October 2006 (Status: allocated; Note: 2800::/23 was allocated on 2005-11-17. The more recent allocation (2006-10-03) incorporates the previous allocation.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            },
            "2a06:98c1:50::ac40:218e": {
              "asn": 13335,
              "holder": "CLOUDFLARENET - Cloudflare",
              "country": null,
              "confidence": 0.7,
              "confidence_notes": "[provider_ns_glue] ASNs seen: [13335]",
              "supporting_sources": [
                {
                  "name": "ripestat",
                  "asn": 13335,
                  "holder": "CLOUDFLARENET - Cloudflare",
                  "country": null,
                  "raw": {
                    "prefix_overview": {
                      "messages": [
                        [
                          "warning",
                          "Given resource is not announced but result has been aligned to first-level less-specific (2a06:98c1:50::/45)."
                        ]
                      ],
                      "see_also": [],
                      "version": "1.3",
                      "data_call_name": "prefix-overview",
                      "data_call_status": "supported",
                      "cached": false,
                      "query_id": "20260416042943-bfd93e17-8525-46b5-876f-4cdbabd0657d",
                      "process_time": 137,
                      "server_id": "app185",
                      "build_version": "v0.9.7-2026.04.09",
                      "pipeline": "1221926",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-16T04:29:44.101463",
                      "data": {
                        "is_less_specific": true,
                        "announced": true,
                        "asns": [
                          {
                            "asn": 13335,
                            "holder": "CLOUDFLARENET - Cloudflare"
                          }
                        ],
                        "related_prefixes": [],
                        "resource": "2a06:98c1:50::/45",
                        "type": "prefix",
                        "block": {
                          "resource": "2a00::/12",
                          "desc": "Designated to RIPE NCC on 03 October 2006 (Status: allocated; Note: 2a00::/21 was originally allocated on 2005-04-19. 2a01::/23 was allocated on 2005-07-14. 2a01::/16 (incorporating the 2a01::/23) was allocated on 2005-12-15. The more recent allocation (2006-10-03) incorporates these previous allocations.)",
                          "name": "IANA IPv6 Global Unicast Address Assignments"
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
                    "note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"
                  }
                },
                {
                  "name": "peeringdb",
                  "asn": null,
                  "holder": null,
                  "country": null,
                  "raw": {
                    "error": "Client error '429 Too Many Requests' for url 'https://www.peeringdb.com/api/net?asn=13335'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429"
                  }
                }
              ],
              "disclaimers": [
                "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
              ]
            }
          },
          "error": null
        }
      }
    },
    "web_probes": [
      {
        "url": "https://nordvpn.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/",
        "cdn_headers": {
          "cf-ray": "9ed0759868df33f3-PHX",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0759868df33f3"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/competitor_probe/har/d945f098fbd5bb50.har",
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
        "a": [
          "104.18.42.225",
          "172.64.145.31"
        ],
        "aaaa": [
          "2a06:98c1:3101::6812:2ae1",
          "2a06:98c1:3107::ac40:911f"
        ],
        "https_status": 200,
        "https_cdn_headers": {
          "cf-ray": "9ed0759a9fe87244-PHX",
          "server": "cloudflare"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "66.179.156.105",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "66.179.156.105"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 66.179.156.105 (66.179.156.105), 15 hops max, 40 byte packets\n",
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
    "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t66.179.156.105\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tNew Mexico\nCity\tAlbuquerque\nISP\tPacketHub S.A.\nOrganization\tCore IP Solutions LLC\nNetwork\tAS136787 PacketHub S.A. (VPN, VPSH, ANYCAST)\nUsage Type\tCorporate / Business\nTimezone\tAmerica/Denver (MDT)\nLocal Time\tWed, 15 Apr 2026 22:29:00 -0600\nCoordinates\t35.0844,-106.6500\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t66.179.156.105\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t12 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t7e684c334c96706d26f7fddbb064918e\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t66.179.156.0 - 66.179.156.255\nCIDR\t66.179.156.0/24\nName\tUS-COREIP4-20011009\nHandle\t66.179.156.0 - 66.179.156.255\nParent Handle\t0.0.0.0 - 255.255.255.255\nNet Type\tALLOCATED PA\nCountry\tUnited States\nRegistration\tWed, 07 Jan 2026 15:25:27 GMT\nLast Changed\tMon, 19 Jan 2026 14:00:35 GMT\nDescription\tPacketHub United States\nFull Name\tNetwork Operations\nHandle\tNO1983-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tPANAMA\nPanama City\n0801\nOffice 76, Plaza 2000, 50th Street and Marbella, Bella Vista\nFull Name\tCore IP Solutions LLC\nHandle\tORG-CISL14-RIPE\nEntity Roles\tRegistrant\nTelephone\t+40733131313\nAddress\t16192 Coastal Highway\n19958\nLewes, Delaware\nUNITED STATES\nFull Name\tRIPE-NCC-HM-MNT\nHandle\tRIPE-NCC-HM-MNT\nEntity Roles\tRegistrant\nOrganization\tORG-NCC1-RIPE\nFull Name\tUs-coreip-1-mnt\nHandle\tUs-coreip-1-mnt\nEntity Roles\tRegistrant\nFull Name\tAbuse-C Role\nHandle\tAR67868-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tPANAMA\nPanama City\n0801\nOffice 76, Plaza 2000, 50th Street and Marbella, Bella Vista\nFull Name\tLir-pa-packethub-1-MNT\nHandle\tLir-pa-packethub-1-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t66.179.156.105\nISP\tPacketHub S.A.\nLocation\tUnited States, Albuquerque\nDNS Leak Test\nTest Results\tFound 9 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n66.179.156.103\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.104\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.105\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.106\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.107\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.108\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.109\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.110\tPacketHub S.A.\tUnited States, Albuquerque\n66.179.156.111\tPacketHub S.A.\tUnited States, Albuquerque\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t66.179.156.105\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t66.179.156.105\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (217)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_0a7410e0ee6e\nJA3\ta4659a4bde92302ba9035f275c5390f4\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x4A4A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0xEAEA\nGREASE\n\n\n0x0005\nstatus_request\n\n\n0x001B\ncompress_certificate\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x000A\nsupported_groups\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x000D\nsignature_algorithms\n\n\n0x0033\nkey_share\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x002B\nsupported_versions\n\n\n0x0017\nextended_main_secret\n\n\n0xFF01\nrenegotiation_info\n\n\n0x0023\nsession_ticket\n\n\n0x44CD\napplication_settings\n\n\n0x000B\nec_point_formats\n\n\n0x0000\nserver_name\n\n\n0xBABA\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t56\nenc_length\t32\npayload_length\t208\nkey_share\nclient_shares\t\n0xCACA\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brows",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-0f985c14",
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
        "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
        "answer_summary": "Exit IPv4 66.179.156.105; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 66.179.156.105.",
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
        "answer_summary": "Exit IPv4 66.179.156.105 for location us-new-mexico-albuquerque-105.",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 105.156.179.66.in-addr.arpa.",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Albuquerque, New Mexico, United States').",
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
        "answer_summary": "Fingerprint snapshot present.",
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
        "Competitor web/portal probes executed.",
        "Large services_contacted list."
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
        "host": "attribution",
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
        "host": "fingerprint",
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
        "host": "nordcheckout.com",
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
      "ip": "66.179.156.105",
      "country_code": "US",
      "region": "New Mexico",
      "city": "Albuquerque",
      "connection": {
        "asn": 136787,
        "org": "Core Ip Solutions LLC",
        "isp": "Packethub S.A.",
        "domain": "packethub.net"
      },
      "location_id": "us-new-mexico-albuquerque-105",
      "location_label": "Albuquerque, New Mexico, United States"
    },
    "surface_probe": {
      "probes": [
        {
          "url": "https://nordvpn.com/pricing/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing/",
          "cdn_headers": {
            "cf-ray": "9ed0759f9a839869-PHX",
            "server": "cloudflare"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0759f9a839869"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/3cec43152ba057c5.har",
          "page_type": "pricing"
        },
        {
          "url": "https://my.nordaccount.com/",
          "error": null,
          "status": 200,
          "final_url": "https://my.nordaccount.com/",
          "cdn_headers": {
            "cf-ray": "9ed075a11dcc9d47-PHX",
            "server": "cloudflare"
          },
          "scripts": [
            "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
            "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
            "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
            "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
            "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
            "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
            "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
            "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
            "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
            "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
            "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
            "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
            "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
            "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
            "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
            "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
            "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
            "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
            "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
            "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
            "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
            "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
            "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
            "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
            "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
            "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
            "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
            "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
            "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
            "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
            "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
            "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
            "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
            "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
            "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
            "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
            "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
            "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
            "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
            "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
            "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
            "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
            "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
            "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
            "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
            "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
            "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
            "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
            "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
            "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
            "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
            "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
            "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
            "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
            "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
            "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/0096221d6f12d382.har",
          "page_type": "signup"
        },
        {
          "url": "https://nordcheckout.com/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
          "cdn_headers": {
            "cf-ray": "9ed075aa5862f4de-PHX",
            "server": "cloudflare"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed075aa5862f4de"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe/har/5c4416295d131e0b.har",
          "page_type": "checkout"
        }
      ],
      "surface_probe_dir": "runs/nordvpn-20260416T042749Z-00a43d39/raw/us-new-mexico-albuquerque-105/surface_probe"
    }
  }
}
```

---



### nordvpn-20260416T044817Z-976afdc6 / de-hamburg-hamburg-238



- **vpn_provider:** nordvpn
- **Label:** Hamburg, Hamburg, Germany
- **Path:** `runs/nordvpn-20260416T044817Z-976afdc6/locations/de-hamburg-hamburg-238/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-16T04:52:29.837578+00:00
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
| exit_ip_v4 | 185.161.202.238 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.161.202.238",
    "ipv6": null,
    "raw_excerpt": "185.161.202.238",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "91.64.142.30",
    "ipv6": null,
    "raw_excerpt": "91.64.142.30",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.161.202.238",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.161.202.238\"}",
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
      "185.161.202.238"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.161.202.238"
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
| host | udp | fad69e4e-b77c-47a4-ba6a-32b581bb0ebe.local | 59395 | `candidate:3823828978 1 udp 2113937151 fad69e4e-b77c-47a4-ba6a-32b581bb0ebe.local 59395 typ host generation 0 ufrag Tjlf network-cost 999` |
| srflx | udp | 185.161.202.238 | 59899 | `candidate:4134263282 1 udp 1677729535 185.161.202.238 59899 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag Tjlf network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


```json
{
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
  "language": "en-US",
  "hardwareConcurrency": 16,
  "platform": "MacIntel"
}
```


#### Attribution

```json
{
  "asn": 207137,
  "holder": "PACKETHUBSA - PacketHub S.A.",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [207137]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 207137,
      "holder": "PACKETHUBSA - PacketHub S.A.",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (185.161.202.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260416044841-3feb9843-b290-4b4e-86b4-9d12e7973082",
          "process_time": 75,
          "server_id": "app172",
          "build_version": "v0.9.7-thriftpy2-2026.04.10",
          "pipeline": "1223136",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-16T04:48:41.590745",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 207137,
                "holder": "PACKETHUBSA - PacketHub S.A."
              }
            ],
            "related_prefixes": [],
            "resource": "185.161.202.0/24",
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
      "asn": 207137,
      "holder": null,
      "country": null,
      "raw": {
        "asn": 207137,
        "raw_line": "207137 | 185.161.202.0/24 | DE | ripencc | 2016-08-02",
        "parts": [
          "207137",
          "185.161.202.0/24",
          "DE",
          "ripencc",
          "2016-08-02"
        ],
        "disclaimer": [
          "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
        ]
      }
    },
    {
      "name": "peeringdb",
      "asn": null,
      "holder": null,
      "country": null,
      "raw": {
        "error": "The read operation timed out"
      }
    }
  ],
  "disclaimers": [
    "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
    "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
  ]
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:49:54.425109+00:00",
    "sha256": "f0b29c2a54d708c2383bbac6ff8c7f27f614890acac0427f698fadd581fe2a53",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  },
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-16T04:50:00.903247+00:00",
    "sha256": "15374e2ce1d4290f76651d23f1a7b23a92f82e30b0fd6b79a170e76cafee8e44",
    "summary_bullets": [
      "Mentions retention (keyword hit; review source)",
      "Mentions logging (keyword hit; review source)",
      "Mentions law enforcement (keyword hit; review source)",
      "Mentions third parties (keyword hit; review source)",
      "Mentions telemetry (keyword hit; review source)"
    ]
  }
]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `competitor_probe:enabled`

- `competitor_probe:har_summary`

- `dns:lookup:nordvpn.com`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/185.161.202.238`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordcheckout.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/pricing/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260416T044817Z-976afdc6/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/webrtc",
  "ipv6_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/fingerprint",
  "attribution_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/policy",
  "competitor_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe",
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
  "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-ad6418b7",
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
      "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
      "answer_summary": "Exit IPv4 185.161.202.238; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.238, 91.64.142.30.",
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
      "answer_summary": "Exit IPv4 185.161.202.238 for location de-hamburg-hamburg-238.",
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
      "answer_summary": "ASN 207137 — PACKETHUBSA - PacketHub S.A.",
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
      "answer_summary": "ASN 207137 — PACKETHUBSA - PacketHub S.A.",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 238.202.161.185.in-addr.arpa.",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Hamburg, Hamburg, Germany').",
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
      "answer_summary": "Fingerprint snapshot present.",
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
      "host": "fingerprint",
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
      "host": "nordcheckout.com",
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
        "a": [
          "104.16.208.203",
          "104.19.159.190"
        ],
        "aaaa": [],
        "error": "NS: The resolution lifetime expired after 10.204 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
        "txt": [
          "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
          "MS=ms41624661",
          "MS=ms60989570",
          "MS=ms69824556",
          "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
          "oneuptime=2fYJpBXRQsmY3Py",
          "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all"
        ],
        "mx": [
          "1 aspmx.l.google.com",
          "5 alt1.aspmx.l.google.com",
          "5 alt2.aspmx.l.google.com",
          "10 alt3.aspmx.l.google.com",
          "10 alt4.aspmx.l.google.com"
        ],
        "caa": [],
        "rr_errors": {
          "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
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
        "cf-ray": "9ed0948fabea8bf8-HAM"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0948fabea8bf8"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe/har/d945f098fbd5bb50.har",
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
      "a": [
        "104.18.42.225",
        "172.64.145.31"
      ],
      "aaaa": [
        "2a06:98c1:3101::6812:2ae1",
        "2a06:98c1:3107::ac40:911f"
      ],
      "https_status": 200,
      "https_cdn_headers": {
        "server": "cloudflare",
        "cf-ray": "9ed09495fe2c62b4-HAM"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "185.161.202.238",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "185.161.202.238"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 185.161.202.238 (185.161.202.238), 15 hops max, 40 byte packets\n",
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
    "ip": "185.161.202.238",
    "country_code": "DE",
    "region": "Hamburg",
    "city": "Hamburg",
    "connection": {
      "asn": 207137,
      "org": "Packethub S.A.",
      "isp": "Packethub S.A.",
      "domain": "packethub.net"
    },
    "location_id": "de-hamburg-hamburg-238",
    "location_label": "Hamburg, Hamburg, Germany"
  },
  "surface_probe": {
    "probes": [
      {
        "url": "https://nordvpn.com/pricing/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing/",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed0949e0cd362dd-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0949e0cd362dd"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/3cec43152ba057c5.har",
        "page_type": "pricing"
      },
      {
        "url": "https://my.nordaccount.com/",
        "error": null,
        "status": 200,
        "final_url": "https://my.nordaccount.com/",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed094a1fd896301-HAM"
        },
        "scripts": [
          "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
          "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
          "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
          "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
          "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
          "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
          "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
          "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
          "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
          "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
          "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
          "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
          "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
          "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
          "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
          "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
          "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
          "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
          "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
          "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
          "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
          "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
          "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
          "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
          "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
          "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
          "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
          "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
          "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
          "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
          "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
          "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
          "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
          "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
          "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
          "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
          "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
          "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
          "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
          "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
          "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
          "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
          "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
          "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
          "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
          "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
          "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
          "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
          "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
          "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
          "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
          "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
          "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
          "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
          "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
          "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/0096221d6f12d382.har",
        "page_type": "signup"
      },
      {
        "url": "https://nordcheckout.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed094b7edc362c5-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed094b7edc362c5"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/5c4416295d131e0b.har",
        "page_type": "checkout"
      }
    ],
    "surface_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260416T044817Z-976afdc6",
  "timestamp_utc": "2026-04-16T04:52:29.837578+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "de-hamburg-hamburg-238",
  "vpn_location_label": "Hamburg, Hamburg, Germany",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.161.202.238",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.161.202.238",
      "ipv6": null,
      "raw_excerpt": "185.161.202.238",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "91.64.142.30",
      "ipv6": null,
      "raw_excerpt": "91.64.142.30",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.161.202.238",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.161.202.238\"}",
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
        "185.161.202.238"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.161.202.238"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "fad69e4e-b77c-47a4-ba6a-32b581bb0ebe.local",
      "port": 59395,
      "raw": "candidate:3823828978 1 udp 2113937151 fad69e4e-b77c-47a4-ba6a-32b581bb0ebe.local 59395 typ host generation 0 ufrag Tjlf network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.161.202.238",
      "port": 59899,
      "raw": "candidate:4134263282 1 udp 1677729535 185.161.202.238 59899 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag Tjlf network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36",
    "language": "en-US",
    "hardwareConcurrency": 16,
    "platform": "MacIntel"
  },
  "attribution": {
    "asn": 207137,
    "holder": "PACKETHUBSA - PacketHub S.A.",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [207137]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 207137,
        "holder": "PACKETHUBSA - PacketHub S.A.",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (185.161.202.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260416044841-3feb9843-b290-4b4e-86b4-9d12e7973082",
            "process_time": 75,
            "server_id": "app172",
            "build_version": "v0.9.7-thriftpy2-2026.04.10",
            "pipeline": "1223136",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-16T04:48:41.590745",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 207137,
                  "holder": "PACKETHUBSA - PacketHub S.A."
                }
              ],
              "related_prefixes": [],
              "resource": "185.161.202.0/24",
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
        "asn": 207137,
        "holder": null,
        "country": null,
        "raw": {
          "asn": 207137,
          "raw_line": "207137 | 185.161.202.0/24 | DE | ripencc | 2016-08-02",
          "parts": [
            "207137",
            "185.161.202.0/24",
            "DE",
            "ripencc",
            "2016-08-02"
          ],
          "disclaimer": [
            "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
          ]
        }
      },
      {
        "name": "peeringdb",
        "asn": null,
        "holder": null,
        "country": null,
        "raw": {
          "error": "The read operation timed out"
        }
      }
    ],
    "disclaimers": [
      "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
      "Team Cymru notes some upstream inference is imperfect; treat as cross-check."
    ]
  },
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:49:54.425109+00:00",
      "sha256": "f0b29c2a54d708c2383bbac6ff8c7f27f614890acac0427f698fadd581fe2a53",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    },
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-16T04:50:00.903247+00:00",
      "sha256": "15374e2ce1d4290f76651d23f1a7b23a92f82e30b0fd6b79a170e76cafee8e44",
      "summary_bullets": [
        "Mentions retention (keyword hit; review source)",
        "Mentions logging (keyword hit; review source)",
        "Mentions law enforcement (keyword hit; review source)",
        "Mentions third parties (keyword hit; review source)",
        "Mentions telemetry (keyword hit; review source)"
      ]
    }
  ],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "competitor_probe:enabled",
    "competitor_probe:har_summary",
    "dns:lookup:nordvpn.com",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/185.161.202.238",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordcheckout.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/pricing/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260416T044817Z-976afdc6/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/webrtc",
    "ipv6_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/fingerprint",
    "attribution_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/policy",
    "competitor_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe",
    "transitions_json": null
  },
  "competitor_surface": {
    "provider_dns": {
      "domains": {
        "nordvpn.com": {
          "ns": [],
          "a": [
            "104.16.208.203",
            "104.19.159.190"
          ],
          "aaaa": [],
          "error": "NS: The resolution lifetime expired after 10.204 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
          "txt": [
            "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
            "MS=ms41624661",
            "MS=ms60989570",
            "MS=ms69824556",
            "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
            "oneuptime=2fYJpBXRQsmY3Py",
            "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all"
          ],
          "mx": [
            "1 aspmx.l.google.com",
            "5 alt1.aspmx.l.google.com",
            "5 alt2.aspmx.l.google.com",
            "10 alt3.aspmx.l.google.com",
            "10 alt4.aspmx.l.google.com"
          ],
          "caa": [],
          "rr_errors": {
            "caa": "The DNS response does not contain an answer to the question: nordvpn.com. IN CAA"
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
          "cf-ray": "9ed0948fabea8bf8-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0948fabea8bf8"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/competitor_probe/har/d945f098fbd5bb50.har",
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
        "a": [
          "104.18.42.225",
          "172.64.145.31"
        ],
        "aaaa": [
          "2a06:98c1:3101::6812:2ae1",
          "2a06:98c1:3107::ac40:911f"
        ],
        "https_status": 200,
        "https_cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed09495fe2c62b4-HAM"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "185.161.202.238",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "185.161.202.238"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 185.161.202.238 (185.161.202.238), 15 hops max, 40 byte packets\n",
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
    "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.161.202.238\nHostname\tn/a\nIP Address Location\nCountry\tGermany (DE)\nState/Region\tHamburg\nCity\tHamburg\nISP\tPacketHub S.A.\nOrganization\tPackethub S.A\nNetwork\tAS207137 PacketHub S.A. (VPN)\nUsage Type\tCellular\nTimezone\tEurope/Berlin (CEST)\nLocal Time\tThu, 16 Apr 2026 06:50:09 +0200\nCoordinates\t53.5488,9.9872\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.161.202.238\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t14 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\ta2eb0b03269154dcb5b0241f76eb5c7a\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.161.202.0 - 185.161.202.255\nCIDR\t185.161.202.0/24\nName\tPackethub-20240426\nHandle\t185.161.202.0 - 185.161.202.255\nParent Handle\t185.161.202.0 - 185.161.203.255\nNet Type\tASSIGNED PA\nCountry\tGermany\nRegistration\tFri, 26 Apr 2024 13:37:12 GMT\nLast Changed\tFri, 26 Apr 2024 13:37:12 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.161.202.238\nISP\tPacketHub S.A.\nLocation\tGermany, Hamburg\nDNS Leak Test\nTest Results\tFound 17 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.161.202.119\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.232\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.233\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.234\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.235\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.236\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.237\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.238\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.239\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.240\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.241\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.242\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.243\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.244\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.245\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.246\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.247\tPacketHub S.A.\tGermany, Hamburg\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.161.202.238\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.161.202.238\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (217)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\tLoading\nTLS 1.1\tLoading\nTLS 1.0\tLoading\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\tLoading\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_d3ed9d674783\nJA3\t5d0c9c59941ee016d9d365b7be57bd24\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x0A0A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x2A2A\nGREASE\n\n\n0x000D\nsignature_algorithms\n\n\n0x000A\nsupported_groups\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x0000\nserver_name\n\n\n0x0017\nextended_main_secret\n\n\n0x000B\nec_point_formats\n\n\n0xFF01\nrenegotiation_info\n\n\n0x0023\nsession_ticket\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0005\nstatus_request\n\n\n0x0033\nkey_share\n\n\n0x002B\nsupported_versions\n\n\n0x001B\ncompress_certificate\n\n\n0x44CD\napplication_settings\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0xEAEA\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t93\nenc_length\t32\npayload_length\t240\nkey_share\nclient_shares\t\n0xEAEA\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.browserleaks.com\nsignature_algorithms\nalgor",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-ad6418b7",
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
        "answer_summary": "Fingerprint and BrowserLeaks captures present for re-identification risk assessment.",
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
        "answer_summary": "Exit IPv4 185.161.202.238; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.238, 91.64.142.30.",
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
        "answer_summary": "Exit IPv4 185.161.202.238 for location de-hamburg-hamburg-238.",
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
        "answer_summary": "ASN 207137 — PACKETHUBSA - PacketHub S.A.",
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
        "answer_summary": "ASN 207137 — PACKETHUBSA - PacketHub S.A.",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 238.202.161.185.in-addr.arpa.",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Hamburg, Hamburg, Germany').",
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
        "answer_summary": "Fingerprint snapshot present.",
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
        "host": "fingerprint",
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
        "host": "nordcheckout.com",
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
      "ip": "185.161.202.238",
      "country_code": "DE",
      "region": "Hamburg",
      "city": "Hamburg",
      "connection": {
        "asn": 207137,
        "org": "Packethub S.A.",
        "isp": "Packethub S.A.",
        "domain": "packethub.net"
      },
      "location_id": "de-hamburg-hamburg-238",
      "location_label": "Hamburg, Hamburg, Germany"
    },
    "surface_probe": {
      "probes": [
        {
          "url": "https://nordvpn.com/pricing/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing/",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed0949e0cd362dd-HAM"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed0949e0cd362dd"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/3cec43152ba057c5.har",
          "page_type": "pricing"
        },
        {
          "url": "https://my.nordaccount.com/",
          "error": null,
          "status": 200,
          "final_url": "https://my.nordaccount.com/",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed094a1fd896301-HAM"
          },
          "scripts": [
            "https://my.nordaccount.com/assets/runtime.8f001b37f65ca9b94463.js",
            "https://my.nordaccount.com/assets/_formatjs.defaultvendors.490d421b9d5c3e9f8009.js",
            "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.1975ef189c3a5830cbd9.js",
            "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.fed5c69d1d43f3c655ec.js",
            "https://my.nordaccount.com/assets/index.f3f9e2458982da77703f.js",
            "https://my.nordaccount.com/assets/_nordsec.defaultvendors.1cbad33e47ad89bb5d71.chunk.js",
            "https://my.nordaccount.com/assets/date-fns.defaultvendors.27c069bedb2b90eb6745.chunk.js",
            "https://my.nordaccount.com/assets/_nord.defaultvendors.cd2b72f3eabc7aefab85.chunk.js",
            "https://my.nordaccount.com/assets/tslib.defaultvendors.f06c88be99e150fe47a8.chunk.js",
            "https://my.nordaccount.com/assets/_sentry.defaultvendors.25c5c79233b02634b48a.chunk.js",
            "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.12d96cb2c7ef87909b27.chunk.js",
            "https://my.nordaccount.com/assets/graphql.defaultvendors.b4db7c317c7d39b65131.chunk.js",
            "https://my.nordaccount.com/assets/react-intl.defaultvendors.92986a6cbe49509fcab3.chunk.js",
            "https://my.nordaccount.com/assets/graphql-request.defaultvendors.b2146a3e5d0f596bb64a.chunk.js",
            "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.a64bef2b4c371a7c9ca8.chunk.js",
            "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.71d280de527e9735544f.chunk.js",
            "https://my.nordaccount.com/assets/uuid.defaultvendors.487b6d676e3ad7b5e036.chunk.js",
            "https://my.nordaccount.com/assets/_babel.defaultvendors.2455d74e1fb84c624c54.chunk.js",
            "https://my.nordaccount.com/assets/react.defaultvendors.62bda77ffd034248908f.chunk.js",
            "https://my.nordaccount.com/assets/react-dom.defaultvendors.510bc4dc1ad2bf37567c.chunk.js",
            "https://my.nordaccount.com/assets/prop-types.defaultvendors.a656d45b79e86c928e92.chunk.js",
            "https://my.nordaccount.com/assets/react-toastify.defaultvendors.e8751af5398f51cb657f.chunk.js",
            "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.929ba19f051e6cca5269.chunk.js",
            "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.b994cdf10062f0dffbbb.chunk.js",
            "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.81442bee51666b2f5ab0.chunk.js",
            "https://my.nordaccount.com/assets/scheduler.defaultvendors.c87722040a503f4f3f9f.chunk.js",
            "https://my.nordaccount.com/assets/react-is.defaultvendors.92942d4a0302555e30b1.chunk.js",
            "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.4a977f328b9a40836758.chunk.js",
            "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.3dc35daf980ebd689198.chunk.js",
            "https://my.nordaccount.com/assets/react-redux.defaultvendors.55e7cc60ca7ac18a7047.chunk.js",
            "https://my.nordaccount.com/assets/js-cookie.defaultvendors.aa8f86970d616d2ce153.chunk.js",
            "https://my.nordaccount.com/assets/immer.defaultvendors.6fded9f37b4913aa9bd1.chunk.js",
            "https://my.nordaccount.com/assets/clsx.defaultvendors.856bc1a5790a3f606101.chunk.js",
            "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.6faa3d8d1551774e5c0c.chunk.js",
            "https://my.nordaccount.com/assets/classnames.defaultvendors.e2ab443a1f27e04b04df.chunk.js",
            "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.035fb5461cb44aeb4641.chunk.js",
            "https://my.nordaccount.com/assets/react-router.defaultvendors.a09a7faa911420a90ddf.chunk.js",
            "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.e50d96c12a219ec0d5e0.chunk.js",
            "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.4c2b522de6f7bbcd86e8.chunk.js",
            "https://my.nordaccount.com/assets/react-helmet.defaultvendors.bdd36bae03791902fd4c.chunk.js",
            "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.c13160b11e8cbb645318.chunk.js",
            "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.82e28da55d9337fe1e1e.chunk.js",
            "https://my.nordaccount.com/assets/object-assign.defaultvendors.11dad362db8d6f602074.chunk.js",
            "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.53b2e5173290a57b30b5.chunk.js",
            "https://my.nordaccount.com/assets/humps.defaultvendors.d487ed7a935923c9b2e1.chunk.js",
            "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.7171840257da98967b9a.chunk.js",
            "https://my.nordaccount.com/assets/filter-obj.defaultvendors.94c63526e1e718a23c90.chunk.js",
            "https://my.nordaccount.com/assets/file-saver.defaultvendors.375bc154e865cb159827.chunk.js",
            "https://my.nordaccount.com/assets/exenv.defaultvendors.3d6540bc323db97fe9b4.chunk.js",
            "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.96cfd77d74c2797d6fc2.chunk.js",
            "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.1f89cb3ed554da089890.chunk.js",
            "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.c65a97db2a22557ed5b7.chunk.js",
            "https://my.nordaccount.com/assets/split-on-first.defaultvendors.19d27a27e767feeaad1c.chunk.js",
            "https://my.nordaccount.com/assets/query-string.defaultvendors.627b547650dfceb718cd.chunk.js",
            "https://my.nordaccount.com/assets/_remix-run.defaultvendors.580c9c5b720b6c6b3554.chunk.js",
            "https://my.nordaccount.com/assets/4666.c911d9a1839636cab2d6.chunk.js"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/0096221d6f12d382.har",
          "page_type": "signup"
        },
        {
          "url": "https://nordcheckout.com/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed094b7edc362c5-HAM"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed094b7edc362c5"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe/har/5c4416295d131e0b.har",
          "page_type": "checkout"
        }
      ],
      "surface_probe_dir": "runs/nordvpn-20260416T044817Z-976afdc6/raw/de-hamburg-hamburg-238/surface_probe"
    }
  }
}
```

---



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`