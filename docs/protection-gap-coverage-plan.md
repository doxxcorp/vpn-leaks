# Protection Gap Coverage Plan

This document defines the work required to answer the core research question:

> **When using a VPN provider, are there any gaps in the protection that might allow someone to see the client's activity — at any point in the client's relationship with the VPN provider?**

That relationship has three phases, each with distinct threat actors:

| Phase | User State | Key Threat Actors |
|---|---|---|
| **Pre-registered** | Visiting marketing site, signing up, paying | Ad pixels, payment processors, CDNs, DNS resolver |
| **Pre-connected** | App installed, account active, tunnel off | VPN app telemetry, auth providers, server-list endpoints |
| **Connected** | Tunnel active | VPN provider infra, transit ASNs, DNS operators, destination hosts |

The current harness covers the **connected** phase reasonably (DNS/IPv6/WebRTC leaks, per-IP ASN attribution, one-hop upstream). All other phases and several connected-phase gaps are unaddressed.

---

## How to Use This Document

Each task is **independently actionable**. An agent can take one task, read the listed files, implement the steps, verify the acceptance criteria, and stop — without needing the rest of the document for context.

Tasks within a section are ordered by dependency. A task marked `depends: TASK-XX` requires that prior task's data fields to exist before it can be implemented.

**Before starting any task:** run `ruff check vpn_leaks tests && pytest tests -q` to establish a clean baseline. Run the same commands after to verify no regressions.

**To regenerate the report after changes:** `vpn-leaks report --provider nordvpn && open VPNs/NORDVPN.html`

---

## Task Index

