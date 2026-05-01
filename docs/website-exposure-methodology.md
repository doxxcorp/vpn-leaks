# Website Third-Party Exposure Analysis

A step-by-step methodology for measuring how many companies receive user
data when someone visits a VPN provider's website -- and how many more
are embedded in the provider's DNS, email, and platform infrastructure.
This complements the automated harness (`vpn-leaks run`) with manual desk
research that feeds the **S** (systematic) and **I** (inference) evidence
tiers described in
[research-questions-and-evidence.md](research-questions-and-evidence.md).

The analysis has two layers:

1. **Website surface** (Phases 1-7) - what happens when a browser loads
   the page.
2. **DNS infrastructure** (Phase 8) - who operates DNS, email, and
   platform services for the provider's domains. This reveals companies
   the user never sees but that handle their data.

**Relevant SPEC questions (by evidence tier — see
[`configs/framework/questions.yaml`](../configs/framework/questions.yaml)):**

- **Observed (O) — harness:** Phases **1–7** align with `competitor_probe` /
  `surface_urls` outputs (e.g. `har_summary.json`, `web_probes.json`,
  `provider_dns.json`) for **WEB-001**, **WEB-004**, **WEB-008**,
  **SIGNUP-001**, **SIGNUP-004**, **SIGNUP-010**, **THIRDWEB-001**,
  **THIRDWEB-003**, **THIRDWEB-012**, **CTRL-009**, **FP-001**, **FP-011**
  (site / page context).
- **Desk (S) — Phases 8–9 in this doc:** Provider **apex / email / platform**
  DNS (MX, SPF, DMARC, DKIM, TXT, CNAME chains) supports **WEB-001** /
  **WEB-004** context (who terminates TLS, who sends mail, SaaS on-domain) and
  supplemental “supply chain” reasoning. It does **not** answer **DNS-001**
  (*which resolvers are used **while connected*** — that is **`dnsleak/`** and
  `normalized.dns_servers_observed`, **O**). For **DNS-011** (*first-party vs
  third-party resolvers* in the SPEC sense), use resolver IP attribution from
  the harness; Phase 8 here describes **third parties in the provider’s
  authoritative and email stack**, which is a **different** question — label
  **S** and do not merge with client **O** without explanation
  ([research-questions-and-evidence.md](research-questions-and-evidence.md) §A.1).
- **VPN exit org:** **EXIT-003** (*organization that owns the **VPN exit** IP
  range*) comes from **`attribution.json` (O)**. WHOIS on **marketing site** or
  CDN IPs in this methodology supports **web / infra** questions, not EXIT-003.
- **CTRL-004** (*telemetry endpoints during **VPN connection***): page HARs show
  **web-session** beacons only; **app** connection telemetry is out of scope
  here (see TELEM-* in the framework).
- **Inference (I):** **LOG-001**, **LOG-005** — enumerate parties who *could*
  see traffic or mail; not proof of retention or logging.

---

## 1. Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| `curl` | Fetch raw HTML | Ships with macOS/Linux |
| `dig` | DNS resolution | Ships with macOS/Linux (`dnsutils` on Debian) |
| `whois` | IP ownership lookup | Ships with macOS (`whois` on Debian) |
| Chromium-based browser | Bypass Cloudflare challenges, capture network tab | Playwright (`pip install playwright && playwright install chromium`) or a local browser |
| `jq` (optional) | Parse JSON outputs | `brew install jq` / `apt install jq` |

---

## 2. Workflow overview

```
Target URL
    |
    v
[Phase 1] Fetch page (curl or browser)
    |
    v
[Phase 2] Extract all external URLs and resource imports
    |
    v
[Phase 3] Deduplicate hostnames
    |
    v
[Phase 4] DNS-resolve every hostname
    |
    v
[Phase 5] WHOIS / ASN lookup on each IP
    |
    v
[Phase 6] Classify by company and purpose
    |
    v
[Phase 7] Document findings (evidence tier S)
    |
    v
[Phase 8] DNS infrastructure audit (NS, MX, SPF, TXT, DMARC, DKIM)
    |         -- exposes the full platform supply chain
    v
[Phase 9] Compile total third-party inventory
```

---

## 3. Phase 1 - Fetch the page

### 3a. Try curl first

```bash
curl -sL \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' \
  -H 'Accept: text/html,application/xhtml+xml' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  --max-time 20 \
  'https://www.nordvpn.com' -o /tmp/target.html

wc -c /tmp/target.html
```

If the response is under ~10KB and contains `challenge-platform` or
`Just a moment`, the site is behind Cloudflare bot protection. Move to
3b.

### 3b. Use a browser (Playwright or DevTools)

Many VPN provider sites use aggressive bot protection. Two approaches:

**Option A - Browser DevTools (manual)**

