# bgp.tools — integration notes for this project

This document captures how [bgp.tools](https://bgp.tools) relates to the harness and what to verify before **automating** or **bulk-fetching** data.

## What the site offers (public UI)

- **Visitor snapshot:** Connecting IP, covering **prefix**, **ASN**, and org name with links to `/prefix/...` and `/as/<asn>` pages.
- **Super Looking Glass:** [super-lg](https://bgp.tools/super-lg) — query BGP views from collectors; CIDR search and ASN filters.
- **Data products:** Near–real-time BGP, WHOIS-backed records, PeeringDB-derived data, RDNS/anycast tooling (see their `/features` page for refresh intervals).

## Recommended use in vpn-leaks (today)

- **Deep links in reports:** Given an exit IP or merged ASN from [`merge_attribution`](../vpn_leaks/attribution/merge.py), link readers to:
  - `https://bgp.tools/prefix/<prefix>` when you have a covering prefix (e.g. from RIPEstat or Cymru).
  - `https://bgp.tools/as/<asn>` for the attributed ASN.
- **Manual research:** Use Super LG to inspect paths/peers when investigating a specific exit or ASN; results are **not** stored automatically by the harness.

## Automation, ToS, and rate limits

- **Do not** scrape heavy AS pages from CI without reading [bgp.tools](https://bgp.tools) **Terms of Service** / acceptable use and any **rate-limit** guidance. Pages can be slow; automated parallel requests may be blocked.
- Prefer **official APIs** where offered (including paid monitoring products) over HTML scraping for production pipelines.
- **Caching:** If you add fetchers later, use aggressive caching and backoff; ASN/prefix data does not need per-second freshness for benchmark runs.

## Relationship to harness data

- **RIPEstat** (used in-repo) and **Team Cymru** provide authoritative-style prefix/ASN mapping; bgp.tools is useful for **human exploration** and **cross-check**, not as the sole source of truth.
- **Announced prefixes** for an ASN are available in-repo via RIPEstat `announced-prefixes` (see `asn_prefixes.json` per run), which can be compared mentally to bgp.tools AS views.
