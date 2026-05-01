# Nordvpn (nordvpn)

- **Report generated:** 2026-05-01T11:02:17.310655+00:00
- **Runs included:** nordvpn-20260501T100504Z-cc878634, nordvpn-20260501T104455Z-211c373f, nordvpn-20260501T105329Z-8cb49bd0
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
  - answered: 8
  - partially answered: 23
  - unanswered: 7
  - not testable dynamically: 4
- **Reading `answered`:** for some **DYNAMIC_PARTIAL** IDs (e.g. **FP-001**), **`answered`** means the harness captured the intended evidence class in `normalized.json`, not that the English question is fully settled by desk review—interpret using per-ID summaries, category context, and raw artifacts.

**Top severity findings (HIGH/CRITICAL)**


- *None flagged in this rollup.*


## SPEC question coverage (full table)

| ID | Status | Category | Question | Summary | Next steps |
|----|--------|----------|----------|---------|------------|
| `IDENTITY-001` | `partially_answered` | identity_correlation | What identifiers are assigned to the user, app install, browser session, and device? | Browser/session signals captured via fingerprint and optional YourInfo probe. | Run with fingerprint + YourInfo probes enabled; compare `fingerprint_snapshot` and `yourinfo_snapshot` in normalized.json. See RUN-STEPS.md (benchmark phases). |
| `IDENTITY-006` | `partially_answered` | identity_correlation | Are there long-lived client identifiers transmitted during auth or app startup? | Services contacted list enumerates URLs used during harness (may include auth-adjacent endpoints). | Browser `services_contacted` is partial; for app auth traffic use external capture or vendor docs (D). |
| `IDENTITY-009` | `partially_answered` | identity_correlation | Is the browser fingerprinting surface strong enough to re-identify the same user across sessions? | Fingerprint and BrowserLeaks captures present for re-identification risk assessment. | Enable fingerprint capture; without it re-ID risk stays unassessed. |
| `SIGNUP-001` | `partially_answered` | signup_payment | What third parties are involved during signup? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Set `competitor_probe` + `surface_urls` for signup/checkout in the provider YAML; re-run `vpn-leaks run`. |
| `SIGNUP-004` | `partially_answered` | signup_payment | Are analytics or marketing scripts loaded during signup or checkout? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Same as signup surface — competitor web HAR and `har_summary.json`. |
| `SIGNUP-010` | `partially_answered` | signup_payment | Are these surfaces behind a CDN/WAF? | No competitor web HAR in this run; configure competitor_probe and surface_urls. | Enable competitor web probes; check `cdn_headers` / `web_probes` in competitor_surface. |
| `WEB-001` | `unanswered` | website_portal | Where is the marketing site hosted (DNS/routing level)? |  | Configure competitor_probe.provider_domains. — Set `competitor_probe.provider_domains` (and related probes); for desk truth use `dig apex NS` + glue WHOIS (see docs/research-questions-and-evidence.md §H). |
| `WEB-004` | `unanswered` | website_portal | What CDN/WAF is used? |  | No web or portal probes in run. — Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed. |
| `WEB-008` | `partially_answered` | website_portal | Does the site leak origin details through headers, TLS metadata, redirects, or asset URLs? | Review web probe headers, redirects, and HAR for origin leaks. | Enable competitor probes and review HAR / redirects in raw artifacts. |
| `DNS-001` | `answered` | dns | Which DNS resolvers are used while connected? | Resolver tiers observed (local + external). | — |
| `DNS-002` | `partially_answered` | dns | Are DNS requests tunneled (consistent with VPN exit)? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Compare resolver IPs to exit; read `dns_leak_notes` (heuristic). Capture baseline off-VPN if comparing. |
| `DNS-003` | `partially_answered` | dns | Is there DNS fallback to ISP/router/public resolvers? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Same as DNS-002; transition tests help — run with `--transition-tests` when supported. |
| `DNS-004` | `partially_answered` | dns | Does DNS leak during connect/disconnect/reconnect? | Connect/disconnect DNS not sampled; use --transition-tests when supported. | Run `vpn-leaks run` with `--transition-tests` (see RUN-STEPS.md). |
| `DNS-009` | `partially_answered` | dns | Are DoH or DoT endpoints used? | DoH/DoT not isolated from resolver snapshot; inspect raw captures. | Inspect raw DNS captures / resolver lists; DoH/DoT may not be isolated in summary alone. |
| `DNS-011` | `partially_answered` | dns | Are resolvers first-party or third-party? | Leak flag=False; see notes. | Heuristic: no obvious public resolver IPs parsed from external page — Attribute resolver IPs (O); compare to exit ASN (I/D). |
| `IP-001` | `answered` | real_ip_leak | Is the real public IPv4 exposed while connected? | Exit IPv4 194.195.93.96; leak flags dns=False webrtc=False ipv6=False. | — |
| `IP-002` | `partially_answered` | real_ip_leak | Is the real public IPv6 exposed while connected? | No IPv6 exit or IPv6 not returned by endpoints. | Enable IPv6 path in environment; check `ipv6/` artifacts when present. |
| `IP-006` | `answered` | real_ip_leak | Is the real IP exposed through WebRTC? | WebRTC candidates captured; leak flag=False. | — |
| `IP-007` | `partially_answered` | real_ip_leak | Is the local LAN IP exposed through WebRTC or browser APIs? | Inspect host candidates vs LAN; see webrtc_notes. | Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`. |
| `IP-014` | `partially_answered` | real_ip_leak | Do leak-check sites disagree about observed IP identity? | All 3 echo endpoints agree on IPv4 194.195.93.96. | Compare `exit_ip_sources` entries for disagreement. |
| `CTRL-002` | `partially_answered` | control_plane | Which domains and IPs are contacted after the tunnel is up? | Post-harness service list captured. | `services_contacted` in `normalized.json` lists only URLs and probes this harness actually ran (not full-device traffic). Run a fuller benchmark: avoid `--skip-browserleaks` and competitor skip flags where you need those surfaces; add `competitor_probe` / portal / `surface_urls` in the provider YAML per RUN-STEPS.md; add more locations for diversity. For VPN app background traffic, use external capture—see CTRL-003. |
| `CTRL-003` | `not_testable_dynamically` | control_plane | Which control-plane endpoints are used for auth/config/session management? | Auth/control-plane inventory requires internal docs or app instrumentation. | DOCUMENT_RESEARCH: vendor docs, app MITM, or support (D). |
| `CTRL-004` | `partially_answered` | control_plane | Which telemetry endpoints are contacted during connection? | Infer from services_contacted and classified endpoints. | Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*). |
| `CTRL-009` | `unanswered` | control_plane | Is the control plane behind a CDN/WAF? |  | No web or portal probes. — Enable portal/web probes (`portal_probes`); check `https_cdn_headers`. |
| `EXIT-001` | `answered` | exit_infrastructure | What exit IP is assigned for each region? | Exit IPv4 194.195.93.96 for location us-california-san-jose-96. | — |
| `EXIT-002` | `answered` | exit_infrastructure | What ASN announces the exit IP? | ASN 212238 — CDNEXT Datacamp Limited | — |
| `EXIT-003` | `answered` | exit_infrastructure | What organization owns the IP range? | ASN 212238 — CDNEXT Datacamp Limited | — |
| `EXIT-004` | `partially_answered` | exit_infrastructure | What reverse DNS exists for the exit node? | PTR lookup errors: ptr_v4: The DNS query name does not exist: 96.93.195.194.in-addr.arpa. | Check raw `exit_dns.json` / attribution for rDNS when stored. |
| `EXIT-005` | `partially_answered` | exit_infrastructure | Does the observed geolocation match the advertised location? | Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States'). | Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate. |
| `THIRDWEB-001` | `unanswered` | third_party_web | What external JS files are loaded on the site? |  | Enable competitor_probe or surface_urls. — Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`. |
| `THIRDWEB-003` | `unanswered` | third_party_web | What analytics providers are present? |  | Enable competitor_probe or surface_urls. — HAR + `har_summary.json` tracker_candidates when competitor probes run. |
| `THIRDWEB-012` | `unanswered` | third_party_web | What cookies are set by first-party and third-party scripts? |  | Enable competitor_probe or surface_urls. — Review HAR for Set-Cookie; summary may be partial. |
| `FP-001` | `answered` | browser_tracking | Does the site attempt browser fingerprinting? | Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence). | — |
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

- **`WEB-004`** (`unanswered`): No web or portal probes in run. — Enable web/portal probes; headers show CDN/WAF signals. Compare with desk `curl -I` if needed.

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

- **`CTRL-009`** (`unanswered`): No web or portal probes. — Enable portal/web probes (`portal_probes`); check `https_cdn_headers`.

- **`EXIT-004`** (`partially_answered`): Check raw `exit_dns.json` / attribution for rDNS when stored.

- **`EXIT-005`** (`partially_answered`): Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate.

