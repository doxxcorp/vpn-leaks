# Nordvpn (nordvpn)

- **Report generated:** 2026-04-17T07:32:00.981798+00:00
- **Runs included:** nordvpn-20260417T071350Z-5b9ffc60, nordvpn-20260417T072634Z-607907b5
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
  - answered: 8
  - partially answered: 30
  - unanswered: 0
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
| `IP-001` | `answered` | real_ip_leak | Is the real public IPv4 exposed while connected? | Exit IPv4 185.161.202.154; leak flags dns=False webrtc=False ipv6=False. | — |
| `IP-002` | `partially_answered` | real_ip_leak | Is the real public IPv6 exposed while connected? | No IPv6 exit or IPv6 not returned by endpoints. | Enable IPv6 path in environment; check `ipv6/` artifacts when present. |
| `IP-006` | `answered` | real_ip_leak | Is the real IP exposed through WebRTC? | WebRTC candidates captured; leak flag=False. | — |
| `IP-007` | `partially_answered` | real_ip_leak | Is the local LAN IP exposed through WebRTC or browser APIs? | Inspect host candidates vs LAN; see webrtc_notes. | Exit IP appears in candidate set (expected for tunneled public) — Inspect host vs srflx candidates in `webrtc_candidates`. |
| `IP-014` | `partially_answered` | real_ip_leak | Do leak-check sites disagree about observed IP identity? | Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.154, 92.211.2.176. | Compare `exit_ip_sources` entries for disagreement. |
| `CTRL-002` | `partially_answered` | control_plane | Which domains and IPs are contacted after the tunnel is up? | Post-harness service list captured. | `services_contacted` in `normalized.json` lists only URLs and probes this harness actually ran (not full-device traffic). Run a fuller benchmark: avoid `--skip-browserleaks` and competitor skip flags where you need those surfaces; add `competitor_probe` / portal / `surface_urls` in the provider YAML per RUN-STEPS.md; add more locations for diversity. For VPN app background traffic, use external capture—see CTRL-003. |
| `CTRL-003` | `not_testable_dynamically` | control_plane | Which control-plane endpoints are used for auth/config/session management? | Auth/control-plane inventory requires internal docs or app instrumentation. | DOCUMENT_RESEARCH: vendor docs, app MITM, or support (D). |
| `CTRL-004` | `partially_answered` | control_plane | Which telemetry endpoints are contacted during connection? | Infer from services_contacted and classified endpoints. | Classify `services_contacted` hosts; app telemetry needs traffic capture (see TELEM-*). |
| `CTRL-009` | `partially_answered` | control_plane | Is the control plane behind a CDN/WAF? | CDN/WAF hints from web headers. | Enable portal/web probes (`portal_probes`); check `https_cdn_headers`. |
| `EXIT-001` | `answered` | exit_infrastructure | What exit IP is assigned for each region? | Exit IPv4 176.100.43.136 for location ca-british-columbia-vancouver-136. | — |
| `EXIT-002` | `answered` | exit_infrastructure | What ASN announces the exit IP? | ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-003` | `answered` | exit_infrastructure | What organization owns the IP range? | ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A. | — |
| `EXIT-004` | `partially_answered` | exit_infrastructure | What reverse DNS exists for the exit node? | PTR lookup errors: ptr_v4: The DNS response does not contain an answer to the question: 136.43.100.176.in-addr.arpa. IN PTR | Check raw `exit_dns.json` / attribution for rDNS when stored. |
| `EXIT-005` | `partially_answered` | exit_infrastructure | Does the observed geolocation match the advertised location? | Consistent: exit_geo.location_label matches vpn_location_label ('Vancouver, British Columbia, Canada'). | Compare `extra.exit_geo` to `vpn_location_label`; add more regions to validate. |
| `THIRDWEB-001` | `partially_answered` | third_party_web | What external JS files are loaded on the site? | See web HAR + competitor_surface for external scripts/analytics. | Enable `competitor_probe` + marketing URLs; scripts listed in `web_probes.json`. |
| `THIRDWEB-003` | `partially_answered` | third_party_web | What analytics providers are present? | See web HAR + competitor_surface for external scripts/analytics. | HAR + `har_summary.json` tracker_candidates when competitor probes run. |
| `THIRDWEB-012` | `partially_answered` | third_party_web | What cookies are set by first-party and third-party scripts? | See web HAR + competitor_surface for external scripts/analytics. | Review HAR for Set-Cookie; summary may be partial. |
| `FP-001` | `answered` | browser_tracking | Does the site attempt browser fingerprinting? | Fingerprint snapshot captured (harness baseline; does not prove the provider site runs fingerprinting—see THIRDWEB / HAR rows for script-level evidence). | — |
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

- **`OS-001`** (`partially_answered`): Process-level bypass not in default harness; external tooling or manual checks.

- **`FAIL-001`** (`partially_answered`): Use `--transition-tests` for connect-phase leaks when supported.

- **`FAIL-003`** (`partially_answered`): Use `--transition-tests` for reconnect leaks when supported.

- **`LOG-001`** (`partially_answered`): Review `services_contacted` + endpoint classifications; pair with policy/audit (D).

- **`LOG-005`** (`partially_answered`): Fetch policies (`policy_urls` in provider YAML); compare marketing to ISAE/DPAs (D). See docs/research-questions-and-evidence.md.



## Analysis of collected evidence

### Scope

- **Benchmark rows in this report:** 2 (one row per `normalized.json` location).
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
- **CTRL-009** (partial): CDN/WAF hints from web headers.

#### dns

- **DNS-001** (answered): Resolver tiers observed (local + external).
- **DNS-002** (partial): Leak flag=False; see notes.
- **DNS-003** (partial): Leak flag=False; see notes.
- **DNS-004** (partial): Connect/disconnect DNS not sampled; use --transition-tests when supported.
- **DNS-009** (partial): DoH/DoT not isolated from resolver snapshot; inspect raw captures.
- **DNS-011** (partial): Leak flag=False; see notes.

#### exit_infrastructure

- **EXIT-001** (answered): Exit IPv4 176.100.43.136 for location ca-british-columbia-vancouver-136.
- **EXIT-002** (answered): ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-003** (answered): ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.
- **EXIT-004** (partial): PTR lookup errors: ptr_v4: The DNS response does not contain an answer to the question: 136.43.100.176.in-addr.arpa. IN PTR
- **EXIT-005** (partial): Consistent: exit_geo.location_label matches vpn_location_label ('Vancouver, British Columbia, Canada').

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

- **IP-001** (answered): Exit IPv4 185.161.202.154; leak flags dns=False webrtc=False ipv6=False.
- **IP-002** (partial): No IPv6 exit or IPv6 not returned by endpoints.
- **IP-006** (answered): WebRTC candidates captured; leak flag=False.
- **IP-007** (partial): Inspect host candidates vs LAN; see webrtc_notes.
- **IP-014** (partial): Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.154, 92.211.2.176.

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
| Vancouver, BR, CAN | False | False | False |
| Hamburg, HA, DEU | False | False | False |


## Underlay (ASNs)


- **AS147049:** PACKETHUBSA-AS-AP PacketHub S.A.

- **AS207137:** PACKETHUBSA - PacketHub S.A.


## Website and DNS surface (third-party exposure)

Interpretation, manual desk steps, and evidence tiers (O / S / I): [docs/website-exposure-methodology.md](../docs/website-exposure-methodology.md).


### HAR-derived signals (merged across locations)

| Metric | Count |
|--------|-------|
| Unique request hosts | 3 |
| Tracker / analytics candidates | 0 |
| CDN candidates | 0 |




### Provider DNS (apex, from `competitor_probe`)

| Domain | NS (sample) | MX (sample) | TXT (sample) | IPv6 apex |
|--------|-------------|-------------|--------------|-----------|
| `nordvpn.com` | lily.ns.cloudflare.com, seth.ns.cloudflare.com | 1 aspmx.l.google.com, 5 alt1.aspmx.l.google.com, 5 alt2.aspmx.l.google.com (+2 more) | google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw, oneuptime=2fYJpBXRQsmY3Py (+5 more) | no AAAA (IPv4-only apex) |




### Surface URL matrix (`surface_urls`)

| page_type | URL | HTTP status |
|-----------|-----|-------------|
| pricing | https://nordvpn.com/pricing/ | 403 |
| signup | https://my.nordaccount.com/ | 200 |
| checkout | https://nordcheckout.com/ | 403 |




**Portal hosts probed:** `my.nordaccount.com`



**Competitor probe URLs (sample):** https://nordvpn.com/; https://nordvpn.com/




---

## Detailed runs

**Included in this report** (each subsection below mirrors one `normalized.json`):


1. `nordvpn-20260417T071350Z-5b9ffc60` / `ca-british-columbia-vancouver-136` — `runs/nordvpn-20260417T071350Z-5b9ffc60/locations/ca-british-columbia-vancouver-136/normalized.json`

2. `nordvpn-20260417T072634Z-607907b5` / `de-hamburg-hamburg-154` — `runs/nordvpn-20260417T072634Z-607907b5/locations/de-hamburg-hamburg-154/normalized.json`


Large JSON fields use size caps in this markdown file; when an excerpt hits a cap, a **note** appears at the start of that run’s section listing what was capped. **On-disk `normalized.json` is always complete.**



### nordvpn-20260417T071350Z-5b9ffc60 / ca-british-columbia-vancouver-136



- **vpn_provider:** nordvpn
- **Label:** Vancouver, British Columbia, Canada
- **Path:** `runs/nordvpn-20260417T071350Z-5b9ffc60/locations/ca-british-columbia-vancouver-136/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-17T07:17:18.157460+00:00
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
| exit_ip_v4 | 176.100.43.136 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "176.100.43.136",
    "ipv6": null,
    "raw_excerpt": "176.100.43.136",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "176.100.43.136",
    "ipv6": null,
    "raw_excerpt": "176.100.43.136",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "176.100.43.136",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"176.100.43.136\"}",
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
      "176.100.43.136"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "176.100.43.136"
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
| host | udp | 63ab2faa-6416-46af-ad43-493473b7a255.local | 53220 | `candidate:4289004804 1 udp 2113937151 63ab2faa-6416-46af-ad43-493473b7a255.local 53220 typ host generation 0 ufrag cQzE network-cost 999` |
| srflx | udp | 176.100.43.136 | 31208 | `candidate:4289758242 1 udp 1677729535 176.100.43.136 31208 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag cQzE network-cost 999` |


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
  "asn": 147049,
  "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [147049]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 147049,
      "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (176.100.43.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260417071409-078b590a-70f1-4c6b-8859-e8562f900b36",
          "process_time": 97,
          "server_id": "app179",
          "build_version": "v0.9.9-2026.04.16",
          "pipeline": "1232122",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-17T07:14:09.701503",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 147049,
                "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
              }
            ],
            "related_prefixes": [],
            "resource": "176.100.43.0/24",
            "type": "prefix",
            "block": {
              "resource": "176.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-04-17T00:00:00",
            "num_filtered_out": 0
          }
        }
      }
    },
    {
      "name": "team_cymru",
      "asn": 147049,
      "holder": null,
      "country": null,
      "raw": {
        "asn": 147049,
        "raw_line": "147049 | 176.100.43.0/24 | DE | ripencc | 2021-09-01",
        "parts": [
          "147049",
          "176.100.43.0/24",
          "DE",
          "ripencc",
          "2021-09-01"
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
            "id": 29054,
            "org_id": 28491,
            "name": "PacketHub AS147049",
            "aka": "",
            "name_long": "",
            "website": "https://www.packethub.net/",
            "social_media": [
              {
                "service": "website",
                "identifier": "https://www.packethub.net/"
              }
            ],
            "asn": 147049,
            "looking_glass": "",
            "route_server": "",
            "irr_as_set": "APNIC::AS-SET-AS147049",
            "info_type": "",
            "info_types": [],
            "info_prefixes4": 1000,
            "info_prefixes6": 1000,
            "info_traffic": "",
            "info_ratio": "Not Disclosed",
            "info_scope": "Global",
            "info_unicast": true,
            "info_multicast": false,
            "info_ipv6": true,
            "info_never_via_route_servers": false,
            "ix_count": 7,
            "fac_count": 1,
            "notes": "",
            "netixlan_updated": "2026-03-26T15:30:03Z",
            "netfac_updated": "2023-07-18T08:22:19Z",
            "poc_updated": "2022-10-06T09:29:57Z",
            "policy_url": "",
            "policy_general": "Open",
            "policy_locations": "Not Required",
            "policy_ratio": false,
            "policy_contracts": "Not Required",
            "allow_ixp_update": false,
            "status_dashboard": "",
            "rir_status": "ok",
            "rir_status_updated": "2024-06-26T04:47:55Z",
            "logo": null,
            "created": "2022-01-18T09:17:39Z",
            "updated": "2025-11-03T13:33:39Z",
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
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-17T07:14:50.410886+00:00",
    "sha256": "78b2189284f165a8a179e0ad54fc69ac79705499929567c04605996542949b72",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  },
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-17T07:14:52.848394+00:00",
    "sha256": "6a64fc32eac27ca2f94d8748737b636d03df4bd54e6b262d748c84066fb4b93e",
    "summary_bullets": [
      "No keyword hits for common sections; manual review recommended"
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

- `https://ipwho.is/176.100.43.136`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordcheckout.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/pricing/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `surface_probe:har_summary`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/webrtc",
  "ipv6_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/fingerprint",
  "attribution_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/policy",
  "competitor_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe",
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
  "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-8abe8931",
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
      "answer_summary": "Exit IPv4 176.100.43.136; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "All 3 echo endpoints agree on IPv4 176.100.43.136.",
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
      "answer_summary": "Exit IPv4 176.100.43.136 for location ca-british-columbia-vancouver-136.",
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
      "answer_summary": "ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.",
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
      "answer_summary": "ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS response does not contain an answer to the question: 136.43.100.176.in-addr.arpa. IN PTR",
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
      "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Vancouver, British Columbia, Canada').",
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
      "host": "surface_probe",
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


#### Website & DNS surface (summary)


| Metric | This location |
|--------|---------------|
| Unique request hosts | 3 |
| Tracker candidates | 0 |
| CDN candidates | 0 |


**Provider DNS (apex)**

| Domain | NS (sample) | MX (sample) | IPv6 apex |
|--------|-------------|-------------|-----------|
| `nordvpn.com` | lily.ns.cloudflare.com, seth.ns.cloudflare.com | 1 aspmx.l.google.com, 5 alt1.aspmx.l.google.com, 5 alt2.aspmx.l.google.com (+2 more) | no AAAA (IPv4-only apex) |




**Surface URLs**

| page_type | URL | status |
|-----------|-----|--------|
| pricing | https://nordvpn.com/pricing/ | 403 |
| signup | https://my.nordaccount.com/ | 200 |
| checkout | https://nordcheckout.com/ | 403 |





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
          "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
          "oneuptime=2fYJpBXRQsmY3Py",
          "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
          "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
          "MS=ms41624661",
          "MS=ms60989570",
          "MS=ms69824556"
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
                    "query_id": "20260417071524-d2f2576e-8797-49fa-8b7f-705fca55a88c",
                    "process_time": 84,
                    "server_id": "app175",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:24.114399",
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
                      "query_time": "2026-04-17T00:00:00",
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
                      "ix_count": 351,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-17T03:07:10Z",
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
                      "updated": "2026-04-17T03:07:21Z",
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
                    "query_id": "20260417071526-f177592e-7265-4742-adce-5920b02dd7c6",
                    "process_time": 64,
                    "server_id": "app177",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:26.190647",
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
                      "query_time": "2026-04-17T00:00:00",
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
                      "ix_count": 351,
                      "fac_count": 222,
                      "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                      "netixlan_updated": "2026-04-17T03:07:10Z",
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
                      "updated": "2026-04-17T03:07:21Z",
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
                    "query_id": "20260417071528-4dcf952b-9302-4f89-849e-26e26f046d91",
                    "process_time": 42,
                    "server_id": "app194",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:28.254031",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071529-fd800d40-5d9a-430c-9da8-a1ea20080dab",
                    "process_time": 118,
                    "server_id": "app189",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:30.015419",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071531-1129165c-e5ed-447b-a14e-9c0e6f76fcb6",
                    "process_time": 60,
                    "server_id": "app198",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:31.533430",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071532-a6eea3ad-8640-4877-8e05-de8543d9d42d",
                    "process_time": 45,
                    "server_id": "app189",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:33.038818",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071534-667eeb99-0043-4fce-997c-a3afea53d35e",
                    "process_time": 42,
                    "server_id": "app192",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:34.553072",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071536-9065a567-a2c2-490f-9842-ef004fd9a743",
                    "process_time": 44,
                    "server_id": "app160",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:36.256953",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071538-ea234f99-e219-4700-a86c-a78ccaa3259a",
                    "process_time": 82,
                    "server_id": "app172",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:38.335864",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071540-c38eaa66-8f2a-429b-9540-15bed8523dc0",
                    "process_time": 57,
                    "server_id": "app187",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:40.342909",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071541-386ce0ef-6043-4a02-8581-a966a47c42c6",
                    "process_time": 56,
                    "server_id": "app177",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:41.927062",
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
                      "query_time": "2026-04-17T00:00:00",
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
                    "query_id": "20260417071543-c1cb8f29-2cc5-43c7-9fc0-2c1a8a46a573",
                    "process_time": 41,
                    "server_id": "app168",
                    "build_version": "v0.9.9-2026.04.16",
                    "pipeline": "1232122",
                    "status": "ok",
                    "status_code": 200,
                    "time": "2026-04-17T07:15:43.347768",
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
                      "query_time": "2026-04-17T00:00:00",
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
        "server": "cloudflare",
        "cf-ray": "9ed9a61f4f8bc67e-YVR"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a61f4f8bc67e"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe/har/d945f098fbd5bb50.har",
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
        "cf-ray": "9ed9a621eb1be19b-YVR"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "176.100.43.136",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "176.100.43.136"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 176.100.43.136 (176.100.43.136), 15 hops max, 40 byte packets\n",
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
    "ip": "176.100.43.136",
    "country_code": "CA",
    "region": "British Columbia",
    "city": "Vancouver",
    "connection": {
      "asn": 147049,
      "org": "Packethub S.A.",
      "isp": "Packethub S.A.",
      "domain": "net1.de"
    },
    "location_id": "ca-british-columbia-vancouver-136",
    "location_label": "Vancouver, British Columbia, Canada"
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
          "cf-ray": "9ed9a6270d7176b8-SEA"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a6270d7176b8"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/3cec43152ba057c5.har",
        "page_type": "pricing"
      },
      {
        "url": "https://my.nordaccount.com/",
        "error": null,
        "status": 200,
        "final_url": "https://my.nordaccount.com/",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed9a6296e3d6052-YVR"
        },
        "scripts": [
          "https://my.nordaccount.com/assets/runtime.a9c27b97b093c98ae649.js",
          "https://my.nordaccount.com/assets/_formatjs.defaultvendors.ac0846ece32d56901ea4.js",
          "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.eb63fbe45c73fab20cc3.js",
          "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.12b7c8ec7f121d0b5787.js",
          "https://my.nordaccount.com/assets/index.caa7c4317590658d27ac.js",
          "https://my.nordaccount.com/assets/_nordsec.defaultvendors.4c748c7db5cefa2fe8df.chunk.js",
          "https://my.nordaccount.com/assets/date-fns.defaultvendors.eaa415bc21c381d3558b.chunk.js",
          "https://my.nordaccount.com/assets/_nord.defaultvendors.f2b134f66f68507b33fc.chunk.js",
          "https://my.nordaccount.com/assets/tslib.defaultvendors.f240679c709d47693a22.chunk.js",
          "https://my.nordaccount.com/assets/_sentry.defaultvendors.6a26a7e44a35f2381dc2.chunk.js",
          "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.36f404cb5c3d7ff37a26.chunk.js",
          "https://my.nordaccount.com/assets/graphql.defaultvendors.6196445f71efc38548cd.chunk.js",
          "https://my.nordaccount.com/assets/react-intl.defaultvendors.b71793934bfb99d0b581.chunk.js",
          "https://my.nordaccount.com/assets/graphql-request.defaultvendors.25a38b2f26bc2e06c5ff.chunk.js",
          "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.73708e4220415063788d.chunk.js",
          "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.719b911b91adb7aef00b.chunk.js",
          "https://my.nordaccount.com/assets/uuid.defaultvendors.746a61a183a00afcd19c.chunk.js",
          "https://my.nordaccount.com/assets/_babel.defaultvendors.09ede7e9eaeecef6d984.chunk.js",
          "https://my.nordaccount.com/assets/react.defaultvendors.0015e8b82b057f403937.chunk.js",
          "https://my.nordaccount.com/assets/react-dom.defaultvendors.3a1333ac0f7e30c6efdc.chunk.js",
          "https://my.nordaccount.com/assets/prop-types.defaultvendors.07541a84659c6203c26c.chunk.js",
          "https://my.nordaccount.com/assets/react-toastify.defaultvendors.ff2d3ee8bd32115c5105.chunk.js",
          "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.5f3f39fa4221cfe8e9f3.chunk.js",
          "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.de9ccecd85bf07c5aa48.chunk.js",
          "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.8d091fe6bd55d67df739.chunk.js",
          "https://my.nordaccount.com/assets/scheduler.defaultvendors.db974a7e0f5f400c9542.chunk.js",
          "https://my.nordaccount.com/assets/react-is.defaultvendors.c68f828a892f78334b23.chunk.js",
          "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.fde5e082146b4e49cbf9.chunk.js",
          "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.229ce3ff05c6241dc586.chunk.js",
          "https://my.nordaccount.com/assets/react-redux.defaultvendors.fd161b5e1759a70dfe89.chunk.js",
          "https://my.nordaccount.com/assets/js-cookie.defaultvendors.4f558a2177bb0eb5b78d.chunk.js",
          "https://my.nordaccount.com/assets/immer.defaultvendors.0b964b76caa620cff239.chunk.js",
          "https://my.nordaccount.com/assets/clsx.defaultvendors.df823a651876ebf8de25.chunk.js",
          "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.baf6829019a88080d27b.chunk.js",
          "https://my.nordaccount.com/assets/classnames.defaultvendors.c2b96eae94047c76c0ff.chunk.js",
          "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.45faa7f70fa2eebadd6a.chunk.js",
          "https://my.nordaccount.com/assets/react-router.defaultvendors.78aaad2448f5c1b716a5.chunk.js",
          "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.6b7f2f2725b53b198161.chunk.js",
          "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.1d2b074be5f45739167d.chunk.js",
          "https://my.nordaccount.com/assets/react-helmet.defaultvendors.84ea08fb735d01e5cbd2.chunk.js",
          "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.00289033652a15f72cb3.chunk.js",
          "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.c750d7ce2db67f793585.chunk.js",
          "https://my.nordaccount.com/assets/object-assign.defaultvendors.f85101626dd44f58baec.chunk.js",
          "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.e2b6c1d21e29212d4759.chunk.js",
          "https://my.nordaccount.com/assets/humps.defaultvendors.3754860cfe25e6714b78.chunk.js",
          "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.79396dd4378902d7beaa.chunk.js",
          "https://my.nordaccount.com/assets/filter-obj.defaultvendors.84146f4c18b1572ac0ba.chunk.js",
          "https://my.nordaccount.com/assets/file-saver.defaultvendors.cc329c95afaf575e4b41.chunk.js",
          "https://my.nordaccount.com/assets/exenv.defaultvendors.a1af14a17940d6080ed3.chunk.js",
          "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.1e3b43bb5d3c3776b319.chunk.js",
          "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.3e680526e6c07ca51319.chunk.js",
          "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.2f8dd77d6309c41de433.chunk.js",
          "https://my.nordaccount.com/assets/split-on-first.defaultvendors.b3f30d1714518afe82db.chunk.js",
          "https://my.nordaccount.com/assets/query-string.defaultvendors.82e833f4af0d00cbde64.chunk.js",
          "https://my.nordaccount.com/assets/_remix-run.defaultvendors.363e94888ab4b4faff10.chunk.js",
          "https://my.nordaccount.com/assets/4666.705e2d0d1330cfd25bc1.chunk.js"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/0096221d6f12d382.har",
        "page_type": "signup"
      },
      {
        "url": "https://nordcheckout.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed9a634ff7276a6-SEA"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a634ff7276a6"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/5c4416295d131e0b.har",
        "page_type": "checkout"
      }
    ],
    "surface_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe",
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/3cec43152ba057c5.har",
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
        },
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/0096221d6f12d382.har",
          "entry_count": 60,
          "unique_hosts": [
            "my.nordaccount.com"
          ],
          "unique_schemes": [
            "https"
          ],
          "tracker_candidates": [],
          "cdn_candidates": [],
          "error": null
        },
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/5c4416295d131e0b.har",
          "entry_count": 5,
          "unique_hosts": [
            "nordcheckout.com",
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
        "my.nordaccount.com",
        "nordcheckout.com",
        "nordvpn.com"
      ],
      "merged_tracker_candidates": [],
      "merged_cdn_candidates": []
    }
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260417T071350Z-5b9ffc60",
  "timestamp_utc": "2026-04-17T07:17:18.157460+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "ca-british-columbia-vancouver-136",
  "vpn_location_label": "Vancouver, British Columbia, Canada",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "176.100.43.136",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "176.100.43.136",
      "ipv6": null,
      "raw_excerpt": "176.100.43.136",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "176.100.43.136",
      "ipv6": null,
      "raw_excerpt": "176.100.43.136",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "176.100.43.136",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"176.100.43.136\"}",
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
        "176.100.43.136"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "176.100.43.136"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "63ab2faa-6416-46af-ad43-493473b7a255.local",
      "port": 53220,
      "raw": "candidate:4289004804 1 udp 2113937151 63ab2faa-6416-46af-ad43-493473b7a255.local 53220 typ host generation 0 ufrag cQzE network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "176.100.43.136",
      "port": 31208,
      "raw": "candidate:4289758242 1 udp 1677729535 176.100.43.136 31208 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag cQzE network-cost 999"
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
    "asn": 147049,
    "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [147049]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 147049,
        "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (176.100.43.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260417071409-078b590a-70f1-4c6b-8859-e8562f900b36",
            "process_time": 97,
            "server_id": "app179",
            "build_version": "v0.9.9-2026.04.16",
            "pipeline": "1232122",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-17T07:14:09.701503",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 147049,
                  "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
                }
              ],
              "related_prefixes": [],
              "resource": "176.100.43.0/24",
              "type": "prefix",
              "block": {
                "resource": "176.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-04-17T00:00:00",
              "num_filtered_out": 0
            }
          }
        }
      },
      {
        "name": "team_cymru",
        "asn": 147049,
        "holder": null,
        "country": null,
        "raw": {
          "asn": 147049,
          "raw_line": "147049 | 176.100.43.0/24 | DE | ripencc | 2021-09-01",
          "parts": [
            "147049",
            "176.100.43.0/24",
            "DE",
            "ripencc",
            "2021-09-01"
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
              "id": 29054,
              "org_id": 28491,
              "name": "PacketHub AS147049",
              "aka": "",
              "name_long": "",
              "website": "https://www.packethub.net/",
              "social_media": [
                {
                  "service": "website",
                  "identifier": "https://www.packethub.net/"
                }
              ],
              "asn": 147049,
              "looking_glass": "",
              "route_server": "",
              "irr_as_set": "APNIC::AS-SET-AS147049",
              "info_type": "",
              "info_types": [],
              "info_prefixes4": 1000,
              "info_prefixes6": 1000,
              "info_traffic": "",
              "info_ratio": "Not Disclosed",
              "info_scope": "Global",
              "info_unicast": true,
              "info_multicast": false,
              "info_ipv6": true,
              "info_never_via_route_servers": false,
              "ix_count": 7,
              "fac_count": 1,
              "notes": "",
              "netixlan_updated": "2026-03-26T15:30:03Z",
              "netfac_updated": "2023-07-18T08:22:19Z",
              "poc_updated": "2022-10-06T09:29:57Z",
              "policy_url": "",
              "policy_general": "Open",
              "policy_locations": "Not Required",
              "policy_ratio": false,
              "policy_contracts": "Not Required",
              "allow_ixp_update": false,
              "status_dashboard": "",
              "rir_status": "ok",
              "rir_status_updated": "2024-06-26T04:47:55Z",
              "logo": null,
              "created": "2022-01-18T09:17:39Z",
              "updated": "2025-11-03T13:33:39Z",
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
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-17T07:14:50.410886+00:00",
      "sha256": "78b2189284f165a8a179e0ad54fc69ac79705499929567c04605996542949b72",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    },
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-17T07:14:52.848394+00:00",
      "sha256": "6a64fc32eac27ca2f94d8748737b636d03df4bd54e6b262d748c84066fb4b93e",
      "summary_bullets": [
        "No keyword hits for common sections; manual review recommended"
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
    "https://ipwho.is/176.100.43.136",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordcheckout.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/pricing/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "surface_probe:har_summary",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/webrtc",
    "ipv6_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/fingerprint",
    "attribution_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/policy",
    "competitor_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe",
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
            "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
            "oneuptime=2fYJpBXRQsmY3Py",
            "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
            "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
            "MS=ms41624661",
            "MS=ms60989570",
            "MS=ms69824556"
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
                      "query_id": "20260417071524-d2f2576e-8797-49fa-8b7f-705fca55a88c",
                      "process_time": 84,
                      "server_id": "app175",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:24.114399",
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
                        "query_time": "2026-04-17T00:00:00",
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
                        "ix_count": 351,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-17T03:07:10Z",
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
                        "updated": "2026-04-17T03:07:21Z",
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
                      "query_id": "20260417071526-f177592e-7265-4742-adce-5920b02dd7c6",
                      "process_time": 64,
                      "server_id": "app177",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:26.190647",
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
                        "query_time": "2026-04-17T00:00:00",
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
                        "ix_count": 351,
                        "fac_count": 222,
                        "notes": "Cloudflare operates a global anycast network. All peers are required to have a complete PeeringDB entry and 24x7 NOC. PeeringDB is used for provisioning peering sessions. The number of prefixes we advertise will vary across sessions, and over time.\n\n**Automatic IX peering** is available through [**Cloudflare Peering Portal**](https://peering.cloudflare.com/). Authenticate using PeeringDB OIDC. ASN admins on PeeringDB are authorized to request peering.\n\nNetworks exchanging more than 10 Gbps of traffic in a single location may request a PNI. Only Nx100G LR4 connections are supported. Networks may also be eligible for embedded caches.\n\nPeering and embedded cache guidelines available at [**cloudflare.com/peering-policy**](https://www.cloudflare.com/peering-policy/).\n\nSubmit verifiable abuse reports to [**cloudflare.com/abuse**](https://www.cloudflare.com/trust-hub/abuse-approach/). Do not send abuse reports to NOC / Policy email addresses.",
                        "netixlan_updated": "2026-04-17T03:07:10Z",
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
                        "updated": "2026-04-17T03:07:21Z",
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
                      "query_id": "20260417071528-4dcf952b-9302-4f89-849e-26e26f046d91",
                      "process_time": 42,
                      "server_id": "app194",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:28.254031",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071529-fd800d40-5d9a-430c-9da8-a1ea20080dab",
                      "process_time": 118,
                      "server_id": "app189",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:30.015419",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071531-1129165c-e5ed-447b-a14e-9c0e6f76fcb6",
                      "process_time": 60,
                      "server_id": "app198",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:31.533430",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071532-a6eea3ad-8640-4877-8e05-de8543d9d42d",
                      "process_time": 45,
                      "server_id": "app189",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:33.038818",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071534-667eeb99-0043-4fce-997c-a3afea53d35e",
                      "process_time": 42,
                      "server_id": "app192",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:34.553072",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071536-9065a567-a2c2-490f-9842-ef004fd9a743",
                      "process_time": 44,
                      "server_id": "app160",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:36.256953",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071538-ea234f99-e219-4700-a86c-a78ccaa3259a",
                      "process_time": 82,
                      "server_id": "app172",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:38.335864",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071540-c38eaa66-8f2a-429b-9540-15bed8523dc0",
                      "process_time": 57,
                      "server_id": "app187",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:40.342909",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071541-386ce0ef-6043-4a02-8581-a966a47c42c6",
                      "process_time": 56,
                      "server_id": "app177",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:41.927062",
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
                        "query_time": "2026-04-17T00:00:00",
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
                      "query_id": "20260417071543-c1cb8f29-2cc5-43c7-9fc0-2c1a8a46a573",
                      "process_time": 41,
                      "server_id": "app168",
                      "build_version": "v0.9.9-2026.04.16",
                      "pipeline": "1232122",
                      "status": "ok",
                      "status_code": 200,
                      "time": "2026-04-17T07:15:43.347768",
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
                        "query_time": "2026-04-17T00:00:00",
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
          "server": "cloudflare",
          "cf-ray": "9ed9a61f4f8bc67e-YVR"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a61f4f8bc67e"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/competitor_probe/har/d945f098fbd5bb50.har",
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
          "cf-ray": "9ed9a621eb1be19b-YVR"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "176.100.43.136",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "176.100.43.136"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 176.100.43.136 (176.100.43.136), 15 hops max, 40 byte packets\n",
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
    "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t176.100.43.136\nHostname\tn/a\nIP Address Location\nCountry\tCanada (CA)\nState/Region\tBritish Columbia\nCity\tVancouver\nISP\tPacketHub S.A.\nOrganization\tPackethub S.A\nNetwork\tAS147049 PacketHub S.A. (VPN, VPSH)\nUsage Type\tCorporate / Hosting\nTimezone\tAmerica/Vancouver (PDT)\nLocal Time\tFri, 17 Apr 2026 00:14:59 -0700\nCoordinates\t49.2827,-123.1210\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t176.100.43.136\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t12 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\t120f30e12770d736954aa6dc9fdf427b\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t176.100.43.128 - 176.100.43.255\nCIDR\t176.100.43.128/25\nName\tPACKETUB-20221011\nHandle\t176.100.43.128 - 176.100.43.255\nParent Handle\t176.100.43.0 - 176.100.43.255\nNet Type\tASSIGNED PA\nCountry\tCanada\nRegistration\tTue, 11 Oct 2022 13:29:54 GMT\nLast Changed\tTue, 11 Oct 2022 13:29:54 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tDe-net1-1-mnt\nHandle\tDe-net1-1-mnt\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t176.100.43.136\nISP\tPacketHub S.A.\nLocation\tCanada, Vancouver\nDNS Leak Test\nTest Results\tFound 11 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n176.100.43.133\tPacketHub S.A.\tCanada, Vancouver\n176.100.43.134\tPacketHub S.A.\tCanada, Vancouver\n176.100.43.135\tPacketHub S.A.\tCanada, Vancouver\n176.100.43.136\tPacketHub S.A.\tCanada, Vancouver\n176.100.43.137\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.145\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.179\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.180\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.181\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.182\tPacketHub S.A.\tCanada, Vancouver\n185.153.179.183\tPacketHub S.A.\tCanada, Vancouver\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t176.100.43.136\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t176.100.43.136\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (219)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_5677131c3dd8\nJA3\ted5e0cde876454820cc94b4edf77c1ca\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x1A1A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x8A8A\nGREASE\n\n\n0x0000\nserver_name\n\n\n0x000A\nsupported_groups\n\n\n0x0017\nextended_main_secret\n\n\n0x001B\ncompress_certificate\n\n\n0x44CD\napplication_settings\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x0023\nsession_ticket\n\n\n0x000D\nsignature_algorithms\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x002B\nsupported_versions\n\n\n0xFF01\nrenegotiation_info\n\n\n0x0005\nstatus_request\n\n\n0x0033\nkey_share\n\n\n0x000B\nec_point_formats\n\n\n0x4A4A\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t48\nenc_length\t32\npayload_length\t144\nkey_share\nclient_shares\t\n0x8A8A\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brows",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-8abe8931",
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
        "answer_summary": "Exit IPv4 176.100.43.136; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "All 3 echo endpoints agree on IPv4 176.100.43.136.",
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
        "answer_summary": "Exit IPv4 176.100.43.136 for location ca-british-columbia-vancouver-136.",
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
        "answer_summary": "ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.",
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
        "answer_summary": "ASN 147049 — PACKETHUBSA-AS-AP PacketHub S.A.",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS response does not contain an answer to the question: 136.43.100.176.in-addr.arpa. IN PTR",
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
        "answer_summary": "Consistent: exit_geo.location_label matches vpn_location_label ('Vancouver, British Columbia, Canada').",
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
        "host": "surface_probe",
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
      "ip": "176.100.43.136",
      "country_code": "CA",
      "region": "British Columbia",
      "city": "Vancouver",
      "connection": {
        "asn": 147049,
        "org": "Packethub S.A.",
        "isp": "Packethub S.A.",
        "domain": "net1.de"
      },
      "location_id": "ca-british-columbia-vancouver-136",
      "location_label": "Vancouver, British Columbia, Canada"
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
            "cf-ray": "9ed9a6270d7176b8-SEA"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a6270d7176b8"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/3cec43152ba057c5.har",
          "page_type": "pricing"
        },
        {
          "url": "https://my.nordaccount.com/",
          "error": null,
          "status": 200,
          "final_url": "https://my.nordaccount.com/",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed9a6296e3d6052-YVR"
          },
          "scripts": [
            "https://my.nordaccount.com/assets/runtime.a9c27b97b093c98ae649.js",
            "https://my.nordaccount.com/assets/_formatjs.defaultvendors.ac0846ece32d56901ea4.js",
            "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.eb63fbe45c73fab20cc3.js",
            "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.12b7c8ec7f121d0b5787.js",
            "https://my.nordaccount.com/assets/index.caa7c4317590658d27ac.js",
            "https://my.nordaccount.com/assets/_nordsec.defaultvendors.4c748c7db5cefa2fe8df.chunk.js",
            "https://my.nordaccount.com/assets/date-fns.defaultvendors.eaa415bc21c381d3558b.chunk.js",
            "https://my.nordaccount.com/assets/_nord.defaultvendors.f2b134f66f68507b33fc.chunk.js",
            "https://my.nordaccount.com/assets/tslib.defaultvendors.f240679c709d47693a22.chunk.js",
            "https://my.nordaccount.com/assets/_sentry.defaultvendors.6a26a7e44a35f2381dc2.chunk.js",
            "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.36f404cb5c3d7ff37a26.chunk.js",
            "https://my.nordaccount.com/assets/graphql.defaultvendors.6196445f71efc38548cd.chunk.js",
            "https://my.nordaccount.com/assets/react-intl.defaultvendors.b71793934bfb99d0b581.chunk.js",
            "https://my.nordaccount.com/assets/graphql-request.defaultvendors.25a38b2f26bc2e06c5ff.chunk.js",
            "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.73708e4220415063788d.chunk.js",
            "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.719b911b91adb7aef00b.chunk.js",
            "https://my.nordaccount.com/assets/uuid.defaultvendors.746a61a183a00afcd19c.chunk.js",
            "https://my.nordaccount.com/assets/_babel.defaultvendors.09ede7e9eaeecef6d984.chunk.js",
            "https://my.nordaccount.com/assets/react.defaultvendors.0015e8b82b057f403937.chunk.js",
            "https://my.nordaccount.com/assets/react-dom.defaultvendors.3a1333ac0f7e30c6efdc.chunk.js",
            "https://my.nordaccount.com/assets/prop-types.defaultvendors.07541a84659c6203c26c.chunk.js",
            "https://my.nordaccount.com/assets/react-toastify.defaultvendors.ff2d3ee8bd32115c5105.chunk.js",
            "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.5f3f39fa4221cfe8e9f3.chunk.js",
            "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.de9ccecd85bf07c5aa48.chunk.js",
            "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.8d091fe6bd55d67df739.chunk.js",
            "https://my.nordaccount.com/assets/scheduler.defaultvendors.db974a7e0f5f400c9542.chunk.js",
            "https://my.nordaccount.com/assets/react-is.defaultvendors.c68f828a892f78334b23.chunk.js",
            "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.fde5e082146b4e49cbf9.chunk.js",
            "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.229ce3ff05c6241dc586.chunk.js",
            "https://my.nordaccount.com/assets/react-redux.defaultvendors.fd161b5e1759a70dfe89.chunk.js",
            "https://my.nordaccount.com/assets/js-cookie.defaultvendors.4f558a2177bb0eb5b78d.chunk.js",
            "https://my.nordaccount.com/assets/immer.defaultvendors.0b964b76caa620cff239.chunk.js",
            "https://my.nordaccount.com/assets/clsx.defaultvendors.df823a651876ebf8de25.chunk.js",
            "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.baf6829019a88080d27b.chunk.js",
            "https://my.nordaccount.com/assets/classnames.defaultvendors.c2b96eae94047c76c0ff.chunk.js",
            "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.45faa7f70fa2eebadd6a.chunk.js",
            "https://my.nordaccount.com/assets/react-router.defaultvendors.78aaad2448f5c1b716a5.chunk.js",
            "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.6b7f2f2725b53b198161.chunk.js",
            "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.1d2b074be5f45739167d.chunk.js",
            "https://my.nordaccount.com/assets/react-helmet.defaultvendors.84ea08fb735d01e5cbd2.chunk.js",
            "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.00289033652a15f72cb3.chunk.js",
            "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.c750d7ce2db67f793585.chunk.js",
            "https://my.nordaccount.com/assets/object-assign.defaultvendors.f85101626dd44f58baec.chunk.js",
            "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.e2b6c1d21e29212d4759.chunk.js",
            "https://my.nordaccount.com/assets/humps.defaultvendors.3754860cfe25e6714b78.chunk.js",
            "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.79396dd4378902d7beaa.chunk.js",
            "https://my.nordaccount.com/assets/filter-obj.defaultvendors.84146f4c18b1572ac0ba.chunk.js",
            "https://my.nordaccount.com/assets/file-saver.defaultvendors.cc329c95afaf575e4b41.chunk.js",
            "https://my.nordaccount.com/assets/exenv.defaultvendors.a1af14a17940d6080ed3.chunk.js",
            "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.1e3b43bb5d3c3776b319.chunk.js",
            "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.3e680526e6c07ca51319.chunk.js",
            "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.2f8dd77d6309c41de433.chunk.js",
            "https://my.nordaccount.com/assets/split-on-first.defaultvendors.b3f30d1714518afe82db.chunk.js",
            "https://my.nordaccount.com/assets/query-string.defaultvendors.82e833f4af0d00cbde64.chunk.js",
            "https://my.nordaccount.com/assets/_remix-run.defaultvendors.363e94888ab4b4faff10.chunk.js",
            "https://my.nordaccount.com/assets/4666.705e2d0d1330cfd25bc1.chunk.js"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/0096221d6f12d382.har",
          "page_type": "signup"
        },
        {
          "url": "https://nordcheckout.com/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed9a634ff7276a6-SEA"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9a634ff7276a6"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/5c4416295d131e0b.har",
          "page_type": "checkout"
        }
      ],
      "surface_probe_dir": "runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe",
      "har_summary": {
        "har_files": [
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/3cec43152ba057c5.har",
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
          },
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/0096221d6f12d382.har",
            "entry_count": 60,
            "unique_hosts": [
              "my.nordaccount.com"
            ],
            "unique_schemes": [
              "https"
            ],
            "tracker_candidates": [],
            "cdn_candidates": [],
            "error": null
          },
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T071350Z-5b9ffc60/raw/ca-british-columbia-vancouver-136/surface_probe/har/5c4416295d131e0b.har",
            "entry_count": 5,
            "unique_hosts": [
              "nordcheckout.com",
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
          "my.nordaccount.com",
          "nordcheckout.com",
          "nordvpn.com"
        ],
        "merged_tracker_candidates": [],
        "merged_cdn_candidates": []
      }
    }
  }
}
```

---



### nordvpn-20260417T072634Z-607907b5 / de-hamburg-hamburg-154



- **vpn_provider:** nordvpn
- **Label:** Hamburg, Hamburg, Germany
- **Path:** `runs/nordvpn-20260417T072634Z-607907b5/locations/de-hamburg-hamburg-154/normalized.json`
- **schema_version:** 1.4
- **timestamp_utc:** 2026-04-17T07:30:17.153959+00:00
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
| exit_ip_v4 | 185.161.202.154 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.161.202.154",
    "ipv6": null,
    "raw_excerpt": "185.161.202.154",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "92.211.2.176",
    "ipv6": null,
    "raw_excerpt": "92.211.2.176",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.161.202.154",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.161.202.154\"}",
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
      "185.161.202.86"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.161.202.154"
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
| host | udp | 4f528194-7dbb-4b1b-adbd-7c803e5cbef7.local | 64573 | `candidate:1642710040 1 udp 2113937151 4f528194-7dbb-4b1b-adbd-7c803e5cbef7.local 64573 typ host generation 0 ufrag JF9E network-cost 999` |
| srflx | udp | 185.161.202.154 | 15783 | `candidate:1643922750 1 udp 1677729535 185.161.202.154 15783 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag JF9E network-cost 999` |


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
          "query_id": "20260417072657-f6666e80-6902-437a-971b-c7a2cdf06d5a",
          "process_time": 103,
          "server_id": "app178",
          "build_version": "v0.9.9-2026.04.16",
          "pipeline": "1232122",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-17T07:26:57.949238",
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
            "query_time": "2026-04-17T00:00:00",
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
        "data": [
          {
            "id": 31153,
            "org_id": 28491,
            "name": "PacketHub AS207137",
            "aka": "",
            "name_long": "",
            "website": "https://www.packethub.net/",
            "social_media": [
              {
                "service": "website",
                "identifier": "https://www.packethub.net/"
              }
            ],
            "asn": 207137,
            "looking_glass": "",
            "route_server": "",
            "irr_as_set": "AS-SET-AS207137",
            "info_type": "",
            "info_types": [],
            "info_prefixes4": 5000,
            "info_prefixes6": 5000,
            "info_traffic": "",
            "info_ratio": "Not Disclosed",
            "info_scope": "Global",
            "info_unicast": true,
            "info_multicast": false,
            "info_ipv6": true,
            "info_never_via_route_servers": false,
            "ix_count": 3,
            "fac_count": 0,
            "notes": "",
            "netixlan_updated": "2026-03-30T06:43:18Z",
            "netfac_updated": null,
            "poc_updated": "2022-10-06T09:33:32Z",
            "policy_url": "",
            "policy_general": "Open",
            "policy_locations": "Not Required",
            "policy_ratio": false,
            "policy_contracts": "Not Required",
            "allow_ixp_update": false,
            "status_dashboard": "",
            "rir_status": "ok",
            "rir_status_updated": "2024-06-26T04:47:55Z",
            "logo": null,
            "created": "2022-10-06T06:26:09Z",
            "updated": "2024-07-04T10:28:36Z",
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
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://nordvpn.com/privacy-policy/",
    "fetched_at_utc": "2026-04-17T07:27:41.484273+00:00",
    "sha256": "0356c22757c29fa25716facf9112f6218a280bb052870a411e85a8c3d4ff22a3",
    "summary_bullets": [
      "Mentions logging (keyword hit; review source)"
    ]
  },
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-17T07:27:48.021371+00:00",
    "sha256": "93970d55f0fa62dc09a922561479264394ed4f6cebc0be5db5199d940e0ad2f6",
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

- `https://ipwho.is/185.161.202.154`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordcheckout.com/`

