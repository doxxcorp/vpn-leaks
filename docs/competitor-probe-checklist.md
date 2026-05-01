# `competitor_probe` checklist (per provider YAML)

Use this when filling [`configs/vpns/<slug>.yaml`](../configs/vpns/nordvpn.yaml) under `competitor_probe`. All keys are optional except that an empty section skips the phase entirely.

## `provider_domains`

Public apex domains used for **authoritative DNS** surface (NS, A, AAAA, TXT, MX, CAA in harness output).

- [ ] Primary marketing / product domain (e.g. `examplevpn.com`)
- [ ] Account / billing / SSO domain if different (e.g. `account.example.com` as apex if delegated that way)
- [ ] Support or helpdesk apex if separate and security-relevant

**Tip:** Include every apex you care to compare against policy and CDN claims.

## `probe_urls`

HTTPS URLs loaded with Playwright; **HAR** + response headers + inline `script[src]` / `img[src]` capture.

- [ ] Marketing homepage
- [ ] Public **API** base or documented JSON endpoint (e.g. `/v1/servers/count`) — shows CDN/WAF in front of API
- [ ] Status page if not under main domain
- [ ] Download or “apps” page if tracking-heavy

**Tip:** Order stable URLs first; some sites return 403 to automation (still useful as a signal).

## `portal_hosts`

Hostnames only (no scheme) for **account / login** portals.

- [ ] Web account portal (e.g. `my.account.example.com`)
- [ ] Business or team dashboard host if different

Harness resolves A/AAAA and issues HTTPS GET for CDN header signals.

## `stray_json`

Low-rate GET of optional paths on given **origins** (scheme + host).

- [ ] `origins`: `https://examplevpn.com`, `https://my.account.example.com`
- [ ] `paths`: `/data.json`, `/config.json`, or provider-specific paths you expect to exist

**Tip:** Keep the list small; these are best-effort probes, not a crawler.

## Policy and status (outside `competitor_probe`)

Not part of `competitor_probe`, but align runs with the same provider story:

- [ ] `policy_urls` / `underlay_policy_urls` for legal text used in `policies` capture
- [ ] Document any **status** or **trust** subdomain in `probe_urls` or `provider_domains` if you need them in the graph

## Run flags (CLI)

Skip individual phases when debugging:

- `--skip-competitor-dns` — apex DNS + NS glue
- `--skip-competitor-web` — Playwright + HAR
- `--skip-competitor-portal` — portal DNS + HTTPS
- `--skip-competitor-transit` — traceroute toward exit IP
- `--skip-competitor-stray-json` — stray path GETs

## After `vpn-leaks run`: website exposure (automated + optional desk)

Two layers:

1. **Harness `competitor_probe`** writes **OBSERVED (O)** artifacts (below): apex DNS (**`provider_dns.json`**: NS/A/AAAA/TXT/MX/CAA, NS glue + attribution), web/HAR, portals, transit. That is **not** client DNS leak evidence while connected (**DNS-001** lives in **`dnsleak/`**).

2. **Automated `website_exposure_methodology`** (same run, **`normalized.json`**) performs a **desk automation** projection—including SPF walks, DMARC/DKIM/TXT probing, subdomain CNAME scan, and **`phase9_third_party_inventory`**—tiered distinctly from **tunnel DNS leak tests** (read **`evidence_tier_note`** in JSON). Deep raw detail also under **`raw/<location>/website_exposure/`** when emitted.

**Phase mapping**

| Layer | Harness (O) — `competitor_surface` | Desk automation — `website_exposure_methodology` | Manual desk (S) — optional deepening |
|-------|------------------------------------|--------------------------------------------------|---------------------------------------|
| Page load, HAR, hosts | `probe_urls`, `surface_urls` → `har/`, `har_summary.json` | Uses merged host inventory | Phases 1–7 interpretation + archival narrative |
| Apex / infra DNS | `provider_dns.json` (authoritative lookups) | **Phase 8** (`phase8_dns_infra` / SPF, DMARC, DKIM probes, …) layered on apex | Full **`dig`** transcript archive if needed |
| Third-party inventory | HAR-derived hints inside `competitor_surface` | **Phase 9** (`phase9_third_party_inventory`) | Combine with manual SPEC narrative |

Manual checklist (**optional**):

- [ ] For each apex in `provider_domains`, extend with handwritten **Phase 8–9** transcript or paste [scripts/desk_dns_audit.sh](../scripts/desk_dns_audit.sh) output when automation **`limits`/errors** require narrative **S**.
- [ ] Archive dated transcript: `research/desk-<date>-<apex>.txt` (or equivalent).
- [ ] In reports, distinguish **O** (harness probes + `dnsleak/`), desk automation (**`website_exposure_methodology`**), and manual **S**; **never** cite apex MX/SPF/DMARC automation as tunnel **DNS leak** (**DNS-001**).

## Artifacts written

Under `runs/<run_id>/raw/<location_id>/competitor_probe/`:

| File | Role |
|------|------|
| `provider_dns.json` | Apex NS/A/AAAA/TXT/MX/CAA; NS glue + attribution |
| `web_probes.json` | Per-URL status, CDN headers, script/image lists |
| `har/*.har` | Full network capture for each `probe_url` |
| `har_summary.json` | Aggregated unique request hosts + tracker/CDN hints from HARs |
| `portal_probes.json` | Portal DNS + HTTPS headers |
| `transit.json` | Traceroute toward exit IPv4 |
| `stray_json.json` | Stray path probes |