1. Open the target URL in Chrome/Edge/Firefox.
2. Open DevTools (F12) -> Network tab.
3. Reload the page.
4. Wait for full load (watch the waterfall finish).
5. Right-click the network list -> "Save all as HAR with content."
6. Copy the HAR file to `runs/` or a scratch directory.

**Option B - Playwright (scripted)**

The harness already does this. Use `surface_urls` in your provider YAML:

```yaml
surface_urls:
  - page_type: home
    url: "https://www.nordvpn.com/"
  - page_type: pricing
    url: "https://nordvpn.com/pricing/"
  - page_type: signup
    url: "https://my.nordaccount.com/"
```

Then run:

```bash
vpn-leaks run --provider nordvpn --skip-vpn --force
```

The harness stores Playwright HARs under
`runs/<run_id>/raw/<location>/surface_probe/har/` and a probe summary at
`surface_probe/web_probes.json`.

**Option C - Cursor IDE browser MCP (interactive)**

If you have the `cursor-ide-browser` MCP available:

1. Navigate: `browser_navigate` to the target URL.
2. Wait for load, then `browser_snapshot` to confirm content rendered.
3. Use `browser_network_requests` to get every request the page made.

This is the most reliable method for Cloudflare-protected pages because
the Cursor browser handles challenges automatically.

---

## 4. Phase 2 - Extract URLs and resource imports

### From a HAR file

```bash
jq -r '.log.entries[].request.url' /path/to/file.har | sort -u
```

### From browser network requests (MCP output)

The `browser_network_requests` tool returns JSON with `url`, `method`,
`resourceType`, and `statusCode` per request. Group by `resourceType`:

| resourceType | What it captures |
|--------------|-----------------|
| `document` | The HTML page itself |
| `stylesheet` | CSS files |
| `script` | JavaScript files |
| `image` | Images, SVGs, favicons |
| `font` | Web fonts |
| `xhr` / `fetch` | API calls, analytics beacons |
| `ping` | Tracking pixels, sendBeacon() |
| `websocket` | Live connections |
| `media` | Video/audio |

### From raw HTML (curl succeeded)

```bash
# Extract src= and href= attribute values
grep -oP '(?:src|href)="[^"]*"' /tmp/target.html \
  | sed 's/^[^"]*"//;s/"$//' \
  | sort -u
```

### What to capture

For each URL, record:

- **Full URL**
- **Resource type** (script, stylesheet, image, font, xhr, ping)
- **HTTP method** (GET vs POST -- POST usually means data is being sent)
- **Response status** (200, 204, 302, etc.)

---

## 5. Phase 3 - Deduplicate hostnames

Extract unique hostnames from the URL list:

```bash
# From a saved URL list
sed 's|https\?://||;s|/.*||' urls.txt | sort -u > hostnames.txt
```

Or from a HAR:

```bash
jq -r '.log.entries[].request.url' file.har \
  | sed 's|https\?://||;s|/.*||' \
  | sort -u > hostnames.txt
```

---

## 6. Phase 4 - DNS resolution

Resolve every hostname to IP addresses:

```bash
while read host; do
  echo "=== $host ==="
  dig +short "$host"
  echo ""
done < hostnames.txt | tee dns-results.txt
```

For a structured output:

```bash
while read host; do
  ips=$(dig +short "$host" | tr '\n' ',')
  echo "$host -> $ips"
done < hostnames.txt | tee dns-structured.txt
```

**Record the date.** DNS changes; results are only valid for the session.

---

## 7. Phase 5 - WHOIS / hosting identification

For each unique IP, identify the hosting organization:

```bash
# Extract unique IPs from Phase 4
grep -oP '\d+\.\d+\.\d+\.\d+' dns-results.txt | sort -u > ips.txt

# WHOIS each IP
while read ip; do
  echo "=== $ip ==="
  whois "$ip" 2>/dev/null \
    | grep -iE '^(OrgName|Organization|NetName|netname|descr|owner):' \
    | head -3
  echo ""
done < ips.txt | tee whois-results.txt
```

**Key WHOIS fields:**

| Field | Meaning |
|-------|---------|
| `OrgName` / `Organization` | Company that owns the IP block |
| `NetName` | Network allocation name |
| `Country` | Registered country of the block |
| `descr` | Description (RIPE/APNIC style) |

### Common hosting providers by IP range

| IP prefix | Provider |
|-----------|----------|
| `104.16.x.x` - `104.31.x.x` | Cloudflare |
| `172.64.x.x` - `172.71.x.x` | Cloudflare |
| `151.101.x.x` | Fastly |
| `13.x.x.x`, `52.x.x.x`, `54.x.x.x` | AWS |
| `13.224.x.x` - `13.227.x.x` | AWS CloudFront |
| `172.217.x.x`, `142.250.x.x` | Google |
| `20.x.x.x`, `40.x.x.x` | Microsoft Azure |
| `76.223.x.x`, `99.83.x.x` | AWS Global Accelerator |
| `216.150.x.x` | Vercel |