- `https://nordvpn.com/`

- `https://nordvpn.com/pricing/`

- `https://nordvpn.com/privacy-policy/`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `surface_probe:har_summary`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260417T072634Z-607907b5/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/webrtc",
  "ipv6_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/fingerprint",
  "attribution_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/attribution.json",
  "asn_prefixes_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/asn_prefixes.json",
  "exit_dns_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/exit_dns.json",
  "policy_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/policy",
  "competitor_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe",
  "browserleaks_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/browserleaks_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/yourinfo_probe",
  "baseline_json": null,
  "surface_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe",
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
  "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/yourinfo_probe/yourinfo.har",
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
      "id": "finding-yourinfo-5cc89707",
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
      "answer_summary": "Exit IPv4 185.161.202.154; leak flags dns=False webrtc=False ipv6=False.",
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
      "answer_summary": "Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.154, 92.211.2.176.",
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
      "answer_summary": "Exit IPv4 185.161.202.154 for location de-hamburg-hamburg-154.",
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
      "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 154.202.161.185.in-addr.arpa.",
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
      "host": "surface_probe",
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


#### Website & DNS surface (summary)


| Metric | This location |
|--------|---------------|
| Unique request hosts | 3 |
| Tracker candidates | 0 |
| CDN candidates | 0 |