| ID | Title | Phase | Depends | Scope |
|---|---|---|---|---|
| [TASK-01](#task-01) | Propagate full BGP AS path through data pipeline | Connected | — | Medium |
| [TASK-02](#task-02) | Add flow count column to IP table | Connected | — | Small |
| [TASK-03](#task-03) | Role classification for IP contacts | All | — | Medium |
| [TASK-04](#task-04) | DNS operator attribution | Connected | — | Medium |
| [TASK-05](#task-05) | Multi-hop upstream DAG | Connected | TASK-01 | Medium |
| [TASK-06](#task-06) | Role-based KPI bar | All | TASK-03 | Small |
| [TASK-07](#task-07) | Add signup/checkout surface URLs to provider configs | Pre-reg | — | Small |
| [TASK-08](#task-08) | Checkout and signup HAR deep analysis | Pre-reg | TASK-07 | Medium |
| [TASK-09](#task-09) | Payment processor and analytics event fingerprinting | Pre-reg | TASK-07 | Medium |
| [TASK-10](#task-10) | Pre-connection idle telemetry capture mode | Pre-conn | — | Large |
| [TASK-11](#task-11) | TLS certificate chain capture | Connected | — | Medium |
| [TASK-12](#task-12) | Known analytics SDK endpoint detection from PCAP | Pre-conn | — | Medium |

---

## Section A — Connected Phase: Surface Existing Data

---

### TASK-01

**Propagate full BGP AS path through the data pipeline**

**Gap it closes:** The `bgp_lookup.lookup_ip()` function already returns a full `as_path` string (e.g., `"3356 7018 13335"`) representing every ASN a packet traverses from internet ingress to the destination. This is currently discarded. Only the last ASN (`upstream_asn`) is kept. Surfacing the full path shows the Tier-1 backbone carriers — Lumen, Cogent, NTT, Tata — that move traffic across the internet, not just the Tier-2 handoff point.

**Files to modify:**
1. `vpn_leaks/reporting/web_exposure.py`
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`

**Implementation steps:**

1. **In `pcap_host_intelligence()` (~line 478):** After `row["upstream_asn"] = bgp.get("upstream_asn")`, add:
   ```python
   row["as_path"] = bgp.get("as_path") or None
   ```
   The `bgp` dict comes from `_bgp_lookup_cached()`. The field is a space-separated string like `"174 3356 13335"`.

2. **In `build_capture_workspace_rollup()` (~line 1099):** Add extraction alongside `upstream_asn`:
   ```python
   as_path = row.get("as_path") or None
   ```
   Add `"as_path": as_path` to the `ip_index[ip]` dict at creation (~line 1113).
   In the accumulation block (~line 1129), add promotion logic:
   ```python
   if not entry.get("as_path") and as_path:
       entry["as_path"] = as_path
   ```

3. **In the Jinja2 template (`vpn_report_document.html.j2`):** The JSON blob serialized at the `dag-companies` script tag includes the full `cw.companies` structure, so `as_path` will be available to JavaScript automatically once added to `ip_index`. No change needed to the data blob itself.

4. **In the IP table (~line 147–200 of the template):** Add a new column header `AS Path` after the `Upstream` column. In the row loop, render:
   ```html
   <td class="ip-col-aspath">
     {% if ip_row.as_path and ip_row.as_path != '—' %}
       <span class="aspath-pill">{{ ip_row.as_path }}</span>
     {% else %}—{% endif %}
   </td>
   ```

5. **In `report.css`:** Add `.ip-col-aspath { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); white-space: nowrap; }` and `.aspath-pill { letter-spacing: 0.02em; }`.

**Acceptance criteria:**
- `VPNs/NORDVPN.html` IP table shows an AS Path column with values like `"174 3356 13335"` for IPs with BGP data, `—` for private or unresolved IPs.
- `ruff check` and `pytest tests -q` pass with no new failures.

---

### TASK-02

**Add flow count column to IP table**

**Gap it closes:** `flows` (number of distinct PCAP flows per IP) is already present in every `ip_index` entry and serialized to `dag-companies` JSON, but the IP table only shows `bytes`. An IP with 1 flow × 10 MB is a content download. An IP with 900 flows × 2 KB is a telemetry beacon. These have completely different implications.

**Files to modify:**
1. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`
2. `vpn_leaks/reporting/static/report.css`

**Implementation steps:**

1. In the IP table header row, add `<th class="ip-col-flows">Flows</th>` immediately after the `Bytes` header.

2. In the IP table body row loop, add:
   ```html
   <td class="ip-col-flows">{{ ip_row.flows if ip_row.flows else '—' }}</td>
   ```
   immediately after the bytes cell.

3. In `report.css`, add `.ip-col-flows { text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--text-muted); }`.

**Acceptance criteria:**
- IP table shows a `Flows` column. Rows with PCAP-sourced IPs have numeric values. Non-PCAP rows show `—`.

---

### TASK-03

**Role classification for IP contacts**

**Gap it closes:** Currently all IP contacts are visually equal — there is no distinction between a VPN control-plane call (auth, server list), a data-plane tunnel endpoint, a provider-chosen analytics vendor, a DNS resolver, and a routing-infrastructure hop. The classifications have completely different threat-model implications: the user chose to contact the VPN provider; they did not choose to expose their activity to a third-party analytics vendor or a Tier-1 backbone carrier.

**Files to modify:**
1. `vpn_leaks/reporting/web_exposure.py`
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`
3. `vpn_leaks/reporting/static/report.css`

**Implementation steps:**

1. **Add `classify_contact_role()` function in `web_exposure.py`** (add near `_heuristic_canonical`, around line 920):

   ```python
   _ANALYTICS_VENDOR_PATTERNS = [
       "amplitude", "segment", "mixpanel", "braze", "fullstory", "heap",
       "firebase", "google analytics", "adobe analytics", "datadog",
       "new relic", "appsflyer", "adjust", "branch.io", "sentry",
       "cloudflare insights", "hotjar", "mouseflow", "logrocket",
   ]

   def classify_contact_role(
       owner: str,
       canonical_company: str,
       provider_name: str,
       sources: str,
   ) -> str:
       """Return one of: vpn-control | vpn-data | provider-analytics | dns-resolver | routing-infra | unknown."""
       owner_l = (owner or "").lower()
       company_l = (canonical_company or "").lower()
       provider_l = (provider_name or "").lower().replace(" ", "").replace("-", "")

       # DNS resolvers: source contains pcap_dns but NOT pcap_peer_ip
       if "pcap_dns" in (sources or "") and "pcap_peer_ip" not in (sources or ""):
           return "dns-resolver"

       # VPN provider own infrastructure
       company_stripped = company_l.replace(" ", "").replace("-", "")
       if provider_l and (provider_l in company_stripped or company_stripped in provider_l):
           return "vpn-control"

       # Known analytics / telemetry vendors
       for pattern in _ANALYTICS_VENDOR_PATTERNS:
           if pattern in owner_l or pattern in company_l:
               return "provider-analytics"

       return "unknown"
   ```

2. **In `build_capture_workspace_rollup()`:** Pass `provider_name` into the function (it is available from the run's metadata — look for how `vpn_provider` is accessed, likely passed in as a parameter or available from run objects). In the ip_index construction loop, add:
   ```python
   entry["role"] = classify_contact_role(
       owner=entry.get("owner", ""),
       canonical_company=company_name,
       provider_name=provider_name,
       sources=entry.get("sources", ""),
   )
   ```
   Note: `company_name` is only known after the grouping step. Add the role assignment after company names are finalized (~line 1200+), or set it provisionally and refine after normalization.

3. **In the template IP table:** Add a `Role` column with a color-coded badge. Use CSS classes `role-vpn-control`, `role-vpn-data`, `role-provider-analytics`, `role-dns-resolver`, `role-unknown`.

4. **In `report.css`:** Add badge styles:
   ```css
   .role-badge { display: inline-block; font-size: 0.62rem; padding: 0.1rem 0.35rem; border-radius: 3px; font-family: 'JetBrains Mono', monospace; }
   .role-vpn-control    { background: rgba(27,193,188,0.15); color: var(--teal-bright); }
   .role-provider-analytics { background: rgba(219,0,219,0.15); color: #DB00DB; }
   .role-dns-resolver   { background: rgba(154,145,200,0.2); color: #9A91C8; }
   .role-unknown        { background: rgba(255,255,255,0.06); color: var(--text-muted); }
   ```

**Acceptance criteria:**
- Every IP row in the table has a Role badge. At minimum: NordVPN's own IPs show `vpn-control`, DNS-only contacts show `dns-resolver`.
- The classification function has a unit test in `tests/` covering at least: dns-resolver (pcap_dns source), vpn-control (owner matches provider name), provider-analytics (amplitude pattern), unknown fallback.

---

### TASK-04

**DNS operator attribution**

**Gap it closes:** The PCAP captures DNS hostnames the VPN client queries. The authoritative nameserver for each hostname is operated by a company (Cloudflare, AWS Route53, Google, the VPN provider themselves). That nameserver operator sees every query, meaning they have query-level visibility into what the user is contacting — even before a TCP connection is made. Currently the DNS hostnames are listed raw with no operator attribution.

**Files to modify:**
1. `vpn_leaks/reporting/web_exposure.py`
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`
3. `vpn_leaks/reporting/static/report.css`

**Implementation steps:**

1. **Add `_resolve_dns_operators()` in `web_exposure.py`** (near `_cymru_asn_names_bulk`):

   ```python
   def _resolve_dns_operators(
       hostnames: list[str],
       ip_intel_cache: dict[str, Any],
   ) -> dict[str, dict[str, str]]:
       """
       For each hostname, resolve its NS records and run bgp_lookup on each NS IP.
       Returns {hostname: {"ns_host": str, "ns_ip": str, "ns_asn": str, "ns_org": str}}.
       Caches results in ip_intel_cache["__dns_operators__"].
       """
       import dns.resolver
       from vpn_leaks.attribution.bgp_lookup import lookup_ip

       cache = dict(ip_intel_cache.get("__dns_operators__") or {})
       results: dict[str, dict[str, str]] = {}

       for hostname in hostnames:
           if hostname in cache:
               results[hostname] = cache[hostname]
               continue
           try:
               # Get the apex domain (last 2 parts) for NS lookup
               parts = hostname.rstrip(".").split(".")
               apex = ".".join(parts[-2:]) if len(parts) >= 2 else hostname
               ns_answers = dns.resolver.resolve(apex, "NS", lifetime=4.0)
               ns_host = str(ns_answers[0].target).rstrip(".")
               # Resolve NS host to IP
               a_answers = dns.resolver.resolve(ns_host, "A", lifetime=4.0)
               ns_ip = str(a_answers[0])
               # BGP lookup on NS IP
               bgp = lookup_ip(ns_ip)
               entry = {
                   "ns_host": ns_host,
                   "ns_ip": ns_ip,
                   "ns_asn": bgp.get("asn") or "—",
                   "ns_org": bgp.get("upstream_asn") or bgp.get("asn") or "—",
               }
           except Exception:
               entry = {"ns_host": "—", "ns_ip": "—", "ns_asn": "—", "ns_org": "—"}
           cache[hostname] = entry
           results[hostname] = entry

       ip_intel_cache["__dns_operators__"] = cache
       return results
   ```

   Use `dnspython` which is already a dependency (used in `website_exposure_methodology.py`).

2. **In `build_capture_workspace_rollup()`:** After building the ip_index, retrieve DNS hostnames from the pcap data:
   ```python
   dns_hostnames = []
   for run_id, loc_data in run_location_pairs:  # adjust to actual iteration pattern
       pcap = loc_data.get("pcap_derived") or {}
       dns_hostnames.extend(pcap.get("dns_hostnames_unique") or [])
   dns_hostnames = list(dict.fromkeys(dns_hostnames))[:200]  # dedupe, cap at 200
   dns_operators = _resolve_dns_operators(dns_hostnames, _dc)  # _dc is the ip_intel cache
   ```
   Add `dns_operators` to the workspace object (`cw`) returned from this function.

3. **In the template:** Add a collapsible "DNS Operators" subsection in the Network Intelligence section (after the company clusters), showing a table: `Hostname | Nameserver | Operator ASN`. Group by operator so it's clear when 40 hostnames all resolve via Cloudflare's NS.

4. **In the KPI bar:** Add a count: `{{ cw.dns_operator_count }} DNS operator(s)` derived from the distinct `ns_asn` values in `dns_operators`.

**Acceptance criteria:**
- A DNS Operators table appears in the Network Intelligence section.
- Hostnames that use Cloudflare NS (e.g., `ns1.cloudflare.com`) are attributed to Cloudflare's ASN.
- Results are cached in `ip_intel.json` under `__dns_operators__` so re-runs are instant.
- `dnspython` import error is caught gracefully and the section is omitted rather than crashing.

---

### TASK-05

**Multi-hop upstream DAG**

**Gap it closes:** The DAG currently has two layers: Upstream (immediate transit, `upstream_asn`) → Company. The actual routing path for most traffic involves multiple transit ASNs. With the full `as_path` from TASK-01, the DAG can show every transit hop, making it visually clear that traffic passes through Lumen, Tata, or Cogent before reaching the destination.

**Depends on:** TASK-01 (the `as_path` field must be present in `cw.companies[i].asns[j].ips[k]`)

**Files to modify:**
1. `vpn_leaks/reporting/templates/vpn_report_document.html.j2` (the `initDag()` JS function)
2. `vpn_leaks/reporting/static/report.css`

**Implementation steps:**

1. **In `initDag()`, during node/link construction:** After building company nodes (layer 1) and their upstream nodes (layer 0), additionally parse the full `as_path` to create intermediate transit nodes at layers `-1`, `-2`, etc. (or renumber: layer 0 = Tier-1, layer 1 = Tier-2/immediate upstream, layer 2 = company).

   ```javascript
   // For each IP, parse as_path into ordered transit hops
   (ag.ips || []).forEach(function(ip) {
     var pathStr = ip.as_path;
     if (!pathStr || pathStr === '—') return;
     var hops = pathStr.trim().split(/\s+/);
     // hops[last] = origin ASN (= ip.asn), hops[0] = ingress/Tier-1
     // Only add hops that aren't already the origin or immediate upstream
     var origin = 'AS' + hops[hops.length - 1];
     var upstream = ip.upstream_asn;
     hops.slice(0, -1).forEach(function(hopAsn, i) {
       var hId = 'h:AS' + hopAsn;
       var hopLayer = -(hops.length - 2 - i);  // negative layers above upstream
       if (!nodeById[hId]) {
         nodes.push({ id: hId, type: 'transit', name: 'AS' + hopAsn, layer: hopLayer });
         nodeById[hId] = nodes[nodes.length - 1];
       }
       // Link: this hop → next hop or upstream
       var nextId = i < hops.length - 2 ? 'h:AS' + hops[i + 1] : ('u:' + (ip.upstream_org || upstream));
       links.push({ source: hId, target: nextId, type: 'transit' });
     });
   });
   ```

   Adjust `LY` (layer Y positions) to accommodate negative layers. The current `LY = {0: 130, 1: 390, 2: 660}` — add entries for `-1: 80`, `-2: 40`, etc., or compute dynamically from `Math.min(layer)`.

2. **Add transit node styling in `report.css`:**
   ```css
   .dag-node-transit circle { stroke: rgba(255,160,60,0.6); }
   .dag-label-transit { fill: rgba(255,160,60,0.7); font-size: 9px; }
   ```

3. **In `barycenterLayout()`:** Extend `seedLayer` and `bcSortLayer` to handle the new layer numbers (currently hardcoded for layers 0, 1, 2). Replace the `[0, 1, 2]` array with a dynamic range:
   ```javascript
   var allLayers = [...new Set(nodes.map(function(n) { return n.layer; }))].sort(function(a,b){return a-b;});
   allLayers.forEach(function(ly) { seedLayer(ly); });
   ```

**Acceptance criteria:**
- DAG renders transit ASN nodes between the upstream row and the company row for IPs that have multi-hop AS paths.
- DAG still renders correctly (no JS errors) for IPs with no `as_path` or single-hop paths.

---

### TASK-06

**Role-based KPI bar**

**Gap it closes:** The current KPI bar shows raw counts (organizations, WHOIS handles, peer IPs, SNI+DNS). These numbers don't convey the threat model distinction. "12 organizations saw your traffic" is less meaningful than "3 provider-chosen analytics vendors + 2 DNS operators + 7 routing infrastructure providers saw your traffic."

**Depends on:** TASK-03 (role classification must be complete)

**Files to modify:**
1. `vpn_leaks/reporting/web_exposure.py` (workspace builder, KPI computation)
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`

**Implementation steps:**

1. **In `build_capture_workspace_rollup()`:** After role classification is applied to all IPs, compute role counts:
   ```python
   role_counts = {}
   for entry in ip_index.values():
       r = entry.get("role") or "unknown"
       role_counts[r] = role_counts.get(r, 0) + 1
   cw.role_counts = role_counts
   ```

2. **In the template KPI row:** Replace or augment the existing "organizations" KPI tile with role-split counts. Add a secondary row or tooltip below the main KPI numbers:
   ```
   {{ role_counts.get('provider-analytics', 0) }} analytics vendors
   {{ role_counts.get('dns-resolver', 0) }} DNS resolvers
   {{ role_counts.get('vpn-control', 0) }} VPN control plane
   ```

**Acceptance criteria:**
- KPI bar shows at minimum one role-based count that distinguishes provider-chosen third parties from routing infrastructure.

---

## Section B — Pre-registration Phase: Signup and Payment Exposure

---

### TASK-07

**Add signup/checkout surface URLs to provider configs**

**Gap it closes:** The `surface_probe` and `website_exposure_methodology` checks can analyze third-party scripts and trackers on any URL, but only if those URLs are listed in the provider's YAML config. The current `nordvpn.yaml` has no `surface_urls`. This task adds them so subsequent tasks have HAR data to analyze.

**Files to modify:**
1. `configs/vpns/nordvpn.yaml`
2. `configs/vpns/expressvpn.yaml` (if it exists and is used)

**Implementation steps:**

1. Add the following to `configs/vpns/nordvpn.yaml`:

   ```yaml
   surface_urls:
     - page_type: home
       url: "https://nordvpn.com/"
     - page_type: pricing
       url: "https://nordvpn.com/pricing/"
     - page_type: signup
       url: "https://nordvpn.com/order/"
     - page_type: checkout
       url: "https://nordvpn.com/checkout/"
     - page_type: download
       url: "https://nordvpn.com/download/"
     - page_type: login
       url: "https://my.nordaccount.com/"

   competitor_probe:
     provider_domains:
       - nordvpn.com
       - nordaccount.com
       - nordvpn.net
     skip_browserleaks: false
   ```

2. The `surface_probe` check in `vpn_leaks/checks/surface_probe.py` (or wherever it's invoked from `cli.py`) will automatically visit these URLs and save HAR + `har_summary.json` per page when `vpn-leaks run` is executed. No code changes needed for this task — the YAML addition is sufficient to activate existing infrastructure.

3. Run `vpn-leaks run --provider nordvpn --skip-vpn` to collect the surface probe artifacts. Verify `runs/<run_id>/raw/<loc>/surface_probe/` contains HAR files for each page type.

**Acceptance criteria:**
- After a fresh `vpn-leaks run --provider nordvpn --skip-vpn`, the `surface_probe` artifacts directory contains HAR files for at least the `pricing` and `signup` page types.

---

### TASK-08

**Checkout and signup HAR deep analysis**

**Gap it closes:** The existing `website_exposure_methodology` classifies third-party domains loaded on a page (trackers, CDNs, analytics). But for signup/checkout pages specifically, the more important signal is what fires *during user interaction* — specifically, what conversion/purchase events are sent to analytics platforms, and what data is submitted to form action endpoints. This task adds a dedicated analysis pass over the HAR files for `signup` and `checkout` page types.

**Depends on:** TASK-07 (HAR files must exist for signup/checkout pages)

**Files to create/modify:**
1. `vpn_leaks/reporting/web_exposure.py` (new function `analyze_signup_exposure()`)
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2` (new report section)
3. `vpn_leaks/reporting/static/report.css`

**Implementation steps:**

1. **Create `analyze_signup_exposure(surface_probe_artifacts_dir)` in `web_exposure.py`:**

   This function reads HAR files for pages with `page_type` of `signup`, `checkout`, `pricing`, or `order`, and returns a structured dict:

   ```python
   def analyze_signup_exposure(artifacts_dir: Path) -> dict[str, Any]:
       """
       Analyzes HAR files from signup/checkout surface probe pages.
       Returns {
           "third_party_domains": list of {domain, category, request_count, sends_on_load},
           "form_action_endpoints": list of {url, method, domain},
           "analytics_event_requests": list of {url, platform, event_type},
           "cross_origin_requests": list of {url, domain, type},
       }
       """
   ```

   **Third-party domain detection:** Parse the HAR `entries[].request.url` for each entry. Any domain not matching the VPN provider's apex domain is a third party. Cross-reference against a known-bad list (Google Analytics, Meta Pixel, Hotjar, DoubleClick, etc.) using the same patterns as `_classify_hosts()` in `website_exposure_methodology.py`.

   **Analytics event detection:** Look for requests matching patterns:
   - `google-analytics.com/collect` or `analytics.google.com/g/collect` → Google Analytics event
   - `facebook.com/tr` → Meta Pixel
   - `px.ads.linkedin.com` → LinkedIn Pixel
   - `snap.licdn.com` or `sc-static.net` → Snapchat Pixel
   - `analytics.amplitude.com` → Amplitude
   - Any URL with `?event=purchase` or `?event_type=purchase` in the query string

   **Form action detection:** In the HAR, look for POST requests to non-provider domains during the page session. These are form submissions or AJAX calls that carry user data.

2. **Call this function from `build_capture_workspace_rollup()`** (or from the report generator in `generate_reports.py`) and attach the result to the workspace as `cw.signup_exposure`.

3. **In the template:** Add a "Signup & Checkout Exposure" collapsible section in the pre-connection panel (before the benchmark run cards). Show:
   - A table of third-party domains present on signup/checkout pages, with category badges (Analytics, Advertising, CDN, Unknown)
   - A highlighted callout if any advertising pixels (Meta, Google Ads, LinkedIn) fire on the checkout page — these receive purchase attribution data
   - A list of form action / POST endpoints for non-provider domains

**Acceptance criteria:**
- After running with TASK-07's config and a fresh `vpn-leaks report`, the HTML shows a "Signup & Checkout Exposure" section listing third-party domains on the NordVPN checkout page.
- Google Analytics, Meta Pixel, or similar are flagged if detected in the HAR.

---

### TASK-09

**Payment processor and analytics event fingerprinting**

**Gap it closes:** When a user pays for a VPN subscription, the payment processor (Stripe, PayPal, Adyen, etc.) permanently links the user's real identity (billing name, card, email) to the fact that they purchased a VPN subscription. This is one of the most durable privacy violations in the entire relationship — the VPN tunnel can be perfect, but the payment processor already knows. This task identifies which payment processor(s) the VPN provider uses and what data they receive at checkout.

**Depends on:** TASK-07 (checkout HAR must exist)

**Files to create/modify:**
1. `vpn_leaks/reporting/web_exposure.py` (new function `fingerprint_payment_processors()`)
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`

**Implementation steps:**

1. **Create `fingerprint_payment_processors(har_entries)` in `web_exposure.py`:**

   ```python
   _PAYMENT_PROCESSORS = {
       "stripe.com": "Stripe",
       "js.stripe.com": "Stripe",
       "q.stripe.com": "Stripe",
       "paypal.com": "PayPal",
       "paypalobjects.com": "PayPal",
       "braintreegateway.com": "Braintree (PayPal)",
       "adyen.com": "Adyen",
       "checkout.com": "Checkout.com",
       "klarna.com": "Klarna",
       "coinbase.com": "Coinbase Commerce",
       "btcpay": "BTCPay (self-hosted)",
       "cryptomus.com": "Cryptomus",
       "coingate.com": "CoinGate",
   }

   def fingerprint_payment_processors(har_entries: list[dict]) -> list[dict]:
       """
       Returns list of {processor_name, domain, evidence, data_exposure}.
       data_exposure is a human-readable description of what the processor can see.
       """
   ```

   **Data exposure descriptions** (hardcoded per processor):
   - Stripe: "Card number, billing name, billing address, email, IP address, device fingerprint. Links payment identity to VPN subscription."
   - PayPal: "PayPal account email or card details, billing address, transaction metadata, IP address."
   - Crypto processor: "Wallet address, transaction hash, amount. Lower identity linkage but transaction is public on-chain."

2. **In the template:** Add a "Payment Infrastructure" subsection within TASK-08's "Signup & Checkout Exposure" section. For each detected processor, show a card with: processor name, what data they receive, and a risk callout if the processor is a traditional financial institution (since they can link identity to VPN usage regardless of the VPN's privacy policy).

**Acceptance criteria:**
- If NordVPN's checkout HAR contains requests to `js.stripe.com` or `q.stripe.com`, the report shows "Stripe" in the payment infrastructure section with the data exposure description.
- No crash if no payment processor is detected.

---

## Section C — Pre-connected Phase: App Telemetry Before Tunnel

---

### TASK-10

**Pre-connection idle telemetry capture mode**

**Gap it closes:** After installing the VPN app but before connecting, the app may phone home with telemetry, app analytics, authentication tokens, or server-list fetch calls — all using the user's real IP. This is exposure the user has no way to prevent short of not running the app. Currently there is no way to capture this with the harness.

**Files to create/modify:**
1. `vpn_leaks/cli.py` (new `capture idle` subcommand)
2. `vpn_leaks/checks/idle_telemetry.py` (new check module)
3. `vpn_leaks/models.py` (new `IdleTelemetryResult` model + field on `NormalizedRun`)
4. `vpn_leaks/reporting/web_exposure.py` (new `analyze_idle_telemetry()` function)
5. `vpn_leaks/reporting/templates/vpn_report_document.html.j2` (new report section)

**Implementation steps:**

1. **Add `idle` subcommand to `capture` in `cli.py`:**

   After the existing `abort` subparser (~line 782), add:
   ```python
   pst4 = csub.add_parser("idle", help="Capture app telemetry before VPN connects (requires sudo)")
   pst4.add_argument("--provider", required=True)
   pst4.add_argument("--duration", type=int, default=120, help="Seconds to capture (default: 120)")
   pst4.add_argument("-i", "--interface", default="en0")
   pst4.add_argument("-o", "--output", help="Output JSON path (default: runs/<id>/idle_telemetry.json)")
   ```

   In `cmd_capture()`, add the `idle` branch:
   ```python
   if cmd == "idle":
       from vpn_leaks.checks.idle_telemetry import run_idle_capture
       result = run_idle_capture(
           provider=args.provider,
           duration=args.duration,
           interface=args.interface,
           output=getattr(args, "output", None),
       )
       print(json.dumps(result, indent=2))
   ```

2. **Create `vpn_leaks/checks/idle_telemetry.py`:**

   ```python
   """
   Captures network traffic while the VPN app is running but not connected.
   Operator: run this AFTER launching the VPN app, BEFORE clicking connect.
   Requires sudo (tcpdump).
   """

   def run_idle_capture(
       provider: str,
       duration: int = 120,
       interface: str = "en0",
       output: str | None = None,
   ) -> dict[str, Any]:
       """
       1. Start tcpdump for `duration` seconds.
       2. Run pcap_summarize on the result.
       3. Run pcap_host_intelligence on the summary.
       4. Return structured result with all contacts attributed.
       """
   ```

   Reuse `vpn_leaks.capture.session.start()` / `abort()` for tcpdump management. Reuse `vpn_leaks.checks.pcap_summarize.summarize_pcap()` and `vpn_leaks.reporting.web_exposure.pcap_host_intelligence()` for attribution.

   Output structure:
   ```python
   {
       "provider": str,
       "duration_seconds": int,
       "captured_at": ISO8601 timestamp,
       "contacts": [  # same structure as pcap_host_intelligence rows
           {"ip": str, "asn": str, "owner": str, "bytes": int, "flows": int,
            "reverse_dns": str, "upstream_asn": str, "upstream_org": str, "sources": str}
       ],
       "summary": {
           "total_contacts": int,
           "provider_owned": int,    # contacts matching provider's org name
           "third_party": int,       # contacts not owned by provider
           "dns_resolvers": int,
       }
   }
   ```

3. **Add `IdleTelemetryResult` to `models.py`** as a Pydantic model with the fields above. Add `idle_telemetry: IdleTelemetryResult | None = None` field to `NormalizedRun`. Schema version bumps to `1.6`.

4. **In `generate_reports.py`**: When building the HTML report, load `idle_telemetry.json` from the run artifacts if present and pass it to the template.

5. **In the template:** Add an "App Idle Telemetry" collapsible section in the Network Intelligence tier. Show a table of contacts with role badges. Highlight any third-party contacts (non-provider-owned IPs) with a warning, since these represent data exposure before the user has decided to connect.

**Acceptance criteria:**
- `vpn-leaks capture idle --provider nordvpn --duration 30` runs, captures PCAP for 30 seconds, and produces a JSON file with attributed contacts.
- If the VPN app phones home during the capture window, those contacts appear in the report.
- `pytest tests -q` passes.

---

## Section D — Connected Phase: TLS and Certificate Visibility

---

### TASK-11

**TLS certificate chain capture**

**Gap it closes:** Every HTTPS connection the VPN client makes involves a TLS handshake where the server presents a certificate issued by a Certificate Authority. The issuing CA has a permanent record (via Certificate Transparency logs) that the server exists. The CA's OCSP responder sees connection attempts to revocation-check the cert. This is a less obvious but real source of third-party visibility. This task captures the TLS certificate chain for each SNI hostname contacted during the PCAP window.

**Files to create/modify:**
1. `vpn_leaks/checks/tls_probe.py` (new module)
2. `vpn_leaks/reporting/web_exposure.py` (call new probe; add CA attribution)
3. `vpn_leaks/models.py` (add `tls_chain_summary` to `NormalizedRun`)
4. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`

**Implementation steps:**

1. **Create `vpn_leaks/checks/tls_probe.py`:**

   ```python
   import ssl, socket
   from typing import Any

   def probe_tls_chain(hostname: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
       """
       Connect to hostname:port, retrieve TLS certificate chain.
       Returns {
           "hostname": str,
           "issuer_cn": str,        # e.g. "R11"
           "issuer_o": str,         # e.g. "Let's Encrypt"
           "root_ca": str,          # e.g. "ISRG Root X1"
           "ocsp_url": str | None,
           "ct_log_url": str | None,
           "valid_from": str,
           "valid_until": str,
           "error": str | None,
       }
       """
       ctx = ssl.create_default_context()
       ctx.check_hostname = False
       ctx.verify_mode = ssl.CERT_NONE
       try:
           with socket.create_connection((hostname, port), timeout=timeout) as sock:
               with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                   cert = ssock.getpeercert(binary_form=False)
                   # Parse issuer, validity, OCSP extension
                   ...
       except Exception as e:
           return {"hostname": hostname, "error": str(e)}
   ```

   For OCSP URL extraction, use `ssl.DER_cert_to_PEM_cert()` + `cryptography` library's `x509.load_pem_x509_certificate()` if available, or parse the `subjectAltName` and `authorityInfoAccess` extensions from `getpeercert()`.

2. **In `pcap_host_intelligence()` in `web_exposure.py`:** For each SNI hostname (those with `source == "pcap_sni"`), call `probe_tls_chain()` and add the result to the row:
   ```python
   if row.get("source") == "pcap_sni":
       row["tls_chain"] = probe_tls_chain(row["host"])
   ```
   Cache results in `_dc` (ip_intel.json) under `__tls_chains__` keyed by hostname.

3. **Add a `tls_chain` field** to the ip_index entries in `build_capture_workspace_rollup()`.

4. **In the template:** Add an `Issuer` mini-column in the IP table for SNI rows, showing the `issuer_o` (e.g., "Let's Encrypt", "DigiCert", "Amazon"). Add a "Certificate Authorities" KPI count: how many distinct CAs issued certificates for hosts in the capture.

**Acceptance criteria:**
- SNI rows in the IP table show a certificate issuer name.
- The `ip_intel.json` cache stores TLS chain data so re-runs don't re-probe.
- Probing failures (timeout, connection refused) are caught and stored as `{"error": "..."}` without crashing the report.

---

## Section E — Cross-Cutting: Analytics SDK Detection

---

### TASK-12

**Known analytics SDK endpoint detection from PCAP**

**Gap it closes:** VPN apps often embed analytics SDKs (Amplitude, Firebase Analytics, Segment, Sentry, Mixpanel) that transmit usage telemetry — which features were used, when, from what device — back to third-party servers. These SDK calls happen over the user's real connection before the tunnel activates and potentially over the tunnel during VPN use. The current PCAP attribution identifies IP owners but does not flag well-known SDK endpoints specifically.

**Files to modify:**
1. `vpn_leaks/reporting/web_exposure.py`
2. `vpn_leaks/reporting/templates/vpn_report_document.html.j2`

**Implementation steps:**

1. **Add `_SDK_ENDPOINT_PATTERNS` dict to `web_exposure.py`** (near `_ANALYTICS_VENDOR_PATTERNS` from TASK-03):

   ```python
   _SDK_ENDPOINT_PATTERNS: dict[str, str] = {
       "api.amplitude.com": "Amplitude (usage analytics)",
       "api2.amplitude.com": "Amplitude (usage analytics)",
       "api.segment.io": "Segment (CDP)",
       "cdn.segment.com": "Segment (CDP)",
       "firebaseinstallations.googleapis.com": "Firebase Installations",
       "firebaseremoteconfig.googleapis.com": "Firebase Remote Config",
       "app-measurement.com": "Google Analytics for Firebase",
       "sentry.io": "Sentry (crash reporting)",
       "ingest.sentry.io": "Sentry (crash reporting)",
       "api.mixpanel.com": "Mixpanel (analytics)",
       "api.appsflyer.com": "AppsFlyer (attribution)",
       "sdk.iad-01.braze.com": "Braze (CRM/messaging)",
       "logs.browser-intake-datadoghq.com": "Datadog (observability)",
       "bam.nr-data.net": "New Relic (observability)",
       "splunk.com": "Splunk (logging)",
   }
   ```

2. **In `pcap_host_intelligence()`:** After resolving the `reverse_dns` for each row, check if the hostname or IP matches any `_SDK_ENDPOINT_PATTERNS` key:
   ```python
   for pattern, sdk_name in _SDK_ENDPOINT_PATTERNS.items():
       if pattern in (row.get("reverse_dns") or "").lower() or pattern in host.lower():
           row["sdk_match"] = sdk_name
           break
   ```

3. **Propagate `sdk_match`** through `build_capture_workspace_rollup()` ip_index entries.

4. **In the template:** Flag rows with `sdk_match` set with a magenta warning badge in the IP table Role column (overriding the role classification from TASK-03). Add a summary callout at the top of the Network Intelligence section: "⚠ N analytics SDKs detected: [list]" if any `sdk_match` values exist.

**Acceptance criteria:**
- If NordVPN's PCAP contains contacts to `api.amplitude.com` or `ingest.sentry.io`, those rows are flagged in the table with the SDK name.
- No false positives on non-SDK rows.

---

## Appendix: Data Field Reference

### Fields added to `ip_index` entries across all tasks

| Field | Type | Added by | Notes |
|---|---|---|---|
| `as_path` | `str \| None` | TASK-01 | Space-separated ASN string from bgp_lookup |
| `role` | `str` | TASK-03 | One of: `vpn-control`, `vpn-data`, `provider-analytics`, `dns-resolver`, `routing-infra`, `unknown` |
| `tls_chain` | `dict \| None` | TASK-11 | SNI rows only; `{issuer_cn, issuer_o, root_ca, ocsp_url, ...}` |
| `sdk_match` | `str \| None` | TASK-12 | SDK name if matched, else absent |

### Fields added to workspace (`cw`) object

| Field | Type | Added by |
|---|---|---|
| `dns_operators` | `dict[hostname, {ns_host, ns_ip, ns_asn, ns_org}]` | TASK-04 |
| `dns_operator_count` | `int` | TASK-04 |
| `role_counts` | `dict[role_name, int]` | TASK-06 |
| `signup_exposure` | `dict` | TASK-08 |

### New `NormalizedRun` fields

| Field | Type | Added by | Schema version |
|---|---|---|---|
| `idle_telemetry` | `IdleTelemetryResult \| None` | TASK-10 | 1.6 |

### New CLI commands

| Command | Added by | Description |
|---|---|---|
| `vpn-leaks capture idle --provider <slug> --duration <s>` | TASK-10 | PCAP capture before VPN connects |