---

## 8. Phase 6 - Classify by company and purpose

Build a table mapping each hostname to its owning company, the data it
receives, and the privacy risk level:

### Classification template

| Hostname | IPs | Owner | Role | Data received | Risk |
|----------|-----|-------|------|--------------|------|
| `nordvpn.com` | 104.19.x | Cloudflare (proxy) / Nord Security (origin) | Main site | Full page load, IP, UA, referrer | First-party |
| `www.googletagmanager.com` | 172.217.x | Google LLC | Analytics tag manager | IP, page URL, browser fingerprint, referrer | **Third-party tracker** |
| `stats.g.doubleclick.net` | 172.217.x | Google LLC | Ad network beacon | IP, GA client ID, cross-site correlation | **Third-party ad tracker** |
| `browser.sentry-cdn.com` | 151.101.x | Fastly (CDN) / Sentry (code) | Error tracking SDK | IP (fetch only), JS execution context | Third-party SDK |
| `s1.nordcdn.com` | 104.16.x | Cloudflare / Nord | CDN | IP, request headers | First-party CDN |

### Risk categories

| Category | Description | Example |
|----------|-------------|---------|
| **First-party** | Provider's own infrastructure | `nordvpn.com`, `nordcdn.com` |
| **First-party CDN** | Provider-branded but CDN-hosted | `s1.nordcdn.com` via Cloudflare |
| **Infrastructure proxy** | CDN/WAF that terminates TLS | Cloudflare sitting in front of origin |
| **Third-party analytics** | Tracking/measurement service | Google Analytics, Mixpanel |
| **Third-party ad tracker** | Cross-site ad correlation | DoubleClick, Facebook Pixel |
| **Third-party SDK** | Error/performance monitoring | Sentry, Datadog RUM |
| **Third-party consent** | Cookie consent platform | OneTrust, Cookiebot |
| **Third-party font/asset** | External font or asset CDN | Google Fonts, Typekit |

### Key questions to answer

1. **How many distinct companies receive the visitor's IP address?**
   Count unique organizations from WHOIS results. Include CDN/WAF
   providers since they terminate TLS.

2. **Which companies can correlate this visit with other sites?**
   Any third-party with cross-site cookies or identifiers (Google
   Analytics, DoubleClick, Facebook Pixel).

3. **Is the TLS-terminating proxy the same company as the VPN provider?**
   If Cloudflare terminates TLS, they see request/response content in
   the clear. This is standard but worth documenting.

4. **Are there POST requests or tracking beacons?**
   POST to analytics endpoints means data is actively being sent, not
   just passively loaded.

5. **Does the provider proxy analytics through their own domain?**
   Some providers (like NordVPN with `cm.nordvpn.com` for GA) proxy
   analytics to reduce third-party exposure in browser privacy tools.
   The data still reaches Google, but the browser does not make a
   direct cross-origin request.

---

## 9. Phase 7 - Document findings

### File naming

Save results under `research/` in the repo or inline in a report
appendix:

```
research/
  web-exposure-<provider>-<YYYY-MM-DD>.md
  dns-<provider>-<YYYY-MM-DD>.txt
  whois-<provider>-<YYYY-MM-DD>.txt
```

### Required metadata

Every write-up must include:

- **Date (UTC)** of the analysis
- **Source URL(s)** tested
- **Method** (curl, browser DevTools, Playwright, MCP browser)
- **Resolver used** for DNS (system default, `1.1.1.1`, `8.8.8.8`, etc.)
- **Location** of the tester (results differ by geography/CDN POP)

### Output format

```markdown
## Web Exposure Analysis: NordVPN
**Date:** 2026-04-16 UTC
**Target:** https://www.nordvpn.com
**Method:** Cursor IDE browser (MCP), network requests capture
**DNS resolver:** system default (CenturyLink residential)
**Tester location:** US-West

### Companies contacted on page load (no interaction)

| # | Company | Hostnames | Purpose |
|---|---------|-----------|---------|
| 1 | Nord Security | nordvpn.com, *.nordcdn.com, ... | Site + CDN + API |
| 2 | Cloudflare | (reverse proxy for above) | TLS termination |
| 3 | Google | googletagmanager.com, doubleclick.net | Analytics + ads |
| 4 | Fastly | browser.sentry-cdn.com | CDN for Sentry SDK |
| 5 | Sentry | (JS runs locally) | Error tracking |

### Summary
5 companies receive user data from a single page load.
Google's DoubleClick enables cross-site ad correlation.
```

---

## 10. Mapping to the harness

The manual workflow above produces **S-tier evidence**. Here is how each
phase maps to automated harness features:

| Manual phase | Harness equivalent | Config / flag |
|-------------|-------------------|---------------|
| Fetch page | `surface_probe` (Playwright HAR) | `surface_urls` in provider YAML |
| Extract URLs | `har_summary.py` (auto-classifies tracker/CDN hosts) | Runs automatically on `competitor_probe` HARs |
| DNS resolution | `competitor_probes.run_provider_dns()` | `competitor_probe.provider_domains` in YAML |
| WHOIS / ASN | `attribution/merge.py` (RIPEstat + Cymru + PeeringDB) | `configs/tools/attribution.yaml` |
| Classify hosts | `framework/endpoints.py` + `classification_rules.yaml` | Auto during `--no-framework` is off |
| DNS audit (NS/MX/SPF/TXT) | `competitor_probes.run_provider_dns()` (NS, A, AAAA, TXT, MX, CAA + glue attribution) | `competitor_probe.provider_domains` in YAML |
| Phase 8–9 desk bundle | `website_exposure_methodology` in `vpn-leaks run` ([`vpn_leaks/checks/website_exposure_methodology.py`](../vpn_leaks/checks/website_exposure_methodology.py)) | **Requires** apex domains via `competitor_probe.provider_domains` (and HAR/surface hosts benefit inventory); output in `normalized.json` + `raw/.../website_exposure/` |
| PCAP-derived remotes / SNI / DNS (competitive runs) | `pcap_derived` after `run --attach-capture` or `vpn-leaks pcap-summarize` | See [competitive-capture-playbook.md](competitive-capture-playbook.md) |
| Document | `vpn-leaks report --provider <slug>` | Generates `VPNs/<SLUG>.md` + `.html` (methodology + PCAP subsection when present) |

**Automation vs manual residual:** The run pipeline now projects **Phases 1–7** (host/DNS/classification hints from HAR + resolver samples) and **Phase 8** (SPF walk, DMARC parse, DKIM selector probes, bounded subdomain CNAME scan, TXT token extraction where applicable) and **Phase 9** (unified third-party inventory with provenance) into **`website_exposure_methodology`**, fail-soft per phase. Gaps (`limits`, resolver timeouts, **`permerror`** SPF, absent selectors) remain explicit in JSON—repeat or extend with **manual** transcript + [scripts/desk_dns_audit.sh](scripts/desk_dns_audit.sh) / [research/desk-exposure-template.md](research/desk-exposure-template.md) when you need narrative-only evidence tiers.

### Adding a new provider

1. Copy `configs/vpns/example.yaml` to `configs/vpns/<slug>.yaml`.
2. Fill in `provider_domains`, `probe_urls`, `portal_hosts`, and
   `surface_urls` using the hostnames you discovered manually.
3. Run: `vpn-leaks run --provider <slug> --skip-vpn --force`
4. Report: `vpn-leaks report --provider <slug>`

---

## 11. Repeating for subpages

The homepage is the minimum. For a thorough analysis, repeat Phases 1-6
on these additional pages:

| Page type | Why it matters |
|-----------|---------------|
| **Pricing** (`/pricing/`) | May load payment processor scripts (Stripe, Braintree) |
| **Signup / account creation** | Reveals authentication third parties (Auth0, Okta) |
| **Checkout** | Payment processor, fraud detection (reCAPTCHA, Forter) |
| **Login portal** (`my.nordaccount.com`) | Control plane CDN, session management |
| **Download page** | May load platform-detection scripts, app store redirects |
| **Support / help center** | Often a separate SaaS (Zendesk, Intercom) with its own trackers |
| **Blog** | Frequently has more aggressive ad/analytics than the main site |

The harness supports this via `surface_urls` in the provider YAML:

```yaml
surface_urls:
  - page_type: home
    url: "https://www.nordvpn.com/"
  - page_type: pricing
    url: "https://nordvpn.com/pricing/"
  - page_type: signup
    url: "https://my.nordaccount.com/"
  - page_type: checkout
    url: "https://nordcheckout.com/"
  - page_type: support
    url: "https://support.nordvpn.com/"
  - page_type: blog
    url: "https://nordvpn.com/blog/"
```

---

## 12. Interpreting results

### What counts as "exposure"?

A company receives exposure when any of the following occur during a page
load:

- **TLS termination** - CDN/WAF sees plaintext request and response
- **Script execution** - JS from their domain runs in the user's browser
- **Resource fetch** - Browser sends IP + headers to their server
- **Beacon/pixel** - Data actively pushed via POST, sendBeacon, or img pixel
- **Cookie set** - Their domain sets or reads a cookie (first or third-party)

### What does NOT count

- **Same-origin subdomains** that resolve to the provider's own IPs
  (though the CDN in front still counts separately)
- **DNS resolution** (the user's resolver sees the hostname, but the
  target server does not receive the request unless the browser fetches it)

