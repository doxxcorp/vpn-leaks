# Nordvpn (nordvpn)

- **Report generated:** 2026-05-01T10:09:24.562530+00:00
- **Runs included:** nordvpn-20260501T100504Z-cc878634
- **Normalized locations:** 1

> **How to read this report**
>
> - The **Matrix**, **Leak summary**, and **Underlay (ASNs)** sections below are a **high-level rollup only**.
> - **Per-location benchmarks** (exit IP, DNS, WebRTC, IPv6, fingerprint, attribution, policies, services, artifacts, YourInfo, competitor probes, and the full JSON record) are in **`## Detailed runs`** — they are **not omitted**; scroll or open this file as plain text if the preview shows only the first screen.
> - The **canonical** machine-readable record for each location is always `runs/<run_id>/locations/<location_id>/normalized.json` (paths are repeated under each run). For very large JSON, use your editor or a JSON viewer rather than Markdown preview alone.

## Matrix

| Field | Value |
|-------|-------|
| Connection modes observed | manual_gui |
| Locations covered | 1 |

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

- **Benchmark rows in this report:** 1 (one row per `normalized.json` location).
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


## Underlay (ASNs)


- **AS212238:** CDNEXT Datacamp Limited


## Website and DNS surface (third-party exposure)

Interpretation, manual desk steps, and evidence tiers (O / S / I): [docs/website-exposure-methodology.md](../docs/website-exposure-methodology.md).


*No website surface or provider DNS signals in these runs (no `competitor_probe` / `surface_urls` data, or probes empty).*



---

## Detailed runs

**Included in this report** (each subsection below mirrors one `normalized.json`):