- **`THIRDWEB-001`** (`unanswered`): Enable competitor_probe or surface_urls. — Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`.

- **`THIRDWEB-003`** (`unanswered`): Enable competitor_probe or surface_urls. — HAR + `har_summary.json` tracker_candidates when competitor probes run.

- **`THIRDWEB-012`** (`unanswered`): Enable competitor_probe or surface_urls. — Review HAR for Set-Cookie; summary may be partial.

- **`OS-001`** (`partially_answered`): Process-level bypass not in default harness; external tooling or manual checks.

- **`FAIL-001`** (`partially_answered`): Use `--transition-tests` for connect-phase leaks when supported.

- **`FAIL-003`** (`partially_answered`): Use `--transition-tests` for reconnect leaks when supported.

- **`LOG-001`** (`partially_answered`): Review `services_contacted` + endpoint classifications; pair with policy/audit (D).

- **`LOG-005`** (`unanswered`): No policy fetch or failed fetch. — Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md.



## Analysis of collected evidence

### Scope

- **Benchmark rows in this report:** 3 (one row per `normalized.json` location).
- **Merge rule:** For each SPEC question ID, the status shown in the table is the **strictest** across rows: unanswered > partially_answered > answered > not_testable_dynamically.

### Risk and findings

- **Rollup severity (max across runs):** `LOW`
- **HIGH / CRITICAL framework findings:** none in this rollup.

### By category (merged coverage)

#### browser_tracking

- **FP-001** (answered): Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).
- **FP-011** (answered): WebRTC exercised by harness on leak-test pages.

#### control_plane

- **CTRL-002** (partial): Post-harness service list captured.
- **CTRL-003** (`not_testable_dynamically`): Auth/control-plane inventory requires internal docs or app instrumentation.
- **CTRL-004** (partial): Infer from services_contacted and classified endpoints.
- **CTRL-009** (unanswered): No web or portal probes.

#### dns

- **DNS-001** (answered): Resolver tiers observed (local + external).
- **DNS-002** (partial): Leak flag=False; see notes.
- **DNS-003** (partial): Leak flag=False; see notes.
- **DNS-004** (partial): Connect/disconnect DNS not sampled; use --transition-tests when supported.
- **DNS-009** (partial): DoH/DoT not isolated from resolver snapshot; inspect raw captures.
- **DNS-011** (partial): Leak flag=False; see notes.

#### exit_infrastructure

- **EXIT-001** (answered): Exit IPv4 194.195.93.96 for location us-california-san-jose-96.
- **EXIT-002** (answered): ASN 212238 — CDNEXT Datacamp Limited
- **EXIT-003** (answered): ASN 212238 — CDNEXT Datacamp Limited
- **EXIT-004** (partial): PTR lookup errors: ptr_v4: The DNS query name does not exist: 96.93.195.194.in-addr.arpa.
- **EXIT-005** (partial): Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').

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
- **LOG-005** (unanswered): No policy fetch or failed fetch.

#### os_specific

- **OS-001** (partial): OS snapshot: Darwin 25.4.0; no process-level tunnel bypass test in this run.

#### real_ip_leak

- **IP-001** (answered): Exit IPv4 194.195.93.96; leak flags dns=False webrtc=False ipv6=False.
- **IP-002** (partial): No IPv6 exit or IPv6 not returned by endpoints.
- **IP-006** (answered): WebRTC candidates captured; leak flag=False.
- **IP-007** (partial): Inspect host candidates vs LAN; see webrtc_notes.
- **IP-014** (partial): All 3 echo endpoints agree on IPv4 194.195.93.96.

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
- **WEB-004** (unanswered): No web or portal probes in run.
- **WEB-008** (partial): Review web probe headers, redirects, and HAR for origin leaks.

### Limitations

- Leak flags and DNS notes are **heuristic / harness-defined**; read raw `runs/.../raw/` artifacts for full context.
- **Observed leak flags (any location):** DNS=False, WebRTC=False, IPv6=False.
- **App telemetry (TELEM-001, TELEM-004)** and some control-plane details are **not** proven by browser-only harness paths; use **D** (documents) or external traffic studies where applicable.
- **Desk research (S)** (e.g. apex `dig`, glue WHOIS) is not auto-merged into this report; compare to `competitor_probe` / provider DNS when both exist.




## Leak summary

| Location | DNS leak | WebRTC leak | IPv6 leak |
|----------|----------|-------------|-----------|
| San Jose, CA, USA | False | False | False |
| San Jose, CA, USA | False | False | False |
| San Jose, CA, USA | False | False | False |


## Underlay (ASNs)


- **AS212238:** CDNEXT Datacamp Limited


## Website and DNS surface (third-party exposure)

Interpretation, manual desk steps, and evidence tiers (O / S / I): [docs/website-exposure-methodology.md](../docs/website-exposure-methodology.md).


*No website surface or provider DNS signals in these runs (no `competitor_probe` / `surface_urls` data, or probes empty).*



---

## Detailed runs

**Included in this report** (each subsection below mirrors one `normalized.json`):


1. `nordvpn-20260501T100504Z-cc878634` / `us-california-san-jose-96` — `runs/nordvpn-20260501T100504Z-cc878634/locations/us-california-san-jose-96/normalized.json`

2. `nordvpn-20260501T104455Z-211c373f` / `us-california-san-jose-87` — `runs/nordvpn-20260501T104455Z-211c373f/locations/us-california-san-jose-87/normalized.json`

3. `nordvpn-20260501T105329Z-8cb49bd0` / `us-california-san-jose-87` — `runs/nordvpn-20260501T105329Z-8cb49bd0/locations/us-california-san-jose-87/normalized.json`


Large JSON fields use size caps in this markdown file; when an excerpt hits a cap, a **note** appears at the start of that run’s section listing what was capped. **On-disk `normalized.json` is always complete.**



### nordvpn-20260501T100504Z-cc878634 / us-california-san-jose-96



- **vpn_provider:** nordvpn
- **Label:** San Jose, California, United States
- **Path:** `runs/nordvpn-20260501T100504Z-cc878634/locations/us-california-san-jose-96/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-05-01T10:06:01.781103+00:00
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
| exit_ip_v4 | 194.195.93.96 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "194.195.93.96",
    "ipv6": null,
    "raw_excerpt": "194.195.93.96",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "194.195.93.96",
    "ipv6": null,
    "raw_excerpt": "194.195.93.96",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "194.195.93.96",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"194.195.93.96\"}",
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
      "194.195.93.90"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "194.195.93.96"
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
| host | udp | 3b9f4e9c-6b38-475e-a1c6-f326f99f42dd.local | 49400 | `candidate:1153250707 1 udp 2113937151 3b9f4e9c-6b38-475e-a1c6-f326f99f42dd.local 49400 typ host generation 0 ufrag nOCi network-cost 999` |
| srflx | udp | 194.195.93.96 | 53546 | `candidate:1151906997 1 udp 1677729535 194.195.93.96 53546 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag nOCi network-cost 999` |


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
  "holder": "CDNEXT Datacamp Limited",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [212238]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 212238,
      "holder": "CDNEXT Datacamp Limited",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (194.195.93.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260501100527-2a3ceaf3-0bc5-4082-8020-438595b2d7c0",
          "process_time": 61,
          "server_id": "app171",
          "build_version": "v0.9.15-2026.04.30",
          "pipeline": "1248748",
          "status": "ok",
          "status_code": 200,
          "time": "2026-05-01T10:05:27.171183",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 212238,
                "holder": "CDNEXT Datacamp Limited"
              }
            ],
            "related_prefixes": [],
            "resource": "194.195.93.0/24",
            "type": "prefix",
            "block": {
              "resource": "194.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-05-01T00:00:00",
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
        "raw_line": "212238 | 194.195.93.0/24 | DE | ripencc | 1995-09-14",
        "parts": [
          "212238",
          "194.195.93.0/24",
          "DE",
          "ripencc",
          "1995-09-14"
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
[]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/194.195.93.96`

- `https://test-ipv6.com/`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260501T100504Z-cc878634/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/webrtc",
  "ipv6_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/fingerprint",
  "attribution_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/policy",
  "competitor_probe_dir": null,
  "browserleaks_probe_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": null,
  "transitions_json": null,
  "website_exposure_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/website_exposure",
  "capture_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/capture"
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
  "har_path": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-7737d9dd",
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
      "notes": "No web or portal probes in run."
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
      "answer_summary": "Exit IPv4 194.195.93.96; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 194.195.93.96.",
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
      "notes": "No web or portal probes."
    },
    {
      "question_id": "EXIT-001",
      "question_text": "What exit IP is assigned for each region?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 194.195.93.96 for location us-california-san-jose-96.",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 96.93.195.194.in-addr.arpa.",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
      "answer_status": "answered",
      "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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


#### Website & DNS surface (summary)


*No surface/DNS summary for this location (`competitor_surface` / `extra.surface_probe` empty or absent).*


#### Automated website-exposure methodology & PCAP


**Desk automation note:** Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.

| Third-party inventory rows | Phase-8 domains with deep audit |
|---------------------------|--------------------------------|
| 1 | 0 |

**Inventory (sample)**

| Company (hypothesis) | Role | How discovered |
|---------------------|------|----------------|
| (provider first-party) | marketing_and_app_surface | config_urls |



**Methodology limits:** *Does_not_replace_human_narrative_for_executive_disclosure*; *Cloudflare_or_bot_WAF_may_distort_HAR_coverage*; *Skipped_phase8_no_provider_domains_in_config*





**PCAP-derived metadata** (no Wireshark; see `pcap_derived` in JSON)

| Unique flows (estimate) | Packets (total) |
|-------------------------|-----------------|
| 357 | 12015 |


**TLS SNI (sample):** `api2.cursor.sh`, `cognito-identity.us-east-1.amazonaws.com`, `firehose.us-east-1.amazonaws.com`, `logs.us-east-1.amazonaws.com`


**Cleartext DNS names (UDP/53 sample):** `apple.com`, `b._dns-sd._udp.0.0.5.10.in-addr.arpa`, `browser-intake-us5-datadoghq.com`, `db._dns-sd._udp.0.0.5.10.in-addr.arpa`, `doh-dns-apple-com.v.aaplimg.com`, `doh.dns.apple.com`, `icloud.com`, `lb._dns-sd._udp.0.0.5.10.in-addr.arpa`, `ssl.gstatic.com`


**PCAP interpretation limits:** *ECH_ESNI_not_visible*; *DoH_not_inferred_from_udp_53*; *tcp_segmentation_may_fragment_clienthello*; *inner_vpn_payload_may_be_opaque*



#### PCAP host intelligence




- Scope: public peer IPs from PCAP flows/pairs plus DNS/SNI hostnames from PCAP.

- Live lookups are fail-soft and may vary by resolver/time.



| Host | Source | IP / IPs | Reverse DNS | ASN | Owner | WHOIS summary | dig summary | Bytes | Flows | Lookup errors |
|------|--------|----------|-------------|-----|-------|---------------|-------------|-------|-------|---------------|
| `194.195.93.13` | pcap_peer_ip | 194.195.93.13 | — | AS136787 | PACKETHUB-20220731 | netname:        PACKETHUB-20220731 | country:        US | org-name:       Packethub S.A. | origin:         as136787 | origin:         AS212238 | PTR=— | 7778262 | 4 | reverse_dns_failed |
| `151.101.67.6` | pcap_peer_ip | 151.101.67.6 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. | PTR=— | 2158922 | 6 | reverse_dns_failed |
| `104.18.34.244` | pcap_peer_ip | 104.18.34.244 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 1767794 | 12 | reverse_dns_failed |
| `104.16.155.111` | pcap_peer_ip | 104.16.155.111 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 158742 | 6 | reverse_dns_failed |
| `44.255.66.41` | pcap_peer_ip | 44.255.66.41 | ec2-44-255-66-41.us-west-2.compute.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-255-66-41.us-west-2.compute.amazonaws.com | 144607 | 3 | — |
| `44.213.21.24` | pcap_peer_ip | 44.213.21.24 | ec2-44-213-21-24.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-213-21-24.compute-1.amazonaws.com | 76514 | 18 | — |
| `8.8.4.4` | pcap_peer_ip | 8.8.4.4 | dns.google | — | GOGL | NetName:        GOGL | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dns.google | 76472 | 4 | — |
| `142.251.218.110` | pcap_peer_ip | 142.251.218.110 | pnsfoa-ab-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ab-in-f14.1e100.net | 75784 | 7 | — |
| `44.210.246.125` | pcap_peer_ip | 44.210.246.125 | ec2-44-210-246-125.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-210-246-125.compute-1.amazonaws.com | 62519 | 3 | — |
| `3.236.94.133` | pcap_peer_ip | 3.236.94.133 | ec2-3-236-94-133.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-236-94-133.compute-1.amazonaws.com | 60382 | 3 | — |
| `151.101.3.6` | pcap_peer_ip | 151.101.3.6 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. | PTR=— | 60004 | 6 | reverse_dns_failed |
| `216.239.36.223` | pcap_peer_ip | 216.239.36.223 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 53074 | 7 | reverse_dns_failed |
| `142.251.151.119` | pcap_peer_ip | 142.251.151.119 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 51240 | 3 | reverse_dns_failed |
| `104.16.208.203` | pcap_peer_ip | 104.16.208.203 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 42041 | 3 | reverse_dns_failed |
| `17.253.144.10` | pcap_peer_ip | 17.253.144.10 | brkgls.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=brkgls.com, icloud.com, iphone.apple.com, podcast.apple.com, appstore.com, firewire.apple.com, livepage.apple.com, seminars.apple.com, applejava.apple.com, world-any.aaplimg.com, advertising.apple.com, applescript.apple.com, applecomputer.co.kr, itunespartner.apple.com, iworktrialbuy.apple.com, safaricampaign.apple, aperturetrialbuy.apple.com, vipd-healthcheck.a01.3banana.com, squeakytoytrainingcamp.com, www.brkgls.com, asia.apple.com, apple.ca, apple.co.uk, apple.de, apple.es, apple.fr, apple.it, apple.nl, apple.com, apple.com.ai, apple.com.au, apple.com.bo, apple.com.cn, apple.com.co, apple.com.do, apple.com.gy, apple.com.hn, apple.com.lk, apple.com.mx, apple.com.my, apple.com.pa, apple.com.pe, apple.com.py, apple.com.sg, apple.com.tt, apple.com.uy, guide.apple.com, shake.apple.com | 41174 | 5 | — |
| `23.67.33.152` | pcap_peer_ip | 23.67.33.152 | a23-67-33-152.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-67-33-152.deploy.static.akamaitechnologies.com | 40151 | 5 | — |
| `17.253.5.160` | pcap_peer_ip | 17.253.5.160 | ussjc2-vip-fx-115.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-115.b.aaplimg.com | 36813 | 5 | — |
| `104.18.41.41` | pcap_peer_ip | 104.18.41.41 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 31523 | 13 | reverse_dns_failed |
| `142.251.219.10` | pcap_peer_ip | 142.251.219.10 | ncsfoa-aq-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-aq-in-f10.1e100.net | 30616 | 5 | — |
| `142.251.214.35` | pcap_peer_ip | 142.251.214.35 | pnsfoa-ae-in-f3.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ae-in-f3.1e100.net | 27466 | 3 | — |
| `104.18.18.125` | pcap_peer_ip | 104.18.18.125 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 23443 | 7 | reverse_dns_failed |
| `3.95.44.182` | pcap_peer_ip | 3.95.44.182 | ec2-3-95-44-182.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-95-44-182.compute-1.amazonaws.com | 21746 | 3 | — |
| `162.125.40.2` | pcap_peer_ip | 162.125.40.2 | — | — | DROPB | NetName:        DROPB | OriginAS: | Organization:   Dropbox, Inc. (DROPB) | OrgName:        Dropbox, Inc. | Country:        US | PTR=— | 21094 | 3 | reverse_dns_failed |
| `13.219.38.100` | pcap_peer_ip | 13.219.38.100 | ec2-13-219-38-100.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-13-219-38-100.compute-1.amazonaws.com | 11304 | 2 | — |
| `17.253.5.142` | pcap_peer_ip | 17.253.5.142 | ussjc2-vip-fx-106.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-106.b.aaplimg.com | 11178 | 2 | — |
| `52.40.100.195` | pcap_peer_ip | 52.40.100.195 | ec2-52-40-100-195.us-west-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-52-40-100-195.us-west-2.compute.amazonaws.com | 10240 | 2 | — |
| `142.251.218.206` | pcap_peer_ip | 142.251.218.206 | ncsfoa-ao-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ao-in-f14.1e100.net | 9257 | 4 | — |
| `157.240.11.35` | pcap_peer_ip | 157.240.11.35 | edge-star-mini-shv-02-lax3.facebook.com | — | THEFA-3 | NetName:        THEFA-3 | OriginAS: | Organization:   Facebook, Inc. (THEFA-3) | OrgName:        Facebook, Inc. | Country:        US | PTR=edge-star-mini-shv-02-lax3.facebook.com | 8775 | 2 | — |
| `18.118.116.227` | pcap_peer_ip | 18.118.116.227 | ec2-18-118-116-227.us-east-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-18-118-116-227.us-east-2.compute.amazonaws.com | 8583 | 22 | — |
| `172.217.12.110` | pcap_peer_ip | 172.217.12.110 | sfo03s33-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=sfo03s33-in-f14.1e100.net, atl26s14-in-f14.1e100.net | 7016 | 2 | — |
| `64.78.200.1` | pcap_peer_ip | 64.78.200.1 | doh.dns.apple.com | — | WOODYN | NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US | PTR=doh.dns.apple.com | 6746 | 2 | — |
| `142.251.218.170` | pcap_peer_ip | 142.251.218.170 | ncsfoa-ak-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ak-in-f10.1e100.net | 6398 | 4 | — |
| `44.207.201.88` | pcap_peer_ip | 44.207.201.88 | ec2-44-207-201-88.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-207-201-88.compute-1.amazonaws.com | 6110 | 2 | — |
| `172.64.148.235` | pcap_peer_ip | 172.64.148.235 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 5630 | 10 | reverse_dns_failed |
| `104.18.39.21` | pcap_peer_ip | 104.18.39.21 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 4702 | 8 | reverse_dns_failed |
| `162.159.136.234` | pcap_peer_ip | 162.159.136.234 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 4491 | 2 | reverse_dns_failed |
| `34.149.66.154` | pcap_peer_ip | 34.149.66.154 | 154.66.149.34.bc.googleusercontent.com | — | GOOGL-2 | NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | PTR=154.66.149.34.bc.googleusercontent.com | 4087 | 2 | — |
| `3.233.158.31` | pcap_peer_ip | 3.233.158.31 | ec2-3-233-158-31.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-233-158-31.compute-1.amazonaws.com | 3735 | 2 | — |
| `172.217.12.106` | pcap_peer_ip | 172.217.12.106 | atl26s14-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=atl26s14-in-f10.1e100.net, sfo03s33-in-f10.1e100.net | 3233 | 2 | — |
| `8.8.8.8` | pcap_peer_ip | 8.8.8.8 | dns.google | — | GOGL | NetName:        GOGL | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dns.google | 2943 | 28 | — |
| `104.18.31.84` | pcap_peer_ip | 104.18.31.84 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 2645 | 1 | reverse_dns_failed |
| `104.18.14.131` | pcap_peer_ip | 104.18.14.131 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 2594 | 2 | reverse_dns_failed |
| `142.251.214.46` | pcap_peer_ip | 142.251.214.46 | pnsfoa-ae-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ae-in-f14.1e100.net | 2472 | 2 | — |
| `104.18.15.131` | pcap_peer_ip | 104.18.15.131 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 2390 | 2 | reverse_dns_failed |
| `162.125.40.1` | pcap_peer_ip | 162.125.40.1 | — | — | DROPB | NetName:        DROPB | OriginAS: | Organization:   Dropbox, Inc. (DROPB) | OrgName:        Dropbox, Inc. | Country:        US | PTR=— | 2369 | 3 | reverse_dns_failed |
| `3.220.93.0` | pcap_peer_ip | 3.220.93.0 | ec2-3-220-93-0.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-220-93-0.compute-1.amazonaws.com | 2160 | 2 | — |
| `57.144.220.141` | pcap_peer_ip | 57.144.220.141 | edge-star-shv-01-sjc6.facebook.com | — | FB-BLOCK | netname:        FB-BLOCK | country:        IE | org-name:       Meta Platforms Ireland Limited | country:        IE | PTR=edge-star-shv-01-sjc6.facebook.com | 1758 | 6 | — |
| `142.251.210.138` | pcap_peer_ip | 142.251.210.138 | dclaxa-as-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dclaxa-as-in-f10.1e100.net | 1665 | 1 | — |
| `16.58.181.75` | pcap_peer_ip | 16.58.181.75 | ec2-16-58-181-75.us-east-2.compute.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-16-58-181-75.us-east-2.compute.amazonaws.com | 1572 | 4 | — |
| `16.59.118.108` | pcap_peer_ip | 16.59.118.108 | ec2-16-59-118-108.us-east-2.compute.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-16-59-118-108.us-east-2.compute.amazonaws.com | 1508 | 4 | — |
| `18.97.36.71` | pcap_peer_ip | 18.97.36.71 | ec2-18-97-36-71.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-18-97-36-71.compute-1.amazonaws.com | 1397 | 2 | — |
| `75.2.76.8` | pcap_peer_ip | 75.2.76.8 | ae2c518386054b8a3.awsglobalaccelerator.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ae2c518386054b8a3.awsglobalaccelerator.com | 1266 | 2 | — |
| `57.144.221.134` | pcap_peer_ip | 57.144.221.134 | edge-z-p3-shv-01-sjc6.facebook.com | — | FB-BLOCK | netname:        FB-BLOCK | country:        IE | org-name:       Meta Platforms Ireland Limited | country:        IE | PTR=edge-z-p3-shv-01-sjc6.facebook.com | 1261 | 2 | — |
| `142.251.218.234` | pcap_peer_ip | 142.251.218.234 | pnsfoa-af-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-af-in-f10.1e100.net | 1192 | 2 | — |
| `34.36.73.246` | pcap_peer_ip | 34.36.73.246 | 246.73.36.34.bc.googleusercontent.com | — | GOOGL-2 | NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | PTR=246.73.36.34.bc.googleusercontent.com | 1056 | 8 | — |
| `100.49.221.249` | pcap_peer_ip | 100.49.221.249 | ec2-100-49-221-249.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-100-49-221-249.compute-1.amazonaws.com | 993 | 2 | — |
| `3.101.224.52` | pcap_peer_ip | 3.101.224.52 | ec2-3-101-224-52.us-west-1.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-101-224-52.us-west-1.compute.amazonaws.com | 948 | 2 | — |
| `18.97.36.60` | pcap_peer_ip | 18.97.36.60 | ec2-18-97-36-60.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-18-97-36-60.compute-1.amazonaws.com | 938 | 2 | — |
| `140.82.112.26` | pcap_peer_ip | 140.82.112.26 | lb-140-82-112-26-iad.github.com | — | GITHU | NetName:        GITHU | OriginAS: | Organization:   GitHub, Inc. (GITHU) | OrgName:        GitHub, Inc. | Country:        US | PTR=lb-140-82-112-26-iad.github.com | 929 | 1 | — |
| `3.143.136.10` | pcap_peer_ip | 3.143.136.10 | ec2-3-143-136-10.us-east-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-143-136-10.us-east-2.compute.amazonaws.com | 899 | 2 | — |
| `18.223.130.140` | pcap_peer_ip | 18.223.130.140 | ec2-18-223-130-140.us-east-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-18-223-130-140.us-east-2.compute.amazonaws.com | 897 | 2 | — |
| `17.253.5.138` | pcap_peer_ip | 17.253.5.138 | ussjc2-vip-fx-104.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-104.b.aaplimg.com | 894 | 2 | — |
| `54.241.60.143` | pcap_peer_ip | 54.241.60.143 | ec2-54-241-60-143.us-west-1.compute.amazonaws.com | — | AMAZON-2011L | NetName:        AMAZON-2011L | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-54-241-60-143.us-west-1.compute.amazonaws.com | 882 | 2 | — |
| `140.82.113.25` | pcap_peer_ip | 140.82.113.25 | lb-140-82-113-25-iad.github.com | — | GITHU | NetName:        GITHU | OriginAS: | Organization:   GitHub, Inc. (GITHU) | OrgName:        GitHub, Inc. | Country:        US | PTR=lb-140-82-113-25-iad.github.com | 751 | 1 | — |
| `142.251.218.174` | pcap_peer_ip | 142.251.218.174 | ncsfoa-ak-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ak-in-f14.1e100.net | 740 | 2 | — |
| `3.134.250.63` | pcap_peer_ip | 3.134.250.63 | ec2-3-134-250-63.us-east-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-3-134-250-63.us-east-2.compute.amazonaws.com | 729 | 2 | — |
| `142.251.219.42` | pcap_peer_ip | 142.251.219.42 | ncsfoa-an-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-an-in-f10.1e100.net | 660 | 2 | — |
| `8.0.6.4` | pcap_peer_ip | 8.0.6.4 | dns-8-0-6-4.atlanta1.level3.net | — | LVLT-ORG-8-8 | NetName:        LVLT-ORG-8-8 | OriginAS: | Organization:   Level 3 Parent, LLC (LPL-141) | OrgName:        Level 3 Parent, LLC | Country:        US | PTR=DNS-8-0-6-4.Atlanta1.Level3.net | 654 | 1 | — |
| `8.6.0.1` | pcap_peer_ip | 8.6.0.1 | — | — | LVLT-ORG-8-8 | NetName:        LVLT-ORG-8-8 | OriginAS: | Organization:   Level 3 Parent, LLC (LPL-141) | OrgName:        Level 3 Parent, LLC | Country:        US | PTR=— | 654 | 1 | reverse_dns_failed |
| `57.144.220.145` | pcap_peer_ip | 57.144.220.145 | edge-dgw-shv-01-sjc6.facebook.com | — | FB-BLOCK | netname:        FB-BLOCK | country:        IE | org-name:       Meta Platforms Ireland Limited | country:        IE | PTR=edge-dgw-shv-01-sjc6.facebook.com | 636 | 2 | — |
| `23.20.198.51` | pcap_peer_ip | 23.20.198.51 | ec2-23-20-198-51.compute-1.amazonaws.com | — | AMAZON-EC2-USEAST-10 | NetName:        AMAZON-EC2-USEAST-10 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-23-20-198-51.compute-1.amazonaws.com | 588 | 2 | — |
| `17.253.5.133` | pcap_peer_ip | 17.253.5.133 | ussjc2-vip-fx-102.a.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-102.a.aaplimg.com | 492 | 1 | — |
| `17.253.5.140` | pcap_peer_ip | 17.253.5.140 | ussjc2-vip-fx-105.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-105.b.aaplimg.com | 492 | 1 | — |
| `23.37.16.29` | pcap_peer_ip | 23.37.16.29 | a23-37-16-29.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-37-16-29.deploy.static.akamaitechnologies.com | 492 | 1 | — |
| `23.67.33.104` | pcap_peer_ip | 23.67.33.104 | a23-67-33-104.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-67-33-104.deploy.static.akamaitechnologies.com | 492 | 1 | — |
| `23.67.33.74` | pcap_peer_ip | 23.67.33.74 | a23-67-33-74.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-67-33-74.deploy.static.akamaitechnologies.com | 492 | 1 | — |
| `140.82.113.21` | pcap_peer_ip | 140.82.113.21 | lb-140-82-113-21-iad.github.com | — | GITHU | NetName:        GITHU | OriginAS: | Organization:   GitHub, Inc. (GITHU) | OrgName:        GitHub, Inc. | Country:        US | PTR=lb-140-82-113-21-iad.github.com | 468 | 2 | — |
| `140.82.116.3` | pcap_peer_ip | 140.82.116.3 | lb-140-82-116-3-sea.github.com | — | GITHU | NetName:        GITHU | OriginAS: | Organization:   GitHub, Inc. (GITHU) | OrgName:        GitHub, Inc. | Country:        US | PTR=lb-140-82-116-3-sea.github.com | 447 | 2 | — |
| `34.149.66.147` | pcap_peer_ip | 34.149.66.147 | 147.66.149.34.bc.googleusercontent.com | — | GOOGL-2 | NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | PTR=147.66.149.34.bc.googleusercontent.com | 444 | 2 | — |
| `142.251.153.119` | pcap_peer_ip | 142.251.153.119 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 428 | 2 | reverse_dns_failed |
| `23.67.33.155` | pcap_peer_ip | 23.67.33.155 | a23-67-33-155.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-67-33-155.deploy.static.akamaitechnologies.com | 414 | 2 | — |
| `13.59.24.137` | pcap_peer_ip | 13.59.24.137 | ec2-13-59-24-137.us-east-2.compute.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-13-59-24-137.us-east-2.compute.amazonaws.com | 402 | 1 | — |
| `17.253.83.133` | pcap_peer_ip | 17.253.83.133 | uslax1-vip-fx-102.a.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=uslax1-vip-fx-102.a.aaplimg.com | 402 | 1 | — |
| `17.253.83.143` | pcap_peer_ip | 17.253.83.143 | uslax1-vip-fx-107.a.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=uslax1-vip-fx-107.a.aaplimg.com | 402 | 1 | — |
| `17.57.144.118` | pcap_peer_ip | 17.57.144.118 | — | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=— | 402 | 1 | reverse_dns_failed |
| `23.67.33.148` | pcap_peer_ip | 23.67.33.148 | a23-67-33-148.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-67-33-148.deploy.static.akamaitechnologies.com | 396 | 2 | — |
| `54.71.177.201` | pcap_peer_ip | 54.71.177.201 | ec2-54-71-177-201.us-west-2.compute.amazonaws.com | — | AMAZON-2011L | NetName:        AMAZON-2011L | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-54-71-177-201.us-west-2.compute.amazonaws.com | 373 | 2 | — |
| `142.251.218.133` | pcap_peer_ip | 142.251.218.133 | pnsfoa-ad-in-f5.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ad-in-f5.1e100.net, qro04s06-in-f5.1e100.net | 318 | 2 | — |
| `142.251.2.188` | pcap_peer_ip | 142.251.2.188 | dl-in-f188.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dl-in-f188.1e100.net | 240 | 2 | — |
| `44.202.79.176` | pcap_peer_ip | 44.202.79.176 | ec2-44-202-79-176.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-202-79-176.compute-1.amazonaws.com | 228 | 4 | — |
| `104.17.91.187` | pcap_peer_ip | 104.17.91.187 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 198 | 2 | reverse_dns_failed |
| `104.18.19.125` | pcap_peer_ip | 104.18.19.125 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 198 | 2 | reverse_dns_failed |
| `104.21.94.58` | pcap_peer_ip | 104.21.94.58 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 198 | 2 | reverse_dns_failed |
| `18.173.121.129` | pcap_peer_ip | 18.173.121.129 | server-18-173-121-129.sfo53.r.cloudfront.net | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=server-18-173-121-129.sfo53.r.cloudfront.net | 198 | 2 | — |
| `18.244.214.106` | pcap_peer_ip | 18.244.214.106 | server-18-244-214-106.sfo53.r.cloudfront.net | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=server-18-244-214-106.sfo53.r.cloudfront.net | 198 | 2 | — |
| `142.250.101.188` | pcap_peer_ip | 142.250.101.188 | dz-in-f188.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dz-in-f188.1e100.net | 120 | 2 | — |
| `34.224.248.249` | pcap_peer_ip | 34.224.248.249 | ec2-34-224-248-249.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-34-224-248-249.compute-1.amazonaws.com | 120 | 2 | — |
| `44.213.98.9` | pcap_peer_ip | 44.213.98.9 | ec2-44-213-98-9.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-44-213-98-9.compute-1.amazonaws.com | 114 | 2 | — |
| `2e09:ef96:806:1:800:604:2:ce24` | pcap_peer_ip | 2e09:ef96:806:1:800:604:2:ce24 | — | — | — | — | PTR=— | 42 | 1 | reverse_dns_failed |
| `2e09:ef96:a00:2b:9260:7b53:ed62:a00` | pcap_peer_ip | 2e09:ef96:a00:2b:9260:7b53:ed62:a00 | — | — | — | — | PTR=— | 42 | 1 | reverse_dns_failed |
| `api2.cursor.sh` | pcap_sni | 44.221.232.213, 98.86.32.51, 75.101.211.195, 98.94.136.195, 100.51.70.29, 52.3.58.251, 100.31.31.206, 32.192.143.204 | ec2-100-31-31-206.compute-1.amazonaws.com, ec2-100-51-70-29.compute-1.amazonaws.com, ec2-32-192-143-204.compute-1.amazonaws.com, ec2-44-221-232-213.compute-1.amazonaws.com, ec2-52-3-58-251.compute-1.amazonaws.com, ec2-75-101-211-195.compute-1.amazonaws.com, ec2-98-86-32-51.compute-1.amazonaws.com, ec2-98-94-136-195.compute-1.amazonaws.com | — | AMAZO-4, AMAZON-EC2-4, AT-88-Z | 44.221.232.213=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 98.86.32.51=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 75.101.211.195=>NetName:        AMAZON-EC2-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 98.94.136.195=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 100.51.70.29=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 52.3.58.251=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 100.31.31.206=>NetName:        AMAZO-4 | OriginAS: | | A=api2geo.cursor.sh., api2direct.cursor.sh., 44.221.232.213, 98.86.32.51, 75.101.211.195, 98.94.136.195; AAAA=—; CNAME=api2geo.cursor.sh.; MX=—; TXT=— | 0 | 0 | — |
| `apple.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | brkgls.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=20 mx-in-vib.apple.com., 10 mx-in.g.apple.com., 20 mx-in-ma.apple.com., 20 mx-in-rn.apple.com., 20 mx-in-sg.apple.com., 20 mx-in-hfd.apple.com. | 0 | 0 | dig_txt:timeout:dig |
| `b._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `browser-intake-us5-datadoghq.com` | pcap_dns | 34.149.66.154, 2600:1901:0:179c:: | 154.66.149.34.bc.googleusercontent.com | — | GOOGL-2, GOOGLE-CLOUD | 34.149.66.154=>NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US || 2600:1901:0:179c::=>NetName:        GOOGLE-CLOUD | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | A=34.149.66.154; AAAA=2600:1901:0:179c::; CNAME=—; MX=—; TXT=— | 0 | 0 | 2600:1901:0:179c:::reverse_dns_failed |
| `cognito-identity.us-east-1.amazonaws.com` | pcap_sni | 18.205.49.157, 54.243.177.246, 18.214.48.122, 34.230.150.233, 13.219.38.100, 3.214.55.246, 100.26.120.36, 100.30.138.56, 2600:1f10:469b:a100:cfde:8be3:a42e:448b, 2600:1f10:469b:a102:a4a7:4544:a8be:8ca8, 2600:1f10:469b:a101:4eba:f829:2b13:dfa, 2600:1f10:469b:a102:4c3e:3371:85e0:df66 | ec2-100-26-120-36.compute-1.amazonaws.com, ec2-100-30-138-56.compute-1.amazonaws.com, ec2-13-219-38-100.compute-1.amazonaws.com, ec2-18-205-49-157.compute-1.amazonaws.com, ec2-18-214-48-122.compute-1.amazonaws.com, ec2-3-214-55-246.compute-1.amazonaws.com, ec2-34-230-150-233.compute-1.amazonaws.com, ec2-54-243-177-246.compute-1.amazonaws.com | — | AMAZO-4, AMAZON-2011L, AMZ-EC2, AT-88-Z | 18.205.49.157=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 54.243.177.246=>NetName:        AMAZON-2011L | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 18.214.48.122=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 34.230.150.233=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 13.219.38.100=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.214.55.246=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologi | A=18.205.49.157, 54.243.177.246, 18.214.48.122, 34.230.150.233, 13.219.38.100, 3.214.55.246; AAAA=2600:1f10:469b:a100:cfde:8be3:a42e:448b, 2600:1f10:469b:a102:a4a7:4544:a8be:8ca8, 2600:1f10:469b:a101:4eba:f829:2b13:dfa, 2600:1f10:469b:a102:4c3e:3371:85e0:df66, 2600:1f10:469b:a100:2c8:4774:8005:f190, 2600:1f10:469b:a100:b60:3c67:10fb:5cb; CNAME=—; MX=—; TXT=— | 0 | 0 | 2600:1f10:469b:a100:cfde:8be3:a42e:448b:reverse_dns_failed; 2600:1f10:469b:a102:a4a7:4544:a8be:8ca8:reverse_dns_failed; 2600:1f10:469b:a101:4eba:f829:2b13:dfa:reverse_dns_failed; 2600:1f10:469b:a102:4c3e:3371:85e0:df66:reverse_dns_failed |
| `db._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `doh-dns-apple-com.v.aaplimg.com` | pcap_dns | 64.78.200.1, 17.132.91.13, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11, 2620:149:a0c:3000::1c2, 2620:149:9cc::15, 2620:171:80c::1, 2620:171:80d::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.13=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:3000::1c2=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | Or | A=64.78.200.1, 17.132.91.13, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11; AAAA=2620:149:a0c:3000::1c2, 2620:149:9cc::15, 2620:171:80c::1, 2620:171:80d::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2; CNAME=—; MX=—; TXT=— | 0 | 0 | 17.132.91.13:reverse_dns_failed; 17.132.91.11:reverse_dns_failed; 2620:149:9cc::15:reverse_dns_failed; 2620:149:9cc::14:reverse_dns_failed |
| `doh.dns.apple.com` | pcap_dns | 17.132.91.13, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11, 64.78.200.1, 2620:171:80c::1, 2620:171:80d::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2, 2620:149:9cc::15 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 17.132.91.13=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 2620:171:80c::1=>NetName:        WOODYNET-V6-NET02 | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | O | A=doh-dns-apple-com.v.aaplimg.com., 17.132.91.13, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11; AAAA=doh-dns-apple-com.v.aaplimg.com., 2620:171:80c::1, 2620:171:80d::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2; CNAME=doh-dns-apple-com.v.aaplimg.com.; MX=—; TXT=— | 0 | 0 | — |
| `firehose.us-east-1.amazonaws.com` | pcap_sni | 3.237.107.19 | ec2-3-237-107-19.compute-1.amazonaws.com | — | AT-88-Z | 3.237.107.19=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | A=3.237.107.19; AAAA=—; CNAME=—; MX=—; TXT=3.237.107.1c32e1 52.46.143.48c0e0 44.210.246.122c32e1 3.237.107.34c32e1 52.119.196.193c0e0 52.119.198.79c0e0 3.237.107.62c32e1 " "52.46.140.96c0e0 72.21.195.15c0e0 52.119.197.123c0e0 3.237.107.44c32e1 44.210.246.73c32e1 3.237.107.50c32e1 209.54.178.67c0e0 5" "2.46.153.116c0e0 52.46.153.120c0e0 209.54.176.79c0e0 3.237.107.47c32e1 3.237.107.0c32e1 3.237.107.114c32e1 52.94.232.253c0e0 3." "237.107.19c32e1 52.46.128.67c0e0 52.46.142.17c0e0 3.237.107.53c32e1 3.237.107.97c32e1 3.237.107.30c32e1 52.46.132.133c0e0 3.237" ".107.9c32e1 3.237.107.102c32e1 52.46.132.196c0e0 52.119.198.155c0e0 44.210.246.102c32e1 52.119.197.143c0e0 54.239.25.120c0e0 3." "237.107.49c32e1 52.119.197.133c0e0 44.210.246.99c32e1 3.237.107.116c32e1 52.46.135.48c0e0 52.94.225.129c0e0 52.119.196.176c0e0 " "3.237.107.41c32e1 52.119.198.13c0e0 52.46.135.137c0e0 52.46.130.240c0e0 52.46.155.54c0e0 3.237.107.15c32e1 3.237.107.96c32e1 44" ".210.246.125c32e1 52.119.197.233c0e0 3.237.107.38c32e1 3.237.107.29c32e1 3.237.107.46c32e1 52.119.196.185c0e0 3.237.107.99c32e1" " 52.119.198.71c0e0 52.46.151.48c0e0 3.237.107.59c32e1 3.237.107.121c32e1 54.239.30.232c0e0 3.237.107.66c32e1 3.237.107.21c32e1 " "52.94.225.147c0e0 52.46.146.100c0e0 3.237.107.124c32e1 n1 | 0 | 0 | — |
| `icloud.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | brkgls.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=10 mx02.mail.icloud.com., 10 mx01.mail.icloud.com.; TXT=v=spf1 ip4:17.41.0.0/16 ip4:17.58.0.0/16 ip4:17.142.0.0/15 ip4:17.57.155.0/24 ip4:17.57.156.0/24 ip4:144.178.36.0/24 ip4:144.178.38.0/24 ip4:112.19.199.64/29 ip4:112.19.242.64/29 ip4:222.73.195.64/29 ip4:157.255.1.64/29" " ip4:106.39.212.64/29 ip4:123.126.78.64/29 ip4:183.240.219.64/29 ip4:39.156.163.64/29 ip4:57.103.64.0/18" " ip6:2a01:b747:3000:200::/56 ip6:2a01:b747:3001:200::/56 ip6:2a01:b747:3002:200::/56 ip6:2a01:b747:3003:200::/56 ip6:2a01:b747:3004:200::/56 ip6:2a01:b747:3005:200::/56 ip6:2a01:b747:3006:200::/56 ~all, google-site-verification=Ik3jMkCjHnUgyIoFR0Kw74srr0H5ynFmUk8fyY1uBck, google-site-verification=knAEOH4QxR29I4gjRkpkvmUmP2AA7WrDk8Kq0wu9g9o | 0 | 0 | — |
| `lb._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `logs.us-east-1.amazonaws.com` | pcap_sni | 3.236.94.219, 3.236.94.170, 3.236.94.163, 3.236.94.211, 3.236.94.187, 44.202.79.222, 44.202.79.167, 44.202.79.212 | ec2-3-236-94-163.compute-1.amazonaws.com, ec2-3-236-94-170.compute-1.amazonaws.com, ec2-3-236-94-187.compute-1.amazonaws.com, ec2-3-236-94-211.compute-1.amazonaws.com, ec2-3-236-94-219.compute-1.amazonaws.com, ec2-44-202-79-167.compute-1.amazonaws.com, ec2-44-202-79-212.compute-1.amazonaws.com, ec2-44-202-79-222.compute-1.amazonaws.com | — | AMAZO-4, AT-88-Z | 3.236.94.219=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.170=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.163=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.211=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.187=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 44.202.79.222=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        U | A=3.236.94.219, 3.236.94.170, 3.236.94.163, 3.236.94.211, 3.236.94.187, 44.202.79.222; AAAA=—; CNAME=—; MX=— | 0 | 0 | dig_txt:timeout:dig |
| `ssl.gstatic.com` | pcap_dns | 142.251.218.163, 2607:f8b0:4005:815::2003 | ncsfoa-ak-in-f3.1e100.net, pnsfoa-af-in-x03.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.163=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:815::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.163; AAAA=2607:f8b0:4005:815::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |






**Capture finalize:** session_id=439b84af78df


#### Competitor surface (provider YAML probes)


*`competitor_surface` is null; no competitor data for this run.*


#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "194.195.93.96",
    "country_code": "US",
    "region": "California",
    "city": "San Jose",
    "connection": {
      "asn": 212238,
      "org": "Packethub S.A.",
      "isp": "Datacamp Limited",
      "domain": "packethub.net"
    },
    "location_id": "us-california-san-jose-96",
    "location_label": "San Jose, California, United States"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260501T100504Z-cc878634",
  "timestamp_utc": "2026-05-01T10:06:01.781103+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-san-jose-96",
  "vpn_location_label": "San Jose, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "194.195.93.96",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "194.195.93.96",
      "ipv6": null,
      "raw_excerpt": "194.195.93.96",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "194.195.93.96",
      "ipv6": null,
      "raw_excerpt": "194.195.93.96",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "194.195.93.96",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"194.195.93.96\"}",
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
        "194.195.93.90"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "194.195.93.96"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "3b9f4e9c-6b38-475e-a1c6-f326f99f42dd.local",
      "port": 49400,
      "raw": "candidate:1153250707 1 udp 2113937151 3b9f4e9c-6b38-475e-a1c6-f326f99f42dd.local 49400 typ host generation 0 ufrag nOCi network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "194.195.93.96",
      "port": 53546,
      "raw": "candidate:1151906997 1 udp 1677729535 194.195.93.96 53546 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag nOCi network-cost 999"
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
    "holder": "CDNEXT Datacamp Limited",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [212238]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 212238,
        "holder": "CDNEXT Datacamp Limited",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (194.195.93.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260501100527-2a3ceaf3-0bc5-4082-8020-438595b2d7c0",
            "process_time": 61,
            "server_id": "app171",
            "build_version": "v0.9.15-2026.04.30",
            "pipeline": "1248748",
            "status": "ok",
            "status_code": 200,
            "time": "2026-05-01T10:05:27.171183",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 212238,
                  "holder": "CDNEXT Datacamp Limited"
                }
              ],
              "related_prefixes": [],
              "resource": "194.195.93.0/24",
              "type": "prefix",
              "block": {
                "resource": "194.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-05-01T00:00:00",
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
          "raw_line": "212238 | 194.195.93.0/24 | DE | ripencc | 1995-09-14",
          "parts": [
            "212238",
            "194.195.93.0/24",
            "DE",
            "ripencc",
            "1995-09-14"
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
  "policies": [],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/194.195.93.96",
    "https://test-ipv6.com/",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260501T100504Z-cc878634/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/webrtc",
    "ipv6_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/fingerprint",
    "attribution_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/policy",
    "competitor_probe_dir": null,
    "browserleaks_probe_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": null,
    "transitions_json": null,
    "website_exposure_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/website_exposure",
    "capture_dir": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/capture"
  },
  "competitor_surface": null,
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t194.195.93.96\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tCalifornia\nCity\tSan Francisco\nISP\tDatacamp Limited\nOrganization\tPackethub S.A\nNetwork\tAS212238 Datacamp Limited (VPN, VPSH, TOR, CONTENT)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Los_Angeles (PDT)\nLocal Time\tFri, 01 May 2026 03:05:37 -0700\nCoordinates\t37.7749,-122.4190\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t194.195.93.96\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t17 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t437f182f3a134158cde58fe599adcf65\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t194.195.93.0 - 194.195.93.255\nCIDR\t194.195.93.0/24\nName\tPACKETHUB-20220731\nHandle\t194.195.93.0 - 194.195.93.255\nParent Handle\t194.195.80.0 - 194.195.95.255\nNet Type\tASSIGNED PA\nCountry\tUnited States\nRegistration\tSun, 31 Jul 2022 06:29:12 GMT\nLast Changed\tFri, 19 Aug 2022 08:49:03 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (456)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t194.195.93.96\nISP\tDatacamp Limited\nLocation\tUnited States, San Francisco\nDNS Leak Test\nTest Results\tFound 11 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n194.195.93.14\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.87\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.88\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.89\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.90\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.91\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.92\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.93\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.94\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.95\tDatacamp Limited\tUnited States, San Francisco\n194.195.93.96\tDatacamp Limited\tUnited States, San Francisco\nLeave a Comment (245)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t194.195.93.96\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t194.195.93.96\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (221)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_c6f01690e9bd\nJA3\t562db65e9501d7230c96973ef9f206e2\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x3A3A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0xCACA\nGREASE\n\n\n0x000D\nsignature_algorithms\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x0023\nsession_ticket\n\n\n0x002B\nsupported_versions\n\n\n0x0005\nstatus_request\n\n\n0x001B\ncompress_certificate\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x000A\nsupported_groups\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0033\nkey_share\n\n\n0x0017\nextended_main_secret\n\n\n0x000B\nec_point_formats\n\n\n0x0000\nserver_name\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0xFF01\nrenegotiation_info\n\n\n0x44CD\napplication_settings\n\n\n0xAAAA\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t3\nenc_length\t32\npayload_length\t176\nkey_share\nclient_shares\t\n0xAAAA\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.browse",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-7737d9dd",
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
        "notes": "No web or portal probes in run."
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
        "answer_summary": "Exit IPv4 194.195.93.96; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 194.195.93.96.",
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
        "notes": "No web or portal probes."
      },
      {
        "question_id": "EXIT-001",
        "question_text": "What exit IP is assigned for each region?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 194.195.93.96 for location us-california-san-jose-96.",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 96.93.195.194.in-addr.arpa.",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
        "answer_status": "answered",
        "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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
  "website_exposure_methodology": {
    "methodology_schema_version": "1.0",
    "evidence_tier_note": "Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.",
    "phases": {
      "1_fetch": "urls_from_config_and_har_summaries",
      "2_extract": "hosts_parsed_via_urlparse",
      "3_dedupe": "unique_hosts=0",
      "4_resolve": "A_AAAA_optional_public_ip_attribution",
      "5_whois_via_attribution": "sample_only_for_selected_public_ips",
      "6_classify": "har_tracker_cdn_hints_plus_unknown_bucket",
      "7_document": "machine_json_hosts_inventory_plus_resolver_samples",
      "8_dns_infra": "skipped",
      "9_inventory": "rows=1"
    },
    "hosts_inventory": {
      "unique_hosts": [],
      "approx_count": 0,
      "sources": {}
    },
    "resolver_results": {},
    "classifications": {
      "rows": [],
      "notes": "Heuristic tags from HAR hints + host presence only."
    },
    "phase8_dns_infra": {},
    "phase9_third_party_inventory": [
      {
        "company_hypothesis": "(provider first-party)",
        "role": "marketing_and_app_surface",
        "how_discovered": "config_urls",
        "evidence_summary": "~0 web hosts observed",
        "evidence_tier": "desk_automation"
      }
    ],
    "raw_relpaths": {
      "hosts_inventory": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/website_exposure/hosts_inventory.json",
      "resolver_sample": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/website_exposure/resolver_sample.json",
      "phase9_inventory": "runs/nordvpn-20260501T100504Z-cc878634/raw/us-california-san-jose-96/website_exposure/phase9_inventory.json"
    },
    "limits": [
      "Does_not_replace_human_narrative_for_executive_disclosure",
      "Cloudflare_or_bot_WAF_may_distort_HAR_coverage",
      "Skipped_phase8_no_provider_domains_in_config"
    ],
    "errors": []
  },
  "pcap_derived": {
    "schema_version": "1.0",
    "source_pcap": "/Users/alauder/Source/doxx/vpn-leaks/.vpn-leaks/capture/session_439b84af78df.pcap",
    "packet_counts": {
      "total": 12015,
      "l3_seen": 12015
    },
    "flows_unique_estimate": 357,
    "flows_sample": [
      {
        "key": [
          "ip4",
          "c2c35d0d",
          "0a00002b",
          "51820",
          "61247"
        ],
        "bytes": 2352118
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "c2c35d0d",
          "61247",
          "51820"
        ],
        "bytes": 1537013
      },
      {
        "key": [
          "ip4",
          "97654306",
          "0a00002b",
          "443",
          "59695"
        ],
        "bytes": 1057625
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a00002b",
          "443",
          "62483"
        ],
        "bytes": 800360
      },
      {
        "key": [
          "ip4",
          "2cff4229",
          "0a00002b",
          "443",
          "53473"
        ],
        "bytes": 70340
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a00002b",
          "443",
          "58695"
        ],
        "bytes": 33615
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a00002b",
          "443",
          "60794"
        ],
        "bytes": 32393
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "03ec5e85",
          "62473",
          "443"
        ],
        "bytes": 28428
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd2f67d",
          "62475",
          "443"
        ],
        "bytes": 27262
      },
      {
        "key": [
          "ip4",
          "08080404",
          "0a00002b",
          "443",
          "56936"
        ],
        "bytes": 26190
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efb9777",
          "55314",
          "443"
        ],
        "bytes": 23832
      },
      {
        "key": [
          "ip4",
          "6810d0cb",
          "0a00002b",
          "443",
          "55788"
        ],
        "bytes": 17526
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "681222f4",
          "62483",
          "443"
        ],
        "bytes": 16257
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "53964"
        ],
        "bytes": 14707
      },
      {
        "key": [
          "ip4",
          "97650306",
          "0a00002b",
          "443",
          "62476"
        ],
        "bytes": 13323
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "97654306",
          "59695",
          "443"
        ],
        "bytes": 12115
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a00002b",
          "443",
          "62485"
        ],
        "bytes": 12109
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a00002b",
          "443",
          "62494"
        ],
        "bytes": 12086
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080404",
          "56936",
          "443"
        ],
        "bytes": 12046
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a00002b",
          "443",
          "62482"
        ],
        "bytes": 11947
      },
      {
        "key": [
          "ip4",
          "8efbda6e",
          "0a00002b",
          "443",
          "59881"
        ],
        "bytes": 11912
      },
      {
        "key": [
          "ip4",
          "8efbda6e",
          "0a00002b",
          "443",
          "53856"
        ],
        "bytes": 11711
      },
      {
        "key": [
          "ip4",
          "8efbdb0a",
          "0a00002b",
          "443",
          "60523"
        ],
        "bytes": 11635
      },
      {
        "key": [
          "ip4",
          "d8ef24df",
          "0a00002b",
          "443",
          "59014"
        ],
        "bytes": 11397
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a00002b",
          "443",
          "62493"
        ],
        "bytes": 11278
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "681222f4",
          "62493",
          "443"
        ],
        "bytes": 10066
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "a27d2802",
          "61812",
          "443"
        ],
        "bytes": 9785
      },
      {
        "key": [
          "ip4",
          "035f2cb6",
          "0a00002b",
          "8884",
          "62480"
        ],
        "bytes": 9684
      },
      {
        "key": [
          "ip4",
          "8efbd623",
          "0a00002b",
          "443",
          "65258"
        ],
        "bytes": 9482
      },
      {
        "key": [
          "ip4",
          "17432198",
          "0a00002b",
          "443",
          "62484"
        ],
        "bytes": 8582
      },
      {
        "key": [
          "ip4",
          "0ddb2664",
          "0a00002b",
          "443",
          "62474"
        ],
        "bytes": 8555
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbd623",
          "65258",
          "443"
        ],
        "bytes": 8502
      },
      {
        "key": [
          "ip4",
          "11fd900a",
          "0a00002b",
          "443",
          "62491"
        ],
        "bytes": 8441
      },
      {
        "key": [
          "ip4",
          "11fd058e",
          "0a00002b",
          "443",
          "62477"
        ],
        "bytes": 8196
      },
      {
        "key": [
          "ip4",
          "2cd2f67d",
          "0a00002b",
          "443",
          "62475"
        ],
        "bytes": 7995
      },
      {
        "key": [
          "ip4",
          "11fd900a",
          "0a00002b",
          "443",
          "62492"
        ],
        "bytes": 7814
      },
      {
        "key": [
          "ip4",
          "11fd05a0",
          "0a00002b",
          "443",
          "62488"
        ],
        "bytes": 7719
      },
      {
        "key": [
          "ip4",
          "11fd05a0",
          "0a00002b",
          "443",
          "62490"
        ],
        "bytes": 7584
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbda6e",
          "53856",
          "443"
        ],
        "bytes": 7513
      },
      {
        "key": [
          "ip4",
          "97654306",
          "0a00002b",
          "443",
          "62478"
        ],
        "bytes": 7386
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68109b6f",
          "60794",
          "443"
        ],
        "bytes": 7343
      },
      {
        "key": [
          "ip4",
          "17432198",
          "0a00002b",
          "443",
          "62481"
        ],
        "bytes": 7228
      },
      {
        "key": [
          "ip4",
          "97650306",
          "0a00002b",
          "443",
          "59314"
        ],
        "bytes": 7192
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdb0a",
          "60523",
          "443"
        ],
        "bytes": 7066
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6810d0cb",
          "55788",
          "443"
        ],
        "bytes": 6989
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "d8ef24df",
          "59014",
          "443"
        ],
        "bytes": 6895
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbda6e",
          "59881",
          "443"
        ],
        "bytes": 6686
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 6280
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdace",
          "54138",
          "443"
        ],
        "bytes": 6274
      },
      {
        "key": [
          "ip4",
          "d8ef24df",
          "0a00002b",
          "443",
          "62486"
        ],
        "bytes": 6223
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68109b6f",
          "58695",
          "443"
        ],
        "bytes": 6020
      },
      {
        "key": [
          "ip4",
          "9df00b23",
          "0a00002b",
          "443",
          "54394"
        ],
        "bytes": 5907
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62479"
        ],
        "bytes": 5884
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "342864c3",
          "50070",
          "443"
        ],
        "bytes": 5702
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "97650306",
          "62476",
          "443"
        ],
        "bytes": 5582
      },
      {
        "key": [
          "ip4",
          "acd90c6e",
          "0a00002b",
          "443",
          "59412"
        ],
        "bytes": 5396
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "17432198",
          "62484",
          "443"
        ],
        "bytes": 5185
      },
      {
        "key": [
          "ip4",
          "342864c3",
          "0a00002b",
          "443",
          "50070"
        ],
        "bytes": 4538
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "11fd900a",
          "62491",
          "443"
        ],
        "bytes": 4432
      },
      {
        "key": [
          "ip4",
          "2ccfc958",
          "0a00002b",
          "443",
          "62377"
        ],
        "bytes": 4415
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6812127d",
          "56675",
          "443"
        ],
        "bytes": 4411
      },
      {
        "key": [
          "ip4",
          "0a000007",
          "ffffffff",
          "49154",
          "6666"
        ],
        "bytes": 4240
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "11fd900a",
          "62492",
          "443"
        ],
        "bytes": 4232
      },
      {
        "key": [
          "ip4",
          "404ec801",
          "0a00002b",
          "443",
          "62489"
        ],
        "bytes": 4219
      },
      {
        "key": [
          "ip4",
          "a29f88ea",
          "0a00002b",
          "443",
          "61673"
        ],
        "bytes": 4172
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cff4229",
          "53473",
          "443"
        ],
        "bytes": 3927
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "97650306",
          "59314",
          "443"
        ],
        "bytes": 3905
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6812127d",
          "56841",
          "443"
        ],
        "bytes": 3606
      },
      {
        "key": [
          "ip4",
          "8efb9777",
          "0a00002b",
          "443",
          "55314"
        ],
        "bytes": 3576
      },
      {
        "key": [
          "ip4",
          "03ec5e85",
          "0a00002b",
          "443",
          "62473"
        ],
        "bytes": 3526
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a00002b",
          "443",
          "60342"
        ],
        "bytes": 3359
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "17432198",
          "62481",
          "443"
        ],
        "bytes": 3346
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "681222f4",
          "62482",
          "443"
        ],
        "bytes": 3320
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "681222f4",
          "62485",
          "443"
        ],
        "bytes": 3303
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62479",
          "443"
        ],
        "bytes": 3245
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "681222f4",
          "62494",
          "443"
        ],
        "bytes": 3171
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "11fd05a0",
          "62488",
          "443"
        ],
        "bytes": 3128
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "11fd05a0",
          "62490",
          "443"
        ],
        "bytes": 3079
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62498",
          "443"
        ],
        "bytes": 3048
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "11fd058e",
          "62477",
          "443"
        ],
        "bytes": 2982
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62495",
          "443"
        ],
        "bytes": 2981
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62497",
          "443"
        ],
        "bytes": 2972
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62496",
          "443"
        ],
        "bytes": 2969
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62499",
          "443"
        ],
        "bytes": 2969
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "9df00b23",
          "54394",
          "443"
        ],
        "bytes": 2868
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6812127d",
          "56676",
          "443"
        ],
        "bytes": 2757
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62500"
        ],
        "bytes": 2753
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0ddb2664",
          "62474",
          "443"
        ],
        "bytes": 2749
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "0a00002b",
          "7000",
          "62533"
        ],
        "bytes": 2729
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a00002b",
          "7000",
          "62502"
        ],
        "bytes": 2726
      },
      {
        "key": [
          "ip4",
          "68121f54",
          "0a00002b",
          "443",
          "61180"
        ],
        "bytes": 2645
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "03e99e1f",
          "62324",
          "443"
        ],
        "bytes": 2606
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2295429a",
          "62325",
          "443"
        ],
        "bytes": 2604
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62500",
          "443"
        ],
        "bytes": 2549
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "404ec801",
          "62489",
          "443"
        ],
        "bytes": 2527
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a00002b",
          "443",
          "54138"
        ],
        "bytes": 2512
      },
      {
        "key": [
          "ip4",
          "0a000027",
          "0a00002b",
          "7000",
          "62501"
        ],
        "bytes": 2417
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "035f2cb6",
          "62480",
          "8884"
        ],
        "bytes": 2378
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "97654306",
          "62478",
          "443"
        ],
        "bytes": 2335
      },
      {
        "key": [
          "ip4",
          "acd90c6a",
          "0a00002b",
          "443",
          "58680"
        ],
        "bytes": 2328
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a00002b",
          "443",
          "61869"
        ],
        "bytes": 2270
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "d8ef24df",
          "62486",
          "443"
        ],
        "bytes": 1952
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62498"
        ],
        "bytes": 1907
      },
      {
        "key": [
          "ip4",
          "68120e83",
          "0a00002b",
          "443",
          "61072"
        ],
        "bytes": 1888
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2ccfc958",
          "62377",
          "443"
        ],
        "bytes": 1695
      },
      {
        "key": [
          "ip4",
          "68120f83",
          "0a00002b",
          "443",
          "57733"
        ],
        "bytes": 1684
      },
      {
        "key": [
          "ip4",
          "8efbd28a",
          "0a00002b",
          "443",
          "57573"
        ],
        "bytes": 1665
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbd62e",
          "58412",
          "443"
        ],
        "bytes": 1657
      },
      {
        "key": [
          "ip4",
          "a27d2801",
          "0a00002b",
          "443",
          "61848"
        ],
        "bytes": 1629
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "acd90c6e",
          "59412",
          "443"
        ],
        "bytes": 1620
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62497"
        ],
        "bytes": 1572
      },
      {
        "key": [
          "ip4",
          "0a000020",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 1572
      },
      {
        "key": [
          "ip4",
          "a27d2802",
          "0a00002b",
          "443",
          "61812"
        ],
        "bytes": 1524
      },
      {
        "key": [
          "ip4",
          "2295429a",
          "0a00002b",
          "443",
          "62325"
        ],
        "bytes": 1483
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62495"
        ],
        "bytes": 1479
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62496"
        ],
        "bytes": 1479
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62499"
        ],
        "bytes": 1479
      },
      {
        "key": [
          "ip6",
          "fe800000000000001c180eef8a345da8",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 1469
      },
      {
        "key": [
          "ip4",
          "03dc5d00",
          "0a00002b",
          "443",
          "62197"
        ],
        "bytes": 1188
      },
      {
        "key": [
          "ip4",
          "03e99e1f",
          "0a00002b",
          "443",
          "62324"
        ],
        "bytes": 1129
      },
      {
        "key": [
          "ip4",
          "3990dd86",
          "0a00002b",
          "443",
          "60971"
        ],
        "bytes": 1059
      },
      {
        "key": [
          "ip4",
          "8efbdaea",
          "0a00002b",
          "443",
          "63146"
        ],
        "bytes": 1047
      },
      {
        "key": [
          "ip4",
          "68122715",
          "0a00002b",
          "443",
          "61574"
        ],
        "bytes": 1032
      },
      {
        "key": [
          "ip4",
          "68122715",
          "0a00002b",
          "443",
          "61623"
        ],
        "bytes": 1032
      },
      {
        "key": [
          "ip4",
          "68122715",
          "0a00002b",
          "443",
          "61955"
        ],
        "bytes": 1032
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "03dc5d00",
          "62197",
          "443"
        ],
        "bytes": 972
      },
      {
        "key": [
          "ip4",
          "12612447",
          "0a00002b",
          "443",
          "62176"
        ],
        "bytes": 970
      },
      {
        "key": [
          "ip4",
          "ac4094eb",
          "0a00002b",
          "443",
          "61296"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "ac4094eb",
          "0a00002b",
          "443",
          "61350"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "ac4094eb",
          "0a00002b",
          "443",
          "61315"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "ac4094eb",
          "0a00002b",
          "443",
          "61317"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "68122715",
          "0a00002b",
          "443",
          "61825"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "ac4094eb",
          "0a00002b",
          "443",
          "61158"
        ],
        "bytes": 966
      },
      {
        "key": [
          "ip4",
          "6431ddf9",
          "0a00002b",
          "443",
          "56789"
        ],
        "bytes": 939
      },
      {
        "key": [
          "ip4",
          "8c52701a",
          "0a00002b",
          "443",
          "61381"
        ],
        "bytes": 929
      },
      {
        "key": [
          "ip4",
          "4b024c08",
          "0a00002b",
          "443",
          "62326"
        ],
        "bytes": 924
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "acd90c6a",
          "58680",
          "443"
        ],
        "bytes": 905
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a00002b",
          "443",
          "58412"
        ],
        "bytes": 815
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "53964",
          "443"
        ],
        "bytes": 789
      },
      {
        "key": [
          "ip4",
          "8c527119",
          "0a00002b",
          "443",
          "62462"
        ],
        "bytes": 751
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68120f83",
          "57733",
          "443"
        ],
        "bytes": 706
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68120e83",
          "61072",
          "443"
        ],
        "bytes": 706
      },
      {
        "key": [
          "ip4",
          "0a000027",
          "0a00002b",
          "49152",
          "57448"
        ],
        "bytes": 706
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdaaa",
          "60342",
          "443"
        ],
        "bytes": 703
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57752"
        ],
        "bytes": 701
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57755"
        ],
        "bytes": 701
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57770"
        ],
        "bytes": 701
      },
      {
        "key": [
          "ip4",
          "038f880a",
          "0a00002b",
          "443",
          "60667"
        ],
        "bytes": 701
      },
      {
        "key": [
          "ip4",
          "12df828c",
          "0a00002b",
          "443",
          "50233"
        ],
        "bytes": 700
      },
      {
        "key": [
          "ip4",
          "2cd51518",
          "0a00002b",
          "443",
          "62472"
        ],
        "bytes": 683
      },
      {
        "key": [
          "ip4",
          "6812127d",
          "0a00002b",
          "443",
          "56675"
        ],
        "bytes": 683
      },
      {
        "key": [
          "ip4_raw",
          "08060001",
          "08000604",
          "0",
          "0"
        ],
        "bytes": 654
      },
      {
        "key": [
          "ip4",
          "103ab54b",
          "0a00002b",
          "443",
          "62145"
        ],
        "bytes": 649
      },
      {
        "key": [
          "ip4",
          "6812127d",
          "0a00002b",
          "443",
          "56676"
        ],
        "bytes": 607
      },
      {
        "key": [
          "ip4",
          "6812127d",
          "0a00002b",
          "443",
          "56841"
        ],
        "bytes": 605
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57745"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57747"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57741"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57758"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57748"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57768"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "103b766c",
          "0a00002b",
          "443",
          "60828"
        ],
        "bytes": 557
      },
      {
        "key": [
          "ip4",
          "103b766c",
          "0a00002b",
          "443",
          "60832"
        ],
        "bytes": 556
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57728"
        ],
        "bytes": 546
      },
      {
        "key": [
          "ip4",
          "0365e034",
          "0a00002b",
          "443",
          "62275"
        ],
        "bytes": 540
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "1261243c",
          "60924",
          "443"
        ],
        "bytes": 532
      },
      {
        "key": [
          "ip4",
          "0386fa3f",
          "0a00002b",
          "443",
          "60492"
        ],
        "bytes": 532
      },
      {
        "key": [
          "ip4",
          "103ab54b",
          "0a00002b",
          "443",
          "62147"
        ],
        "bytes": 531
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000027",
          "62501",
          "7000"
        ],
        "bytes": 531
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a00000e",
          "62502",
          "7000"
        ],
        "bytes": 531
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a00000d",
          "62533",
          "7000"
        ],
        "bytes": 531
      },
      {
        "key": [
          "ip4",
          "11fd0585",
          "0a00002b",
          "443",
          "62390"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "11fd058a",
          "0a00002b",
          "443",
          "62386"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "1725101d",
          "0a00002b",
          "443",
          "62384"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "11fd058c",
          "0a00002b",
          "443",
          "62402"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "17432168",
          "0a00002b",
          "443",
          "62266"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "1743214a",
          "0a00002b",
          "443",
          "62220"
        ],
        "bytes": 492
      },
      {
        "key": [
          "ip4",
          "a27d2801",
          "0a00002b",
          "443",
          "62469"
        ],
        "bytes": 489
      },
      {
        "key": [
          "ip4",
          "36f13c8f",
          "0a00002b",
          "443",
          "62192"
        ],
        "bytes": 474
      },
      {
        "key": [
          "ip4",
          "1714c633",
          "0a00002b",
          "443",
          "59247"
        ],
        "bytes": 468
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000027",
          "57448",
          "49152"
        ],
        "bytes": 463
      },
      {
        "key": [
          "ip4",
          "8efbdaae",
          "0a00002b",
          "443",
          "49531"
        ],
        "bytes": 442
      },
      {
        "key": [
          "ip4",
          "8efbdb2a",
          "0a00002b",
          "443",
          "59571"
        ],
        "bytes": 440
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "12612447",
          "62176",
          "443"
        ],
        "bytes": 427
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0365e034",
          "62275",
          "443"
        ],
        "bytes": 408
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "36f13c8f",
          "62192",
          "443"
        ],
        "bytes": 408
      },
      {
        "key": [
          "ip4",
          "1261243c",
          "0a00002b",
          "443",
          "60924"
        ],
        "bytes": 406
      },
      {
        "key": [
          "ip4",
          "8c527115",
          "0a00002b",
          "443",
          "62389"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "11399076",
          "0a00002b",
          "5223",
          "58837"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "11fd538f",
          "0a00002b",
          "443",
          "62383"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "11fd058a",
          "0a00002b",
          "443",
          "62387"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "0d3b1889",
          "0a00002b",
          "443",
          "55746"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57739"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57738"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "127674e3",
          "0a00002b",
          "443",
          "57725"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "11fd5385",
          "0a00002b",
          "443",
          "62401"
        ],
        "bytes": 402
      },
      {
        "key": [
          "ip4",
          "22954293",
          "0a00002b",
          "443",
          "62338"
        ],
        "bytes": 378
      },
      {
        "key": [
          "ip4",
          "3990dc8d",
          "0a00002b",
          "443",
          "57737"
        ],
        "bytes": 344
      },
      {
        "key": [
          "ip4",
          "3990dc8d",
          "0a00002b",
          "443",
          "49856"
        ],
        "bytes": 344
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "4b024c08",
          "62326",
          "443"
        ],
        "bytes": 342
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3990dc8d",
          "57737",
          "443"
        ],
        "bytes": 328
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3990dc8d",
          "49856",
          "443"
        ],
        "bytes": 328
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a00002b",
          "443",
          "58829"
        ],
        "bytes": 325
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3990dc91",
          "60034",
          "443"
        ],
        "bytes": 322
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "a29f88ea",
          "61673",
          "443"
        ],
        "bytes": 319
      },
      {
        "key": [
          "ip4",
          "3990dc91",
          "0a00002b",
          "443",
          "60034"
        ],
        "bytes": 314
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdaae",
          "49531",
          "443"
        ],
        "bytes": 298
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a00002b",
          "0",
          "0"
        ],
        "bytes": 294
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000001",
          "0",
          "0"
        ],
        "bytes": 294
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd51518",
          "62472",
          "443"
        ],
        "bytes": 288
      },
      {
        "key": [
          "ip4",
          "8efb9977",
          "0a00002b",
          "443",
          "65499"
        ],
        "bytes": 286
      },
      {
        "key": [
          "ip4",
          "8c527403",
          "0a00002b",
          "443",
          "62459"
        ],
        "bytes": 261
      },
      {
        "key": [
          "ip6",
          "fd0523cf1eff4faa04be995fe2298ad2",
          "fd0523cf1eff4faa04c9bcb35fce531c",
          "0",
          "0"
        ],
        "bytes": 258
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "a27d2801",
          "62469",
          "443"
        ],
        "bytes": 251
      },
      {
        "key": [
          "ip4",
          "3990dc8d",
          "0a00002b",
          "443",
          "57735"
        ],
        "bytes": 250
      },
      {
        "key": [
          "ip4",
          "17432194",
          "0a00002b",
          "443",
          "62425"
        ],
        "bytes": 222
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdb2a",
          "59571",
          "443"
        ],
        "bytes": 220
      },
      {
        "key": [
          "ip4",
          "1743219b",
          "0a00002b",
          "443",
          "62328"
        ],
        "bytes": 216
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "65128"
        ],
        "bytes": 215
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3647b1c9",
          "62399",
          "443"
        ],
        "bytes": 202
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3990dd86",
          "60971",
          "443"
        ],
        "bytes": 202
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57758",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57752",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57755",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57748",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57768",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57770",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "103b766c",
          "60828",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "038f880a",
          "60667",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "1743219b",
          "62328",
          "443"
        ],
        "bytes": 198
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "103b766c",
          "60832",
          "443"
        ],
        "bytes": 197
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0386fa3f",
          "60492",
          "443"
        ],
        "bytes": 197
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "12df828c",
          "50233",
          "443"
        ],
        "bytes": 197
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "103ab54b",
          "62147",
          "443"
        ],
        "bytes": 196
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "103ab54b",
          "62145",
          "443"
        ],
        "bytes": 196
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbda85",
          "62351",
          "443"
        ],
        "bytes": 186
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8c527403",
          "62459",
          "443"
        ],
        "bytes": 186
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "44289"
        ],
        "bytes": 182
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "17432194",
          "62425",
          "443"
        ],
        "bytes": 174
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "54546"
        ],
        "bytes": 173
      },
      {
        "key": [
          "ip4",
          "3647b1c9",
          "0a00002b",
          "443",
          "62399"
        ],
        "bytes": 171
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "3990dc8d",
          "57735",
          "443"
        ],
        "bytes": 164
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "ac4094eb",
          "61296",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "ac4094eb",
          "61350",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "ac4094eb",
          "61315",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122715",
          "61574",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "ac4094eb",
          "61317",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122715",
          "61825",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "ac4094eb",
          "61158",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122715",
          "61623",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122715",
          "61955",
          "443"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip6",
          "fe800000000000003a22e2fffe4e4566",
          "ff020000000000000000000000010002",
          "546",
          "547"
        ],
        "bytes": 160
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "56745"
        ],
        "bytes": 151
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdace",
          "58829",
          "443"
        ],
        "bytes": 146
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdaea",
          "63146",
          "443"
        ],
        "bytes": 145
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "56763"
        ],
        "bytes": 145
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efb9977",
          "65499",
          "443"
        ],
        "bytes": 142
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "61687"
        ],
        "bytes": 138
      },
      {
        "key": [
          "ip4",
          "0a00001a",
          "effffffa",
          "1900",
          "1900"
        ],
        "bytes": 136
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "32271"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "8efbda85",
          "0a00002b",
          "443",
          "62351"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "222449f6",
          "0a00002b",
          "443",
          "62436"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "222449f6",
          "0a00002b",
          "443",
          "62435"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "222449f6",
          "62436",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "222449f6",
          "62435",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "222449f6",
          "0a00002b",
          "443",
          "62434"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "222449f6",
          "62434",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "222449f6",
          "0a00002b",
          "443",
          "62437"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "222449f6",
          "62437",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdb0a",
          "62487",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68155e3a",
          "62438",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "62451",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "62449",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "62453",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "62450",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68122929",
          "62452",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "68115bbb",
          "62343",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "12f4d66a",
          "62445",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6812137d",
          "58851",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "12ad7981",
          "60944",
          "443"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip4",
          "8efb02bc",
          "0a000032",
          "5228",
          "49165"
        ],
        "bytes": 132
      },
      {
        "key": [
          "ip6",
          "fe8000000000000010489695fc3fc856",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 121
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "1714c633",
          "59247",
          "443"
        ],
        "bytes": 120
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "12517"
        ],
        "bytes": 108
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb02bc",
          "49165",
          "5228"
        ],
        "bytes": 108
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 101
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "61114",
          "53"
        ],
        "bytes": 97
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "49800",
          "53"
        ],
        "bytes": 97
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "61114"
        ],
        "bytes": 97
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "49800"
        ],
        "bytes": 97
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "62274",
          "53"
        ],
        "bytes": 96
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "62274"
        ],
        "bytes": 96
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000020",
          "3722",
          "3722"
        ],
        "bytes": 92
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "44289",
          "53"
        ],
        "bytes": 92
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "12517",
          "53"
        ],
        "bytes": 92
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "5749"
        ],
        "bytes": 91
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "56745",
          "53"
        ],
        "bytes": 91
      },
      {
        "key": [
          "ip6",
          "fe8000000000000014c3d760cd6235e0",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 90
      },
      {
        "key": [
          "ip6",
          "fe800000000000000042ec78e0ff5a42",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 90
      },
      {
        "key": [
          "ip6",
          "fe800000000000001c180eef8a345da8",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 90
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "59841"
        ],
        "bytes": 86
      },
      {
        "key": [
          "ip4",
          "0a000013",
          "0a00002b",
          "5353",
          "5353"
        ],
        "bytes": 86
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a00002b",
          "5353",
          "5353"
        ],
        "bytes": 86
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "0a00002b",
          "5353",
          "5353"
        ],
        "bytes": 86
      },
      {
        "key": [
          "ip4",
          "08080808",
          "0a00002b",
          "53",
          "56986"
        ],
        "bytes": 85
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "54546",
          "53"
        ],
        "bytes": 77
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "65128",
          "53"
        ],
        "bytes": 77
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "32271",
          "53"
        ],
        "bytes": 75
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "5749",
          "53"
        ],
        "bytes": 75
      },
      {
        "key": [
          "ip4",
          "8efbdb0a",
          "0a00002b",
          "443",
          "62487"
        ],
        "bytes": 74
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbda6e",
          "0",
          "0"
        ],
        "bytes": 70
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "56763",
          "53"
        ],
        "bytes": 70
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "59841",
          "53"
        ],
        "bytes": 70
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "d8ef24df",
          "0",
          "0"
        ],
        "bytes": 70
      },
      {
        "key": [
          "ip4",
          "0a000020",
          "0a00002b",
          "0",
          "0"
        ],
        "bytes": 70
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "61687",
          "53"
        ],
        "bytes": 69
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "08080808",
          "56986",
          "53"
        ],
        "bytes": 69
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57745",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57747",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "127674e3",
          "57741",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "8efa65bc",
          "0a00002b",
          "5228",
          "58843"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "22e0f8f9",
          "0a00002b",
          "443",
          "60473"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efbdaaa",
          "61869",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8c527115",
          "62389",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "22954293",
          "62338",
          "443"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68155e3a",
          "0a00002b",
          "443",
          "62438"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "12f4d66a",
          "0a00002b",
          "443",
          "62445"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "12ad7981",
          "0a00002b",
          "443",
          "60944"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "62451"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "6812137d",
          "0a00002b",
          "443",
          "58851"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68115bbb",
          "0a00002b",
          "443",
          "62343"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "62449"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "62452"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "62453"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "68122929",
          "0a00002b",
          "443",
          "62450"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a00002b",
          "49153",
          "57447"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "0a00002b",
          "49153",
          "57452"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a00000e",
          "57446",
          "49152"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000013",
          "57554",
          "49152"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000013",
          "57813",
          "49821"
        ],
        "bytes": 66
      },
      {
        "key": [
          "ip4",
          "2cd56209",
          "0a00002b",
          "443",
          "62362"
        ],
        "bytes": 60
      },
      {
        "key": [
          "ip4",
          "2cca4fb0",
          "0a00002b",
          "443",
          "62366"
        ],
        "bytes": 60
      },
      {
        "key": [
          "ip4",
          "2cca4fb0",
          "0a00002b",
          "443",
          "62365"
        ],
        "bytes": 60
      },
      {
        "key": [
          "ip4",
          "0a000030",
          "e00000fb",
          "0",
          "0"
        ],
        "bytes": 60
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "8efa65bc",
          "58843",
          "5228"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "22e0f8f9",
          "60473",
          "443"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cd56209",
          "62362",
          "443"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cca4fb0",
          "62366",
          "443"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "2cca4fb0",
          "62365",
          "443"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "6431ddf9",
          "56789",
          "443"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a00000e",
          "57447",
          "49153"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a00000d",
          "57452",
          "49153"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a00002b",
          "49152",
          "57446"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a000013",
          "0a00002b",
          "49152",
          "57554"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a000013",
          "0a00002b",
          "49821",
          "57813"
        ],
        "bytes": 54
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a00002b",
          "3722",
          "3722"
        ],
        "bytes": 46
      },
      {
        "key": [
          "ip6_raw",
          "2e09ef9608060001080006040002ce24",
          "2e09ef960a00002b92607b53ed620a00",
          "0",
          "0"
        ],
        "bytes": 42
      }
    ],
    "tls_clienthello_snis_unique": [
      "api2.cursor.sh",
      "cognito-identity.us-east-1.amazonaws.com",
      "firehose.us-east-1.amazonaws.com",
      "logs.us-east-1.amazonaws.com"
    ],
    "opaque_tls_hints": 47,
    "dns_hostnames_unique": [
      "apple.com",
      "b._dns-sd._udp.0.0.5.10.in-addr.arpa",
      "browser-intake-us5-datadoghq.com",
      "db._dns-sd._udp.0.0.5.10.in-addr.arpa",
      "doh-dns-apple-com.v.aaplimg.com",
      "doh.dns.apple.com",
      "icloud.com",
      "lb._dns-sd._udp.0.0.5.10.in-addr.arpa",
      "ssl.gstatic.com"
    ],
    "quic_udp_443_packets": 1748,
    "quic_heuristic_notes": 170,
    "top_inet_pairs_sample": [
      {
        "src": "194.195.93.13",
        "dst": "10.0.0.43",
        "bytes": 2352118
      },
      {
        "src": "10.0.0.43",
        "dst": "194.195.93.13",
        "bytes": 1537013
      },
      {
        "src": "151.101.67.6",
        "dst": "10.0.0.43",
        "bytes": 1065011
      },
      {
        "src": "104.18.34.244",
        "dst": "10.0.0.43",
        "bytes": 847780
      },
      {
        "src": "44.255.66.41",
        "dst": "10.0.0.43",
        "bytes": 70340
      },
      {
        "src": "104.16.155.111",
        "dst": "10.0.0.43",
        "bytes": 66008
      },
      {
        "src": "10.0.0.43",
        "dst": "104.18.34.244",
        "bytes": 36117
      },
      {
        "src": "10.0.0.43",
        "dst": "3.236.94.133",
        "bytes": 28428
      },
      {
        "src": "10.0.0.43",
        "dst": "44.210.246.125",
        "bytes": 27262
      },
      {
        "src": "8.8.4.4",
        "dst": "10.0.0.43",
        "bytes": 26190
      },
      {
        "src": "10.0.0.43",
        "dst": "142.251.151.119",
        "bytes": 23832
      },
      {
        "src": "142.251.218.110",
        "dst": "10.0.0.43",
        "bytes": 23623
      },
      {
        "src": "10.0.0.43",
        "dst": "44.213.21.24",
        "bytes": 21021
      },
      {
        "src": "151.101.3.6",
        "dst": "10.0.0.43",
        "bytes": 20515
      },
      {
        "src": "216.239.36.223",
        "dst": "10.0.0.43",
        "bytes": 17620
      },
      {
        "src": "104.16.208.203",
        "dst": "10.0.0.43",
        "bytes": 17526
      },
      {
        "src": "44.213.21.24",
        "dst": "10.0.0.43",
        "bytes": 17236
      },
      {
        "src": "17.253.144.10",
        "dst": "10.0.0.43",
        "bytes": 16255
      },
      {
        "src": "23.67.33.152",
        "dst": "10.0.0.43",
        "bytes": 15810
      },
      {
        "src": "17.253.5.160",
        "dst": "10.0.0.43",
        "bytes": 15303
      },
      {
        "src": "104.18.41.41",
        "dst": "10.0.0.43",
        "bytes": 15037
      },
      {
        "src": "10.0.0.43",
        "dst": "151.101.67.6",
        "bytes": 14450
      },
      {
        "src": "10.0.0.43",
        "dst": "142.251.218.110",
        "bytes": 14269
      },
      {
        "src": "10.0.0.43",
        "dst": "104.16.155.111",
        "bytes": 13363
      },
      {
        "src": "10.0.0.43",
        "dst": "8.8.4.4",
        "bytes": 12046
      },
      {
        "src": "142.251.219.10",
        "dst": "10.0.0.43",
        "bytes": 11709
      },
      {
        "src": "10.0.0.43",
        "dst": "104.18.18.125",
        "bytes": 10774
      },
      {
        "src": "10.0.0.43",
        "dst": "162.125.40.2",
        "bytes": 9785
      },
      {
        "src": "3.95.44.182",
        "dst": "10.0.0.43",
        "bytes": 9684
      },
      {
        "src": "10.0.0.43",
        "dst": "151.101.3.6",
        "bytes": 9487
      },
      {
        "src": "142.251.214.35",
        "dst": "10.0.0.43",
        "bytes": 9482
      },
      {
        "src": "10.0.0.43",
        "dst": "216.239.36.223",
        "bytes": 8917
      }
    ],
    "limits": [
      "ECH_ESNI_not_visible",
      "DoH_not_inferred_from_udp_53",
      "tcp_segmentation_may_fragment_clienthello",
      "inner_vpn_payload_may_be_opaque"
    ],
    "errors": [],
    "ja3_ja4": []
  },
  "capture_finalize": {
    "session_id": "439b84af78df",
    "finalized_at_utc": "2026-05-01T10:06:02.029110+00:00",
    "source_pcap_cache_path": "/Users/alauder/Source/doxx/vpn-leaks/.vpn-leaks/capture/session_439b84af78df.pcap",
    "finalize_errors": []
  },
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "194.195.93.96",
      "country_code": "US",
      "region": "California",
      "city": "San Jose",
      "connection": {
        "asn": 212238,
        "org": "Packethub S.A.",
        "isp": "Datacamp Limited",
        "domain": "packethub.net"
      },
      "location_id": "us-california-san-jose-96",
      "location_label": "San Jose, California, United States"
    }
  }
}
```

---



### nordvpn-20260501T104455Z-211c373f / us-california-san-jose-87



- **vpn_provider:** nordvpn
- **Label:** San Jose, California, United States
- **Path:** `runs/nordvpn-20260501T104455Z-211c373f/locations/us-california-san-jose-87/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-05-01T10:45:59.252017+00:00
- **connection_mode:** manual_gui

#### Runner environment

```json
{
  "os": "Darwin 25.4.0",
  "kernel": "25.4.0",
  "python": "3.12.13 (main, Mar  3 2026, 12:39:30) [Clang 21.0.0 (clang-2100.0.123.102)]",
  "browser": null,
  "vpn_protocol": "manual_gui",
  "vpn_client": null
}
```

#### Exit IP

| Field | Value |
|-------|-------|
| exit_ip_v4 | 185.211.32.87 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "185.211.32.87",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "185.211.32.87",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.211.32.87\"}",
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
      "185.211.32.89"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.211.32.87"
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
| host | udp | f777795e-e55c-459e-b82f-01dc905f9822.local | 49672 | `candidate:2386622520 1 udp 2113937151 f777795e-e55c-459e-b82f-01dc905f9822.local 49672 typ host generation 0 ufrag jqAZ network-cost 999` |
| srflx | udp | 185.211.32.87 | 60748 | `candidate:2387966238 1 udp 1677729535 185.211.32.87 60748 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag jqAZ network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


```json
{
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36",
  "language": "en-US",
  "hardwareConcurrency": 12,
  "platform": "MacIntel"
}
```


#### Attribution

```json
{
  "asn": 212238,
  "holder": "CDNEXT Datacamp Limited",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [212238]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 212238,
      "holder": "CDNEXT Datacamp Limited",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (185.211.32.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260501104522-b2f963fb-86f3-4e9b-b10e-17deef1dc9b8",
          "process_time": 59,
          "server_id": "app183",
          "build_version": "v0.9.15-2026.04.30",
          "pipeline": "1248748",
          "status": "ok",
          "status_code": 200,
          "time": "2026-05-01T10:45:22.123612",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 212238,
                "holder": "CDNEXT Datacamp Limited"
              }
            ],
            "related_prefixes": [],
            "resource": "185.211.32.0/24",
            "type": "prefix",
            "block": {
              "resource": "185.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-05-01T00:00:00",
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
        "raw_line": "212238 | 185.211.32.0/24 | DE | ripencc | 2017-06-30",
        "parts": [
          "212238",
          "185.211.32.0/24",
          "DE",
          "ripencc",
          "2017-06-30"
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
[]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/185.211.32.87`

- `https://test-ipv6.com/`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260501T104455Z-211c373f/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/webrtc",
  "ipv6_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/fingerprint",
  "attribution_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/policy",
  "competitor_probe_dir": null,
  "browserleaks_probe_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": null,
  "transitions_json": null,
  "website_exposure_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/website_exposure",
  "capture_dir": null
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
  "har_path": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-389897da",
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
      "notes": "No web or portal probes in run."
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
      "answer_summary": "Exit IPv4 185.211.32.87; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 185.211.32.87.",
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
      "notes": "No web or portal probes."
    },
    {
      "question_id": "EXIT-001",
      "question_text": "What exit IP is assigned for each region?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 185.211.32.87 for location us-california-san-jose-87.",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 87.32.211.185.in-addr.arpa.",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
      "answer_status": "answered",
      "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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


#### Website & DNS surface (summary)


*No surface/DNS summary for this location (`competitor_surface` / `extra.surface_probe` empty or absent).*


#### Automated website-exposure methodology & PCAP


**Desk automation note:** Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.

| Third-party inventory rows | Phase-8 domains with deep audit |
|---------------------------|--------------------------------|
| 1 | 0 |

**Inventory (sample)**

| Company (hypothesis) | Role | How discovered |
|---------------------|------|----------------|
| (provider first-party) | marketing_and_app_surface | config_urls |



**Methodology limits:** *Does_not_replace_human_narrative_for_executive_disclosure*; *Cloudflare_or_bot_WAF_may_distort_HAR_coverage*; *Skipped_phase8_no_provider_domains_in_config*





*No `pcap_derived` merge on this location (no **`--attach-capture`** / **`--with-pcap`**, missing active capture session at finalize, or empty PCAP artifact).*



#### Competitor surface (provider YAML probes)


*`competitor_surface` is null; no competitor data for this run.*


#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "185.211.32.87",
    "country_code": "US",
    "region": "California",
    "city": "San Jose",
    "connection": {
      "asn": 212238,
      "org": "Packethub S.A.",
      "isp": "Datacamp Limited",
      "domain": "packethub.net"
    },
    "location_id": "us-california-san-jose-87",
    "location_label": "San Jose, California, United States"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260501T104455Z-211c373f",
  "timestamp_utc": "2026-05-01T10:45:59.252017+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.13 (main, Mar  3 2026, 12:39:30) [Clang 21.0.0 (clang-2100.0.123.102)]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-san-jose-87",
  "vpn_location_label": "San Jose, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.211.32.87",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "185.211.32.87",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "185.211.32.87",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.211.32.87\"}",
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
        "185.211.32.89"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.211.32.87"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "f777795e-e55c-459e-b82f-01dc905f9822.local",
      "port": 49672,
      "raw": "candidate:2386622520 1 udp 2113937151 f777795e-e55c-459e-b82f-01dc905f9822.local 49672 typ host generation 0 ufrag jqAZ network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.211.32.87",
      "port": 60748,
      "raw": "candidate:2387966238 1 udp 1677729535 185.211.32.87 60748 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag jqAZ network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36",
    "language": "en-US",
    "hardwareConcurrency": 12,
    "platform": "MacIntel"
  },
  "attribution": {
    "asn": 212238,
    "holder": "CDNEXT Datacamp Limited",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [212238]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 212238,
        "holder": "CDNEXT Datacamp Limited",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (185.211.32.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260501104522-b2f963fb-86f3-4e9b-b10e-17deef1dc9b8",
            "process_time": 59,
            "server_id": "app183",
            "build_version": "v0.9.15-2026.04.30",
            "pipeline": "1248748",
            "status": "ok",
            "status_code": 200,
            "time": "2026-05-01T10:45:22.123612",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 212238,
                  "holder": "CDNEXT Datacamp Limited"
                }
              ],
              "related_prefixes": [],
              "resource": "185.211.32.0/24",
              "type": "prefix",
              "block": {
                "resource": "185.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-05-01T00:00:00",
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
          "raw_line": "212238 | 185.211.32.0/24 | DE | ripencc | 2017-06-30",
          "parts": [
            "212238",
            "185.211.32.0/24",
            "DE",
            "ripencc",
            "2017-06-30"
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
  "policies": [],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/185.211.32.87",
    "https://test-ipv6.com/",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260501T104455Z-211c373f/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/webrtc",
    "ipv6_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/fingerprint",
    "attribution_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/policy",
    "competitor_probe_dir": null,
    "browserleaks_probe_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": null,
    "transitions_json": null,
    "website_exposure_dir": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/website_exposure",
    "capture_dir": null
  },
  "competitor_surface": null,
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.211.32.87\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tCalifornia\nCity\tSan Francisco\nISP\tDatacamp Limited\nOrganization\tPackethub S.A\nNetwork\tAS212238 Datacamp Limited (VPN, VPSH, TOR, CONTENT)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Los_Angeles (PDT)\nLocal Time\tFri, 01 May 2026 03:45:35 -0700\nCoordinates\t37.7749,-122.4190\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.211.32.87\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t17 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t8d28422d0775d9cdec4b4638680b0cdf\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"HeadlessChrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.211.32.0 - 185.211.32.255\nCIDR\t185.211.32.0/24\nName\tPackethub-L20221011\nHandle\t185.211.32.0 - 185.211.32.255\nParent Handle\t185.211.32.0 - 185.211.34.255\nNet Type\tASSIGNED PA\nCountry\tUnited States\nRegistration\tMon, 23 Jun 2025 11:38:03 GMT\nLast Changed\tMon, 23 Jun 2025 11:38:03 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tDe-kis2-1-mnt\nHandle\tDe-kis2-1-mnt\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (456)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.211.32.87\nISP\tDatacamp Limited\nLocation\tUnited States, San Francisco\nDNS Leak Test\nTest Results\tFound 15 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.211.32.77\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.78\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.79\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.80\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.81\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.82\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.83\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.84\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.85\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.86\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.87\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.88\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.89\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.90\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.91\tDatacamp Limited\tUnited States, San Francisco\nLeave a Comment (245)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.211.32.87\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.211.32.87\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (221)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\tLoading\nTLS 1.1\tLoading\nTLS 1.0\tLoading\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\tLoading\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_f511ea7872b2\nJA3\t6feedea882a9f228fec16b668e4d076e\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x8A8A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x5A5A\nGREASE\n\n\n0x0023\nsession_ticket\n\n\n0x001B\ncompress_certificate\n\n\n0x0000\nserver_name\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0017\nextended_main_secret\n\n\n0x0033\nkey_share\n\n\n0x0005\nstatus_request\n\n\n0x000D\nsignature_algorithms\n\n\n0xFF01\nrenegotiation_info\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x000A\nsupported_groups\n\n\n0x002B\nsupported_versions\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x000B\nec_point_formats\n\n\n0x44CD\napplication_settings\n\n\n0xEAEA\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t23\nenc_length\t32\npayload_length\t240\nkey_share\nclient_shares\t\n0xAAAA\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.browserleaks.com\nsignature_algorithms\nalgo",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-389897da",
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
        "notes": "No web or portal probes in run."
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
        "answer_summary": "Exit IPv4 185.211.32.87; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 185.211.32.87.",
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
        "notes": "No web or portal probes."
      },
      {
        "question_id": "EXIT-001",
        "question_text": "What exit IP is assigned for each region?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 185.211.32.87 for location us-california-san-jose-87.",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 87.32.211.185.in-addr.arpa.",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
        "answer_status": "answered",
        "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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
  "website_exposure_methodology": {
    "methodology_schema_version": "1.0",
    "evidence_tier_note": "Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.",
    "phases": {
      "1_fetch": "urls_from_config_and_har_summaries",
      "2_extract": "hosts_parsed_via_urlparse",
      "3_dedupe": "unique_hosts=0",
      "4_resolve": "A_AAAA_optional_public_ip_attribution",
      "5_whois_via_attribution": "sample_only_for_selected_public_ips",
      "6_classify": "har_tracker_cdn_hints_plus_unknown_bucket",
      "7_document": "machine_json_hosts_inventory_plus_resolver_samples",
      "8_dns_infra": "skipped",
      "9_inventory": "rows=1"
    },
    "hosts_inventory": {
      "unique_hosts": [],
      "approx_count": 0,
      "sources": {}
    },
    "resolver_results": {},
    "classifications": {
      "rows": [],
      "notes": "Heuristic tags from HAR hints + host presence only."
    },
    "phase8_dns_infra": {},
    "phase9_third_party_inventory": [
      {
        "company_hypothesis": "(provider first-party)",
        "role": "marketing_and_app_surface",
        "how_discovered": "config_urls",
        "evidence_summary": "~0 web hosts observed",
        "evidence_tier": "desk_automation"
      }
    ],
    "raw_relpaths": {
      "hosts_inventory": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/website_exposure/hosts_inventory.json",
      "resolver_sample": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/website_exposure/resolver_sample.json",
      "phase9_inventory": "runs/nordvpn-20260501T104455Z-211c373f/raw/us-california-san-jose-87/website_exposure/phase9_inventory.json"
    },
    "limits": [
      "Does_not_replace_human_narrative_for_executive_disclosure",
      "Cloudflare_or_bot_WAF_may_distort_HAR_coverage",
      "Skipped_phase8_no_provider_domains_in_config"
    ],
    "errors": []
  },
  "pcap_derived": null,
  "capture_finalize": null,
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "185.211.32.87",
      "country_code": "US",
      "region": "California",
      "city": "San Jose",
      "connection": {
        "asn": 212238,
        "org": "Packethub S.A.",
        "isp": "Datacamp Limited",
        "domain": "packethub.net"
      },
      "location_id": "us-california-san-jose-87",
      "location_label": "San Jose, California, United States"
    }
  }
}
```

---



### nordvpn-20260501T105329Z-8cb49bd0 / us-california-san-jose-87



- **vpn_provider:** nordvpn
- **Label:** San Jose, California, United States
- **Path:** `runs/nordvpn-20260501T105329Z-8cb49bd0/locations/us-california-san-jose-87/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-05-01T10:54:20.994055+00:00
- **connection_mode:** manual_gui