### The irony metric

For a VPN provider selling privacy, the key finding is:

> How many companies that the user did NOT choose to interact with receive
> their IP address, browser fingerprint, or behavioral data simply by
> visiting the provider's marketing page?

Document this as a single number with a breakdown. It is the most
impactful summary for reports.

---

## 13. Phase 8 - DNS infrastructure audit

The website surface (Phases 1-7) only captures what the **browser** does.
The provider's DNS records reveal the full platform supply chain: who
runs their nameservers, who handles their email, what SaaS platforms have
verified domain ownership, and whether they even support IPv6.

### 13a. Record types to query

Run all of these against the provider's **apex domain** and every related
domain (account, checkout, corporate):

```bash
DOMAIN="nordvpn.com"

echo "=== NS ===" && dig +short "$DOMAIN" NS
echo "=== A ===" && dig +short "$DOMAIN" A
echo "=== AAAA ===" && dig +short "$DOMAIN" AAAA
echo "=== MX ===" && dig +short "$DOMAIN" MX
echo "=== TXT ===" && dig +short "$DOMAIN" TXT
echo "=== CAA ===" && dig +short "$DOMAIN" CAA
echo "=== SOA ===" && dig +short "$DOMAIN" SOA
```

Repeat for related domains. For NordVPN the set is:
`nordvpn.com`, `nordaccount.com`, `nordcheckout.com`, `nordsec.com`,
`nordsecurity.com`.

### 13b. What each record reveals

| Record | What it tells you | Third-party exposure |
|--------|------------------|---------------------|
| **NS** | Who operates authoritative DNS | NS provider sees every DNS query for the domain |
| **A / AAAA** | Where the site is hosted; whether IPv6 is supported | Hosting/CDN provider |
| **MX** | Who handles inbound email | Email provider sees all incoming mail |
| **TXT (SPF)** | Who is authorized to *send* email as this domain | Every `include:` is a company that can send mail on their behalf |
| **TXT (verification)** | Which SaaS platforms have verified domain ownership | `MS=` = Microsoft 365, `google-site-verification=` = Google, `atlassian-domain-verification=` = Atlassian, etc. |
| **CAA** | Which CAs can issue TLS certificates | Absence means any CA can issue |
| **SOA** | Zone authority and operator | Confirms the DNS host |

### 13c. Resolve NS and MX glue IPs

Nameserver and mail exchanger hostnames are not enough. Resolve them and
WHOIS the IPs to confirm the operating company:

```bash
# NS glue
for ns in $(dig +short "$DOMAIN" NS); do
  echo "=== $ns ==="
  echo "A:"; dig +short "$ns" A
  echo "AAAA:"; dig +short "$ns" AAAA
done

# MX glue
for mx in $(dig +short "$DOMAIN" MX | awk '{print $2}'); do
  echo "=== $mx ==="
  echo "A:"; dig +short "$mx" A
  echo "AAAA:"; dig +short "$mx" AAAA
done
```

### 13d. Parse SPF includes (email supply chain)

The SPF record lists every company authorized to send email as
`@<domain>`. Follow each `include:` recursively:

```bash
dig +short TXT "$DOMAIN" | grep spf
```

For each `include:<host>`, resolve that TXT record to find the IP ranges
and any further includes. This builds the complete email sending chain.

Example for `nordvpn.com`:

```
v=spf1 include:mail.zendesk.com include:_spf.google.com include:icloud.com -all
```

This means **Zendesk**, **Google**, and **Apple iCloud** can all send
email as `@nordvpn.com`.

### 13e. Check DMARC and DKIM

```bash
# DMARC policy
dig +short TXT _dmarc."$DOMAIN"

# DKIM selectors (try common ones)
for sel in google zendesk1 zendesk2 default s1 s2 k1 selector1 selector2; do
  result=$(dig +short TXT "${sel}._domainkey.${DOMAIN}" 2>/dev/null)
  if [ -n "$result" ]; then
    echo "DKIM $sel: $result"
  fi
done
```

DMARC `rua=` and `ruf=` addresses reveal where aggregate and forensic
email reports are sent (often a different domain like `nordsec.com`).

### 13f. Check subdomains for CNAME chains

Key subdomains often CNAME to third-party SaaS:

```bash
for sub in mail support help status blog docs api; do
  cname=$(dig +short CNAME "${sub}.${DOMAIN}")
  if [ -n "$cname" ]; then
    echo "${sub}.${DOMAIN} -> CNAME $cname"
  fi
done
```

Common CNAME patterns:

| CNAME target | Third party |
|-------------|------------|
| `*.zendesk.com` | Zendesk (support) |
| `*.sparkpostmail.com` | SparkPost/Bird (transactional email) |
| `*.hubspot.com` | HubSpot (CRM/marketing) |
| `*.ghost.io` | Ghost (blog) |
| `*.statuspage.io` | Atlassian Statuspage |
| `*.intercom.io` | Intercom (chat) |
| `*.freshdesk.com` | Freshworks (support) |

