# VPN Leaks project spec

_As of 2026-04-09 (America/Los_Angeles). Repo target: entity["company","GitHub","code hosting platform"]._

## Background and goals

doxxnet’s bar for privacy is not “we have a policy,” it’s “we can point to every realistic leak path and show it’s blocked or minimized.” This project, **VPN Leaks**, is a repeatable benchmarking harness that signs up for competitor VPN services (paid accounts), connects through every available location, and records what information is exposed through common leak vectors and through underlying infrastructure attribution.

The core outputs are:
1) a per‑VPN provider report (what leaks, where, under what conditions), and  
2) a per‑underlying network/provider report (who appears to operate the exit IP space and what their policies say about logging/retention).

This scope explicitly focuses on **privacy exposure observable from the client side**. It does not try to “prove” what a VPN logs internally (you generally cannot measure that directly), but it does map what third parties can observe and what underlay providers claim in their published terms.

## Scope and threat model

### What “leaks” means for this project

A “leak” is any situation where traffic or metadata that a user expects to be confined to the VPN tunnel is instead exposed to a third party (often the local ISP, a Wi‑Fi operator, or a DNS resolver), or where identifying metadata is exposed in a way that materially weakens anonymity.

The practical categories you should track:

**Network path leaks**
- **Public IP exposure**: does any traffic ever egress with the user’s real ISP IP during connect, steady state, network transitions, or disconnect (kill-switch behavior).
- **DNS leaks**: DNS queries going outside the VPN tunnel to non‑VPN resolvers (or being transparently proxied by an ISP). DNSLeaktest.com describes DNS leak testing as determining whether DNS requests are being leaked, and notes cases like transparent DNS proxying. citeturn0search2turn0search13  
  IPLeak.net’s DNS leak explainer is also useful because it calls out OS behavior (notably Windows per-interface DNS handling) as a cause of DNS queries escaping the VPN tunnel. citeturn0search1
- **IPv6 leaks**: IPv6 traffic bypassing the tunnel when only IPv4 is tunneled or filtering is incomplete. An easy external check is test‑ipv6.com, which explicitly tests IPv6 readiness and shows your current IPv4 and IPv6 addresses. citeturn5search3
- **WebRTC leaks**: WebRTC can reveal IP address candidates via ICE/STUN behavior; BrowserLeaks’ WebRTC test is designed to show “WebRTC IP” exposure. citeturn0search0  
  At the protocol level, STUN can be used by an endpoint to determine the IP/port allocated by NAT, and ICE is a NAT traversal framework that uses STUN/TURN. citeturn3search2turn3search3

**Application and browser fingerprinting signals (not strictly “VPN leaks,” but critical privacy exposure)**
- Even with a clean VPN tunnel, a user can be tracked via browser/device fingerprinting. The entity["organization","Electronic Frontier Foundation","digital rights nonprofit"]’s Cover Your Tracks test is explicitly about showing how uniquely identifiable a browser is to trackers. citeturn2search4  
- AmIUnique describes fingerprinting as systematic collection of device/browser attributes for identification. citeturn2search1  
- BrowserLeaks also includes tests that expose client TLS capabilities and generates JA3/JA4 fingerprints (useful to understand “how unique is this client,” especially when automation is involved). citeturn2search3

**Underlay exposure (what third parties can infer from exit IPs)**
- Map exit IPs to ASN/organization, then to likely hosting or transit providers. Use authoritative network intelligence sources like RIPEstat Data API (RIPE NCC) and Team Cymru’s IP→ASN mapping. citeturn1search12turn1search1  
- Use PeeringDB to enrich “who/where” with interconnection context; PeeringDB describes itself as a user‑maintained database of networks and interconnection data. citeturn1search14  
- For offline enrichment, MaxMind’s GeoLite ASN database includes fields for ASN number and ASN organization. citeturn1search15

### What “data privacy handling procedures” means here

For this project, “privacy handling procedures” are captured as:
- **Observed behaviors** (leak tests + packet captures where appropriate).
- **Documented claims** (VPN provider privacy policy + underlay provider privacy policy / acceptable use clauses).
- **Underlay risk context** (whether the exit IP belongs to a third-party datacenter ASN, and what that datacenter says about logs/retention).

A key motivation is that network operators can retain flow metadata like source/destination addresses and byte counts. Cisco describes NetFlow as operational data/statistics collection on packets/flows, and the IETF’s IPFIX spec (RFC 7011) defines Flow Records that include measured properties (e.g., bytes) and characteristic properties (e.g., source IP address). citeturn3search0turn3search1  
You usually cannot force a provider to disclose their exact retention, but you can systematically collect and summarize what they publicly state.