1. `nordvpn-20260501T100504Z-cc878634` / `us-california-san-jose-96` — `runs/nordvpn-20260501T100504Z-cc878634/locations/us-california-san-jose-96/normalized.json`


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
| `17.253.144.10` | pcap_peer_ip | 17.253.144.10 | applejava.apple.com | — | APPLE-WWNET | NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US | PTR=applejava.apple.com, world-any.aaplimg.com, advertising.apple.com, applescript.apple.com, applecomputer.co.kr, itunespartner.apple.com, iworktrialbuy.apple.com, safaricampaign.apple, aperturetrialbuy.apple.com, vipd-healthcheck.a01.3banana.com, squeakytoytrainingcamp.com, www.brkgls.com, asia.apple.com, apple.ca, apple.co.uk, apple.de, apple.es, apple.fr, apple.it, apple.nl, apple.com, apple.com.ai, apple.com.au, apple.com.bo, apple.com.cn, apple.com.co, apple.com.do, apple.com.gy, apple.com.hn, apple.com.lk, apple.com.mx, apple.com.my, apple.com.pa, apple.com.pe, apple.com.py, apple.com.sg, apple.com.tt, apple.com.uy, guide.apple.com, shake.apple.com, brkgls.com, icloud.com, iphone.apple.com, podcast.apple.com, appstore.com, firewire.apple.com, livepage.apple.com, seminars.apple.com | 41174 | 5 | — |
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
| `api2.cursor.sh` | pcap_sni | 52.200.55.247, 35.169.56.1, 54.158.82.70, 98.88.12.110, 52.4.106.125, 3.220.160.22, 54.205.252.33, 3.216.68.241 | ec2-3-216-68-241.compute-1.amazonaws.com, ec2-3-220-160-22.compute-1.amazonaws.com, ec2-35-169-56-1.compute-1.amazonaws.com, ec2-52-200-55-247.compute-1.amazonaws.com, ec2-52-4-106-125.compute-1.amazonaws.com, ec2-54-158-82-70.compute-1.amazonaws.com, ec2-54-205-252-33.compute-1.amazonaws.com, ec2-98-88-12-110.compute-1.amazonaws.com | — | AMAZO-4, AMAZON, AT-88-Z | 52.200.55.247=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 35.169.56.1=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 54.158.82.70=>NetName:        AMAZON | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 98.88.12.110=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 52.4.106.125=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.220.160.22=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US  | A=api2geo.cursor.sh., api2direct.cursor.sh., 52.200.55.247, 35.169.56.1, 54.158.82.70, 98.88.12.110; AAAA=—; CNAME=api2geo.cursor.sh.; MX=—; TXT=— | 0 | 0 | — |
| `apple.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | applejava.apple.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=20 mx-in-vib.apple.com., 10 mx-in.g.apple.com., 20 mx-in-ma.apple.com., 20 mx-in-rn.apple.com., 20 mx-in-sg.apple.com., 20 mx-in-hfd.apple.com. | 0 | 0 | dig_txt:timeout:dig |
| `b._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `browser-intake-us5-datadoghq.com` | pcap_dns | 34.149.66.154, 2600:1901:0:179c:: | 154.66.149.34.bc.googleusercontent.com | — | GOOGL-2, GOOGLE-CLOUD | 34.149.66.154=>NetName:        GOOGL-2 | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US || 2600:1901:0:179c::=>NetName:        GOOGLE-CLOUD | OriginAS: | Organization:   Google LLC (GOOGL-2) | OrgName:        Google LLC | Country:        US | A=34.149.66.154; AAAA=2600:1901:0:179c::; CNAME=—; MX=—; TXT=— | 0 | 0 | 2600:1901:0:179c:::reverse_dns_failed |
| `cognito-identity.us-east-1.amazonaws.com` | pcap_sni | 13.219.38.100, 54.161.95.217, 18.205.49.157, 100.50.99.35, 100.30.138.56, 34.199.27.29, 34.194.23.234, 52.5.134.248, 2600:1f10:469b:a100:2c8:4774:8005:f190, 2600:1f10:469b:a102:fb76:bf83:61b6:5e82, 2600:1f10:469b:a100:155f:69ab:9620:4920, 2600:1f10:469b:a101:5d5f:ec55:cd2e:4dcf | ec2-100-30-138-56.compute-1.amazonaws.com, ec2-100-50-99-35.compute-1.amazonaws.com, ec2-13-219-38-100.compute-1.amazonaws.com, ec2-18-205-49-157.compute-1.amazonaws.com, ec2-34-194-23-234.compute-1.amazonaws.com, ec2-34-199-27-29.compute-1.amazonaws.com, ec2-52-5-134-248.compute-1.amazonaws.com, ec2-54-161-95-217.compute-1.amazonaws.com | — | AMAZO-4, AMAZON, AMZ-EC2, AT-88-Z | 13.219.38.100=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 54.161.95.217=>NetName:        AMAZON | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 18.205.49.157=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 100.50.99.35=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 100.30.138.56=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 34.199.27.29=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 34.194.23 | A=13.219.38.100, 54.161.95.217, 18.205.49.157, 100.50.99.35, 100.30.138.56, 34.199.27.29; AAAA=2600:1f10:469b:a100:2c8:4774:8005:f190, 2600:1f10:469b:a102:fb76:bf83:61b6:5e82, 2600:1f10:469b:a100:155f:69ab:9620:4920, 2600:1f10:469b:a101:5d5f:ec55:cd2e:4dcf, 2600:1f10:469b:a102:2262:ce0d:a40f:facb, 2600:1f10:469b:a101:5ebb:cbda:8260:ce95; CNAME=—; MX=—; TXT=— | 0 | 0 | 2600:1f10:469b:a100:2c8:4774:8005:f190:reverse_dns_failed; 2600:1f10:469b:a102:fb76:bf83:61b6:5e82:reverse_dns_failed; 2600:1f10:469b:a100:155f:69ab:9620:4920:reverse_dns_failed; 2600:1f10:469b:a101:5d5f:ec55:cd2e:4dcf:reverse_dns_failed |
| `db._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `doh-dns-apple-com.v.aaplimg.com` | pcap_dns | 64.78.200.1, 17.253.16.247, 17.253.16.119, 17.132.91.14, 64.78.201.1, 17.132.91.15, 2620:171:80c::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2, 2620:149:9cc::13, 2620:171:80d::1 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.132.91.14=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.15=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:171:80c::1=>NetName:        WOODYNET-V6-NET02 | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | O | A=64.78.200.1, 17.253.16.247, 17.253.16.119, 17.132.91.14, 64.78.201.1, 17.132.91.15; AAAA=2620:171:80c::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2, 2620:149:9cc::13, 2620:171:80d::1; CNAME=—; MX=—; TXT=— | 0 | 0 | 17.132.91.14:reverse_dns_failed; 17.132.91.15:reverse_dns_failed; 2620:149:9cc::14:reverse_dns_failed; 2620:149:9cc::13:reverse_dns_failed |
| `doh.dns.apple.com` | pcap_dns | 17.132.91.14, 64.78.201.1, 17.132.91.15, 64.78.200.1, 17.253.16.247, 17.253.16.119, 2620:171:80d::1, 2620:171:80c::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2, 2620:149:9cc::13 | doh.dns.apple.com, usscz2-doh-001.aaplimg.com, usscz2-doh-002.aaplimg.com | — | APPLE-WWNET, WOODYN, WOODYNET-V6-NET02 | 17.132.91.14=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.201.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.132.91.15=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 64.78.200.1=>NetName:        WOODYN | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | OrgName:        WoodyNet, Inc. | Country:        US || 17.253.16.247=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 17.253.16.119=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:171:80d::1=>NetName:        WOODYNET-V6-NET02 | OriginAS: | Organization:   WoodyNet, Inc. (WOODYN) | O | A=doh-dns-apple-com.v.aaplimg.com., 17.132.91.14, 64.78.201.1, 17.132.91.15, 64.78.200.1, 17.253.16.247; AAAA=doh-dns-apple-com.v.aaplimg.com., 2620:171:80d::1, 2620:171:80c::1, 2620:149:9cc::14, 2620:149:a0c:4000::1c2, 2620:149:a0c:3000::1c2; CNAME=doh-dns-apple-com.v.aaplimg.com.; MX=—; TXT=— | 0 | 0 | — |
| `firehose.us-east-1.amazonaws.com` | pcap_sni | 3.237.107.102 | ec2-3-237-107-102.compute-1.amazonaws.com | — | AT-88-Z | 3.237.107.102=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US | A=3.237.107.102; AAAA=—; CNAME=—; MX=—; TXT=3.237.107.1c32e1 52.46.143.48c0e0 44.210.246.122c32e1 3.237.107.34c32e1 52.119.196.193c0e0 52.119.198.79c0e0 3.237.107.62c32e1 " "52.46.140.96c0e0 72.21.195.15c0e0 52.119.197.123c0e0 3.237.107.44c32e1 44.210.246.73c32e1 3.237.107.50c32e1 209.54.178.67c0e0 5" "2.46.153.116c0e0 52.46.153.120c0e0 209.54.176.79c0e0 3.237.107.47c32e1 3.237.107.0c32e1 3.237.107.114c32e1 52.94.232.253c0e0 3." "237.107.19c32e1 52.46.128.67c0e0 52.46.142.17c0e0 3.237.107.53c32e1 3.237.107.97c32e1 3.237.107.30c32e1 52.46.132.133c0e0 3.237" ".107.9c32e1 3.237.107.102c32e1 52.46.132.196c0e0 52.119.198.155c0e0 44.210.246.102c32e1 52.119.197.143c0e0 54.239.25.120c0e0 3." "237.107.49c32e1 52.119.197.133c0e0 44.210.246.99c32e1 3.237.107.116c32e1 52.46.135.48c0e0 52.94.225.129c0e0 52.119.196.176c0e0 " "3.237.107.41c32e1 52.119.198.13c0e0 52.46.135.137c0e0 52.46.130.240c0e0 52.46.155.54c0e0 3.237.107.15c32e1 3.237.107.96c32e1 44" ".210.246.125c32e1 52.119.197.233c0e0 3.237.107.38c32e1 3.237.107.29c32e1 3.237.107.46c32e1 52.119.196.185c0e0 3.237.107.99c32e1" " 52.119.198.71c0e0 52.46.151.48c0e0 3.237.107.59c32e1 3.237.107.121c32e1 54.239.30.232c0e0 3.237.107.66c32e1 3.237.107.21c32e1 " "52.94.225.147c0e0 52.46.146.100c0e0 3.237.107.124c32e1 n1 | 0 | 0 | — |
| `icloud.com` | pcap_dns | 17.253.144.10, 2620:149:af0::10 | applejava.apple.com, icloud.com | — | APPLE-WWNET | 17.253.144.10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1-Z) | OrgName:        Apple Inc. | Country:        US || 2620:149:af0::10=>NetName:        APPLE-WWNET | OriginAS: | Organization:   Apple Inc. (APPLEC-1) | OrgName:        Apple Inc. | Country:        US | A=17.253.144.10; AAAA=2620:149:af0::10; CNAME=—; MX=10 mx02.mail.icloud.com., 10 mx01.mail.icloud.com.; TXT=v=spf1 ip4:17.41.0.0/16 ip4:17.58.0.0/16 ip4:17.142.0.0/15 ip4:17.57.155.0/24 ip4:17.57.156.0/24 ip4:144.178.36.0/24 ip4:144.178.38.0/24 ip4:112.19.199.64/29 ip4:112.19.242.64/29 ip4:222.73.195.64/29 ip4:157.255.1.64/29" " ip4:106.39.212.64/29 ip4:123.126.78.64/29 ip4:183.240.219.64/29 ip4:39.156.163.64/29 ip4:57.103.64.0/18" " ip6:2a01:b747:3000:200::/56 ip6:2a01:b747:3001:200::/56 ip6:2a01:b747:3002:200::/56 ip6:2a01:b747:3003:200::/56 ip6:2a01:b747:3004:200::/56 ip6:2a01:b747:3005:200::/56 ip6:2a01:b747:3006:200::/56 ~all, google-site-verification=Ik3jMkCjHnUgyIoFR0Kw74srr0H5ynFmUk8fyY1uBck, google-site-verification=knAEOH4QxR29I4gjRkpkvmUmP2AA7WrDk8Kq0wu9g9o | 0 | 0 | — |
| `lb._dns-sd._udp.0.0.5.10.in-addr.arpa` | pcap_dns | — | — | — | — | — | A=—; AAAA=—; CNAME=—; MX=—; TXT=— | 0 | 0 | — |
| `logs.us-east-1.amazonaws.com` | pcap_sni | 3.236.94.238, 3.236.94.167, 3.236.94.237, 3.236.94.194, 44.202.79.131, 3.236.94.236, 3.236.94.130, 3.236.94.208 | ec2-3-236-94-130.compute-1.amazonaws.com, ec2-3-236-94-167.compute-1.amazonaws.com, ec2-3-236-94-194.compute-1.amazonaws.com, ec2-3-236-94-208.compute-1.amazonaws.com, ec2-3-236-94-236.compute-1.amazonaws.com, ec2-3-236-94-237.compute-1.amazonaws.com, ec2-3-236-94-238.compute-1.amazonaws.com, ec2-44-202-79-131.compute-1.amazonaws.com | — | AMAZO-4, AT-88-Z | 3.236.94.238=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.167=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.237=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 3.236.94.194=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        US || 44.202.79.131=>NetName:        AMAZO-4 | OriginAS: | Organization:   Amazon.com, Inc. (AMAZO-4) | OrgName:        Amazon.com, Inc. | Country:        US || 3.236.94.236=>NetName:        AT-88-Z | OriginAS: | Organization:   Amazon Technologies Inc. (AT-88-Z) | OrgName:        Amazon Technologies Inc. | Country:        U | A=3.236.94.238, 3.236.94.167, 3.236.94.237, 3.236.94.194, 44.202.79.131, 3.236.94.236; AAAA=—; CNAME=—; MX=— | 0 | 0 | dig_txt:timeout:dig |
| `ssl.gstatic.com` | pcap_dns | 142.251.219.35, 2607:f8b0:4005:803::2003 | ncsfoa-an-in-f3.1e100.net, sfo03s33-in-x03.1e100.net | — | GOOGLE, GOOGLE-IPV6 | 142.251.219.35=>NetName:        GOOGLE | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US || 2607:f8b0:4005:803::2003=>NetName:        GOOGLE-IPV6 | OriginAS: | Organization:   Google LLC (GOGL) | OrgName:        Google LLC | Country:        US | A=142.251.219.35; AAAA=2607:f8b0:4005:803::2003; CNAME=—; MX=—; TXT=— | 0 | 0 | — |






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



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`