### 13g. Check for AAAA (IPv6) support

A VPN provider that does not publish AAAA records on their own domain
cannot serve IPv6 traffic to their website. This is worth noting since
IPv6 leak protection is a selling point for VPN products.

```bash
echo "A:"; dig +short "$DOMAIN" A
echo "AAAA:"; dig +short "$DOMAIN" AAAA
```

If AAAA is empty, the provider's site is IPv4-only.

### 13h. Parse TXT verification tokens

TXT records contain domain-verification tokens for SaaS platforms. Each
one means the provider has an active account with that vendor:

| TXT pattern | Platform |
|-------------|----------|
| `MS=...` | Microsoft 365 |
| `google-site-verification=...` | Google (Search Console, Workspace) |
| `atlassian-domain-verification=...` | Atlassian (Jira, Confluence) |
| `atlassian-sending-domain-verification=...` | Atlassian (email sending) |
| `facebook-domain-verification=...` | Meta / Facebook |
| `_github-pages-challenge=...` | GitHub Pages |
| `stripe-verification=...` | Stripe (payments) |
| `oneuptime=...` | OneUptime (monitoring) |
| `docusign=...` | DocuSign |
| `adobe-idp-site-verification=...` | Adobe |
| `apple-domain-verification=...` | Apple |
| `hubspot-developer-verification=...` | HubSpot |
| `asv=...` (on nordsec.com) | AppsFlyer (mobile attribution) |

Multiple `MS=` tokens on the same domain indicate multiple Microsoft 365
tenants or re-verifications over time.

---

## 14. Phase 9 - Compile total third-party inventory

Combine findings from both layers (website surface + DNS infrastructure)
into a single table. The goal is to answer:

> If I become a NordVPN customer, how many companies handle some part of
> my relationship with Nord - from visiting their site, to receiving
> emails, to filing support tickets?

### Inventory template

| # | Company | How discovered | Role | What they can see |
|---|---------|---------------|------|-------------------|
| 1 | Provider (Nord Security) | A record, content | Origin | Everything |
| 2 | Cloudflare | NS, A, WHOIS | DNS + CDN + WAF | All DNS queries, all HTTP traffic (TLS terminating) |
| 3 | Google | MX, SPF, GTM, DoubleClick | Email + analytics + ads | Emails, website visits, cross-site ad correlation |
| 4 | ... | ... | ... | ... |

### Categories to include

- **DNS authority** - who runs the nameservers
- **CDN / WAF** - who terminates TLS and proxies HTTP
- **Email (inbound)** - who handles MX
- **Email (outbound)** - every SPF `include:` sender
- **Support** - CNAME targets for support/help subdomains
- **Transactional email** - CNAME for mail subdomain (SparkPost, SendGrid, etc.)
- **Analytics / ads** - scripts loaded on the website
- **Error tracking** - Sentry, Datadog, etc.
- **Internal tooling** - revealed by TXT verification tokens (Microsoft, Atlassian, Salesforce)
- **Monitoring** - uptime/status services (OneUptime, Statuspage)
- **CRM / marketing** - revealed by SPF includes or TXT tokens (Salesforce, HubSpot, Mindmatrix)
- **Hosting** - where non-Cloudflare domains resolve (Vercel, AWS, etc.)

---

## 15. Worked example: NordVPN (2026-04-16)

### 15a. Website surface - network requests from a single page load

| # | Company | Hostnames | Resource types | Risk category |
|---|---------|-----------|---------------|---------------|
| 1 | **Nord Security** | `nordvpn.com`, `s1.nordcdn.com`, `ic.nordcdn.com`, `sb.nordcdn.com`, `cm.nordvpn.com`, `d.nordvpn.com`, `web-api.nordvpn.com`, `debug.nordvpn.com` | document, script, stylesheet, image, font, xhr, ping | First-party |
| 2 | **Cloudflare** | Reverse proxy for all `*.nordvpn.com` and `*.nordcdn.com` | TLS termination | Infrastructure proxy |
| 3 | **Google** | `www.googletagmanager.com`, `stats.g.doubleclick.net` | script, ping | **Third-party ad tracker** |
| 4 | **Fastly** | `browser.sentry-cdn.com` | script | Third-party CDN |
| 5 | **Sentry** | JS executes locally; payloads to `debug.nordvpn.com` | xhr (error reports) | Third-party SDK |

### Observations

- **Google DoubleClick** (`stats.g.doubleclick.net`) enables cross-site
  ad profile correlation. A user visiting nordvpn.com can be linked to
  their activity on any other site using Google ads or analytics.