## Measurement methodology

### Standardized run loop

This project’s “one location run” should follow a deterministic sequence so results are comparable across VPNs and across time:

1) **Account ready**: user has a paid plan and credentials (manual + stored in secrets manager; automation optional and fragile).
2) **Connect**: establish tunnel using either the vendor client or a standard config (WireGuard/OpenVPN config file).
3) **Stabilize and verify routing**: confirm default route through tunnel and record local interfaces.
4) **Exit IP capture**: query multiple independent “what is my IP” endpoints and store results (to reduce dependence on one service). ipify documents plain-text and JSON public IP retrieval. citeturn5search0
5) **Leak test suite**:
   - DNS leak detection (external + local)
   - WebRTC leak detection (browser-based)
   - IPv6 leak detection (external + local)
   - Fingerprinting exposure snapshot (browser-based, optional but recommended)
6) **Underlay attribution**:
   - Map exit IP to ASN/holder via RIPEstat Data API. citeturn1search12turn1search4
   - Cross-check via Team Cymru. Note: Team Cymru explicitly warns that some “peer/upstream” inference is imperfect, so store confidence and avoid overstating conclusions. citeturn1search1
   - Enrich with PeeringDB and (optionally) offline ASN DB like GeoLite ASN. citeturn1search14turn1search15
7) **Policy capture**:
   - Fetch and store privacy policies for: (a) the VPN provider, and (b) the attributed ASN org / datacenter / transit ISP when relevant.
8) **Disconnect + reset**: ensure traffic is back on baseline network; flush DNS caches; close browsers; snapshot logs.
9) **Repeat for all locations** for that VPN provider.

### Leak test resources to integrate

The process should support both **external web tests** (good for realism) and **local deterministic tests** (good for automation and stability).

Primary web-based resources you should wire in:

- entity["organization","BrowserLeaks","privacy leak test website"]: suite of browser privacy tests including WebRTC leak testing and TLS client fingerprint display. citeturn2search7turn2search3  
- entity["organization","IPLeak.net","vpn leak test website"]: explicitly defines DNS leaks as unencrypted DNS queries sent outside the VPN tunnel and discusses Windows DNS behavior as a cause. citeturn0search1  
- entity["organization","DNSLeaktest.com","dns leak test website"]: documents DNS leak test behavior (standard vs extended) and how the test drives your client to resolve domains, revealing DNS servers involved. citeturn0search6  
- entity["organization","test-ipv6.com","ipv6 connectivity test website"]: tests IPv6 connectivity/readiness and shows IPv4/IPv6 addresses. citeturn5search3  
- entity["organization","Mullvad","vpn service provider"] connection check: explicitly positioned as a tool to verify VPN usage and check for DNS and WebRTC leaks (useful as a cross-check, even if you are not using Mullvad). citeturn4search0turn4search7  
- entity["company","Proton VPN","vpn service provider"] documentation provides a structured explanation of DNS leak scenarios and emphasizes built-in DNS leak protection (useful as an example of what vendor docs claim vs what you measure). citeturn4search1turn4search9

Recommended deterministic local checks to add (automation-friendly):
- DNS resolver identification via system configuration and controlled DNS queries; complement with external DNS leak tests because some leaks are context-specific (e.g., OS services bypassing expected routes). citeturn0search1turn4search14
- IPv6 presence checks via `curl -6` to known IPv6 endpoints and comparing reported IP/ASN to expected tunnel behavior; then validate with external IPv6 testing. citeturn5search3
- WebRTC IP candidate extraction via scripted browser session; you can justify this as grounded in WebRTC using ICE/STUN for NAT traversal. citeturn3search2turn3search3turn0search0

### Underlay attribution resources

For each exit IP, store both raw and enriched attribution:

- entity["organization","RIPE NCC","regional internet registry"] RIPEstat Data API: a public data interface; use endpoints like prefix overview and AS overview to capture originating ASN and holder metadata. citeturn1search12turn1search0turn1search4  
- entity["organization","Team Cymru","internet security organization"] IP→ASN mapping: fast cross-check; store disclaimers about uncertainty and treat upstream inference as “best effort.” citeturn1search1turn1search5  
- entity["organization","PeeringDB","interconnection database project"]: enrich ASNs with interconnection/facility context (user-maintained, so treat as advisory). citeturn1search14turn1search10  
- entity["company","MaxMind","ip data and geolocation company"] GeoLite ASN: offline ASN/org enrichment with explicit ASN/org fields. citeturn1search15turn1search19