**Provider DNS (apex)**

| Domain | NS (sample) | MX (sample) | IPv6 apex |
|--------|-------------|-------------|-----------|
| `nordvpn.com` | — | 1 aspmx.l.google.com, 5 alt1.aspmx.l.google.com, 5 alt2.aspmx.l.google.com (+2 more) | no AAAA (IPv4-only apex) |




**Surface URLs**

| page_type | URL | status |
|-----------|-----|--------|
| pricing | https://nordvpn.com/pricing/ | 403 |
| signup | https://my.nordaccount.com/ | 200 |
| checkout | https://nordcheckout.com/ | 403 |





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
        "error": "NS: The resolution lifetime expired after 10.203 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
        "txt": [
          "MS=ms60989570",
          "MS=ms69824556",
          "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
          "oneuptime=2fYJpBXRQsmY3Py",
          "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
          "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
          "MS=ms41624661"
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
        "cf-ray": "9ed9b90e2db2630a-HAM"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b90e2db2630a"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe/har/d945f098fbd5bb50.har"
    }
  ],
  "har_summary": {
    "har_files": [
      {
        "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe/har/d945f098fbd5bb50.har",
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
        "cf-ray": "9ed9b9153f6f62cb-HAM"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "185.161.202.154",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "185.161.202.154"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 185.161.202.154 (185.161.202.154), 15 hops max, 40 byte packets\n",
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
    "ip": "185.161.202.154",
    "country_code": "DE",
    "region": "Hamburg",
    "city": "Hamburg",
    "connection": {
      "asn": 207137,
      "org": "Packethub S.A.",
      "isp": "Packethub S.A.",
      "domain": "packethub.net"
    },
    "location_id": "de-hamburg-hamburg-154",
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
          "cf-ray": "9ed9b91f6dfe3392-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b91f6dfe3392"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/3cec43152ba057c5.har",
        "page_type": "pricing"
      },
      {
        "url": "https://my.nordaccount.com/",
        "error": null,
        "status": 200,
        "final_url": "https://my.nordaccount.com/",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed9b9235d8b62d7-HAM"
        },
        "scripts": [
          "https://my.nordaccount.com/assets/runtime.a9c27b97b093c98ae649.js",
          "https://my.nordaccount.com/assets/_formatjs.defaultvendors.ac0846ece32d56901ea4.js",
          "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.eb63fbe45c73fab20cc3.js",
          "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.12b7c8ec7f121d0b5787.js",
          "https://my.nordaccount.com/assets/index.caa7c4317590658d27ac.js",
          "https://my.nordaccount.com/assets/_nordsec.defaultvendors.4c748c7db5cefa2fe8df.chunk.js",
          "https://my.nordaccount.com/assets/date-fns.defaultvendors.eaa415bc21c381d3558b.chunk.js",
          "https://my.nordaccount.com/assets/_nord.defaultvendors.f2b134f66f68507b33fc.chunk.js",
          "https://my.nordaccount.com/assets/tslib.defaultvendors.f240679c709d47693a22.chunk.js",
          "https://my.nordaccount.com/assets/_sentry.defaultvendors.6a26a7e44a35f2381dc2.chunk.js",
          "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.36f404cb5c3d7ff37a26.chunk.js",
          "https://my.nordaccount.com/assets/graphql.defaultvendors.6196445f71efc38548cd.chunk.js",
          "https://my.nordaccount.com/assets/react-intl.defaultvendors.b71793934bfb99d0b581.chunk.js",
          "https://my.nordaccount.com/assets/graphql-request.defaultvendors.25a38b2f26bc2e06c5ff.chunk.js",
          "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.73708e4220415063788d.chunk.js",
          "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.719b911b91adb7aef00b.chunk.js",
          "https://my.nordaccount.com/assets/uuid.defaultvendors.746a61a183a00afcd19c.chunk.js",
          "https://my.nordaccount.com/assets/_babel.defaultvendors.09ede7e9eaeecef6d984.chunk.js",
          "https://my.nordaccount.com/assets/react.defaultvendors.0015e8b82b057f403937.chunk.js",
          "https://my.nordaccount.com/assets/react-dom.defaultvendors.3a1333ac0f7e30c6efdc.chunk.js",
          "https://my.nordaccount.com/assets/prop-types.defaultvendors.07541a84659c6203c26c.chunk.js",
          "https://my.nordaccount.com/assets/react-toastify.defaultvendors.ff2d3ee8bd32115c5105.chunk.js",
          "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.5f3f39fa4221cfe8e9f3.chunk.js",
          "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.de9ccecd85bf07c5aa48.chunk.js",
          "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.8d091fe6bd55d67df739.chunk.js",
          "https://my.nordaccount.com/assets/scheduler.defaultvendors.db974a7e0f5f400c9542.chunk.js",
          "https://my.nordaccount.com/assets/react-is.defaultvendors.c68f828a892f78334b23.chunk.js",
          "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.fde5e082146b4e49cbf9.chunk.js",
          "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.229ce3ff05c6241dc586.chunk.js",
          "https://my.nordaccount.com/assets/react-redux.defaultvendors.fd161b5e1759a70dfe89.chunk.js",
          "https://my.nordaccount.com/assets/js-cookie.defaultvendors.4f558a2177bb0eb5b78d.chunk.js",
          "https://my.nordaccount.com/assets/immer.defaultvendors.0b964b76caa620cff239.chunk.js",
          "https://my.nordaccount.com/assets/clsx.defaultvendors.df823a651876ebf8de25.chunk.js",
          "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.baf6829019a88080d27b.chunk.js",
          "https://my.nordaccount.com/assets/classnames.defaultvendors.c2b96eae94047c76c0ff.chunk.js",
          "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.45faa7f70fa2eebadd6a.chunk.js",
          "https://my.nordaccount.com/assets/react-router.defaultvendors.78aaad2448f5c1b716a5.chunk.js",
          "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.6b7f2f2725b53b198161.chunk.js",
          "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.1d2b074be5f45739167d.chunk.js",
          "https://my.nordaccount.com/assets/react-helmet.defaultvendors.84ea08fb735d01e5cbd2.chunk.js",
          "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.00289033652a15f72cb3.chunk.js",
          "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.c750d7ce2db67f793585.chunk.js",
          "https://my.nordaccount.com/assets/object-assign.defaultvendors.f85101626dd44f58baec.chunk.js",
          "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.e2b6c1d21e29212d4759.chunk.js",
          "https://my.nordaccount.com/assets/humps.defaultvendors.3754860cfe25e6714b78.chunk.js",
          "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.79396dd4378902d7beaa.chunk.js",
          "https://my.nordaccount.com/assets/filter-obj.defaultvendors.84146f4c18b1572ac0ba.chunk.js",
          "https://my.nordaccount.com/assets/file-saver.defaultvendors.cc329c95afaf575e4b41.chunk.js",
          "https://my.nordaccount.com/assets/exenv.defaultvendors.a1af14a17940d6080ed3.chunk.js",
          "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.1e3b43bb5d3c3776b319.chunk.js",
          "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.3e680526e6c07ca51319.chunk.js",
          "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.2f8dd77d6309c41de433.chunk.js",
          "https://my.nordaccount.com/assets/split-on-first.defaultvendors.b3f30d1714518afe82db.chunk.js",
          "https://my.nordaccount.com/assets/query-string.defaultvendors.82e833f4af0d00cbde64.chunk.js",
          "https://my.nordaccount.com/assets/_remix-run.defaultvendors.363e94888ab4b4faff10.chunk.js",
          "https://my.nordaccount.com/assets/4666.705e2d0d1330cfd25bc1.chunk.js"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/0096221d6f12d382.har",
        "page_type": "signup"
      },
      {
        "url": "https://nordcheckout.com/",
        "error": null,
        "status": 403,
        "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
        "cdn_headers": {
          "server": "cloudflare",
          "cf-ray": "9ed9b9394a836311-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b9394a836311"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/5c4416295d131e0b.har",
        "page_type": "checkout"
      }
    ],
    "surface_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe",
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/3cec43152ba057c5.har",
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
        },
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/0096221d6f12d382.har",
          "entry_count": 60,
          "unique_hosts": [
            "my.nordaccount.com"
          ],
          "unique_schemes": [
            "https"
          ],
          "tracker_candidates": [],
          "cdn_candidates": [],
          "error": null
        },
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/5c4416295d131e0b.har",
          "entry_count": 5,
          "unique_hosts": [
            "nordcheckout.com",
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
        "my.nordaccount.com",
        "nordcheckout.com",
        "nordvpn.com"
      ],
      "merged_tracker_candidates": [],
      "merged_cdn_candidates": []
    }
  }
}
```

#### Complete normalized record (verbatim)

Same content as `normalized.json` for this location; only a ~2 MiB safety cap can shorten this fenced block.

```json
{
  "schema_version": "1.4",
  "run_id": "nordvpn-20260417T072634Z-607907b5",
  "timestamp_utc": "2026-04-17T07:30:17.153959+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "de-hamburg-hamburg-154",
  "vpn_location_label": "Hamburg, Hamburg, Germany",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.161.202.154",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.161.202.154",
      "ipv6": null,
      "raw_excerpt": "185.161.202.154",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "92.211.2.176",
      "ipv6": null,
      "raw_excerpt": "92.211.2.176",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.161.202.154",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.161.202.154\"}",
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
        "185.161.202.86"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.161.202.154"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "4f528194-7dbb-4b1b-adbd-7c803e5cbef7.local",
      "port": 64573,
      "raw": "candidate:1642710040 1 udp 2113937151 4f528194-7dbb-4b1b-adbd-7c803e5cbef7.local 64573 typ host generation 0 ufrag JF9E network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.161.202.154",
      "port": 15783,
      "raw": "candidate:1643922750 1 udp 1677729535 185.161.202.154 15783 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag JF9E network-cost 999"
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
            "query_id": "20260417072657-f6666e80-6902-437a-971b-c7a2cdf06d5a",
            "process_time": 103,
            "server_id": "app178",
            "build_version": "v0.9.9-2026.04.16",
            "pipeline": "1232122",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-17T07:26:57.949238",
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
              "query_time": "2026-04-17T00:00:00",
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
          "data": [
            {
              "id": 31153,
              "org_id": 28491,
              "name": "PacketHub AS207137",
              "aka": "",
              "name_long": "",
              "website": "https://www.packethub.net/",
              "social_media": [
                {
                  "service": "website",
                  "identifier": "https://www.packethub.net/"
                }
              ],
              "asn": 207137,
              "looking_glass": "",
              "route_server": "",
              "irr_as_set": "AS-SET-AS207137",
              "info_type": "",
              "info_types": [],
              "info_prefixes4": 5000,
              "info_prefixes6": 5000,
              "info_traffic": "",
              "info_ratio": "Not Disclosed",
              "info_scope": "Global",
              "info_unicast": true,
              "info_multicast": false,
              "info_ipv6": true,
              "info_never_via_route_servers": false,
              "ix_count": 3,
              "fac_count": 0,
              "notes": "",
              "netixlan_updated": "2026-03-30T06:43:18Z",
              "netfac_updated": null,
              "poc_updated": "2022-10-06T09:33:32Z",
              "policy_url": "",
              "policy_general": "Open",
              "policy_locations": "Not Required",
              "policy_ratio": false,
              "policy_contracts": "Not Required",
              "allow_ixp_update": false,
              "status_dashboard": "",
              "rir_status": "ok",
              "rir_status_updated": "2024-06-26T04:47:55Z",
              "logo": null,
              "created": "2022-10-06T06:26:09Z",
              "updated": "2024-07-04T10:28:36Z",
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
  "policies": [
    {
      "role": "vpn",
      "url": "https://nordvpn.com/privacy-policy/",
      "fetched_at_utc": "2026-04-17T07:27:41.484273+00:00",
      "sha256": "0356c22757c29fa25716facf9112f6218a280bb052870a411e85a8c3d4ff22a3",
      "summary_bullets": [
        "Mentions logging (keyword hit; review source)"
      ]
    },
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-17T07:27:48.021371+00:00",
      "sha256": "93970d55f0fa62dc09a922561479264394ed4f6cebc0be5db5199d940e0ad2f6",
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
    "https://ipwho.is/185.161.202.154",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordcheckout.com/",
    "https://nordvpn.com/",
    "https://nordvpn.com/pricing/",
    "https://nordvpn.com/privacy-policy/",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "surface_probe:har_summary",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260417T072634Z-607907b5/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/webrtc",
    "ipv6_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/fingerprint",
    "attribution_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/attribution.json",
    "asn_prefixes_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/asn_prefixes.json",
    "exit_dns_json": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/exit_dns.json",
    "policy_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/policy",
    "competitor_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe",
    "browserleaks_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/browserleaks_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/yourinfo_probe",
    "baseline_json": null,
    "surface_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe",
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
          "error": "NS: The resolution lifetime expired after 10.203 seconds: Server Do53:100.64.0.2@53 answered The DNS operation timed out.; Server Do53:100.64.0.2@53 answered The DNS operation timed out.",
          "txt": [
            "MS=ms60989570",
            "MS=ms69824556",
            "google-site-verification=QIh6YGom6DuhiCuoCX1mtuBcxf3zLzUXrMUzZpWkVyw",
            "oneuptime=2fYJpBXRQsmY3Py",
            "v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all",
            "MS=9AAAE7D4B160BBC17B316D2992B6B14C64DF4E13",
            "MS=ms41624661"
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
          "cf-ray": "9ed9b90e2db2630a-HAM"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b90e2db2630a"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe/har/d945f098fbd5bb50.har"
      }
    ],
    "har_summary": {
      "har_files": [
        {
          "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/competitor_probe/har/d945f098fbd5bb50.har",
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
          "cf-ray": "9ed9b9153f6f62cb-HAM"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "185.161.202.154",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "185.161.202.154"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 185.161.202.154 (185.161.202.154), 15 hops max, 40 byte packets\n",
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
    "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/yourinfo_probe/yourinfo.har",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWhat Is My IP Address\nMy IP Address\nIP Address\t185.161.202.154\nHostname\tn/a\nIP Address Location\nCountry\tGermany (DE)\nState/Region\tHamburg\nCity\tHamburg\nISP\tPacketHub S.A.\nOrganization\tPackethub S.A\nNetwork\tAS207137 PacketHub S.A. (VPN)\nUsage Type\tCellular\nTimezone\tEurope/Berlin (CEST)\nLocal Time\tFri, 17 Apr 2026 09:27:56 +0200\nCoordinates\t53.5488,9.9872\nIPv6 Leak Test\nIPv6 Address\tn/a\nWebRTC Leak Test\nLocal IP Address\tn/a\nPublic IP Address\t185.161.202.154\nDNS Leak Test\nTest Results\t\nRun DNS Leak Test\n\nTCP/IP Fingerprint\nOS\tAndroid\nMTU\t1500\nLink Type\tEthernet or modem\nDistance\t14 Hops\nJA4T\t65535_2-4-8-1-3_1460_9\nTLS Fingerprint\nJA4\tt13d1516h2_8daaf6152771_d8a2da3f94cd\nJA3 Hash\tb5bad6ebc1cd8e9bbe32db5616150ae1\nHTTP/2 Fingerprint\nAkamai Hash\t52d84b11737d980aef856699f885ca86\nHTTP Headers\nraw headers\n\nRequest\tGET /ip HTTP/2.0\nSec-CH-UA\t\"Not:A-Brand\";v=\"99\", \"HeadlessChrome\";v=\"145\", \"Chromium\";v=\"145\"\nSec-CH-UA-Mobile\t?0\nSec-CH-UA-Platform\t\"macOS\"\nUpgrade-Insecure-Requests\t1\nUser-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nAccept\ttext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\nSec-Fetch-Site\tnone\nSec-Fetch-Mode\tnavigate\nSec-Fetch-User\t?1\nSec-Fetch-Dest\tdocument\nAccept-Encoding\tgzip, deflate, br, zstd\nPriority\tu=0, i\nHost\tbrowserleaks.com\nTor Relay Details\nRelays\tThis IP is not identified to be a Tor Relay\nWhere is My IP\n\nIP Address Whois\nSource Registry\tRIPE NCC\nNet Range\t185.161.202.0 - 185.161.202.255\nCIDR\t185.161.202.0/24\nName\tPackethub-20240426\nHandle\t185.161.202.0 - 185.161.202.255\nParent Handle\t185.161.202.0 - 185.161.203.255\nNet Type\tASSIGNED PA\nCountry\tGermany\nRegistration\tFri, 26 Apr 2024 13:37:12 GMT\nLast Changed\tFri, 26 Apr 2024 13:37:12 GMT\nDescription\tPackethub S.A.\nFull Name\tAlina Gatsaniuk\nHandle\tAG25300-RIPE\nEntity Roles\tAdministrative, Technical\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tPackethub S.A.\nHandle\tORG-PS409-RIPE\nEntity Roles\tRegistrant\nTelephone\t+5078336503\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nFull Name\tPackethub S.A. IT Department\nHandle\tPSID1-RIPE\nEntity Roles\tAbuse\nEmail\tabuse@packethub.tech\nAddress\tOffice 76, Plaza 2000, 50 Street and Marbella, Bella Vista\nPanama City\nPanama\nFull Name\tTERRATRANSIT-MNT\nHandle\tTERRATRANSIT-MNT\nEntity Roles\tRegistrant\nIP Geolocation by DB-IP\nFurther Reading\nLeave a Comment (451)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nDNS Leak Test\n\nIncorrect network configurations or faulty VPN/proxy software can lead to your device sending DNS requests directly to your ISP's server, potentially enabling ISPs or other third parties to monitor your online activity.\n\nThe DNS Leak Test is a tool used to determine which DNS servers your browser is using to resolve domain names. This test attempts to resolve 50 randomly generated domain names, of which 25 are IPv4-only and 25 are IPv6-only.\n\nYour IP Address\nIP Address\t185.161.202.154\nISP\tPacketHub S.A.\nLocation\tGermany, Hamburg\nDNS Leak Test\nTest Results\tFound 17 Servers, 1 ISP, 1 Location\nYour DNS Servers\t\nIP Address :\tISP :\tLocation :\n185.161.202.86\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.87\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.88\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.89\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.90\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.91\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.92\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.93\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.94\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.95\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.96\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.97\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.98\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.99\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.111\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.154\tPacketHub S.A.\tGermany, Hamburg\n185.161.202.155\tPacketHub S.A.\tGermany, Hamburg\nLeave a Comment (244)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nWebRTC Leak Test\nYour Remote IP\nIPv4 Address\t185.161.202.154\nIPv6 Address\t-\nWebRTC Support Detection\nRTCPeerConnection\t\n✔\nTrue\nRTCDataChannel\t\n✔\nTrue\nYour WebRTC IP\nWebRTC Leak Test\t\n✔\nNo Leak\nLocal IP Address\t-\nPublic IP Address\t185.161.202.154\nSession Description\nSDP Log\t\n\nMedia Devices\nAPI Support\t\n✔\nTrue\nAudio Permissions\t\n?\nPrompt\nVideo Permissions\t\n?\nPrompt\nMedia Devices\t    kind: audioinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: videoinput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\n    kind: audiooutput\n   label: n/a\ndeviceId: n/a\n groupId: n/a\n\nHow to Disable WebRTC\nFurther Reading\nLeave a Comment (219)\nBrowserLeaks © 2011-2026 All Rights Reserved\nmoc.skaelresworb@tcatnoc:otliam",
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
        "text_excerpt": "Home Page\nIP Address\nJavaScript\nWebRTC Leak Test\nCanvas Fingerprint\nWebGL Report\nFont Fingerprinting\nGeolocation API\nFeatures Detection\nTLS Client Test\nContent Filters\nMore Tools\nSettings\nTLS Client Test\n\nThis page displays your web browser's SSL/TLS capabilities, including supported TLS protocols, cipher suites, extensions, and key exchange groups. It highlights any weak or insecure options and generates a TLS fingerprint in JA3/JA4 formats. Additionally, it tests how your browser handles insecure mixed content requests.\n\nYour Web Browser\nHTTP User-Agent\tMozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/145.0.7632.6 Safari/537.36\nProtocol Support\nTLS 1.3\t\n✔\nEnabled\nTLS 1.2\t\n✔\nEnabled\nTLS 1.1\t\n✖\nDisabled (Good)\nTLS 1.0\t\n✖\nDisabled (Good)\nMixed Content Test\nActive Content\t\n✔\nBlocked\nPassive Content\t\n✔\nUpgraded to HTTPS\nTLS Fingerprint\nJA4\t\nt13d1516h2_8daaf6152771_d8a2da3f94cd\n\nJA4_o\tt13d1516h2_acb858a92679_eff677aa8b5f\nJA3\t38ab6050218fdad967ea1a5b2cffa048\nJA3_n\t8e19337e7524d2573be54efb2b0784c9\nTLS Handshake\ndec values\n\nTLS Protocol\t\n0x0304\nTLS 1.3\n\nCipher Suite\t\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\nKey Exchange\t\n0x11EC\nX25519MLKEM768\n\nSignature Scheme\t\n0x0403\necdsa_secp256r1_sha256\n\nEncrypted Client Hello\nECH Success\t\n✖\nFalse\nOuter SNI\ttls.browserleaks.com\nInner SNI\tn/a\nSupported Cipher Suites (in order as received)\nCipher Suites\t\n0x4A4A\nGREASE\n\n\n0x1301\nTLS_AES_128_GCM_SHA256\nRecommended\nTLS 1.3\n\n\n0x1302\nTLS_AES_256_GCM_SHA384\nRecommended\nTLS 1.3\n\n\n0x1303\nTLS_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.3\n\n\n0xC02B\nTLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02F\nTLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256\nRecommended\nTLS 1.2\n\n\n0xC02C\nTLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xC030\nTLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384\nRecommended\nTLS 1.2\n\n\n0xCCA9\nTLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xCCA8\nTLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256\nRecommended\nTLS 1.2\n\n\n0xC013\nTLS_ECDHE_RSA_WITH_AES_128_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0xC014\nTLS_ECDHE_RSA_WITH_AES_256_CBC_SHA\nCBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x009C\nTLS_RSA_WITH_AES_128_GCM_SHA256\nNO PFS\nTLS 1.2\n\n\n0x009D\nTLS_RSA_WITH_AES_256_GCM_SHA384\nNO PFS\nTLS 1.2\n\n\n0x002F\nTLS_RSA_WITH_AES_128_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\n\n\n0x0035\nTLS_RSA_WITH_AES_256_CBC_SHA\nNO PFS, CBC, SHA-1\nTLS 1.0,1.1,1.2\nSupported TLS Extensions (in order as received)\n\nTLS Extensions\t\n0x3A3A\nGREASE\n\n\n0x002B\nsupported_versions\n\n\n0x002D\npsk_key_exchange_modes\n\n\n0x44CD\napplication_settings\n\n\n0x0010\napplication_layer_protocol_negotiation\n\n\n0x000D\nsignature_algorithms\n\n\n0x0005\nstatus_request\n\n\n0x000B\nec_point_formats\n\n\n0x000A\nsupported_groups\n\n\n0x0017\nextended_main_secret\n\n\n0x0000\nserver_name\n\n\n0x001B\ncompress_certificate\n\n\n0xFE0D\nencrypted_client_hello\n\n\n0x0023\nsession_ticket\n\n\n0xFF01\nrenegotiation_info\n\n\n0x0012\nsigned_certificate_timestamp\n\n\n0x0033\nkey_share\n\n\n0x8A8A\nGREASE\n\napplication_layer_protocol_negotiation\nprotocol_name_list\th2\nhttp/1.1\napplication_settings\nsupported_protocols\th2\ncompress_certificate\nalgorithms\t\n0x0002\nbrotli\n\nec_point_formats\nec_point_format_list\t\n0x0000\nuncompressed\n\nencrypted_client_hello\ntype\touter\nkdf_id\t\n0x0001\nHKDF-SHA256\n\naead_id\t\n0x0001\nAES-128-GCM\n\nconfig_id\t112\nenc_length\t32\npayload_length\t176\nkey_share\nclient_shares\t\n0x6A6A\nGREASE\n\n\n0x11EC\nX25519MLKEM768\n\n\n0x001D\nx25519\n\npsk_key_exchange_modes\nke_modes\t\n0x0001\npsk_dhe_ke\n\nserver_name\nserver_name\ttls.brow",
        "text_excerpt_truncated": true,
        "cdn_headers": {
          "server": "nginx"
        },
        "error": null
      }
    ],
    "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/browserleaks_probe/browserleaks.har",
    "error": null
  },
  "framework": {
    "question_bank_version": "1",
    "test_matrix_version": "1",
    "findings": [
      {
        "id": "finding-yourinfo-5cc89707",
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
        "answer_summary": "Exit IPv4 185.161.202.154; leak flags dns=False webrtc=False ipv6=False.",
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
        "answer_summary": "Disagreement: distinct IPv4 values across echo endpoints: 185.161.202.154, 92.211.2.176.",
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
        "answer_summary": "Exit IPv4 185.161.202.154 for location de-hamburg-hamburg-154.",
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
        "answer_summary": "PTR lookup errors: ptr_v4: The DNS query name does not exist: 154.202.161.185.in-addr.arpa.",
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
        "host": "surface_probe",
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
      "ip": "185.161.202.154",
      "country_code": "DE",
      "region": "Hamburg",
      "city": "Hamburg",
      "connection": {
        "asn": 207137,
        "org": "Packethub S.A.",
        "isp": "Packethub S.A.",
        "domain": "packethub.net"
      },
      "location_id": "de-hamburg-hamburg-154",
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
            "cf-ray": "9ed9b91f6dfe3392-HAM"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b91f6dfe3392"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/3cec43152ba057c5.har",
          "page_type": "pricing"
        },
        {
          "url": "https://my.nordaccount.com/",
          "error": null,
          "status": 200,
          "final_url": "https://my.nordaccount.com/",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed9b9235d8b62d7-HAM"
          },
          "scripts": [
            "https://my.nordaccount.com/assets/runtime.a9c27b97b093c98ae649.js",
            "https://my.nordaccount.com/assets/_formatjs.defaultvendors.ac0846ece32d56901ea4.js",
            "https://my.nordaccount.com/assets/regenerator-runtime.defaultvendors.eb63fbe45c73fab20cc3.js",
            "https://my.nordaccount.com/assets/promise-polyfill.defaultvendors.12b7c8ec7f121d0b5787.js",
            "https://my.nordaccount.com/assets/index.caa7c4317590658d27ac.js",
            "https://my.nordaccount.com/assets/_nordsec.defaultvendors.4c748c7db5cefa2fe8df.chunk.js",
            "https://my.nordaccount.com/assets/date-fns.defaultvendors.eaa415bc21c381d3558b.chunk.js",
            "https://my.nordaccount.com/assets/_nord.defaultvendors.f2b134f66f68507b33fc.chunk.js",
            "https://my.nordaccount.com/assets/tslib.defaultvendors.f240679c709d47693a22.chunk.js",
            "https://my.nordaccount.com/assets/_sentry.defaultvendors.6a26a7e44a35f2381dc2.chunk.js",
            "https://my.nordaccount.com/assets/_sentry-internal.defaultvendors.36f404cb5c3d7ff37a26.chunk.js",
            "https://my.nordaccount.com/assets/graphql.defaultvendors.6196445f71efc38548cd.chunk.js",
            "https://my.nordaccount.com/assets/react-intl.defaultvendors.b71793934bfb99d0b581.chunk.js",
            "https://my.nordaccount.com/assets/graphql-request.defaultvendors.25a38b2f26bc2e06c5ff.chunk.js",
            "https://my.nordaccount.com/assets/_reduxjs.defaultvendors.73708e4220415063788d.chunk.js",
            "https://my.nordaccount.com/assets/react-transition-group.defaultvendors.719b911b91adb7aef00b.chunk.js",
            "https://my.nordaccount.com/assets/uuid.defaultvendors.746a61a183a00afcd19c.chunk.js",
            "https://my.nordaccount.com/assets/_babel.defaultvendors.09ede7e9eaeecef6d984.chunk.js",
            "https://my.nordaccount.com/assets/react.defaultvendors.0015e8b82b057f403937.chunk.js",
            "https://my.nordaccount.com/assets/react-dom.defaultvendors.3a1333ac0f7e30c6efdc.chunk.js",
            "https://my.nordaccount.com/assets/prop-types.defaultvendors.07541a84659c6203c26c.chunk.js",
            "https://my.nordaccount.com/assets/react-toastify.defaultvendors.ff2d3ee8bd32115c5105.chunk.js",
            "https://my.nordaccount.com/assets/dom-helpers.defaultvendors.5f3f39fa4221cfe8e9f3.chunk.js",
            "https://my.nordaccount.com/assets/intl-messageformat.defaultvendors.de9ccecd85bf07c5aa48.chunk.js",
            "https://my.nordaccount.com/assets/use-sync-external-store.defaultvendors.8d091fe6bd55d67df739.chunk.js",
            "https://my.nordaccount.com/assets/scheduler.defaultvendors.db974a7e0f5f400c9542.chunk.js",
            "https://my.nordaccount.com/assets/react-is.defaultvendors.c68f828a892f78334b23.chunk.js",
            "https://my.nordaccount.com/assets/react-inlinesvg.defaultvendors.fde5e082146b4e49cbf9.chunk.js",
            "https://my.nordaccount.com/assets/react-from-dom.defaultvendors.229ce3ff05c6241dc586.chunk.js",
            "https://my.nordaccount.com/assets/react-redux.defaultvendors.fd161b5e1759a70dfe89.chunk.js",
            "https://my.nordaccount.com/assets/js-cookie.defaultvendors.4f558a2177bb0eb5b78d.chunk.js",
            "https://my.nordaccount.com/assets/immer.defaultvendors.0b964b76caa620cff239.chunk.js",
            "https://my.nordaccount.com/assets/clsx.defaultvendors.df823a651876ebf8de25.chunk.js",
            "https://my.nordaccount.com/assets/_standard-schema.defaultvendors.baf6829019a88080d27b.chunk.js",
            "https://my.nordaccount.com/assets/classnames.defaultvendors.c2b96eae94047c76c0ff.chunk.js",
            "https://my.nordaccount.com/assets/react-side-effect.defaultvendors.45faa7f70fa2eebadd6a.chunk.js",
            "https://my.nordaccount.com/assets/react-router.defaultvendors.78aaad2448f5c1b716a5.chunk.js",
            "https://my.nordaccount.com/assets/react-router-dom.defaultvendors.6b7f2f2725b53b198161.chunk.js",
            "https://my.nordaccount.com/assets/react-intersection-observer.defaultvendors.1d2b074be5f45739167d.chunk.js",
            "https://my.nordaccount.com/assets/react-helmet.defaultvendors.84ea08fb735d01e5cbd2.chunk.js",
            "https://my.nordaccount.com/assets/react-fast-compare.defaultvendors.00289033652a15f72cb3.chunk.js",
            "https://my.nordaccount.com/assets/react-content-loader.defaultvendors.c750d7ce2db67f793585.chunk.js",
            "https://my.nordaccount.com/assets/object-assign.defaultvendors.f85101626dd44f58baec.chunk.js",
            "https://my.nordaccount.com/assets/lodash.isequal.defaultvendors.e2b6c1d21e29212d4759.chunk.js",
            "https://my.nordaccount.com/assets/humps.defaultvendors.3754860cfe25e6714b78.chunk.js",
            "https://my.nordaccount.com/assets/hoist-non-react-statics.defaultvendors.79396dd4378902d7beaa.chunk.js",
            "https://my.nordaccount.com/assets/filter-obj.defaultvendors.84146f4c18b1572ac0ba.chunk.js",
            "https://my.nordaccount.com/assets/file-saver.defaultvendors.cc329c95afaf575e4b41.chunk.js",
            "https://my.nordaccount.com/assets/exenv.defaultvendors.a1af14a17940d6080ed3.chunk.js",
            "https://my.nordaccount.com/assets/decode-uri-component.defaultvendors.1e3b43bb5d3c3776b319.chunk.js",
            "https://my.nordaccount.com/assets/cross-fetch.defaultvendors.3e680526e6c07ca51319.chunk.js",
            "https://my.nordaccount.com/assets/strict-uri-encode.defaultvendors.2f8dd77d6309c41de433.chunk.js",
            "https://my.nordaccount.com/assets/split-on-first.defaultvendors.b3f30d1714518afe82db.chunk.js",
            "https://my.nordaccount.com/assets/query-string.defaultvendors.82e833f4af0d00cbde64.chunk.js",
            "https://my.nordaccount.com/assets/_remix-run.defaultvendors.363e94888ab4b4faff10.chunk.js",
            "https://my.nordaccount.com/assets/4666.705e2d0d1330cfd25bc1.chunk.js"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/0096221d6f12d382.har",
          "page_type": "signup"
        },
        {
          "url": "https://nordcheckout.com/",
          "error": null,
          "status": 403,
          "final_url": "https://nordvpn.com/pricing?redirected_from=nordcheckout.com%2F",
          "cdn_headers": {
            "server": "cloudflare",
            "cf-ray": "9ed9b9394a836311-HAM"
          },
          "scripts": [
            "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ed9b9394a836311"
          ],
          "images": [],
          "captcha_third_party": false,
          "har_path": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/5c4416295d131e0b.har",
          "page_type": "checkout"
        }
      ],
      "surface_probe_dir": "runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe",
      "har_summary": {
        "har_files": [
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/3cec43152ba057c5.har",
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
          },
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/0096221d6f12d382.har",
            "entry_count": 60,
            "unique_hosts": [
              "my.nordaccount.com"
            ],
            "unique_schemes": [
              "https"
            ],
            "tracker_candidates": [],
            "cdn_candidates": [],
            "error": null
          },
          {
            "har_path": "/Users/alauder/Source/doxx/vpn-leaks/runs/nordvpn-20260417T072634Z-607907b5/raw/de-hamburg-hamburg-154/surface_probe/har/5c4416295d131e0b.har",
            "entry_count": 5,
            "unique_hosts": [
              "nordcheckout.com",
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
          "my.nordaccount.com",
          "nordcheckout.com",
          "nordvpn.com"
        ],
        "merged_tracker_candidates": [],
        "merged_cdn_candidates": []
      }
    }
  }
}
```

---



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`