- **Cloudflare** terminates TLS for 14 of 19 hostnames discovered. They
  can technically read all request/response content in transit.
- **NordVPN proxies GA** through `cm.nordvpn.com`, reducing direct
  browser-to-Google requests, but the data still reaches Google servers.
- **Sentry error payloads** route through `debug.nordvpn.com` (Cloudflare)
  rather than directly to `sentry.io`, limiting direct Sentry exposure.
- The site is built with **Astro** (visible in script filenames).
- App version at time of test: `nordvpn-main@0.247.1`.

### 15b. DNS infrastructure findings

**Authoritative DNS:** All Nord domains (`nordvpn.com`, `nordaccount.com`,
`nordcheckout.com`, `nordsec.com`, `nordsecurity.com`) delegate to the
same Cloudflare nameservers: `lily.ns.cloudflare.com` and
`seth.ns.cloudflare.com`. Nord does not operate their own authoritative
DNS.

**IPv6:** `nordvpn.com` has **no AAAA record** (IPv4-only). The exception
is `my.nordaccount.com` which has Cloudflare IPv6 addresses. The NS
servers themselves (Cloudflare) and the MX servers (Google) support AAAA.

**Email (MX):** All five domains point to Google Workspace
(`aspmx.l.google.com` priority 1, with `alt1`-`alt4` as fallbacks).

**SPF (who can send email as @nordvpn.com):**

| Domain | SPF includes | Companies |
|--------|-------------|-----------|
| `nordvpn.com` | `_spf.google.com`, `mail.zendesk.com`, `icloud.com` | Google, Zendesk, Apple |
| `nordcheckout.com` | `mail.zendesk.com`, `_spf.hushmail.com` | Zendesk, Hushmail (Aptum Technologies, Canada) |
| `nordaccount.com` | `_spf.google.com`, `mail.zendesk.com`, `_spf.hushmail.com` | Google, Zendesk, Hushmail |
| `nordsec.com` | `_spf.google.com`, `_spf.salesforce.com`, `email.prnewswire.com` (SendGrid), `mailgun.org` | Google, Salesforce, SendGrid, Mailgun |
| `nordsecurity.com` | `_spf.google.com`, `_spf.salesforce.com`, `spf.mindmatrix.net` | Google, Salesforce, Mindmatrix |

**DMARC:** `v=DMARC1; p=reject; sp=reject; pct=100` with reports to
`dmarc@nordsec.com`. Strict enforcement.

**DKIM:** Confirmed selectors for Google (`google._domainkey`) and
Zendesk (`zendesk1._domainkey`, `zendesk2._domainkey`).

**TXT verification tokens:**

| Token | Platform | Implication |
|-------|----------|-------------|
| `MS=...` (x3) | Microsoft 365 | Three separate verification tokens suggest multiple tenants or services |
| `google-site-verification=...` | Google | Workspace and/or Search Console |
| `oneuptime=...` | OneUptime | Uptime monitoring active |
| `atlassian-domain-verification=...` (nordsec.com) | Atlassian | Jira/Confluence in use |
| `atlassian-sending-domain-verification=...` (nordsec.com) | Atlassian | Atlassian sends email as this domain |
| `asv=...` (nordsec.com) | AppsFlyer | Mobile attribution/analytics |

**Subdomain CNAME chains:**

| Subdomain | CNAME target | Third party |
|-----------|-------------|------------|
| `mail.nordvpn.com` | `sparkpostmail.com` -> AWS (`54.240.184.x`) | SparkPost/Bird (transactional email) |
| `support.nordvpn.com` | `nordvpn.zendesk.com` -> `216.198.x.x` | Zendesk (customer support) |

### 15c. Complete third-party inventory