## Automation architecture and agent design

### Repository layout

The repo should be designed so you can add a new VPN provider by dropping in a config file and (optionally) an adapter, then rerunning the harness only for that provider.

Proposed layout:

```text
README.md

docs/
  spec.md
  methodology.md
  data-dictionary.md

configs/
  vpns/
    <vpn_slug>.yaml
  locations/
    <vpn_slug>.locations.yaml   # optional cache of location list
  tools/
    leak-tests.yaml             # which tests run + parameters
    attribution.yaml            # RIPEstat/TeamCymru/PeeringDB settings

runs/
  <run_id>/
    raw/
      connect.log
      ip-check.json
      dnsleak/
      webrtc/
      ipv6/
      fingerprint/
      pcap/                     # optional, gated
      attribution.json
      policy/
        vpn_policy.html
        underlay_policy.html
    normalized.json
    summary.md

VPNs/
  <VPN_COMPANY>.md

PROVIDERS/
  <UNDERLYING_PROVIDER>.md

scripts/
  vpn_leaks.py                  # main CLI orchestrator
  adapters/
    <vpn_slug>.py               # optional provider-specific glue
  tests/
    ip_check.py
    dns.py
    ipv6.py
    webrtc.py
    fingerprint.py
  attribution/
    ripestat.py
    cymru.py
    peeringdb.py
    geolite_asn.py
  policy/
    fetch_policy.py
    summarize_policy.py
  reporting/
    generate_reports.py
    templates/
      vpn_report.md.j2
      provider_report.md.j2

.github/
  workflows/
    ci.yml
```

### Data model

A single “location run” should produce `normalized.json` that is stable across VPN providers. Keep it append-only to avoid breaking older runs.

Minimum fields:
- `run_id`, `timestamp_utc`, `runner_env` (os, kernel, browser, vpn_protocol), `vpn_provider`, `vpn_location_id`, `vpn_location_label`
- `exit_ip_v4`, `exit_ip_v6` (if present), `exit_ip_sources` (list of endpoints queried)
- `dns_servers_observed` (from external test + local inference), plus a `dns_leak_flag`
- `webrtc_candidates` (IPs shown), plus a `webrtc_leak_flag`
- `ipv6_status` (supported, tunneled, blocked), plus an `ipv6_leak_flag`
- `fingerprint_snapshot` (anonymous summary only; do not store unnecessary high-entropy identifiers unless you need them)
- `attribution`: ASN, holder/org, country, confidence, supporting sources
- `policies`: captured URLs + hashes + fetch timestamp + extracted retention/logging claims
- `artifacts`: paths for saved HTML/screenshots/pcaps

### Agent roles for an AI build-out

This project benefits from separate “build agents” with crisp inputs/outputs. The goal is that you can hand these prompts to codex/Claude Code/Cursor and get parallel progress.

**Orchestrator Agent**
- Builds `vpn_leaks.py` CLI and the run state machine.
- Must implement idempotent reruns, resumable runs, and “run only new VPN providers.”
- Output: CLI docs in `README.md`, and structured logs.

**VPN Adapter Agent**
- For each VPN provider, builds an adapter that can:
  - install/configure client (or consume OpenVPN/WireGuard configs)
  - enumerate locations (API scrape if allowed; otherwise parse vendor-provided lists)
  - connect/disconnect reliably and expose “connected location” status
- Output: `scripts/adapters/<vpn_slug>.py` plus `configs/vpns/<vpn_slug>.yaml`.

**Leak Test Agent**
- Implements modules for:
  - IP check (multi-source)
  - DNS leak test capture (external + local)
  - IPv6 checks (local + external)
  - WebRTC leak automation (Playwright/Selenium)
  - Fingerprint snapshot (optional, but recommended)
- Must collect raw outputs and normalized flags, and keep evidence artifacts.
- Grounding: the project should treat WebRTC/STUN/ICE behavior as a first-class leak vector. citeturn3search2turn3search3turn0search0  
- Output: `scripts/tests/*`.

**Attribution Agent**
- Implements IP→ASN holder mapping with:
  - RIPEstat queries as primary (API endpoints documented by RIPE NCC). citeturn1search12turn1search0
  - Team Cymru cross-check. citeturn1search5turn1search1
  - PeeringDB enrichment + offline GeoLite ASN option. citeturn1search14turn1search15