#### Runner environment

```json
{
  "os": "Darwin 25.4.0",
  "kernel": "25.4.0",
  "python": "3.12.13 (main, Mar  3 2026, 12:39:30) [Clang 21.0.0 (clang-2100.0.123.102)]",
  "browser": null,
  "vpn_protocol": "manual_gui",
  "vpn_client": null
}
```

#### Exit IP

| Field | Value |
|-------|-------|
| exit_ip_v4 | 185.211.32.87 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "185.211.32.87",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "185.211.32.87",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.211.32.87",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.211.32.87\"}",
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
      "185.211.32.79"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.211.32.87"
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
| host | udp | 011feeb0-b708-42a0-bcd0-2452e16a6592.local | 65122 | `candidate:415465874 1 udp 2113937151 011feeb0-b708-42a0-bcd0-2452e16a6592.local 65122 typ host generation 0 ufrag mlxH network-cost 999` |
| srflx | udp | 185.211.32.87 | 38210 | `candidate:222472082 1 udp 1677729535 185.211.32.87 38210 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag mlxH network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


```json
{
  "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36",
  "language": "en-US",
  "hardwareConcurrency": 12,
  "platform": "MacIntel"
}
```


#### Attribution

```json
{
  "asn": 212238,
  "holder": "CDNEXT Datacamp Limited",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [212238]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 212238,
      "holder": "CDNEXT Datacamp Limited",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (185.211.32.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260501105348-678cc919-2e55-44ab-8433-9298100e8af3",
          "process_time": 61,
          "server_id": "app198",
          "build_version": "v0.9.15-2026.04.30",
          "pipeline": "1248748",
          "status": "ok",
          "status_code": 200,
          "time": "2026-05-01T10:53:48.652576",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 212238,
                "holder": "CDNEXT Datacamp Limited"
              }
            ],
            "related_prefixes": [],
            "resource": "185.211.32.0/24",
            "type": "prefix",
            "block": {
              "resource": "185.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-05-01T00:00:00",
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
        "raw_line": "212238 | 185.211.32.0/24 | DE | ripencc | 2017-06-30",
        "parts": [
          "212238",
          "185.211.32.0/24",
          "DE",
          "ripencc",
          "2017-06-30"
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
[]
```

#### Services contacted




- `browserleaks.com:playwright_chromium`

- `fingerprint:playwright_navigator`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api64.ipify.org`

- `https://browserleaks.com/dns`

- `https://browserleaks.com/ip`

- `https://browserleaks.com/tls`

- `https://browserleaks.com/webrtc`

- `https://ipleak.net/`

- `https://ipwho.is/185.211.32.87`

- `https://test-ipv6.com/`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/webrtc",
  "ipv6_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/fingerprint",
  "attribution_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/policy",
  "competitor_probe_dir": null,
  "browserleaks_probe_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": null,
  "transitions_json": null,
  "website_exposure_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/website_exposure",
  "capture_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/capture"
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
  "har_path": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-2ba3df10",
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
      "notes": "No web or portal probes in run."
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
      "answer_summary": "Exit IPv4 185.211.32.87; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 185.211.32.87.",
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
      "notes": "No web or portal probes."
    },
    {
      "question_id": "EXIT-001",
      "question_text": "What exit IP is assigned for each region?",
      "category": "exit_infrastructure",
      "testability": "DYNAMIC_FULL",
      "answer_status": "answered",
      "answer_summary": "Exit IPv4 185.211.32.87 for location us-california-san-jose-87.",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 87.32.211.185.in-addr.arpa.",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
      "answer_status": "answered",
      "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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


#### Website & DNS surface (summary)


*No surface/DNS summary for this location (`competitor_surface` / `extra.surface_probe` empty or absent).*


#### Automated website-exposure methodology & PCAP


**Desk automation note:** Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.

| Third-party inventory rows | Phase-8 domains with deep audit |
|---------------------------|--------------------------------|
| 1 | 0 |

**Inventory (sample)**

| Company (hypothesis) | Role | How discovered |
|---------------------|------|----------------|
| (provider first-party) | marketing_and_app_surface | config_urls |



**Methodology limits:** *Does_not_replace_human_narrative_for_executive_disclosure*; *Cloudflare_or_bot_WAF_may_distort_HAR_coverage*; *Skipped_phase8_no_provider_domains_in_config*





**PCAP-derived metadata** (no Wireshark; see `pcap_derived` in JSON)

| Unique flows (estimate) | Packets (total) |
|-------------------------|-----------------|
| 847 | 334139 |



**Cleartext DNS names (UDP/53 sample):** `1.courier-push-apple.com.akadns.net`, `1.courier-sandbox-push-apple.com.akadns.net`, `28-courier.push.apple.com`, `45.courier-push-apple.com.akadns.net`, `_8885._https.nc-mqtt.nordpass.com`, `accounts.google.com`, `api-toggle.nordpass.com`, `api.apple-cloudkit.com`, `api.apple-cloudkit.fe2.apple-dns.net`, `api.nordpass.com`, `apis.google.com`, `app-analytics-services.com`, `app-site-association.cdn-apple.com`, `apple.com`, `applytics.napps-1.com`, `auth.napps-1.com`, `auth.nordaccount.com`, `auth.nordpass.com`, `background-weighted.ls4-apple.com.akadns.net`, `bag-cdn.itunes-apple.com.akadns.net`, `chromewebstore.google.com`, `clients2.google.com`, `clients2.googleusercontent.com`, `clientservices.googleapis.com`, `content-autofill.googleapis.com`, `d.nordaccount.com`, `debug.nordpass.com`, `debug.nordsec.com`, `dns-tunnel-check.googlezip.net`, `doh-dns-apple-com.v.aaplimg.com`, `doh.dns.apple.com`, `downloads.napps-1.com`, `downloads.nordcdn.com`, `downloads.npass.app`, `edgedl.me.gvt1.com`, `eip-terr-na.cdp1.digicert.com.akahost.net`, `encrypted-tbn0.gstatic.com`, `feedback-pa.clients6.google.com`, `firebase-settings.crashlytics.com`, `firebaseinstallations.googleapis.com`, `firebaselogging-pa.googleapis.com`, `firebaseremoteconfig.googleapis.com`, `fonts.googleapis.com`, `fonts.gstatic.com`, `gdmf.apple.com`, `gdmf.v.aaplimg.com`, `get-bx.g.aaplimg.com`, `google-ohttp-relay-safebrowsing.fastly-edge.com`


**PCAP interpretation limits:** *ECH_ESNI_not_visible*; *DoH_not_inferred_from_udp_53*; *tcp_segmentation_may_fragment_clienthello*; *inner_vpn_payload_may_be_opaque*; *flows_sample_kept_top_512*



#### PCAP host intelligence




- Scope: public peer IPs from PCAP flows/pairs plus DNS/SNI hostnames from PCAP.

- Live lookups are fail-soft and may vary by resolver/time.



| Host | Source | IP / IPs | Reverse DNS | ASN | Owner | WHOIS summary | dig summary | Bytes | Flows | Lookup errors |
|------|--------|----------|-------------|-----|-------|---------------|-------------|-------|-------|---------------|
| `104.16.155.111` | pcap_peer_ip | 104.16.155.111 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 658208984 | 25 | reverse_dns_failed |
| `142.251.219.33` | pcap_peer_ip | 142.251.219.33 | ncsfoa-an-in-f1.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-an-in-f1.1e100.net | 28195734 | 12 | — |
| `34.104.35.123` | pcap_peer_ip | 34.104.35.123 | 123.35.104.34.bc.googleusercontent.com | — | GOOGL-2 | NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | PTR=123.35.104.34.bc.googleusercontent.com | 15581417 | 3 | — |
| `185.211.32.76` | pcap_peer_ip | 185.211.32.76 | — | AS136787 | Packethub-L20221011 | netname:        Packethub-L20221011 | country:        US | org-name:       Packethub S.A. | origin:         AS136787 | origin:         AS212238 | PTR=— | 5805622 | 4 | reverse_dns_failed |
| `104.18.42.225` | pcap_peer_ip | 104.18.42.225 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 4645794 | 10 | reverse_dns_failed |
| `142.251.157.119` | pcap_peer_ip | 142.251.157.119 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 3031506 | 4 | reverse_dns_failed |
| `142.251.218.142` | pcap_peer_ip | 142.251.218.142 | qro04s06-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=qro04s06-in-f14.1e100.net, pnsfoa-ad-in-f14.1e100.net | 2348934 | 22 | — |
| `142.251.155.119` | pcap_peer_ip | 142.251.155.119 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 1896888 | 8 | reverse_dns_failed |
| `104.18.34.244` | pcap_peer_ip | 104.18.34.244 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 1752416 | 11 | reverse_dns_failed |
| `104.18.19.225` | pcap_peer_ip | 104.18.19.225 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 1054090 | 3 | reverse_dns_failed |
| `142.251.218.206` | pcap_peer_ip | 142.251.218.206 | ncsfoa-ao-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ao-in-f14.1e100.net | 898101 | 17 | — |
| `142.251.218.131` | pcap_peer_ip | 142.251.218.131 | pnsfoa-ad-in-f3.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ad-in-f3.1e100.net, qro04s06-in-f3.1e100.net | 541903 | 17 | — |
| `142.251.219.3` | pcap_peer_ip | 142.251.219.3 | ncsfoa-aq-in-f3.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-aq-in-f3.1e100.net | 479546 | 7 | — |
| `142.251.219.14` | pcap_peer_ip | 142.251.219.14 | ncsfoa-aq-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-aq-in-f14.1e100.net | 441806 | 15 | — |
| `142.251.218.72` | pcap_peer_ip | 142.251.218.72 | pnsfoa-aa-in-f8.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-aa-in-f8.1e100.net | 440877 | 9 | — |
| `216.239.34.157` | pcap_peer_ip | 216.239.34.157 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 387203 | 7 | reverse_dns_failed |
| `142.251.214.46` | pcap_peer_ip | 142.251.214.46 | pnsfoa-ae-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ae-in-f14.1e100.net | 362306 | 25 | — |
| `142.250.101.84` | pcap_peer_ip | 142.250.101.84 | dz-in-f84.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dz-in-f84.1e100.net | 306929 | 9 | — |
| `104.18.5.45` | pcap_peer_ip | 104.18.5.45 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 282766 | 16 | reverse_dns_failed |
| `17.23.18.34` | pcap_peer_ip | 17.23.18.34 | — | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=— | 234979 | 3 | reverse_dns_failed |
| `142.251.219.35` | pcap_peer_ip | 142.251.219.35 | ncsfoa-an-in-f3.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-an-in-f3.1e100.net | 216147 | 5 | — |
| `104.16.156.111` | pcap_peer_ip | 104.16.156.111 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 183830 | 8 | reverse_dns_failed |
| `142.251.218.106` | pcap_peer_ip | 142.251.218.106 | pnsfoa-ab-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ab-in-f10.1e100.net | 135771 | 11 | — |
| `17.248.231.66` | pcap_peer_ip | 17.248.231.66 | — | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=— | 122827 | 3 | reverse_dns_failed |
| `172.217.12.110` | pcap_peer_ip | 172.217.12.110 | sfo03s33-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=sfo03s33-in-f14.1e100.net, atl26s14-in-f14.1e100.net | 74709 | 8 | — |
| `142.251.218.170` | pcap_peer_ip | 142.251.218.170 | ncsfoa-ak-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ak-in-f10.1e100.net | 72150 | 8 | — |
| `142.251.218.138` | pcap_peer_ip | 142.251.218.138 | qro04s06-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=qro04s06-in-f10.1e100.net, pnsfoa-ad-in-f10.1e100.net | 61006 | 10 | — |
| `172.217.12.106` | pcap_peer_ip | 172.217.12.106 | atl26s14-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=atl26s14-in-f10.1e100.net, sfo03s33-in-f10.1e100.net | 53084 | 8 | — |
| `142.251.218.110` | pcap_peer_ip | 142.251.218.110 | pnsfoa-ab-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ab-in-f14.1e100.net | 52347 | 6 | — |
| `151.101.41.91` | pcap_peer_ip | 151.101.41.91 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. | PTR=— | 44954 | 8 | reverse_dns_failed |
| `142.251.218.174` | pcap_peer_ip | 142.251.218.174 | ncsfoa-ak-in-f14.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-ak-in-f14.1e100.net | 35123 | 2 | — |
| `23.46.216.91` | pcap_peer_ip | 23.46.216.91 | a23-46-216-91.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-46-216-91.deploy.static.akamaitechnologies.com | 34426 | 2 | — |
| `98.87.225.182` | pcap_peer_ip | 98.87.225.182 | ec2-98-87-225-182.compute-1.amazonaws.com | — | AMAZO-4 | NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | PTR=ec2-98-87-225-182.compute-1.amazonaws.com | 33337 | 2 | — |
| `52.86.142.63` | pcap_peer_ip | 52.86.142.63 | ec2-52-86-142-63.compute-1.amazonaws.com | — | AT-88-Z | NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-52-86-142-63.compute-1.amazonaws.com | 32705 | 8 | — |
| `142.251.219.42` | pcap_peer_ip | 142.251.219.42 | ncsfoa-an-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-an-in-f10.1e100.net | 32290 | 4 | — |
| `172.64.153.55` | pcap_peer_ip | 172.64.153.55 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 32036 | 4 | reverse_dns_failed |
| `172.64.153.12` | pcap_peer_ip | 172.64.153.12 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 29769 | 4 | reverse_dns_failed |
| `142.251.214.42` | pcap_peer_ip | 142.251.214.42 | pnsfoa-ae-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ae-in-f10.1e100.net | 29129 | 4 | — |
| `54.225.99.62` | pcap_peer_ip | 54.225.99.62 | ec2-54-225-99-62.compute-1.amazonaws.com | — | AMAZON-2011L | NetName:        AMAZON-2011L | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | PTR=ec2-54-225-99-62.compute-1.amazonaws.com | 27460 | 10 | — |
| `17.248.231.65` | pcap_peer_ip | 17.248.231.65 | — | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=— | 27390 | 2 | reverse_dns_failed |
| `17.253.5.139` | pcap_peer_ip | 17.253.5.139 | ussjc2-vip-fx-105.a.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-105.a.aaplimg.com | 27351 | 4 | — |
| `17.253.5.162` | pcap_peer_ip | 17.253.5.162 | ussjc2-vip-fx-116.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-116.b.aaplimg.com | 23976 | 4 | — |
| `151.101.43.6` | pcap_peer_ip | 151.101.43.6 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. | PTR=— | 23662 | 2 | reverse_dns_failed |
| `17.253.127.134` | pcap_peer_ip | 17.253.127.134 | usdal2-vip-fx-102.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=usdal2-vip-fx-102.b.aaplimg.com | 22835 | 4 | — |
| `8.0.6.4` | pcap_peer_ip | 8.0.6.4 | dns-8-0-6-4.atlanta1.level3.net | — | LVLT-ORG-8-8 | NetName:        LVLT-ORG-8-8 | OriginAS: | Organization:   Level 3 Parent, LLC (LPL-141) | OrgName:        Level 3 Parent, LLC | Country:        US | PTR=DNS-8-0-6-4.Atlanta1.Level3.net | 22488 | 1 | — |
| `8.6.0.1` | pcap_peer_ip | 8.6.0.1 | — | — | LVLT-ORG-8-8 | NetName:        LVLT-ORG-8-8 | OriginAS: | Organization:   Level 3 Parent, LLC (LPL-141) | OrgName:        Level 3 Parent, LLC | Country:        US | PTR=— | 22488 | 1 | reverse_dns_failed |
| `17.57.144.118` | pcap_peer_ip | 17.57.144.118 | — | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=— | 21593 | 2 | reverse_dns_failed |
| `142.251.219.10` | pcap_peer_ip | 142.251.219.10 | ncsfoa-aq-in-f10.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-aq-in-f10.1e100.net | 18907 | 2 | — |
| `17.253.144.10` | pcap_peer_ip | 17.253.144.10 | brkgls.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=brkgls.com, icloud.com, iphone.apple.com, podcast.apple.com, appstore.com, firewire.apple.com, livepage.apple.com, seminars.apple.com, applejava.apple.com, world-any.aaplimg.com, advertising.apple.com, applescript.apple.com, applecomputer.co.kr, itunespartner.apple.com, iworktrialbuy.apple.com, safaricampaign.apple, aperturetrialbuy.apple.com, vipd-healthcheck.a01.3banana.com, squeakytoytrainingcamp.com, www.brkgls.com, asia.apple.com, apple.ca, apple.co.uk, apple.de, apple.es, apple.fr, apple.it, apple.nl, apple.com, apple.com.ai, apple.com.au, apple.com.bo, apple.com.cn, apple.com.co, apple.com.do, apple.com.gy, apple.com.hn, apple.com.lk, apple.com.mx, apple.com.my, apple.com.pa, apple.com.pe, apple.com.py, apple.com.sg, apple.com.tt, apple.com.uy, guide.apple.com, shake.apple.com | 18845 | 4 | — |
| `104.18.4.45` | pcap_peer_ip | 104.18.4.45 | — | — | CLOUDFLARENET | NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | PTR=— | 18356 | 4 | reverse_dns_failed |
| `142.251.218.98` | pcap_peer_ip | 142.251.218.98 | pnsfoa-ab-in-f2.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-ab-in-f2.1e100.net | 18233 | 2 | — |
| `142.251.218.66` | pcap_peer_ip | 142.251.218.66 | pnsfoa-aa-in-f2.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=pnsfoa-aa-in-f2.1e100.net | 14860 | 2 | — |
| `142.251.218.134` | pcap_peer_ip | 142.251.218.134 | qro04s06-in-f6.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=qro04s06-in-f6.1e100.net, pnsfoa-ad-in-f6.1e100.net | 14200 | 2 | — |
| `17.253.5.150` | pcap_peer_ip | 17.253.5.150 | ussjc2-vip-fx-110.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-110.b.aaplimg.com | 11596 | 2 | — |
| `216.239.34.223` | pcap_peer_ip | 216.239.34.223 | — | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=— | 11386 | 2 | reverse_dns_failed |
| `17.253.5.134` | pcap_peer_ip | 17.253.5.134 | ussjc2-vip-fx-102.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=ussjc2-vip-fx-102.b.aaplimg.com | 11249 | 2 | — |
| `17.253.83.202` | pcap_peer_ip | 17.253.83.202 | uslax1-vip-get-004.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=uslax1-vip-get-004.b.aaplimg.com | 10709 | 2 | — |
| `142.251.219.22` | pcap_peer_ip | 142.251.219.22 | ncsfoa-aq-in-f22.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=ncsfoa-aq-in-f22.1e100.net | 10078 | 2 | — |
| `17.253.83.198` | pcap_peer_ip | 17.253.83.198 | uslax1-vip-get-002.b.aaplimg.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=uslax1-vip-get-002.b.aaplimg.com | 9653 | 2 | — |
| `64.78.200.1` | pcap_peer_ip | 64.78.200.1 | doh.dns.apple.com | — | WOODYN | NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US | PTR=doh.dns.apple.com | 8376 | 2 | — |
| `23.11.33.159` | pcap_peer_ip | 23.11.33.159 | a23-11-33-159.deploy.static.akamaitechnologies.com | — | AKAMAI | NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | PTR=a23-11-33-159.deploy.static.akamaitechnologies.com | 3480 | 4 | — |
| `142.251.2.188` | pcap_peer_ip | 142.251.2.188 | dl-in-f188.1e100.net | — | GOOGLE | NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | PTR=dl-in-f188.1e100.net | 720 | 2 | — |
| `1.courier-push-apple.com.akadns.net` | pcap_dns | 17.57.144.118 | — | — | APPLE-WWNET | 17.57.144.118=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=us-sw-courier-4.push-apple.com.akadns.net., 17.57.144.118; AAAA=—; CNAME=us-sw-courier-4.push-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | — |
| `1.courier-sandbox-push-apple.com.akadns.net` | pcap_dns | 17.188.178.188, 17.188.143.222, 17.188.178.61, 17.188.178.220, 17.188.178.156, 17.188.143.3, 17.188.178.92, 17.188.178.124 | — | — | APPLE-WWNET | 17.188.178.188=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.143.222=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.178.61=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.178.220=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.178.156=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.143.3=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.188.178.92=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z)  | A=us-sandbox-courier-4.push-apple.com.akadns.net., 17.188.178.188, 17.188.143.222, 17.188.178.61, 17.188.178.220, 17.188.178.156; AAAA=—; CNAME=us-sandbox-courier-4.push-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | 17.188.178.188:reverse_dns_failed; 17.188.143.222:reverse_dns_failed; 17.188.178.61:reverse_dns_failed; 17.188.178.220:reverse_dns_failed; 17.188.178.156:reverse_dns_failed; 17.188.143.3:reverse_dns_failed; 17.188.178.92:reverse_dns_failed; 17.188.178.124:reverse_dns_failed |
| `28-courier.push.apple.com` | pcap_dns | 17.57.144.119 | — | — | APPLE-WWNET | 17.57.144.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=28.courier-push-apple.com.akadns.net., us-sw-courier-4.push-apple.com.akadns.net., 17.57.144.119; AAAA=—; CNAME=28.courier-push-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | 17.57.144.119:reverse_dns_failed |
| `45.courier-push-apple.com.akadns.net` | pcap_dns | 17.57.144.26 | — | — | APPLE-WWNET | 17.57.144.26=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=us-sw-courier-4.push-apple.com.akadns.net., 17.57.144.26; AAAA=—; CNAME=us-sw-courier-4.push-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | 17.57.144.26:reverse_dns_failed |
| `_8885._https.nc-mqtt.nordpass.com` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `accounts.google.com` | pcap_dns | — | — | — | — | — | A=192.0.0.88; AAAA=—; CNAME=—; MX=5 gmr-smtp-in.l.google.com., 40 alt4.gmr-smtp-in.l.google.com., 20 alt2.gmr-smtp-in.l.google.com., 10 alt1.gmr-smtp-in.l.google.com., 30 alt3.gmr-smtp-in.l.google.com.; TXT=google-site-verification=vK4ovh56lkrEBc4GqA6djmGEyFWtcujz3MuRk-wO9cc, v=spf1 redirect=_spf.google.com | 0 | 0 | — |
| `api-toggle.nordpass.com` | pcap_dns | 3.220.195.52, 98.88.138.188, 98.87.225.182 | ec2-3-220-195-52.compute-1.amazonaws.com, ec2-98-87-225-182.compute-1.amazonaws.com, ec2-98-88-138-188.compute-1.amazonaws.com | — | AMAZO-4, AT-88-Z | 3.220.195.52=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 98.88.138.188=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 98.87.225.182=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US | A=api-toggle.us.nordpass.com., 3.220.195.52, 98.88.138.188, 98.87.225.182; AAAA=—; CNAME=api-toggle.us.nordpass.com.; MX=—; TXT=— | 0 | 0 | — |
| `api.apple-cloudkit.com` | pcap_dns | 17.248.192.1, 17.248.192.52, 17.248.192.2, 17.248.192.28, 17.248.192.3 | — | — | APPLE-WWNET | 17.248.192.1=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.52=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.2=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.28=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.3=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=api.apple-cloudkit.fe2.apple-dns.net., 17.248.192.1, 17.248.192.52, 17.248.192.2, 17.248.192.28, 17.248.192.3; AAAA=—; CNAME=api.apple-cloudkit.fe2.apple-dns.net.; MX=—; TXT=— | 0 | 0 | 17.248.192.1:reverse_dns_failed; 17.248.192.52:reverse_dns_failed; 17.248.192.2:reverse_dns_failed; 17.248.192.28:reverse_dns_failed; 17.248.192.3:reverse_dns_failed |
| `api.apple-cloudkit.fe2.apple-dns.net` | pcap_dns | 17.248.192.52, 17.248.192.28, 17.248.192.3 | — | — | APPLE-WWNET | 17.248.192.52=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.28=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.248.192.3=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=17.248.192.52, 17.248.192.28, 17.248.192.3; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `api.nordpass.com` | pcap_dns | 104.18.4.45, 104.18.5.45, 2606:4700::6812:42d, 2606:4700::6812:52d | — | — | CLOUDFLARENET | 104.18.4.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.5.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:42d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:52d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.4.45, 104.18.5.45; AAAA=2606:4700::6812:42d, 2606:4700::6812:52d; CNAME=—; MX=—; TXT=— | 0 | 0 | 2606:4700::6812:42d:reverse_dns_failed; 2606:4700::6812:52d:reverse_dns_failed |
| `apis.google.com` | pcap_dns | 142.251.214.46, 2607:f8b0:4005:809::200e | pnsfoa-ad-in-x0e.1e100.net, pnsfoa-ae-in-f14.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.214.46=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:809::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=plus.l.google.com., 142.251.214.46; AAAA=plus.l.google.com., 2607:f8b0:4005:809::200e; CNAME=plus.l.google.com.; MX=—; TXT=— | 0 | 0 | — |
| `app-analytics-services.com` | pcap_dns | 172.217.12.110, 2607:f8b0:4005:80a::200e | sfo03s33-in-f14.1e100.net, sfo07s17-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 172.217.12.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80a::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=172.217.12.110; AAAA=2607:f8b0:4005:80a::200e; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `app-site-association.cdn-apple.com` | pcap_dns | 17.253.31.140, 17.253.83.135, 17.253.5.135, 17.253.83.150, 17.253.17.205, 17.253.31.141, 17.253.5.137, 17.253.17.210, 2620:149:a00:f000::132, 2620:149:a0c:f000::1, 2620:149:a06:f000::134, 2620:149:a21:f000::134 | uslax1-vip-fx-102.b.aaplimg.com, uslax1-vip-fx-103.a.aaplimg.com, uslax1-vip-fx-110.b.aaplimg.com, usscz2-vip-bx-001.aaplimg.com, usscz2-vip-bx-005.aaplimg.com, usscz2-vip-bx-010.aaplimg.com, ussea4-vip-fx-102.b.aaplimg.com, ussea4-vip-fx-105.b.aaplimg.com, ussea4-vip-fx-106.a.aaplimg.com, ussjc2-vip-fx-101.b.aaplimg.com, ussjc2-vip-fx-103.a.aaplimg.com, ussjc2-vip-fx-104.a.aaplimg.com | — | APPLE-WWNET | 17.253.31.140=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.83.135=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.5.135=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.83.150=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.205=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.31.141=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.5.137=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | Org | A=app-site-association.cdn-apple.com.akadns.net., app-site-association.g.aaplimg.com., 17.253.31.140, 17.253.83.135, 17.253.5.135, 17.253.83.150; AAAA=app-site-association.cdn-apple.com.akadns.net., app-site-association.g.aaplimg.com., 2620:149:a00:f000::132, 2620:149:a0c:f000::1, 2620:149:a06:f000::134, 2620:149:a21:f000::134; CNAME=app-site-association.cdn-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | — |
| `apple.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | brkgls.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=20 mx-in-vib.apple.com., 10 mx-in.g.apple.com., 20 mx-in-ma.apple.com., 20 mx-in-rn.apple.com., 20 mx-in-sg.apple.com., 20 mx-in-hfd.apple.com. | 0 | 0 | dig_txt:timeout:dig |
| `applytics.napps-1.com` | pcap_dns | 104.18.34.244, 172.64.153.12, 2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4 | — | — | CLOUDFLARENET | 104.18.34.244=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 172.64.153.12=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4403::ac40:990c=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4408::6812:22f4=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.34.244, 172.64.153.12; AAAA=2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4; CNAME=—; MX=—; TXT=— | 0 | 0 | 2606:4700:4403::ac40:990c:reverse_dns_failed; 2606:4700:4408::6812:22f4:reverse_dns_failed |
| `auth.napps-1.com` | pcap_dns | 172.64.153.12, 104.18.34.244, 2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4 | — | — | CLOUDFLARENET | 172.64.153.12=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.34.244=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4403::ac40:990c=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4408::6812:22f4=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=172.64.153.12, 104.18.34.244; AAAA=2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `auth.nordaccount.com` | pcap_dns | 172.64.145.31, 104.18.42.225, 2a06:98c1:3101::6812:2ae1, 2a06:98c1:3107::ac40:911f | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 172.64.145.31=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.42.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3101::6812:2ae1=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3107::ac40:911f=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=172.64.145.31, 104.18.42.225; AAAA=2a06:98c1:3101::6812:2ae1, 2a06:98c1:3107::ac40:911f; CNAME=—; MX=—; TXT=— | 0 | 0 | 172.64.145.31:reverse_dns_failed; 2a06:98c1:3101::6812:2ae1:reverse_dns_failed; 2a06:98c1:3107::ac40:911f:reverse_dns_failed |
| `auth.nordpass.com` | pcap_dns | 104.18.4.45, 104.18.5.45, 2606:4700::6812:52d, 2606:4700::6812:42d | — | — | CLOUDFLARENET | 104.18.4.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.5.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:52d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:42d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.4.45, 104.18.5.45; AAAA=2606:4700::6812:52d, 2606:4700::6812:42d; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `background-weighted.ls4-apple.com.akadns.net` | pcap_dns | 17.253.17.211, 17.253.17.212, 2620:149:a0c:f100::12, 2620:149:a0c:f000::11 | usscz2-vip-bx-011.aaplimg.com, usscz2-vip-bx-012.aaplimg.com | — | APPLE-WWNET | 17.253.17.211=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.212=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f100::12=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f000::11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=gspx57-ssl-background.ls.apple.com., get-bx.g.aaplimg.com., 17.253.17.211, 17.253.17.212; AAAA=gspx57-ssl-background.ls.apple.com., get-bx.g.aaplimg.com., 2620:149:a0c:f100::12, 2620:149:a0c:f000::11; CNAME=gspx57-ssl-background.ls.apple.com.; MX=—; TXT=— | 0 | 0 | — |
| `bag-cdn.itunes-apple.com.akadns.net` | pcap_dns | 151.101.43.6, 2a04:4e42:a::774 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK, US-FASTLY-20130718 | 151.101.43.6=>netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. || 2a04:4e42:a::774=>netname:        US-FASTLY-20130718 | country:        EU | org-name:       Fastly, Inc. | country:        US | A=bag-cdn-lb.itunes-apple.com.akadns.net., h3.apis.apple.map.fastly.net., 151.101.43.6; AAAA=bag-cdn-lb.itunes-apple.com.akadns.net., h3.apis.apple.map.fastly.net., 2a04:4e42:a::774; CNAME=bag-cdn-lb.itunes-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | 2a04:4e42:a::774:reverse_dns_failed |
| `chromewebstore.google.com` | pcap_dns | 142.251.219.14, 2607:f8b0:4005:815::200e | ncsfoa-aq-in-f14.1e100.net, pnsfoa-af-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.219.14=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:815::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.14; AAAA=2607:f8b0:4005:815::200e; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `clients2.google.com` | pcap_dns | 142.251.218.110, 2607:f8b0:4005:808::200e | pnsfoa-ab-in-f14.1e100.net, pnsfoa-ab-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:808::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=clients.l.google.com., 142.251.218.110; AAAA=clients.l.google.com., 2607:f8b0:4005:808::200e; CNAME=clients.l.google.com.; MX=—; TXT=— | 0 | 0 | — |
| `clients2.googleusercontent.com` | pcap_dns | 142.251.218.225, 2607:f8b0:4005:816::2001 | ncsfoa-aq-in-x01.1e100.net, pnsfoa-af-in-f1.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.225=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:816::2001=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=googlehosted.l.googleusercontent.com., 142.251.218.225; AAAA=googlehosted.l.googleusercontent.com., 2607:f8b0:4005:816::2001; CNAME=googlehosted.l.googleusercontent.com.; MX=—; TXT=— | 0 | 0 | — |
| `clientservices.googleapis.com` | pcap_dns | 172.217.12.110, 2607:f8b0:4005:80a::200e | sfo03s33-in-f14.1e100.net, sfo07s17-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 172.217.12.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80a::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=172.217.12.110; AAAA=2607:f8b0:4005:80a::200e; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `content-autofill.googleapis.com` | pcap_dns | 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106, 142.251.218.138, 142.251.214.42, 2607:f8b0:4005:80a::200a, 2607:f8b0:4005:801::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-ak-in-x0a.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, nuq04s29-in-x0a.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.10=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.74=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.106=> | A=142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10; AAAA=2607:f8b0:4005:80a::200a, 2607:f8b0:4005:801::200a, 2607:f8b0:4005:815::200a, 2607:f8b0:4005:803::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `d.nordaccount.com` | pcap_dns | 172.64.145.31, 104.18.42.225, 2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1 | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 172.64.145.31=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.42.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3107::ac40:911f=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3101::6812:2ae1=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=172.64.145.31, 104.18.42.225; AAAA=2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `debug.nordpass.com` | pcap_dns | 104.18.5.45, 104.18.4.45, 2606:4700::6812:42d, 2606:4700::6812:52d | — | — | CLOUDFLARENET | 104.18.5.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.4.45=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:42d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:52d=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.5.45, 104.18.4.45; AAAA=2606:4700::6812:42d, 2606:4700::6812:52d; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `debug.nordsec.com` | pcap_dns | 172.64.153.55, 104.18.34.201, 2a06:98c1:3101::6812:22c9, 2a06:98c1:3107::ac40:9937 | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 172.64.153.55=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.34.201=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3101::6812:22c9=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3107::ac40:9937=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=172.64.153.55, 104.18.34.201; AAAA=2a06:98c1:3101::6812:22c9, 2a06:98c1:3107::ac40:9937; CNAME=—; MX=—; TXT=— | 0 | 0 | 104.18.34.201:reverse_dns_failed; 2a06:98c1:3101::6812:22c9:reverse_dns_failed; 2a06:98c1:3107::ac40:9937:reverse_dns_failed |
| `dns-tunnel-check.googlezip.net` | pcap_dns | 216.239.34.159, 2001:4860:4802:34::9f | — | — | GOOGLE, GOOGLE-IPV6 | 216.239.34.159=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2001:4860:4802:34::9f=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=216.239.34.159; AAAA=2001:4860:4802:34::9f; CNAME=—; MX=—; TXT=— | 0 | 0 | 216.239.34.159:reverse_dns_failed; 2001:4860:4802:34::9f:reverse_dns_failed |
| `doh-dns-apple-com.v.aaplimg.com` | pcap_dns | 64.78.200.1, 17.132.91.16, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11, 2620:149:9cc::12, 2620:171:80c::1, 2620:149:a0c:3000::1c2, 2620:149:a0c:4000::1c2, 2620:171:80d::1, 2620:149:9cc::14 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.16=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:9cc::12=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName: | A=64.78.200.1, 17.132.91.16, 17.253.16.119, 17.253.16.247, 64.78.201.1, 17.132.91.11; AAAA=2620:149:9cc::12, 2620:171:80c::1, 2620:149:a0c:3000::1c2, 2620:149:a0c:4000::1c2, 2620:171:80d::1, 2620:149:9cc::14; CNAME=—; MX=—; TXT=— | 0 | 0 | 17.132.91.16:reverse_dns_failed; 17.132.91.11:reverse_dns_failed; 2620:149:9cc::12:reverse_dns_failed; 2620:149:9cc::14:reverse_dns_failed |
| `doh.dns.apple.com` | pcap_dns | 17.132.91.11, 64.78.200.1, 17.132.91.16, 17.253.16.119, 17.253.16.247, 64.78.201.1, 2620:171:80c::1, 2620:149:a0c:3000::1c2, 2620:149:a0c:4000::1c2, 2620:171:80d::1, 2620:149:9cc::14, 2620:149:9cc::12 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 17.132.91.11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.16=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 2620:171:80c::1=>NetName:        WOODYNET-V6-NET02 | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | O | A=doh-dns-apple-com.v.aaplimg.com., 17.132.91.11, 64.78.200.1, 17.132.91.16, 17.253.16.119, 17.253.16.247; AAAA=doh-dns-apple-com.v.aaplimg.com., 2620:171:80c::1, 2620:149:a0c:3000::1c2, 2620:149:a0c:4000::1c2, 2620:171:80d::1, 2620:149:9cc::14; CNAME=doh-dns-apple-com.v.aaplimg.com.; MX=—; TXT=— | 0 | 0 | — |
| `downloads.napps-1.com` | pcap_dns | 104.18.34.244, 172.64.153.12, 2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4 | — | — | CLOUDFLARENET | 104.18.34.244=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 172.64.153.12=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4403::ac40:990c=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4408::6812:22f4=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.34.244, 172.64.153.12; AAAA=2606:4700:4403::ac40:990c, 2606:4700:4408::6812:22f4; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `downloads.nordcdn.com` | pcap_dns | 104.16.156.111, 104.16.155.111, 2606:4700::6810:9b6f, 2606:4700::6810:9c6f | — | — | CLOUDFLARENET | 104.16.156.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.16.155.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9b6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9c6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.16.156.111, 104.16.155.111; AAAA=2606:4700::6810:9b6f, 2606:4700::6810:9c6f; CNAME=—; MX=—; TXT=— | 0 | 0 | 2606:4700::6810:9b6f:reverse_dns_failed; 2606:4700::6810:9c6f:reverse_dns_failed |
| `downloads.npass.app` | pcap_dns | 104.18.19.225, 104.18.18.225, 2606:4700::6812:13e1, 2606:4700::6812:12e1 | — | — | CLOUDFLARENET | 104.18.19.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.18.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:13e1=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:12e1=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.19.225, 104.18.18.225; AAAA=2606:4700::6812:13e1, 2606:4700::6812:12e1; CNAME=—; MX=—; TXT=— | 0 | 0 | 104.18.18.225:reverse_dns_failed; 2606:4700::6812:13e1:reverse_dns_failed; 2606:4700::6812:12e1:reverse_dns_failed |
| `edgedl.me.gvt1.com` | pcap_dns | 34.104.35.123, 2600:1900:4110:86f:: | 123.35.104.34.bc.googleusercontent.com | — | GOOGL-2, GOOGLE-CLOUD | 34.104.35.123=>NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US || 2600:1900:4110:86f::=>NetName:        GOOGLE-CLOUD | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | A=34.104.35.123; AAAA=2600:1900:4110:86f::; CNAME=—; MX=—; TXT=— | 0 | 0 | 2600:1900:4110:86f:::reverse_dns_failed |
| `eip-terr-na.cdp1.digicert.com.akahost.net` | pcap_dns | 23.11.33.159, 2600:14e1:4:6d:: | a23-11-33-159.deploy.static.akamaitechnologies.com, g2600-14e1-0004-006d-0000-0000-0000-0000.deploy.static.akamaitechnologies.com | — | AKAMAI | 23.11.33.159=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 2600:14e1:4:6d::=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | A=23.11.33.159; AAAA=2600:14e1:4:6d::; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `encrypted-tbn0.gstatic.com` | pcap_dns | 142.251.218.78, 2607:f8b0:4005:803::200e | pnsfoa-aa-in-f14.1e100.net, sfo03s33-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.78=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:803::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.78; AAAA=2607:f8b0:4005:803::200e; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `feedback-pa.clients6.google.com` | pcap_dns | 142.251.218.170, 2607:f8b0:4005:803::200a | ncsfoa-ak-in-f10.1e100.net, sfo03s33-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:803::200a=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.170; AAAA=2607:f8b0:4005:803::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `firebase-settings.crashlytics.com` | pcap_dns | 142.251.219.3, 2607:f8b0:4005:80b::2003 | ncsfoa-ao-in-x03.1e100.net, ncsfoa-aq-in-f3.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.219.3=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80b::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.3; AAAA=2607:f8b0:4005:80b::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `firebaseinstallations.googleapis.com` | pcap_dns | 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106, 2607:f8b0:4005:816::200a, 2607:f8b0:4005:806::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, ncsfoa-aq-in-x0a.1e100.net, nuq04s35-in-x0a.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.138=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.10=> | A=142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42; AAAA=2607:f8b0:4005:816::200a, 2607:f8b0:4005:806::200a, 2607:f8b0:4005:808::200a, 2607:f8b0:4005:809::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `firebaselogging-pa.googleapis.com` | pcap_dns | 216.239.36.223, 216.239.34.223, 216.239.32.223, 216.239.38.223, 2001:4860:4802:32::223, 2001:4860:4802:38::223, 2001:4860:4802:36::223, 2001:4860:4802:34::223 | — | — | GOOGLE, GOOGLE-IPV6 | 216.239.36.223=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 216.239.34.223=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 216.239.32.223=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 216.239.38.223=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2001:4860:4802:32::223=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2001:4860:4802:38::223=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2001:4860:4802:36::223=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Cou | A=216.239.36.223, 216.239.34.223, 216.239.32.223, 216.239.38.223; AAAA=2001:4860:4802:32::223, 2001:4860:4802:38::223, 2001:4860:4802:36::223, 2001:4860:4802:34::223; CNAME=—; MX=—; TXT=— | 0 | 0 | 216.239.36.223:reverse_dns_failed; 216.239.32.223:reverse_dns_failed; 216.239.38.223:reverse_dns_failed; 2001:4860:4802:32::223:reverse_dns_failed; 2001:4860:4802:38::223:reverse_dns_failed; 2001:4860:4802:36::223:reverse_dns_failed; 2001:4860:4802:34::223:reverse_dns_failed |
| `firebaseremoteconfig.googleapis.com` | pcap_dns | 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106, 2607:f8b0:4005:809::200a, 2607:f8b0:4005:801::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, nuq04s29-in-x0a.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net, sfo03s08-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.138=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.10=> | A=142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42; AAAA=2607:f8b0:4005:809::200a, 2607:f8b0:4005:801::200a, 2607:f8b0:4005:815::200a, 2607:f8b0:4005:808::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `fonts.googleapis.com` | pcap_dns | 142.251.219.10, 2607:f8b0:4005:80a::200a | ncsfoa-ak-in-x0a.1e100.net, ncsfoa-aq-in-f10.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.219.10=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80a::200a=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.10; AAAA=2607:f8b0:4005:80a::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `fonts.gstatic.com` | pcap_dns | 142.251.218.227, 2607:f8b0:4005:816::2003 | ncsfoa-aq-in-x03.1e100.net, pnsfoa-af-in-f3.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.227=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:816::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.227; AAAA=2607:f8b0:4005:816::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `gdmf.apple.com` | pcap_dns | 17.23.18.34 | — | — | APPLE-WWNET | 17.23.18.34=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=gdmf.v.aaplimg.com., 17.23.18.34; AAAA=—; CNAME=gdmf.v.aaplimg.com.; MX=—; TXT=— | 0 | 0 | — |
| `gdmf.v.aaplimg.com` | pcap_dns | 17.23.18.34 | — | — | APPLE-WWNET | 17.23.18.34=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | A=17.23.18.34; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `get-bx.g.aaplimg.com` | pcap_dns | 17.253.17.211, 17.253.17.212, 2620:149:a0c:f000::11, 2620:149:a0c:f100::12 | usscz2-vip-bx-011.aaplimg.com, usscz2-vip-bx-012.aaplimg.com | — | APPLE-WWNET | 17.253.17.211=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.212=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f000::11=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f100::12=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.17.211, 17.253.17.212; AAAA=2620:149:a0c:f000::11, 2620:149:a0c:f100::12; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `google-ohttp-relay-safebrowsing.fastly-edge.com` | pcap_dns | 151.101.41.91, 2a04:4e42:a::347 | — | — | NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK, US-FASTLY-20130718 | 151.101.41.91=>netname:        NON-RIPE-NCC-MANAGED-ADDRESS-BLOCK | country:        EU # Country is really world wide | NetName:        SKYCA-3 | OriginAS: | Organization:   Fastly, Inc. (SKYCA-3) | OrgName:        Fastly, Inc. || 2a04:4e42:a::347=>netname:        US-FASTLY-20130718 | country:        EU | org-name:       Fastly, Inc. | country:        US | A=151.101.41.91; AAAA=2a04:4e42:a::347; CNAME=—; MX=—; TXT=— | 0 | 0 | 2a04:4e42:a::347:reverse_dns_failed |
| `googleads.g.doubleclick.net` | pcap_dns | 142.251.218.194, 2607:f8b0:4005:80b::2002 | ncsfoa-ao-in-f2.1e100.net, ncsfoa-ao-in-x02.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.194=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80b::2002=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.194; AAAA=2607:f8b0:4005:80b::2002; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `i.ytimg.com` | pcap_dns | 142.251.218.118, 142.251.218.150, 142.251.214.54, 142.251.218.246, 172.217.12.118, 142.251.218.182, 142.251.219.54, 142.251.218.214, 142.251.219.22, 142.251.218.86, 2607:f8b0:4005:80a::2016, 2607:f8b0:4005:801::2016 | atl26s14-in-f22.1e100.net, ncsfoa-ak-in-f22.1e100.net, ncsfoa-an-in-f22.1e100.net, ncsfoa-ao-in-f22.1e100.net, ncsfoa-aq-in-f22.1e100.net, nuq04s29-in-x16.1e100.net, pnsfoa-aa-in-f22.1e100.net, pnsfoa-ab-in-f22.1e100.net, pnsfoa-ad-in-f22.1e100.net, pnsfoa-ae-in-f22.1e100.net, pnsfoa-af-in-f22.1e100.net, sfo07s17-in-x16.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.118=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.150=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.54=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.246=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.118=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.182=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.54=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.214= | A=142.251.218.118, 142.251.218.150, 142.251.214.54, 142.251.218.246, 172.217.12.118, 142.251.218.182; AAAA=2607:f8b0:4005:80a::2016, 2607:f8b0:4005:801::2016, 2607:f8b0:4005:815::2016, 2607:f8b0:4005:803::2016; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `icloud.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | brkgls.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=10 mx02.mail.icloud.com., 10 mx01.mail.icloud.com.; TXT=v=spf1 ip4:17.41.0.0/16 ip4:17.58.0.0/16 ip4:17.142.0.0/15 ip4:17.57.155.0/24 ip4:17.57.156.0/24 ip4:144.178.36.0/24 ip4:144.178.38.0/24 ip4:112.19.199.64/29 ip4:112.19.242.64/29 ip4:222.73.195.64/29 ip4:157.255.1.64/29" " ip4:106.39.212.64/29 ip4:123.126.78.64/29 ip4:183.240.219.64/29 ip4:39.156.163.64/29 ip4:57.103.64.0/18" " ip6:2a01:b747:3000:200::/56 ip6:2a01:b747:3001:200::/56 ip6:2a01:b747:3002:200::/56 ip6:2a01:b747:3003:200::/56 ip6:2a01:b747:3004:200::/56 ip6:2a01:b747:3005:200::/56 ip6:2a01:b747:3006:200::/56 ~all, google-site-verification=Ik3jMkCjHnUgyIoFR0Kw74srr0H5ynFmUk8fyY1uBck, google-site-verification=knAEOH4QxR29I4gjRkpkvmUmP2AA7WrDk8Kq0wu9g9o | 0 | 0 | — |
| `img.youtube.com` | pcap_dns | 142.251.214.46, 142.251.218.238, 172.217.12.110, 142.251.218.174, 142.251.219.46, 142.251.218.206, 142.251.219.14, 142.251.218.78, 142.251.218.110, 142.251.218.142, 2607:f8b0:4005:803::200e, 2607:f8b0:4005:80a::200e | ncsfoa-ak-in-f14.1e100.net, ncsfoa-an-in-f14.1e100.net, ncsfoa-ao-in-f14.1e100.net, ncsfoa-aq-in-f14.1e100.net, pnsfoa-aa-in-f14.1e100.net, pnsfoa-ab-in-f14.1e100.net, pnsfoa-ae-in-f14.1e100.net, pnsfoa-af-in-f14.1e100.net, qro04s06-in-f14.1e100.net, sfo03s33-in-f14.1e100.net, sfo03s33-in-x0e.1e100.net, sfo07s17-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.214.46=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.238=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.174=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.46=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.206=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.14=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.78=>N | A=ytimg.l.google.com., 142.251.214.46, 142.251.218.238, 172.217.12.110, 142.251.218.174, 142.251.219.46; AAAA=ytimg.l.google.com., 2607:f8b0:4005:803::200e, 2607:f8b0:4005:80a::200e, 2607:f8b0:4005:801::200e, 2607:f8b0:4005:815::200e; CNAME=ytimg.l.google.com.; MX=—; TXT=— | 0 | 0 | — |
| `jnn-pa.googleapis.com` | pcap_dns | 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106, 142.251.218.138, 142.251.214.42, 2607:f8b0:4005:80a::200a, 2607:f8b0:4005:817::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-ak-in-x0a.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-an-in-x0a.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.10=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.74=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.106=> | A=142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10; AAAA=2607:f8b0:4005:80a::200a, 2607:f8b0:4005:817::200a, 2607:f8b0:4005:80b::200a, 2607:f8b0:4005:816::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `lensfrontend-pa.googleapis.com` | pcap_dns | 142.251.218.106, 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 2607:f8b0:4005:803::200a, 2607:f8b0:4005:809::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net, sfo03s08-in-x0a.1e100.net, sfo03s33-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.138=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202= | A=142.251.218.106, 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170; AAAA=2607:f8b0:4005:803::200a, 2607:f8b0:4005:809::200a, 2607:f8b0:4005:801::200a, 2607:f8b0:4005:815::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `lh3.googleusercontent.com` | pcap_dns | 142.251.218.225, 2607:f8b0:4005:815::2001 | pnsfoa-af-in-f1.1e100.net, pnsfoa-af-in-x01.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.225=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:815::2001=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=googlehosted.l.googleusercontent.com., 142.251.218.225; AAAA=googlehosted.l.googleusercontent.com., 2607:f8b0:4005:815::2001; CNAME=googlehosted.l.googleusercontent.com.; MX=—; TXT=— | 0 | 0 | — |
| `my.nordaccount.com` | pcap_dns | 172.64.145.31, 104.18.42.225, 2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1 | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 172.64.145.31=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.42.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3107::ac40:911f=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3101::6812:2ae1=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=172.64.145.31, 104.18.42.225; AAAA=2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `napps-1.com` | pcap_dns | 172.64.153.12, 104.18.34.244, 2606:4700:4408::6812:22f4, 2606:4700:4403::ac40:990c | — | — | CLOUDFLARENET | 172.64.153.12=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.34.244=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4408::6812:22f4=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700:4403::ac40:990c=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=172.64.153.12, 104.18.34.244; AAAA=2606:4700:4408::6812:22f4, 2606:4700:4403::ac40:990c; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `nc-mqtt.nordpass.com` | pcap_dns | 54.225.99.62, 100.51.90.255, 52.86.142.63 | ec2-100-51-90-255.compute-1.amazonaws.com, ec2-52-86-142-63.compute-1.amazonaws.com, ec2-54-225-99-62.compute-1.amazonaws.com | — | AMAZO-4, AMAZON-2011L, AT-88-Z | 54.225.99.62=>NetName:        AMAZON-2011L | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 100.51.90.255=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 52.86.142.63=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | A=nordpass-vernemq.nfct-dflt-p-ue1.mountainkube.com., nfct-prod-nordpass-vernemq-72453689ce43abfa.elb.us-east-1.amazonaws.com., 54.225.99.62, 100.51.90.255, 52.86.142.63; AAAA=—; CNAME=nordpass-vernemq.nfct-dflt-p-ue1.mountainkube.com.; MX=—; TXT=— | 0 | 0 | — |
| `nordaccount.com` | pcap_dns | 104.18.42.225, 172.64.145.31, 2a06:98c1:3101::6812:2ae1, 2a06:98c1:3107::ac40:911f | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 104.18.42.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 172.64.145.31=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3101::6812:2ae1=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3107::ac40:911f=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=104.18.42.225, 172.64.145.31; AAAA=2a06:98c1:3101::6812:2ae1, 2a06:98c1:3107::ac40:911f; CNAME=—; MX=5 alt1.aspmx.l.google.com., 5 alt2.aspmx.l.google.com., 1 aspmx.l.google.com., 10 alt3.aspmx.l.google.com., 10 alt4.aspmx.l.google.com.; TXT=v=spf1 include:mail.zendesk.com include:_spf.hushmail.com include:_spf.google.com ~all | 0 | 0 | — |
| `ocsp.digicert.com` | pcap_dns | 23.11.33.159, 2600:14e1:4:6d:: | a23-11-33-159.deploy.static.akamaitechnologies.com, g2600-14e1-0004-006d-0000-0000-0000-0000.deploy.static.akamaitechnologies.com | — | AKAMAI | 23.11.33.159=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 2600:14e1:4:6d::=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | A=ocsp.edge.digicert.com., cdp1.digicert.com.akamaized.net., cdp1.digicert.com.splitter-eip.akadns.net., cdp1.digicert.com.eip.akadns.net., eip-terr-na.cdp1.digicert.com.akahost.net., 23.11.33.159; AAAA=ocsp.edge.digicert.com., cdp1.digicert.com.akamaized.net., cdp1.digicert.com.splitter-eip.akadns.net., cdp1.digicert.com.eip.akadns.net., eip-terr-na.cdp1.digicert.com.akahost.net., 2600:14e1:4:6d::; CNAME=ocsp.edge.digicert.com.; MX=—; TXT=— | 0 | 0 | — |
| `ocsp2.apple.com` | pcap_dns | 17.253.5.151, 17.253.17.202, 17.253.5.136, 17.253.17.210, 2620:149:a0c:f000::9, 2620:149:a00:f000::141, 2620:149:a0c:f100::8, 2620:149:a00:f000::144 | usscz2-vip-bx-002.aaplimg.com, usscz2-vip-bx-008.aaplimg.com, usscz2-vip-bx-009.aaplimg.com, usscz2-vip-bx-010.aaplimg.com, ussjc2-vip-fx-103.b.aaplimg.com, ussjc2-vip-fx-106.a.aaplimg.com, ussjc2-vip-fx-107.b.aaplimg.com, ussjc2-vip-fx-111.a.aaplimg.com | — | APPLE-WWNET | 17.253.5.151=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.202=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.5.136=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.210=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f000::9=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US || 2620:149:a00:f000::141=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US || 2620:149:a0c:f100::8=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. | A=ocsp2.g.aaplimg.com., 17.253.5.151, 17.253.17.202, 17.253.5.136, 17.253.17.210; AAAA=ocsp2.g.aaplimg.com., 2620:149:a0c:f000::9, 2620:149:a00:f000::141, 2620:149:a0c:f100::8, 2620:149:a00:f000::144; CNAME=ocsp2.g.aaplimg.com.; MX=—; TXT=— | 0 | 0 | — |
| `ocsp2.g.aaplimg.com` | pcap_dns | 17.253.5.143, 17.253.5.141, 17.253.17.208, 17.253.17.201, 2600:1406:2e00:89c::dc8, 2600:1406:2e00:880::dc8 | g2600-1406-2e00-0880-0000-0000-0000-0dc8.deploy.static.akamaitechnologies.com, g2600-1406-2e00-089c-0000-0000-0000-0dc8.deploy.static.akamaitechnologies.com, usscz2-vip-bx-001.aaplimg.com, usscz2-vip-bx-008.aaplimg.com, ussjc2-vip-fx-106.a.aaplimg.com, ussjc2-vip-fx-107.a.aaplimg.com | — | AKAMAI, APPLE-WWNET | 17.253.5.143=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.5.141=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.208=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.17.201=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2600:1406:2e00:89c::dc8=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 2600:1406:2e00:880::dc8=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | A=17.253.5.143, 17.253.5.141, 17.253.17.208, 17.253.17.201; AAAA=ocsp2.apple.com.edgekey.net., e3528.dscg.akamaiedge.net., 2600:1406:2e00:89c::dc8, 2600:1406:2e00:880::dc8; CNAME=ocsp2.apple.com.edgekey.net.; MX=—; TXT=— | 0 | 0 | — |
| `ogads-pa.clients6.google.com` | pcap_dns | 142.251.218.202, 2607:f8b0:4005:809::200a | ncsfoa-ao-in-f10.1e100.net, sfo03s08-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:809::200a=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.202; AAAA=2607:f8b0:4005:809::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `ogs.google.com` | pcap_dns | 142.251.218.142, 2607:f8b0:4005:801::200e | pnsfoa-ae-in-x0e.1e100.net, qro04s06-in-f14.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.142=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:801::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=www3.l.google.com., 142.251.218.142; AAAA=www3.l.google.com., 2607:f8b0:4005:801::200e; CNAME=www3.l.google.com.; MX=—; TXT=— | 0 | 0 | — |
| `passwordsleakcheck-pa.googleapis.com` | pcap_dns | 142.251.218.106, 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 2607:f8b0:4005:803::200a, 2607:f8b0:4005:80a::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-ak-in-x0a.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net, sfo03s33-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.138=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.234=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202= | A=142.251.218.106, 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 142.251.218.170; AAAA=2607:f8b0:4005:803::200a, 2607:f8b0:4005:80a::200a, 2607:f8b0:4005:817::200a, 2607:f8b0:4005:80b::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `play.google.com` | pcap_dns | 142.251.219.46, 2607:f8b0:4005:817::200e | ncsfoa-an-in-f14.1e100.net, ncsfoa-an-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.219.46=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:817::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.46; AAAA=2607:f8b0:4005:817::200e; CNAME=—; MX=30 alt3.gmr-smtp-in.l.google.com., 5 gmr-smtp-in.l.google.com., 10 alt1.gmr-smtp-in.l.google.com., 20 alt2.gmr-smtp-in.l.google.com., 40 alt4.gmr-smtp-in.l.google.com.; TXT=v=spf1 redirect=_spf.google.com, facebook-domain-verification=l3ljyvzkhsau69imdwww4eizcqgmma | 0 | 0 | — |
| `s1.nordaccount.com` | pcap_dns | 104.18.42.225, 172.64.145.31, 2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1 | — | AS13335 | CLOUDFLARENET, CLOUDFLARENET-EU | 104.18.42.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 172.64.145.31=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2a06:98c1:3107::ac40:911f=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 || 2a06:98c1:3101::6812:2ae1=>netname:        CLOUDFLARENET-EU | country:        GB | origin:         AS13335 | A=104.18.42.225, 172.64.145.31; AAAA=2a06:98c1:3107::ac40:911f, 2a06:98c1:3101::6812:2ae1; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `s1.nordcdn.com` | pcap_dns | 104.16.155.111, 104.16.156.111, 2606:4700::6810:9b6f, 2606:4700::6810:9c6f | — | — | CLOUDFLARENET | 104.16.155.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.16.156.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9b6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9c6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.16.155.111, 104.16.156.111; AAAA=2606:4700::6810:9b6f, 2606:4700::6810:9c6f; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `s1.npass.app` | pcap_dns | 104.18.19.225, 104.18.18.225, 2606:4700::6812:12e1, 2606:4700::6812:13e1 | — | — | CLOUDFLARENET | 104.18.19.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.18.18.225=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:12e1=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6812:13e1=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.18.19.225, 104.18.18.225; AAAA=2606:4700::6812:12e1, 2606:4700::6812:13e1; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `sandbox.itunes.apple.com` | pcap_dns | 23.46.216.91, 23.46.216.71, 2600:1406:2e00:63::173d:f6d5, 2600:1406:2e00:63::173d:f6c9 | a23-46-216-71.deploy.static.akamaitechnologies.com, a23-46-216-91.deploy.static.akamaitechnologies.com, g2600-1406-2e00-0063-0000-0000-173d-f6c9.deploy.static.akamaitechnologies.com, g2600-1406-2e00-0063-0000-0000-173d-f6d5.deploy.static.akamaitechnologies.com | — | AKAMAI | 23.46.216.91=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 23.46.216.71=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 2600:1406:2e00:63::173d:f6d5=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US || 2600:1406:2e00:63::173d:f6c9=>NetName:        AKAMAI | OriginAS: | Organization:   Akamai Technologies, Inc. (AKAMAI) | OrgName:        Akamai Technologies, Inc. | Country:        US | A=sandbox.itunes-apple.com.akadns.net., sandbox-dist.itunes-apple.com.akadns.net., sandbox.itunes.apple.com.edgesuite.net., a708.dsct.akamai.net., 23.46.216.91, 23.46.216.71; AAAA=sandbox.itunes-apple.com.akadns.net., sandbox-dist.itunes-apple.com.akadns.net., sandbox.itunes.apple.com.edgesuite.net., a708.dsct.akamai.net., 2600:1406:2e00:63::173d:f6d5, 2600:1406:2e00:63::173d:f6c9; CNAME=sandbox.itunes-apple.com.akadns.net.; MX=—; TXT=— | 0 | 0 | — |
| `sb-ssl.google.com` | pcap_dns | 142.251.218.142, 2607:f8b0:4005:808::200e | pnsfoa-ab-in-x0e.1e100.net, qro04s06-in-f14.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.142=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:808::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=sb-ssl.l.google.com., 142.251.218.142; AAAA=sb-ssl.l.google.com., 2607:f8b0:4005:808::200e; CNAME=sb-ssl.l.google.com.; MX=—; TXT=— | 0 | 0 | — |
| `sb.nordcdn.com` | pcap_dns | 104.16.156.111, 104.16.155.111, 2606:4700::6810:9b6f, 2606:4700::6810:9c6f | — | — | CLOUDFLARENET | 104.16.156.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 104.16.155.111=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9b6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US || 2606:4700::6810:9c6f=>NetName:        CLOUDFLARENET | OriginAS: | Organization:   Cloudflare, Inc. (CLOUD14) | OrgName:        Cloudflare, Inc. | Country:        US | A=104.16.156.111, 104.16.155.111; AAAA=2606:4700::6810:9b6f, 2606:4700::6810:9c6f; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `ssl.gstatic.com` | pcap_dns | 142.251.218.163, 2607:f8b0:4005:80a::2003 | ncsfoa-ak-in-f3.1e100.net, ncsfoa-ak-in-x03.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.163=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80a::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.163; AAAA=2607:f8b0:4005:80a::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `static.doubleclick.net` | pcap_dns | 142.251.218.166, 2607:f8b0:4005:806::2006 | ncsfoa-ak-in-f6.1e100.net, pnsfoa-aa-in-x06.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.166=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:806::2006=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.166; AAAA=2607:f8b0:4005:806::2006; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `tunnel.googlezip.net` | pcap_dns | 216.239.34.157, 2001:4860:4802:34::9d | — | — | GOOGLE, GOOGLE-IPV6 | 216.239.34.157=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2001:4860:4802:34::9d=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=216.239.34.157; AAAA=2001:4860:4802:34::9d; CNAME=—; MX=—; TXT=— | 0 | 0 | 2001:4860:4802:34::9d:reverse_dns_failed |
| `update.googleapis.com` | pcap_dns | 172.217.12.110, 2607:f8b0:4005:808::200e | pnsfoa-ab-in-x0e.1e100.net, sfo03s33-in-f14.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 172.217.12.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:808::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=172.217.12.110; AAAA=2607:f8b0:4005:808::200e; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.google-analytics.com` | pcap_dns | 142.251.218.78, 2607:f8b0:4005:801::200e | pnsfoa-aa-in-f14.1e100.net, pnsfoa-ae-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.78=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:801::200e=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.78; AAAA=2607:f8b0:4005:801::200e; CNAME=www-alv.google-analytics.com.; MX=—; TXT=— | 0 | 0 | — |
| `www.google.com` | pcap_dns | — | — | — | — | — | A=192.0.0.88; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.googleadservices.com` | pcap_dns | 142.251.219.2 | ncsfoa-aq-in-f2.1e100.net | — | GOOGLE | 142.251.219.2=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.2; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.googleapis.com` | pcap_dns | 142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106, 142.251.218.138, 142.251.214.42, 142.251.218.234, 172.217.12.106, 2607:f8b0:4005:809::200a, 2607:f8b0:4005:816::200a | atl26s14-in-f10.1e100.net, ncsfoa-ak-in-f10.1e100.net, ncsfoa-an-in-f10.1e100.net, ncsfoa-ao-in-f10.1e100.net, ncsfoa-aq-in-f10.1e100.net, ncsfoa-aq-in-x0a.1e100.net, pnsfoa-aa-in-f10.1e100.net, pnsfoa-ab-in-f10.1e100.net, pnsfoa-ae-in-f10.1e100.net, pnsfoa-af-in-f10.1e100.net, qro04s06-in-f10.1e100.net, sfo03s08-in-x0a.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.170=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.42=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.202=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.10=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.74=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.106=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.138=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.214.42=> | A=142.251.218.170, 142.251.219.42, 142.251.218.202, 142.251.219.10, 142.251.218.74, 142.251.218.106; AAAA=2607:f8b0:4005:809::200a, 2607:f8b0:4005:816::200a, 2607:f8b0:4005:806::200a, 2607:f8b0:4005:808::200a; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.googletagmanager.com` | pcap_dns | 172.217.12.104, 2607:f8b0:4005:806::2008 | atl26s14-in-f8.1e100.net, pnsfoa-aa-in-x08.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 172.217.12.104=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:806::2008=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=172.217.12.104; AAAA=2607:f8b0:4005:806::2008; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.gstatic.com` | pcap_dns | 142.251.218.131, 2607:f8b0:4005:80b::2003 | ncsfoa-ao-in-x03.1e100.net, pnsfoa-ad-in-f3.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.131=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:80b::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.218.131; AAAA=2607:f8b0:4005:80b::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `www.youtube.com` | pcap_dns | 142.251.218.238, 172.217.12.110, 142.251.218.174, 142.251.219.46, 142.251.218.206, 142.251.219.14, 142.251.218.78, 142.251.218.110, 142.251.218.142, 142.251.214.46, 2607:f8b0:4005:80a::200e, 2607:f8b0:4005:817::200e | ncsfoa-ak-in-f14.1e100.net, ncsfoa-an-in-f14.1e100.net, ncsfoa-an-in-x0e.1e100.net, ncsfoa-ao-in-f14.1e100.net, ncsfoa-aq-in-f14.1e100.net, pnsfoa-aa-in-f14.1e100.net, pnsfoa-ab-in-f14.1e100.net, pnsfoa-ae-in-f14.1e100.net, pnsfoa-af-in-f14.1e100.net, qro04s06-in-f14.1e100.net, sfo03s33-in-f14.1e100.net, sfo07s17-in-x0e.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.218.238=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 172.217.12.110=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.174=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.46=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.206=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.219.14=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.78=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 142.251.218.110=> | A=youtube-ui.l.google.com., 142.251.218.238, 172.217.12.110, 142.251.218.174, 142.251.219.46, 142.251.218.206; AAAA=youtube-ui.l.google.com., 2607:f8b0:4005:80a::200e, 2607:f8b0:4005:817::200e, 2607:f8b0:4005:80b::200e, 2607:f8b0:4005:803::200e; CNAME=youtube-ui.l.google.com.; MX=—; TXT=— | 0 | 0 | — |






**Capture finalize:** session_id=1eaa68a91b94


#### Competitor surface (provider YAML probes)


*`competitor_surface` is null; no competitor data for this run.*


#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "185.211.32.87",
    "country_code": "US",
    "region": "California",
    "city": "San Jose",
    "connection": {
      "asn": 212238,
      "org": "Packethub S.A.",
      "isp": "Datacamp Limited",
      "domain": "packethub.net"
    },
    "location_id": "us-california-san-jose-87",
    "location_label": "San Jose, California, United States"
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260501T105329Z-8cb49bd0",
  "timestamp_utc": "2026-05-01T10:54:20.994055+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.13 (main, Mar  3 2026, 12:39:30) [Clang 21.0.0 (clang-2100.0.123.102)]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-san-jose-87",
  "vpn_location_label": "San Jose, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.211.32.87",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "185.211.32.87",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "185.211.32.87",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.211.32.87",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.211.32.87\"}",
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
        "185.211.32.79"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.211.32.87"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "011feeb0-b708-42a0-bcd0-2452e16a6592.local",
      "port": 65122,
      "raw": "candidate:415465874 1 udp 2113937151 011feeb0-b708-42a0-bcd0-2452e16a6592.local 65122 typ host generation 0 ufrag mlxH network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.211.32.87",
      "port": 38210,
      "raw": "candidate:222472082 1 udp 1677729535 185.211.32.87 38210 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag mlxH network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36",
    "language": "en-US",
    "hardwareConcurrency": 12,
    "platform": "MacIntel"
  },
  "attribution": {
    "asn": 212238,
    "holder": "CDNEXT Datacamp Limited",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [212238]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 212238,
        "holder": "CDNEXT Datacamp Limited",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (185.211.32.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260501105348-678cc919-2e55-44ab-8433-9298100e8af3",
            "process_time": 61,
            "server_id": "app198",
            "build_version": "v0.9.15-2026.04.30",
            "pipeline": "1248748",
            "status": "ok",
            "status_code": 200,
            "time": "2026-05-01T10:53:48.652576",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 212238,
                  "holder": "CDNEXT Datacamp Limited"
                }
              ],
              "related_prefixes": [],
              "resource": "185.211.32.0/24",
              "type": "prefix",
              "block": {
                "resource": "185.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-05-01T00:00:00",
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
          "raw_line": "212238 | 185.211.32.0/24 | DE | ripencc | 2017-06-30",
          "parts": [
            "212238",
            "185.211.32.0/24",
            "DE",
            "ripencc",
            "2017-06-30"
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
  "policies": [],
  "services_contacted": [
    "browserleaks.com:playwright_chromium",
    "fingerprint:playwright_navigator",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api64.ipify.org",
    "https://browserleaks.com/dns",
    "https://browserleaks.com/ip",
    "https://browserleaks.com/tls",
    "https://browserleaks.com/webrtc",
    "https://ipleak.net/",
    "https://ipwho.is/185.211.32.87",
    "https://test-ipv6.com/",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/webrtc",
    "ipv6_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/fingerprint",
    "attribution_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/policy",
    "competitor_probe_dir": null,
    "browserleaks_probe_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": null,
    "transitions_json": null,
    "website_exposure_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/website_exposure",
    "capture_dir": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/capture"
  },
  "competitor_surface": null,
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.211.32.87\nHostname\tn/a\nIP Address Location\nCountry\tUnited States (US)\nState/Region\tCalifornia\nCity\tSan Francisco\nISP\tDatacamp Limited\nOrganization\tPackethub S.A\nNetwork\tAS212238 Datacamp Limited (VPN, VPSH, TOR, CONTENT)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Los_Angeles (PDT)\nLocal Time\tFri, 01 May 2026 03:53:57 -0700\nCoordinates\t37.7749,-122.4190\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.211.32.87\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t17 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\tecd7e00dac96050022152a50848bc443\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"HeadlessChrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.211.32.0 - 185.211.32.255\nCIDR\t185.211.32.0/24\nName\tPackethub-L20221011\nHandle\t185.211.32.0 - 185.211.32.255\nParent Handle\t185.211.32.0 - 185.211.34.255\nNet Type\tASSIGNED PA\nCountry\tUnited States\nRegistration\tMon, 23 Jun 2025 11:38:03 GMT\nLast Changed\tMon, 23 Jun 2025 11:38:03 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tDe-kis2-1-mnt\nHandle\tDe-kis2-1-mnt\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (456)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.211.32.87\nISP\tDatacamp Limited\nLocation\tUnited States, San Francisco\nDNS Leak Test\nTest Results\tFound 15 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.211.32.77\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.78\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.79\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.80\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.81\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.82\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.83\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.84\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.85\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.86\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.87\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.88\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.89\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.90\tDatacamp Limited\tUnited States, San Francisco\n185.211.32.91\tDatacamp Limited\tUnited States, San Francisco\nLeave a Comment (245)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.211.32.87\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.211.32.87\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (221)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_e40016c0bfb1\nJA3\tb352560c8fc9422f78aab3d1537bfaca\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x2A2A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x2A2A\nGREASE\n\n\n0x44CD\napplication_settings\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x0033\nkey_share\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x000B\nec_point_formats\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x0005\nstatus_request\n\n\n0x000A\nsupported_groups\n\n\n0x0017\nextended_main_secret\n\n\n0x0023\nsession_ticket\n\n\n0x000D\nsignature_algorithms\n\n\n0x0000\nserver_name\n\n\n0x001B\ncompress_certificate\n\n\n0x002B\nsupported_versions\n\n\n0xFF01\nrenegotiation_info\n\n\n0x1A1A\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t244\nenc_length\t32\npayload_length\t176\nkey_share\nclient_shares\t\n0x4A4A\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.bro",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-2ba3df10",
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
        "notes": "No web or portal probes in run."
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
        "answer_summary": "Exit IPv4 185.211.32.87; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 185.211.32.87.",
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
        "notes": "No web or portal probes."
      },
      {
        "question_id": "EXIT-001",
        "question_text": "What exit IP is assigned for each region?",
        "category": "exit_infrastructure",
        "testability": "DYNAMIC_FULL",
        "answer_status": "answered",
        "answer_summary": "Exit IPv4 185.211.32.87 for location us-california-san-jose-87.",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "ASN 212238 — CDNEXT Datacamp Limited",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 87.32.211.185.in-addr.arpa.",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('San Jose, California, United States').",
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
        "answer_status": "answered",
        "answer_summary": "Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence).",
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
  "website_exposure_methodology": {
    "methodology_schema_version": "1.0",
    "evidence_tier_note": "Desk automation of website-exposure methodology (Phases 1–9). Do not conflate with client resolver / DNS-leak observations (O); see docs/research-questions-and-evidence.md.",
    "phases": {
      "1_fetch": "urls_from_config_and_har_summaries",
      "2_extract": "hosts_parsed_via_urlparse",
      "3_dedupe": "unique_hosts=0",
      "4_resolve": "A_AAAA_optional_public_ip_attribution",
      "5_whois_via_attribution": "sample_only_for_selected_public_ips",
      "6_classify": "har_tracker_cdn_hints_plus_unknown_bucket",
      "7_document": "machine_json_hosts_inventory_plus_resolver_samples",
      "8_dns_infra": "skipped",
      "9_inventory": "rows=1"
    },
    "hosts_inventory": {
      "unique_hosts": [],
      "approx_count": 0,
      "sources": {}
    },
    "resolver_results": {},
    "classifications": {
      "rows": [],
      "notes": "Heuristic tags from HAR hints + host presence only."
    },
    "phase8_dns_infra": {},
    "phase9_third_party_inventory": [
      {
        "company_hypothesis": "(provider first-party)",
        "role": "marketing_and_app_surface",
        "how_discovered": "config_urls",
        "evidence_summary": "~0 web hosts observed",
        "evidence_tier": "desk_automation"
      }
    ],
    "raw_relpaths": {
      "hosts_inventory": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/website_exposure/hosts_inventory.json",
      "resolver_sample": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/website_exposure/resolver_sample.json",
      "phase9_inventory": "runs/nordvpn-20260501T105329Z-8cb49bd0/raw/us-california-san-jose-87/website_exposure/phase9_inventory.json"
    },
    "limits": [
      "Does_not_replace_human_narrative_for_executive_disclosure",
      "Cloudflare_or_bot_WAF_may_distort_HAR_coverage",
      "Skipped_phase8_no_provider_domains_in_config"
    ],
    "errors": []
  },
  "pcap_derived": {
    "schema_version": "1.0",
    "source_pcap": "/Users/macvm/src/vpn-leaks/.vpn-leaks/capture/session_1eaa68a91b94.pcap",
    "packet_counts": {
      "total": 334139,
      "l3_seen": 334139
    },
    "flows_unique_estimate": 847,
    "flows_sample": [
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "64810"
        ],
        "bytes": 324915368
      },
      {
        "key": [
          "ip4",
          "8efbdb21",
          "0a000032",
          "443",
          "56820"
        ],
        "bytes": 12311230
      },
      {
        "key": [
          "ip4",
          "2268237b",
          "0a000032",
          "80",
          "58081"
        ],
        "bytes": 7784281
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "64810",
          "443"
        ],
        "bytes": 2617579
      },
      {
        "key": [
          "ip4",
          "b9d3204c",
          "0a000032",
          "51820",
          "59634"
        ],
        "bytes": 1869726
      },
      {
        "key": [
          "ip4",
          "68122ae1",
          "0a000032",
          "443",
          "49208"
        ],
        "bytes": 1629126
      },
      {
        "key": [
          "ip4",
          "8efbdb21",
          "0a000032",
          "443",
          "49223"
        ],
        "bytes": 1609978
      },
      {
        "key": [
          "ip4",
          "8efb9d77",
          "0a000032",
          "443",
          "61017"
        ],
        "bytes": 1435931
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "b9d3204c",
          "59634",
          "51820"
        ],
        "bytes": 1033085
      },
      {
        "key": [
          "ip4",
          "8efb9b77",
          "0a000032",
          "443",
          "52864"
        ],
        "bytes": 849119
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "49201"
        ],
        "bytes": 810918
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a000032",
          "443",
          "49257"
        ],
        "bytes": 770767
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "54798"
        ],
        "bytes": 765604
      },
      {
        "key": [
          "ip4",
          "681213e1",
          "0a000032",
          "443",
          "49231"
        ],
        "bytes": 523544
      },
      {
        "key": [
          "ip4",
          "68122ae1",
          "0a000032",
          "443",
          "49277"
        ],
        "bytes": 415553
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49185"
        ],
        "bytes": 333866
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "61766"
        ],
        "bytes": 318445
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "52607"
        ],
        "bytes": 294625
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "57788"
        ],
        "bytes": 214903
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49197"
        ],
        "bytes": 197741
      },
      {
        "key": [
          "ip4",
          "8efbda48",
          "0a000032",
          "443",
          "49183"
        ],
        "bytes": 184065
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68122ae1",
          "49208",
          "443"
        ],
        "bytes": 174605
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "49220"
        ],
        "bytes": 139011
      },
      {
        "key": [
          "ip4",
          "8efa6554",
          "0a000032",
          "443",
          "49212"
        ],
        "bytes": 115470
      },
      {
        "key": [
          "ip4",
          "11171222",
          "0a000032",
          "443",
          "58075"
        ],
        "bytes": 114715
      },
      {
        "key": [
          "ip4",
          "8efbdb03",
          "0a000032",
          "443",
          "56223"
        ],
        "bytes": 109670
      },
      {
        "key": [
          "ip4",
          "8efbdb23",
          "0a000032",
          "443",
          "49179"
        ],
        "bytes": 98221
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb21",
          "56820",
          "443"
        ],
        "bytes": 95430
      },
      {
        "key": [
          "ip4",
          "d8ef229d",
          "0a000032",
          "443",
          "49196"
        ],
        "bytes": 95221
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb9d77",
          "61017",
          "443"
        ],
        "bytes": 79822
      },
      {
        "key": [
          "ip4",
          "8efbdb03",
          "0a000032",
          "443",
          "61688"
        ],
        "bytes": 73999
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49191"
        ],
        "bytes": 67705
      },
      {
        "key": [
          "ip4",
          "d8ef229d",
          "0a000032",
          "443",
          "49181"
        ],
        "bytes": 58939
      },
      {
        "key": [
          "ip4",
          "11f8e742",
          "0a000032",
          "443",
          "58857"
        ],
        "bytes": 54794
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49233",
          "443"
        ],
        "bytes": 52547
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb9b77",
          "52864",
          "443"
        ],
        "bytes": 48886
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "53976"
        ],
        "bytes": 47335
      },
      {
        "key": [
          "ip4",
          "8efbdb03",
          "0a000032",
          "443",
          "49203"
        ],
        "bytes": 45130
      },
      {
        "key": [
          "ip4",
          "0a000007",
          "ffffffff",
          "49154",
          "6666"
        ],
        "bytes": 43672
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a000032",
          "443",
          "49255"
        ],
        "bytes": 42852
      },
      {
        "key": [
          "ip4",
          "68122ae1",
          "0a000032",
          "443",
          "49275"
        ],
        "bytes": 41054
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49233"
        ],
        "bytes": 40484
      },
      {
        "key": [
          "ip4",
          "8efb9b77",
          "0a000032",
          "443",
          "51325"
        ],
        "bytes": 35966
      },
      {
        "key": [
          "ip4",
          "68109c6f",
          "0a000032",
          "443",
          "51076"
        ],
        "bytes": 34858
      },
      {
        "key": [
          "ip6",
          "fe800000000000000c1921ae398a3da0",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 30666
      },
      {
        "key": [
          "ip4",
          "172ed85b",
          "0a000032",
          "443",
          "49258"
        ],
        "bytes": 30535
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68122ae1",
          "49275",
          "443"
        ],
        "bytes": 30411
      },
      {
        "key": [
          "ip4",
          "0a000013",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 30179
      },
      {
        "key": [
          "ip4",
          "68109c6f",
          "0a000032",
          "443",
          "49259"
        ],
        "bytes": 30178
      },
      {
        "key": [
          "ip4",
          "8efbdaae",
          "0a000032",
          "443",
          "49230"
        ],
        "bytes": 30005
      },
      {
        "key": [
          "ip4",
          "6257e1b6",
          "0a000032",
          "443",
          "49232"
        ],
        "bytes": 29079
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681222f4",
          "49274",
          "443"
        ],
        "bytes": 27360
      },
      {
        "key": [
          "ip4",
          "d8ef229d",
          "0a000032",
          "443",
          "49205"
        ],
        "bytes": 27109
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "63845"
        ],
        "bytes": 23409
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "57788",
          "443"
        ],
        "bytes": 23080
      },
      {
        "key": [
          "ip4_raw",
          "08060001",
          "08000604",
          "0",
          "0"
        ],
        "bytes": 22488
      },
      {
        "key": [
          "ip6",
          "fe800000000000001c180eef8a345da8",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 21688
      },
      {
        "key": [
          "ip4",
          "8efbdb21",
          "0a000032",
          "443",
          "52403"
        ],
        "bytes": 21324
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "49220",
          "443"
        ],
        "bytes": 21168
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "61028"
        ],
        "bytes": 21037
      },
      {
        "key": [
          "ip4",
          "97652b06",
          "0a000032",
          "443",
          "49260"
        ],
        "bytes": 20716
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "61766",
          "443"
        ],
        "bytes": 20631
      },
      {
        "key": [
          "ip4",
          "0a000020",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 20530
      },
      {
        "key": [
          "ip4",
          "11f8e741",
          "0a000032",
          "443",
          "59659"
        ],
        "bytes": 20255
      },
      {
        "key": [
          "ip4",
          "68109c6f",
          "0a000032",
          "443",
          "59683"
        ],
        "bytes": 19626
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb21",
          "49223",
          "443"
        ],
        "bytes": 16995
      },
      {
        "key": [
          "ip4",
          "8efbda6a",
          "0a000032",
          "443",
          "50661"
        ],
        "bytes": 16863
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "54798",
          "443"
        ],
        "bytes": 16150
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a000032",
          "443",
          "49264"
        ],
        "bytes": 16061
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "52987"
        ],
        "bytes": 16013
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a000032",
          "443",
          "49229"
        ],
        "bytes": 15775
      },
      {
        "key": [
          "ip4",
          "68122ae1",
          "0a000032",
          "443",
          "49211"
        ],
        "bytes": 15163
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "64138"
        ],
        "bytes": 14873
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6e",
          "49239",
          "443"
        ],
        "bytes": 14395
      },
      {
        "key": [
          "ip4",
          "acd90c6a",
          "0a000032",
          "443",
          "49184"
        ],
        "bytes": 13995
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 13859
      },
      {
        "key": [
          "ip4",
          "ac40990c",
          "0a000032",
          "443",
          "49272"
        ],
        "bytes": 13824
      },
      {
        "key": [
          "ip4",
          "8efbda6a",
          "0a000032",
          "443",
          "51254"
        ],
        "bytes": 13782
      },
      {
        "key": [
          "ip4",
          "8efbdb0a",
          "0a000032",
          "443",
          "49214"
        ],
        "bytes": 13658
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49175"
        ],
        "bytes": 13618
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49171"
        ],
        "bytes": 13550
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "63845",
          "443"
        ],
        "bytes": 13467
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11399076",
          "49249",
          "5223"
        ],
        "bytes": 13321
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11f8e742",
          "58857",
          "443"
        ],
        "bytes": 13239
      },
      {
        "key": [
          "ip4",
          "8efbda6e",
          "0a000032",
          "443",
          "55525"
        ],
        "bytes": 13239
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "58867"
        ],
        "bytes": 13180
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a000032",
          "443",
          "49274"
        ],
        "bytes": 13177
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "2268237b",
          "58081",
          "80"
        ],
        "bytes": 12855
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68122ae1",
          "49277",
          "443"
        ],
        "bytes": 12820
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "52607",
          "443"
        ],
        "bytes": 12795
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a000032",
          "443",
          "49283"
        ],
        "bytes": 12693
      },
      {
        "key": [
          "ip4",
          "8efbdb21",
          "0a000032",
          "443",
          "52169"
        ],
        "bytes": 12539
      },
      {
        "key": [
          "ip4",
          "681222f4",
          "0a000032",
          "443",
          "49256"
        ],
        "bytes": 12486
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "49225",
          "443"
        ],
        "bytes": 12461
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 12053
      },
      {
        "key": [
          "ip4",
          "11fd058b",
          "0a000032",
          "443",
          "58078"
        ],
        "bytes": 12019
      },
      {
        "key": [
          "ip4",
          "acd90c6e",
          "0a000032",
          "443",
          "61974"
        ],
        "bytes": 11899
      },
      {
        "key": [
          "ip4",
          "8efbda6e",
          "0a000032",
          "443",
          "61830"
        ],
        "bytes": 11894
      },
      {
        "key": [
          "ip4",
          "acd90c6e",
          "0a000032",
          "443",
          "57366"
        ],
        "bytes": 11866
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "65315"
        ],
        "bytes": 11739
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "ac409937",
          "49210",
          "443"
        ],
        "bytes": 11621
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "49209"
        ],
        "bytes": 11593
      },
      {
        "key": [
          "ip4",
          "8efbda62",
          "0a000032",
          "443",
          "57026"
        ],
        "bytes": 11396
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a000032",
          "443",
          "55526"
        ],
        "bytes": 11322
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "64232"
        ],
        "bytes": 11317
      },
      {
        "key": [
          "ip4",
          "8efbdb21",
          "0a000032",
          "443",
          "54940"
        ],
        "bytes": 11295
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "63114"
        ],
        "bytes": 11266
      },
      {
        "key": [
          "ip4",
          "8efbd62a",
          "0a000032",
          "443",
          "58993"
        ],
        "bytes": 11208
      },
      {
        "key": [
          "ip4",
          "acd90c6e",
          "0a000032",
          "443",
          "49239"
        ],
        "bytes": 11180
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "49225"
        ],
        "bytes": 11101
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "56247"
        ],
        "bytes": 11087
      },
      {
        "key": [
          "ip4",
          "ac409937",
          "0a000032",
          "443",
          "49210"
        ],
        "bytes": 11032
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "49202"
        ],
        "bytes": 10913
      },
      {
        "key": [
          "ip4",
          "8efa6554",
          "0a000032",
          "443",
          "60849"
        ],
        "bytes": 10858
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681222f4",
          "49257",
          "443"
        ],
        "bytes": 10759
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "49221"
        ],
        "bytes": 10758
      },
      {
        "key": [
          "ip4",
          "8efbda48",
          "0a000032",
          "443",
          "54736"
        ],
        "bytes": 10734
      },
      {
        "key": [
          "ip4",
          "acd90c6a",
          "0a000032",
          "443",
          "65475"
        ],
        "bytes": 10593
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49185",
          "443"
        ],
        "bytes": 10540
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "64079",
          "443"
        ],
        "bytes": 10395
      },
      {
        "key": [
          "ip4",
          "8efbdb2a",
          "0a000032",
          "443",
          "49207"
        ],
        "bytes": 10376
      },
      {
        "key": [
          "ip4",
          "8efbda8a",
          "0a000032",
          "443",
          "49193"
        ],
        "bytes": 10053
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49187"
        ],
        "bytes": 10013
      },
      {
        "key": [
          "ip4",
          "8efa6554",
          "0a000032",
          "443",
          "60061"
        ],
        "bytes": 9907
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "51926"
        ],
        "bytes": 9904
      },
      {
        "key": [
          "ip4",
          "8efbda6a",
          "0a000032",
          "443",
          "49222"
        ],
        "bytes": 9696
      },
      {
        "key": [
          "ip6",
          "fe800000000000000042ec78e0ff5a42",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 9632
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "49201",
          "443"
        ],
        "bytes": 9593
      },
      {
        "key": [
          "ip4",
          "8efbd62a",
          "0a000032",
          "443",
          "49263"
        ],
        "bytes": 9535
      },
      {
        "key": [
          "ip4",
          "8efbda42",
          "0a000032",
          "443",
          "64487"
        ],
        "bytes": 9534
      },
      {
        "key": [
          "ip4",
          "8efbda6a",
          "0a000032",
          "443",
          "49213"
        ],
        "bytes": 9442
      },
      {
        "key": [
          "ip4",
          "11fd058b",
          "0a000032",
          "443",
          "58079"
        ],
        "bytes": 9421
      },
      {
        "key": [
          "ip4",
          "8efbdb2a",
          "0a000032",
          "443",
          "53260"
        ],
        "bytes": 9340
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "49279"
        ],
        "bytes": 9300
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb03",
          "56223",
          "443"
        ],
        "bytes": 9253
      },
      {
        "key": [
          "ip4",
          "acd90c6e",
          "0a000032",
          "443",
          "49271"
        ],
        "bytes": 9208
      },
      {
        "key": [
          "ip4",
          "0a00002f",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 9063
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "d8ef229d",
          "49196",
          "443"
        ],
        "bytes": 9062
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "d8ef229d",
          "49181",
          "443"
        ],
        "bytes": 8959
      },
      {
        "key": [
          "ip4",
          "11fd7f86",
          "0a000032",
          "443",
          "49265"
        ],
        "bytes": 8956
      },
      {
        "key": [
          "ip4",
          "8efbda8a",
          "0a000032",
          "443",
          "49218"
        ],
        "bytes": 8915
      },
      {
        "key": [
          "ip4",
          "8efbda6e",
          "0a000032",
          "443",
          "58080"
        ],
        "bytes": 8889
      },
      {
        "key": [
          "ip4",
          "11fd0596",
          "0a000032",
          "443",
          "49254"
        ],
        "bytes": 8884
      },
      {
        "key": [
          "ip4",
          "11fd05a2",
          "0a000032",
          "443",
          "49281"
        ],
        "bytes": 8869
      },
      {
        "key": [
          "ip4",
          "8efbda86",
          "0a000032",
          "443",
          "49206"
        ],
        "bytes": 8843
      },
      {
        "key": [
          "ip4",
          "9765295b",
          "0a000032",
          "443",
          "49219"
        ],
        "bytes": 8723
      },
      {
        "key": [
          "ip4",
          "ac40990c",
          "0a000032",
          "443",
          "49273"
        ],
        "bytes": 8567
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49172"
        ],
        "bytes": 8556
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49174"
        ],
        "bytes": 8556
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49189"
        ],
        "bytes": 8547
      },
      {
        "key": [
          "ip4",
          "11fd0586",
          "0a000032",
          "443",
          "49251"
        ],
        "bytes": 8524
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49173"
        ],
        "bytes": 8482
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49188"
        ],
        "bytes": 8481
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49253"
        ],
        "bytes": 8451
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49186"
        ],
        "bytes": 8414
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "49190"
        ],
        "bytes": 8414
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb03",
          "61688",
          "443"
        ],
        "bytes": 8348
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109c6f",
          "51076",
          "443"
        ],
        "bytes": 8338
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "61990"
        ],
        "bytes": 8280
      },
      {
        "key": [
          "ip4",
          "11399076",
          "0a000032",
          "5223",
          "49249"
        ],
        "bytes": 8272
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb2a",
          "49207",
          "443"
        ],
        "bytes": 8151
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49248"
        ],
        "bytes": 8114
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "53976",
          "443"
        ],
        "bytes": 7972
      },
      {
        "key": [
          "ip4",
          "d8ef22df",
          "0a000032",
          "443",
          "49250"
        ],
        "bytes": 7906
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "58867",
          "443"
        ],
        "bytes": 7887
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda48",
          "49183",
          "443"
        ],
        "bytes": 7880
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49246"
        ],
        "bytes": 7851
      },
      {
        "key": [
          "ip4",
          "11fd7f86",
          "0a000032",
          "443",
          "49267"
        ],
        "bytes": 7801
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6e",
          "61830",
          "443"
        ],
        "bytes": 7778
      },
      {
        "key": [
          "ip4",
          "8efbda48",
          "0a000032",
          "443",
          "49182"
        ],
        "bytes": 7767
      },
      {
        "key": [
          "ip4",
          "11fd05a2",
          "0a000032",
          "443",
          "49280"
        ],
        "bytes": 7750
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdaaa",
          "49229",
          "443"
        ],
        "bytes": 7689
      },
      {
        "key": [
          "ip4",
          "8efbda8a",
          "0a000032",
          "443",
          "49215"
        ],
        "bytes": 7613
      },
      {
        "key": [
          "ip4",
          "8efbda8a",
          "0a000032",
          "443",
          "49216"
        ],
        "bytes": 7613
      },
      {
        "key": [
          "ip4",
          "8efbda8a",
          "0a000032",
          "443",
          "49217"
        ],
        "bytes": 7547
      },
      {
        "key": [
          "ip4",
          "11fd53ca",
          "0a000032",
          "443",
          "58076"
        ],
        "bytes": 7544
      },
      {
        "key": [
          "ip4",
          "34568e3f",
          "0a000032",
          "8885",
          "49242"
        ],
        "bytes": 7531
      },
      {
        "key": [
          "ip4",
          "8efbdb16",
          "0a000032",
          "443",
          "49204"
        ],
        "bytes": 7493
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb21",
          "52169",
          "443"
        ],
        "bytes": 7407
      },
      {
        "key": [
          "ip4",
          "11fd900a",
          "0a000032",
          "443",
          "49269"
        ],
        "bytes": 7361
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49197",
          "443"
        ],
        "bytes": 7336
      },
      {
        "key": [
          "ip4",
          "6812042d",
          "0a000032",
          "443",
          "49240"
        ],
        "bytes": 7293
      },
      {
        "key": [
          "ip4",
          "68109b6f",
          "0a000032",
          "443",
          "60361"
        ],
        "bytes": 7175
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11f8e741",
          "59659",
          "443"
        ],
        "bytes": 7135
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49192"
        ],
        "bytes": 7057
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdaaa",
          "55526",
          "443"
        ],
        "bytes": 7026
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681213e1",
          "49231",
          "443"
        ],
        "bytes": 7002
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "49226"
        ],
        "bytes": 6970
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda62",
          "57026",
          "443"
        ],
        "bytes": 6837
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6e",
          "61974",
          "443"
        ],
        "bytes": 6811
      },
      {
        "key": [
          "ip4",
          "8efbdace",
          "0a000032",
          "443",
          "50560"
        ],
        "bytes": 6809
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6a",
          "51254",
          "443"
        ],
        "bytes": 6798
      },
      {
        "key": [
          "ip4",
          "9765295b",
          "0a000032",
          "443",
          "59758"
        ],
        "bytes": 6768
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb21",
          "52403",
          "443"
        ],
        "bytes": 6766
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "d8ef229d",
          "49205",
          "443"
        ],
        "bytes": 6644
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda48",
          "53848",
          "443"
        ],
        "bytes": 6644
      },
      {
        "key": [
          "ip4",
          "8efa6554",
          "0a000032",
          "443",
          "63631"
        ],
        "bytes": 6611
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "49227"
        ],
        "bytes": 6602
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6e",
          "55525",
          "443"
        ],
        "bytes": 6567
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "49228"
        ],
        "bytes": 6524
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "51654"
        ],
        "bytes": 6456
      },
      {
        "key": [
          "ip4",
          "8efbda48",
          "0a000032",
          "443",
          "53848"
        ],
        "bytes": 6426
      },
      {
        "key": [
          "ip4",
          "8efbdaaa",
          "0a000032",
          "443",
          "57236"
        ],
        "bytes": 6426
      },
      {
        "key": [
          "ip4",
          "11fd900a",
          "0a000032",
          "443",
          "49268"
        ],
        "bytes": 6400
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "9765295b",
          "63165",
          "443"
        ],
        "bytes": 6396
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "61990",
          "443"
        ],
        "bytes": 6385
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "64232",
          "443"
        ],
        "bytes": 6355
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6e",
          "57366",
          "443"
        ],
        "bytes": 6237
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efa6554",
          "49212",
          "443"
        ],
        "bytes": 6168
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "65315",
          "443"
        ],
        "bytes": 6131
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49177"
        ],
        "bytes": 6085
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8a",
          "49193",
          "443"
        ],
        "bytes": 6072
      },
      {
        "key": [
          "ip4",
          "11fd53c6",
          "0a000032",
          "443",
          "58077"
        ],
        "bytes": 6042
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb9b77",
          "51325",
          "443"
        ],
        "bytes": 6022
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49178"
        ],
        "bytes": 6021
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49176"
        ],
        "bytes": 6007
      },
      {
        "key": [
          "ip4",
          "404ec801",
          "0a000032",
          "443",
          "49266"
        ],
        "bytes": 5981
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49194"
        ],
        "bytes": 5943
      },
      {
        "key": [
          "ip4",
          "8efbd62e",
          "0a000032",
          "443",
          "49195"
        ],
        "bytes": 5943
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda48",
          "54736",
          "443"
        ],
        "bytes": 5935
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "34568e3f",
          "49244",
          "8885"
        ],
        "bytes": 5933
      },
      {
        "key": [
          "ip4",
          "8efbdb23",
          "0a000032",
          "443",
          "49180"
        ],
        "bytes": 5919
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6a",
          "65475",
          "443"
        ],
        "bytes": 5894
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49200"
        ],
        "bytes": 5854
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49199"
        ],
        "bytes": 5853
      },
      {
        "key": [
          "ip4",
          "8efbda83",
          "0a000032",
          "443",
          "49198"
        ],
        "bytes": 5852
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49191",
          "443"
        ],
        "bytes": 5832
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49175",
          "443"
        ],
        "bytes": 5824
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49171",
          "443"
        ],
        "bytes": 5806
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "51654",
          "443"
        ],
        "bytes": 5752
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb23",
          "49179",
          "443"
        ],
        "bytes": 5746
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8a",
          "49218",
          "443"
        ],
        "bytes": 5736
      },
      {
        "key": [
          "ip4",
          "acd90c6a",
          "0a000032",
          "443",
          "52418"
        ],
        "bytes": 5694
      },
      {
        "key": [
          "ip4",
          "9765295b",
          "0a000032",
          "443",
          "63165"
        ],
        "bytes": 5607
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11171222",
          "58075",
          "443"
        ],
        "bytes": 5549
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49237"
        ],
        "bytes": 5511
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "63114",
          "443"
        ],
        "bytes": 5505
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49236"
        ],
        "bytes": 5445
      },
      {
        "key": [
          "ip4",
          "8efbdb0e",
          "0a000032",
          "443",
          "56182"
        ],
        "bytes": 5437
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efa6554",
          "60849",
          "443"
        ],
        "bytes": 5378
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda86",
          "49206",
          "443"
        ],
        "bytes": 5357
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda42",
          "64487",
          "443"
        ],
        "bytes": 5326
      },
      {
        "key": [
          "ip4",
          "8efbda6a",
          "0a000032",
          "443",
          "65273"
        ],
        "bytes": 5309
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "56247",
          "443"
        ],
        "bytes": 5304
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "61028",
          "443"
        ],
        "bytes": 5267
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efa6554",
          "63631",
          "443"
        ],
        "bytes": 5259
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0a",
          "49214",
          "443"
        ],
        "bytes": 5249
      },
      {
        "key": [
          "ip4",
          "8efbda8e",
          "0a000032",
          "443",
          "64079"
        ],
        "bytes": 5238
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "64138",
          "443"
        ],
        "bytes": 5230
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6a",
          "50661",
          "443"
        ],
        "bytes": 5200
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdaae",
          "49230",
          "443"
        ],
        "bytes": 5118
      },
      {
        "key": [
          "ip4",
          "8efb9b77",
          "0a000032",
          "443",
          "62892"
        ],
        "bytes": 5090
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "9765295b",
          "52223",
          "443"
        ],
        "bytes": 5058
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62a",
          "58993",
          "443"
        ],
        "bytes": 5054
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "ac409937",
          "49278",
          "443"
        ],
        "bytes": 5026
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49246",
          "443"
        ],
        "bytes": 5000
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "ac40990c",
          "49272",
          "443"
        ],
        "bytes": 4955
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "56182",
          "443"
        ],
        "bytes": 4940
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6a",
          "65273",
          "443"
        ],
        "bytes": 4938
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681222f4",
          "49255",
          "443"
        ],
        "bytes": 4917
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "34568e3f",
          "49242",
          "8885"
        ],
        "bytes": 4855
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6a",
          "52418",
          "443"
        ],
        "bytes": 4836
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "51926",
          "443"
        ],
        "bytes": 4820
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb21",
          "54940",
          "443"
        ],
        "bytes": 4800
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "50560",
          "443"
        ],
        "bytes": 4786
      },
      {
        "key": [
          "ip4",
          "acd90c6a",
          "0a000032",
          "443",
          "55676"
        ],
        "bytes": 4763
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812042d",
          "49240",
          "443"
        ],
        "bytes": 4724
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 4720
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "60361",
          "443"
        ],
        "bytes": 4709
      },
      {
        "key": [
          "ip6",
          "fe8000000000000010489695fc3fc856",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 4699
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "52987",
          "443"
        ],
        "bytes": 4640
      },
      {
        "key": [
          "ip4",
          "9765295b",
          "0a000032",
          "443",
          "52223"
        ],
        "bytes": 4625
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "9765295b",
          "49219",
          "443"
        ],
        "bytes": 4576
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6a",
          "49213",
          "443"
        ],
        "bytes": 4493
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd05a2",
          "49281",
          "443"
        ],
        "bytes": 4481
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efa6554",
          "60061",
          "443"
        ],
        "bytes": 4432
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb2a",
          "53260",
          "443"
        ],
        "bytes": 4423
      },
      {
        "key": [
          "ip4",
          "ac409937",
          "0a000032",
          "443",
          "49278"
        ],
        "bytes": 4357
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "34568e3f",
          "49243",
          "8885"
        ],
        "bytes": 4351
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb03",
          "49203",
          "443"
        ],
        "bytes": 4347
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "49202",
          "443"
        ],
        "bytes": 4265
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6257e1b6",
          "49232",
          "443"
        ],
        "bytes": 4258
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68122ae1",
          "49211",
          "443"
        ],
        "bytes": 4165
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6a",
          "49222",
          "443"
        ],
        "bytes": 4158
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49234"
        ],
        "bytes": 4099
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49173",
          "443"
        ],
        "bytes": 4066
      },
      {
        "key": [
          "ip4",
          "6812042d",
          "0a000032",
          "443",
          "49241"
        ],
        "bytes": 4009
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49235"
        ],
        "bytes": 3998
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49172",
          "443"
        ],
        "bytes": 3980
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda6e",
          "58080",
          "443"
        ],
        "bytes": 3980
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdaaa",
          "57236",
          "443"
        ],
        "bytes": 3954
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49174",
          "443"
        ],
        "bytes": 3948
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdaaa",
          "49264",
          "443"
        ],
        "bytes": 3897
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "172ed85b",
          "49258",
          "443"
        ],
        "bytes": 3891
      },
      {
        "key": [
          "ip4",
          "6812052d",
          "0a000032",
          "443",
          "49238"
        ],
        "bytes": 3866
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "36e1633e",
          "49247",
          "8885"
        ],
        "bytes": 3866
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "36e1633e",
          "49270",
          "8885"
        ],
        "bytes": 3865
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49234",
          "443"
        ],
        "bytes": 3818
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6a",
          "49184",
          "443"
        ],
        "bytes": 3781
      },
      {
        "key": [
          "ip6",
          "fe80000000000000008fa897dc041e87",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 3774
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49176",
          "443"
        ],
        "bytes": 3716
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "36e1633e",
          "49284",
          "8885"
        ],
        "bytes": 3702
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "49209",
          "443"
        ],
        "bytes": 3700
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49178",
          "443"
        ],
        "bytes": 3662
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 3614
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd53c6",
          "58077",
          "443"
        ],
        "bytes": 3611
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49177",
          "443"
        ],
        "bytes": 3598
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49248",
          "443"
        ],
        "bytes": 3597
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "36e1633e",
          "49282",
          "8885"
        ],
        "bytes": 3558
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49253",
          "443"
        ],
        "bytes": 3544
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6a",
          "55676",
          "443"
        ],
        "bytes": 3528
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "36e1633e",
          "49252",
          "8885"
        ],
        "bytes": 3495
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "d8ef22df",
          "49250",
          "443"
        ],
        "bytes": 3480
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "34568e3f",
          "49245",
          "8885"
        ],
        "bytes": 3463
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109c6f",
          "49259",
          "443"
        ],
        "bytes": 3404
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb9b77",
          "62892",
          "443"
        ],
        "bytes": 3361
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62a",
          "49263",
          "443"
        ],
        "bytes": 3332
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd7f86",
          "49265",
          "443"
        ],
        "bytes": 3263
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "9765295b",
          "59758",
          "443"
        ],
        "bytes": 3201
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd53ca",
          "58076",
          "443"
        ],
        "bytes": 3165
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd058b",
          "58078",
          "443"
        ],
        "bytes": 3146
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "acd90c6e",
          "49271",
          "443"
        ],
        "bytes": 3113
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "97652b06",
          "49260",
          "443"
        ],
        "bytes": 2946
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd05a2",
          "49280",
          "443"
        ],
        "bytes": 2876
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd7f86",
          "49267",
          "443"
        ],
        "bytes": 2815
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681222f4",
          "49256",
          "443"
        ],
        "bytes": 2775
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd058b",
          "58079",
          "443"
        ],
        "bytes": 2765
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd0586",
          "49251",
          "443"
        ],
        "bytes": 2725
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd0596",
          "49254",
          "443"
        ],
        "bytes": 2712
      },
      {
        "key": [
          "ip4",
          "34568e3f",
          "0a000032",
          "8885",
          "49244"
        ],
        "bytes": 2664
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "681222f4",
          "49283",
          "443"
        ],
        "bytes": 2655
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd900a",
          "49268",
          "443"
        ],
        "bytes": 2642
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb0e",
          "49221",
          "443"
        ],
        "bytes": 2633
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb16",
          "49204",
          "443"
        ],
        "bytes": 2585
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8a",
          "49217",
          "443"
        ],
        "bytes": 2543
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8a",
          "49216",
          "443"
        ],
        "bytes": 2489
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109c6f",
          "59683",
          "443"
        ],
        "bytes": 2484
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "11fd900a",
          "49269",
          "443"
        ],
        "bytes": 2442
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49192",
          "443"
        ],
        "bytes": 2436
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda48",
          "49182",
          "443"
        ],
        "bytes": 2434
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8a",
          "49215",
          "443"
        ],
        "bytes": 2425
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "ac40990c",
          "49273",
          "443"
        ],
        "bytes": 2423
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "404ec801",
          "49266",
          "443"
        ],
        "bytes": 2395
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "0a000001",
          "0",
          "0"
        ],
        "bytes": 2394
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "49279",
          "443"
        ],
        "bytes": 2392
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812042d",
          "49241",
          "443"
        ],
        "bytes": 2330
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49186",
          "443"
        ],
        "bytes": 2271
      },
      {
        "key": [
          "ip6",
          "fe800000000000001c628c122f1cc477",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 2269
      },
      {
        "key": [
          "ip6",
          "fe800000000000003a22e2fffe4e4566",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 2259
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "49227",
          "443"
        ],
        "bytes": 2248
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49235",
          "443"
        ],
        "bytes": 2242
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49195",
          "443"
        ],
        "bytes": 2228
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "49226",
          "443"
        ],
        "bytes": 2226
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49188",
          "443"
        ],
        "bytes": 2217
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49200",
          "443"
        ],
        "bytes": 2217
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49198",
          "443"
        ],
        "bytes": 2207
      },
      {
        "key": [
          "ip4",
          "0a00000f",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 2199
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49237",
          "443"
        ],
        "bytes": 2188
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49187",
          "443"
        ],
        "bytes": 2187
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49189",
          "443"
        ],
        "bytes": 2185
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdace",
          "49190",
          "443"
        ],
        "bytes": 2185
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda83",
          "49199",
          "443"
        ],
        "bytes": 2185
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49238",
          "443"
        ],
        "bytes": 2178
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbd62e",
          "49194",
          "443"
        ],
        "bytes": 2164
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbda8e",
          "49228",
          "443"
        ],
        "bytes": 2162
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "6812052d",
          "49236",
          "443"
        ],
        "bytes": 2156
      },
      {
        "key": [
          "ip4",
          "0a000027",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 2127
      },
      {
        "key": [
          "ip4",
          "34568e3f",
          "0a000032",
          "8885",
          "49243"
        ],
        "bytes": 2125
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efbdb23",
          "49180",
          "443"
        ],
        "bytes": 2121
      },
      {
        "key": [
          "ip4",
          "36e1633e",
          "0a000032",
          "8885",
          "49247"
        ],
        "bytes": 1948
      },
      {
        "key": [
          "ip4",
          "0a00000f",
          "0a000032",
          "5353",
          "5353"
        ],
        "bytes": 1906
      },
      {
        "key": [
          "ip4",
          "36e1633e",
          "0a000032",
          "8885",
          "49270"
        ],
        "bytes": 1816
      },
      {
        "key": [
          "ip4",
          "34568e3f",
          "0a000032",
          "8885",
          "49245"
        ],
        "bytes": 1783
      },
      {
        "key": [
          "ip4",
          "36e1633e",
          "0a000032",
          "8885",
          "49282"
        ],
        "bytes": 1783
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "0",
          "0"
        ],
        "bytes": 1764
      },
      {
        "key": [
          "ip4",
          "36e1633e",
          "0a000032",
          "8885",
          "49252"
        ],
        "bytes": 1761
      },
      {
        "key": [
          "ip4",
          "36e1633e",
          "0a000032",
          "8885",
          "49284"
        ],
        "bytes": 1666
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "ffffffff",
          "67",
          "68"
        ],
        "bytes": 1180
      },
      {
        "key": [
          "ip4",
          "170b219f",
          "0a000032",
          "80",
          "49261"
        ],
        "bytes": 1111
      },
      {
        "key": [
          "ip4",
          "170b219f",
          "0a000032",
          "80",
          "49262"
        ],
        "bytes": 1111
      },
      {
        "key": [
          "ip4",
          "0a000022",
          "0a0000ff",
          "35749",
          "20002"
        ],
        "bytes": 991
      },
      {
        "key": [
          "ip4",
          "0a000023",
          "0a0000ff",
          "42298",
          "20002"
        ],
        "bytes": 991
      },
      {
        "key": [
          "ip4",
          "0a000004",
          "0a0000ff",
          "60825",
          "20002"
        ],
        "bytes": 991
      },
      {
        "key": [
          "ip6",
          "fe800000000000003a22e2fffe4e4566",
          "ff020000000000000000000000010002",
          "546",
          "547"
        ],
        "bytes": 960
      },
      {
        "key": [
          "ip4",
          "0a000010",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 736
      },
      {
        "key": [
          "ip6",
          "fe800000000000000042ec78e0ff5a42",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 720
      },
      {
        "key": [
          "ip4",
          "00000000",
          "ffffffff",
          "68",
          "67"
        ],
        "bytes": 684
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "170b219f",
          "49261",
          "80"
        ],
        "bytes": 629
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "170b219f",
          "49262",
          "80"
        ],
        "bytes": 629
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "0a0000ff",
          "137",
          "137"
        ],
        "bytes": 606
      },
      {
        "key": [
          "ip6",
          "fe80000000000000466132fffee612f0",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 606
      },
      {
        "key": [
          "ip4",
          "0a000011",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 586
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "0a00000f",
          "5353",
          "5353"
        ],
        "bytes": 583
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "58359"
        ],
        "bytes": 572
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "54807"
        ],
        "bytes": 548
      },
      {
        "key": [
          "ip6",
          "fe800000000000001c180eef8a345da8",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 540
      },
      {
        "key": [
          "ip6",
          "fe8000000000000010489695fc3fc856",
          "ff020000000000000000000000000001",
          "0",
          "0"
        ],
        "bytes": 504
      },
      {
        "key": [
          "ip4",
          "0a00000d",
          "0a000032",
          "5353",
          "5353"
        ],
        "bytes": 498
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109b6f",
          "0",
          "0"
        ],
        "bytes": 490
      },
      {
        "key": [
          "ip4",
          "0a00000e",
          "0a000032",
          "5353",
          "5353"
        ],
        "bytes": 470
      },
      {
        "key": [
          "ip6_raw",
          "41ed134d08060001080006040002dece",
          "41ed134d0a000032e4f4c61bc17e0a00",
          "0",
          "0"
        ],
        "bytes": 462
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "10178"
        ],
        "bytes": 451
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "58139"
        ],
        "bytes": 451
      },
      {
        "key": [
          "ip6",
          "00000000000000000000000000000000",
          "ff020000000000000000000000000001",
          "0",
          "0"
        ],
        "bytes": 430
      },
      {
        "key": [
          "ip4",
          "0a00001a",
          "ffffffff",
          "9999",
          "9999"
        ],
        "bytes": 420
      },
      {
        "key": [
          "ip4",
          "0a000020",
          "e00000fb",
          "0",
          "0"
        ],
        "bytes": 420
      },
      {
        "key": [
          "ip4",
          "0a00002f",
          "e0000002",
          "0",
          "0"
        ],
        "bytes": 414
      },
      {
        "key": [
          "ip4",
          "0a000015",
          "e00000fb",
          "5353",
          "5353"
        ],
        "bytes": 411
      },
      {
        "key": [
          "ip4",
          "0a00001a",
          "effffffa",
          "1900",
          "1900"
        ],
        "bytes": 408
      },
      {
        "key": [
          "ip4",
          "8efb02bc",
          "0a000032",
          "5228",
          "49165"
        ],
        "bytes": 396
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "25829"
        ],
        "bytes": 396
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "58481"
        ],
        "bytes": 396
      },
      {
        "key": [
          "ip6_raw",
          "41ed134d08060001080006040001dece",
          "41ed134d0a000032e4f4c61bc17e0a00",
          "0",
          "0"
        ],
        "bytes": 378
      },
      {
        "key": [
          "ip4",
          "0a00002f",
          "e00000fb",
          "0",
          "0"
        ],
        "bytes": 368
      },
      {
        "key": [
          "ip4",
          "0a000020",
          "e0000002",
          "0",
          "0"
        ],
        "bytes": 360
      },
      {
        "key": [
          "ip6",
          "fe800000000000000c1921ae398a3da0",
          "ff020000000000000000000000000016",
          "0",
          "0"
        ],
        "bytes": 360
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "60201"
        ],
        "bytes": 350
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "0a000001",
          "68",
          "67"
        ],
        "bytes": 343
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "59929"
        ],
        "bytes": 326
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "8efb02bc",
          "49165",
          "5228"
        ],
        "bytes": 324
      },
      {
        "key": [
          "ip4",
          "0a00002b",
          "0a000032",
          "5353",
          "5353"
        ],
        "bytes": 315
      },
      {
        "key": [
          "ip4",
          "00000000",
          "e0000001",
          "0",
          "0"
        ],
        "bytes": 300
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "68109c6f",
          "0",
          "0"
        ],
        "bytes": 280
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "60179"
        ],
        "bytes": 277
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "41828"
        ],
        "bytes": 272
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "52167"
        ],
        "bytes": 272
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "49295"
        ],
        "bytes": 270
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "1821"
        ],
        "bytes": 269
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "5146"
        ],
        "bytes": 264
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "42517"
        ],
        "bytes": 256
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "52561"
        ],
        "bytes": 256
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "52420"
        ],
        "bytes": 255
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "63488"
        ],
        "bytes": 251
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "9109"
        ],
        "bytes": 251
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "47439"
        ],
        "bytes": 251
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "32333"
        ],
        "bytes": 251
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "31252"
        ],
        "bytes": 250
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "18267"
        ],
        "bytes": 241
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "effffffa",
          "0",
          "0"
        ],
        "bytes": 240
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57422"
        ],
        "bytes": 238
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "52480"
        ],
        "bytes": 237
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "61631"
        ],
        "bytes": 237
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "38118"
        ],
        "bytes": 231
      },
      {
        "key": [
          "ip4",
          "0a000013",
          "e00000fb",
          "0",
          "0"
        ],
        "bytes": 230
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "64931"
        ],
        "bytes": 215
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "55963"
        ],
        "bytes": 215
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "64567"
        ],
        "bytes": 215
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "51620"
        ],
        "bytes": 214
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57381"
        ],
        "bytes": 202
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "26762"
        ],
        "bytes": 202
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "2005"
        ],
        "bytes": 193
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "65035"
        ],
        "bytes": 192
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "50490"
        ],
        "bytes": 186
      },
      {
        "key": [
          "ip4",
          "0a00000f",
          "e000013c",
          "0",
          "0"
        ],
        "bytes": 184
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "59388"
        ],
        "bytes": 183
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57158"
        ],
        "bytes": 183
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "40284"
        ],
        "bytes": 181
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "56757"
        ],
        "bytes": 181
      },
      {
        "key": [
          "ip4",
          "0a000015",
          "effffffa",
          "0",
          "0"
        ],
        "bytes": 180
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "50774"
        ],
        "bytes": 180
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "28235"
        ],
        "bytes": 180
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "2648"
        ],
        "bytes": 180
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "53936"
        ],
        "bytes": 180
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "19931"
        ],
        "bytes": 179
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "38208"
        ],
        "bytes": 179
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "50204"
        ],
        "bytes": 178
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "28501"
        ],
        "bytes": 178
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "22348"
        ],
        "bytes": 176
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "63908"
        ],
        "bytes": 175
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "9532"
        ],
        "bytes": 174
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "49871"
        ],
        "bytes": 173
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "53660"
        ],
        "bytes": 173
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "13328"
        ],
        "bytes": 173
      },
      {
        "key": [
          "ip6",
          "fe80000000000000466132fffe01a336",
          "ff0200000000000000000000000000fb",
          "5353",
          "5353"
        ],
        "bytes": 172
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "53270"
        ],
        "bytes": 171
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "47850"
        ],
        "bytes": 171
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "26802"
        ],
        "bytes": 171
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "63554"
        ],
        "bytes": 168
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "1957"
        ],
        "bytes": 165
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "54006"
        ],
        "bytes": 165
      },
      {
        "key": [
          "ip4",
          "0a000004",
          "e00000fb",
          "59373",
          "5353"
        ],
        "bytes": 162
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "39817"
        ],
        "bytes": 159
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "55873"
        ],
        "bytes": 159
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "50413"
        ],
        "bytes": 157
      },
      {
        "key": [
          "ip4",
          "0a000032",
          "0a000001",
          "58359",
          "53"
        ],
        "bytes": 157
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "58630"
        ],
        "bytes": 157
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "15850"
        ],
        "bytes": 156
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "27278"
        ],
        "bytes": 154
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "40773"
        ],
        "bytes": 154
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "25827"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "47784"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "50291"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "37108"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "61905"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57365"
        ],
        "bytes": 153
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57250"
        ],
        "bytes": 152
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "57544"
        ],
        "bytes": 152
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "47382"
        ],
        "bytes": 151
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "53119"
        ],
        "bytes": 151
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "15051"
        ],
        "bytes": 150
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "41193"
        ],
        "bytes": 150
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "61266"
        ],
        "bytes": 150
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "51447"
        ],
        "bytes": 150
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "48766"
        ],
        "bytes": 148
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "42502"
        ],
        "bytes": 148
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "6294"
        ],
        "bytes": 148
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "19989"
        ],
        "bytes": 148
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "60091"
        ],
        "bytes": 147
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "8250"
        ],
        "bytes": 147
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "63843"
        ],
        "bytes": 147
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "42475"
        ],
        "bytes": 147
      },
      {
        "key": [
          "ip4",
          "0a000001",
          "0a000032",
          "53",
          "49424"
        ],
        "bytes": 146
      }
    ],
    "tls_clienthello_snis_unique": [],
    "opaque_tls_hints": 234,
    "dns_hostnames_unique": [
      "1.courier-push-apple.com.akadns.net",
      "1.courier-sandbox-push-apple.com.akadns.net",
      "28-courier.push.apple.com",
      "45.courier-push-apple.com.akadns.net",
      "_8885._https.nc-mqtt.nordpass.com",
      "accounts.google.com",
      "api-toggle.nordpass.com",
      "api.apple-cloudkit.com",
      "api.apple-cloudkit.fe2.apple-dns.net",
      "api.nordpass.com",
      "apis.google.com",
      "app-analytics-services.com",
      "app-site-association.cdn-apple.com",
      "apple.com",
      "applytics.napps-1.com",
      "auth.napps-1.com",
      "auth.nordaccount.com",
      "auth.nordpass.com",
      "background-weighted.ls4-apple.com.akadns.net",
      "bag-cdn.itunes-apple.com.akadns.net",
      "chromewebstore.google.com",
      "clients2.google.com",
      "clients2.googleusercontent.com",
      "clientservices.googleapis.com",
      "content-autofill.googleapis.com",
      "d.nordaccount.com",
      "debug.nordpass.com",
      "debug.nordsec.com",
      "dns-tunnel-check.googlezip.net",
      "doh-dns-apple-com.v.aaplimg.com",
      "doh.dns.apple.com",
      "downloads.napps-1.com",
      "downloads.nordcdn.com",
      "downloads.npass.app",
      "edgedl.me.gvt1.com",
      "eip-terr-na.cdp1.digicert.com.akahost.net",
      "encrypted-tbn0.gstatic.com",
      "feedback-pa.clients6.google.com",
      "firebase-settings.crashlytics.com",
      "firebaseinstallations.googleapis.com",
      "firebaselogging-pa.googleapis.com",
      "firebaseremoteconfig.googleapis.com",
      "fonts.googleapis.com",
      "fonts.gstatic.com",
      "gdmf.apple.com",
      "gdmf.v.aaplimg.com",
      "get-bx.g.aaplimg.com",
      "google-ohttp-relay-safebrowsing.fastly-edge.com",
      "googleads.g.doubleclick.net",
      "i.ytimg.com",
      "icloud.com",
      "img.youtube.com",
      "jnn-pa.googleapis.com",
      "lensfrontend-pa.googleapis.com",
      "lh3.googleusercontent.com",
      "my.nordaccount.com",
      "napps-1.com",
      "nc-mqtt.nordpass.com",
      "nordaccount.com",
      "ocsp.digicert.com",
      "ocsp2.apple.com",
      "ocsp2.g.aaplimg.com",
      "ogads-pa.clients6.google.com",
      "ogs.google.com",
      "passwordsleakcheck-pa.googleapis.com",
      "play.google.com",
      "s1.nordaccount.com",
      "s1.nordcdn.com",
      "s1.npass.app",
      "sandbox.itunes.apple.com",
      "sb-ssl.google.com",
      "sb.nordcdn.com",
      "ssl.gstatic.com",
      "static.doubleclick.net",
      "tunnel.googlezip.net",
      "update.googleapis.com",
      "www.google-analytics.com",
      "www.google.com",
      "www.googleadservices.com",
      "www.googleapis.com",
      "www.googletagmanager.com",
      "www.gstatic.com",
      "www.youtube.com"
    ],
    "quic_udp_443_packets": 308258,
    "quic_heuristic_notes": 814,
    "top_inet_pairs_sample": [
      {
        "src": "104.16.155.111",
        "dst": "10.0.0.50",
        "bytes": 326397442
      },
      {
        "src": "142.251.219.33",
        "dst": "10.0.0.50",
        "bytes": 13966440
      },
      {
        "src": "34.104.35.123",
        "dst": "10.0.0.50",
        "bytes": 7784281
      },
      {
        "src": "10.0.0.50",
        "dst": "104.16.155.111",
        "bytes": 2707050
      },
      {
        "src": "104.18.42.225",
        "dst": "10.0.0.50",
        "bytes": 2100896
      },
      {
        "src": "185.211.32.76",
        "dst": "10.0.0.50",
        "bytes": 1869726
      },
      {
        "src": "142.251.157.119",
        "dst": "10.0.0.50",
        "bytes": 1435931
      },
      {
        "src": "142.251.218.142",
        "dst": "10.0.0.50",
        "bytes": 1093158
      },
      {
        "src": "10.0.0.50",
        "dst": "185.211.32.76",
        "bytes": 1033085
      },
      {
        "src": "142.251.155.119",
        "dst": "10.0.0.50",
        "bytes": 890175
      },
      {
        "src": "104.18.34.244",
        "dst": "10.0.0.50",
        "bytes": 851975
      },
      {
        "src": "104.18.19.225",
        "dst": "10.0.0.50",
        "bytes": 523544
      },
      {
        "src": "142.251.218.206",
        "dst": "10.0.0.50",
        "bytes": 431879
      },
      {
        "src": "142.251.218.131",
        "dst": "10.0.0.50",
        "bytes": 254691
      },
      {
        "src": "142.251.219.3",
        "dst": "10.0.0.50",
        "bytes": 228799
      },
      {
        "src": "10.0.0.50",
        "dst": "104.18.42.225",
        "bytes": 222001
      },
      {
        "src": "142.251.218.72",
        "dst": "10.0.0.50",
        "bytes": 208992
      },
      {
        "src": "142.251.219.14",
        "dst": "10.0.0.50",
        "bytes": 195620
      },
      {
        "src": "216.239.34.157",
        "dst": "10.0.0.50",
        "bytes": 181269
      },
      {
        "src": "142.251.214.46",
        "dst": "10.0.0.50",
        "bytes": 157523
      },
      {
        "src": "142.250.101.84",
        "dst": "10.0.0.50",
        "bytes": 142846
      },
      {
        "src": "10.0.0.50",
        "dst": "142.251.219.33",
        "bytes": 131530
      },
      {
        "src": "17.23.18.34",
        "dst": "10.0.0.50",
        "bytes": 114715
      },
      {
        "src": "142.251.219.35",
        "dst": "10.0.0.50",
        "bytes": 104140
      },
      {
        "src": "104.16.156.111",
        "dst": "10.0.0.50",
        "bytes": 84662
      },
      {
        "src": "10.0.0.50",
        "dst": "142.251.218.142",
        "bytes": 81309
      },
      {
        "src": "10.0.0.50",
        "dst": "142.251.157.119",
        "bytes": 79822
      },
      {
        "src": "104.18.5.45",
        "dst": "10.0.0.50",
        "bytes": 71254
      },
      {
        "src": "10.0.0.50",
        "dst": "104.18.5.45",
        "bytes": 70129
      },
      {
        "src": "10.0.0.50",
        "dst": "142.251.155.119",
        "bytes": 58269
      },
      {
        "src": "142.251.218.106",
        "dst": "10.0.0.50",
        "bytes": 55092
      },
      {
        "src": "17.248.231.66",
        "dst": "10.0.0.50",
        "bytes": 54794
      }
    ],
    "limits": [
      "ECH_ESNI_not_visible",
      "DoH_not_inferred_from_udp_53",
      "tcp_segmentation_may_fragment_clienthello",
      "inner_vpn_payload_may_be_opaque",
      "flows_sample_kept_top_512"
    ],
    "errors": [],
    "ja3_ja4": []
  },
  "capture_finalize": {
    "session_id": "1eaa68a91b94",
    "finalized_at_utc": "2026-05-01T10:54:23.733031+00:00",
    "source_pcap_cache_path": "/Users/macvm/src/vpn-leaks/.vpn-leaks/capture/session_1eaa68a91b94.pcap",
    "finalize_errors": []
  },
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "185.211.32.87",
      "country_code": "US",
      "region": "California",
      "city": "San Jose",
      "connection": {
        "asn": 212238,
        "org": "Packethub S.A.",
        "isp": "Datacamp Limited",
        "domain": "packethub.net"
      },
      "location_id": "us-california-san-jose-87",
      "location_label": "San Jose, California, United States"
    }
  }
}
```

---



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`