| # | Company | How discovered | Role | What they can see |
|---|---------|---------------|------|-------------------|
| 1 | **Cloudflare** | NS, A, WHOIS | DNS authority + CDN/WAF for all domains | Every DNS query, all HTTP traffic in cleartext (TLS terminating proxy) |
| 2 | **Google** | MX, SPF, TXT, GTM, DoubleClick | Email (Workspace), analytics (GA4), ads (DoubleClick), search verification | All inbound email, website visitor tracking, cross-site ad profile correlation |
| 3 | **Microsoft** | TXT (`MS=` x3) | Microsoft 365 (internal services) | Whatever services Nord uses (Teams, Azure AD, SharePoint, etc.) |
| 4 | **Zendesk** | SPF, CNAME, DKIM | Customer support platform | Support tickets, customer PII, outbound support emails |
| 5 | **Apple** | SPF (`icloud.com`) | iCloud Mail (employee email) | Emails sent via iCloud by Nord employees |
| 6 | **SparkPost/Bird** | CNAME (`mail.nordvpn.com`) | Transactional email delivery | Email metadata, recipient addresses, delivery status |
| 7 | **Hushmail** | SPF (checkout + account domains) | Encrypted email for checkout/account | Transactional email for payment-related flows |
| 8 | **Sentry** | JS SDK on website | Error tracking | Browser errors, stack traces, user session context |
| 9 | **Fastly** | WHOIS on Sentry CDN IPs | CDN for Sentry JS bundle | IP addresses downloading the SDK |
| 10 | **Salesforce** | SPF (nordsec.com, nordsecurity.com) | CRM / email campaigns | Customer and prospect data, email content |
| 11 | **Atlassian** | TXT (nordsec.com) | Jira / Confluence (internal tools) | Internal project data, documentation, email sending |
| 12 | **Mailgun** | SPF (nordsec.com) | Email delivery | Email metadata and content for nordsec.com |
| 13 | **SendGrid** | SPF via prnewswire (nordsec.com) | PR distribution email | Press release emails |
| 14 | **Mindmatrix** | SPF (nordsecurity.com) | Channel/partner marketing | Partner and affiliate email campaigns |
| 15 | **OneUptime** | TXT | Uptime monitoring | Website/API availability, endpoint health |
| 16 | **Vercel** | WHOIS (`nordsecurity.com`) | Hosting for corporate site | Request logs, visitor IPs for nordsecurity.com |
| 17 | **AWS** | WHOIS (NordLocker, SparkPost IPs) | Hosting for NordLocker + email infra | Varies by service |

### 15d. Verdict

**17 companies** have some level of access to NordVPN's infrastructure,
customer data, or user traffic. Of these:

- **5** are contacted directly by a visitor's browser on a single page
  load (website surface).
- **12 more** are embedded in the DNS, email, and platform infrastructure
  and handle data invisibly.
- **Google** has the deepest cross-cutting access: email (Workspace), web
  analytics (GA4), ad tracking (DoubleClick), and domain verification.
- **Cloudflare** has the broadest infrastructure access: authoritative
  DNS for all domains plus TLS-terminating reverse proxy.

---

## Appendix A: Quick reference commands

```bash
# Full pipeline in one shot (if curl works)
URL="https://example-vpn.com"
curl -sL "$URL" -o /tmp/page.html

# Extract hostnames from HTML
grep -oP 'https?://[^/"]+' /tmp/page.html | sed 's|https\?://||' | sort -u > /tmp/hosts.txt

# Resolve + WHOIS all hostnames
while read h; do
  ip=$(dig +short "$h" | head -1)
  org=$(whois "$ip" 2>/dev/null | grep -i 'OrgName' | head -1 | sed 's/OrgName:\s*//')
  echo "$h -> $ip -> $org"
done < /tmp/hosts.txt
```

## Appendix B: HAR analysis one-liner

```bash
# Top 20 third-party hosts from a HAR file
jq -r '.log.entries[].request.url' file.har \
  | sed 's|https\?://||;s|/.*||' \
  | sort | uniq -c | sort -rn | head -20
```

## Appendix C: Harness tracker classification

The harness (`vpn_leaks/checks/har_summary.py`) auto-tags hosts using
substring matching. Current tracker hints include:

- `google-analytics.com`, `googletagmanager.com`, `doubleclick.net`
- `facebook.net`, `facebook.com/tr`
- `hotjar.com`, `segment.io`, `mixpanel.com`, `clarity.ms`
- `bat.bing.com`, `ads.linkedin.com`, `plausible.io`
- `/gtag/`, `/gtm.js`, `cdn-cgi/rum`

CDN hints include:

- `cloudflare`, `fastly`, `akamai`, `cloudfront.net`
- `azureedge.net`, `cdn.`, `stackpath`, `incapsula`

To add new patterns, edit `_TRACKER_HINTS` and `_CDN_HINTS` in
[`vpn_leaks/checks/har_summary.py`](../vpn_leaks/checks/har_summary.py).

## Appendix D: Full DNS audit one-liner

```bash
DOMAIN="nordvpn.com"
for rtype in NS A AAAA MX TXT CAA SOA; do
  echo "=== $rtype ==="
  dig +short "$DOMAIN" "$rtype"
  echo ""
done

# SPF chain
dig +short TXT "$DOMAIN" | grep spf

# DMARC
dig +short TXT "_dmarc.${DOMAIN}"

# DKIM (common selectors)
for sel in google zendesk1 zendesk2 default s1 s2 k1 selector1 selector2; do
  r=$(dig +short TXT "${sel}._domainkey.${DOMAIN}" 2>/dev/null)
  [ -n "$r" ] && echo "DKIM [$sel]: found"
done

# Subdomain CNAME scan
for sub in mail support help status blog docs api autodiscover; do
  c=$(dig +short CNAME "${sub}.${DOMAIN}")
  [ -n "$c" ] && echo "${sub} -> $c"
done
```