- Must output a confidence score and short explanation per run.

**Policy Agent**
- Fetches privacy policies for:
  - VPN provider
  - underlay org (ASN holder / datacenter)
- Extracts and summarizes key clauses:
  - categories collected
  - retention windows
  - sharing/third parties
  - law enforcement language
  - telemetry/diagnostics clauses
- Must store raw HTML + a content hash so you can detect policy changes over time.

**Reporting Agent**
- Generates:
  - `VPNs/<VPN_COMPANY>.md` from all runs for that VPN
  - `PROVIDERS/<UNDERLYING_PROVIDER>.md` aggregating across all VPNs that used that underlay org
  - rollups in `README.md` (high-level scorecard)
- Must clearly separate:
  - observed results vs inferred attribution vs policy claims.

### Automation boundaries

Some steps will remain manual or semi-automated:
- **Signup/payment**: realistic, but brittle to automate and often hostile to automation. Treat as manual by default with an option to use a headless browser runner if you explicitly decide the ToS risk is acceptable.
- **2FA/CAPTCHAs**: assume manual.
- **Vendor GUI clients**: automating GUI reliably across OS versions is painful; prefer config-based connections when possible.

## Reporting and deliverables

### Markdown file expectations

Each VPN provider report in `VPNs/<VPN_COMPANY>.md` should include:
- Tested protocols (client app, OpenVPN, WireGuard), OS/browser matrix, and exact test date range.
- Location coverage (what percentage of locations tested, with reasons for omissions).
- Leak findings:
  - DNS leak cases and conditions
  - IPv6 behavior (tunneled, blocked, leaking)
  - WebRTC exposure results
  - Kill-switch/transition findings (if tested)
- Underlay summary:
  - top ASNs/orgs observed across locations
  - concentration risk (e.g., “70% of locations appear to exit via a single datacenter org”)
- Appendix: links to run artifacts and hashes.

Each underlying provider report in `PROVIDERS/<UNDERLYING_PROVIDER>.md` should include:
- Evidence that ties exit IPs to the org (ASN holder data, RIPEstat/Team Cymru output).
- Policy summary and change tracking (hashes over time).
- Risk notes grounded in flow-record reality (NetFlow/IPFIX can capture metadata like source IP and byte counts). citeturn3search0turn3search1

### Definition of done

MVP is complete when:
- You can add a new VPN provider by creating one YAML config + (if needed) one adapter, then run only that provider.
- For a single provider, the harness can iterate all locations (or a defined subset) and produce:
  - normalized JSON per location run
  - a per-VPN markdown report
  - per-underlay provider markdown reports
- The test suite includes, at minimum, exit IP capture, DNS leak detection, IPv6 checks, WebRTC leak checks, and underlay ASN attribution. citeturn0search1turn5search3turn0search0turn1search12

## Operational considerations and guardrails

### Legal, ToS, and ethics

This project should stay in “consumer-side measurement” territory:
- Only test services you have paid access to.
- Do not attempt to bypass access controls, exploit vulnerabilities, or load-test infrastructure.
- Treat automated signups and scraping of vendor APIs as a ToS-risk decision; make it an explicit opt-in.

### Security of credentials and test artifacts

- Do not store VPN credentials in the repo. Use local environment variables, an encrypted secrets store, or CI secrets.
- Be careful with packet captures: even test traffic can include sensitive tokens if you use real accounts. Default to **pcap off**, and gate it behind a flag.
- Expect that third-party leak-test sites log what they receive (your exit IP, user agent, and whatever the page collects). That’s fine for benchmarking, but record which services were contacted so you can reason about data exposure.

### Reproducibility and bias control

- Run tests in an isolated environment (dedicated VM or network namespace), with a clean baseline snapshot per provider/location.
- Record versions (OS, kernel, browser, VPN client) because leak behavior can change with OS updates.
- Prefer multi-source checks (multiple IP endpoints; multiple attribution sources). Team Cymru explicitly notes limitations in some inference approaches, so treat disagreement as a signal and preserve both results. citeturn1search1turn5search0

### Notes on diagnosing “network provider metadata” risk

When you document underlay provider risk, keep claims precise:
- It’s accurate to say that flow monitoring standards like IPFIX define flow records that can include source IP and byte counts. citeturn3search1  
- It’s accurate that NetFlow is used for operational monitoring/statistics on flows through routers. citeturn3search0  
- It is **not** accurate to claim a specific ASN “definitely retains netflow” unless their policy explicitly says so. That’s why the policy capture step is a first-class deliverable.

