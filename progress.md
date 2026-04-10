# VPN Leaks — project progress

_Last updated: 2026-04-09._

## Where the project stands

The **VPN Leaks harness is implemented and usable end-to-end** in this repository:

- **CLI:** `vpn-leaks run` and `vpn-leaks report` (install with `pip install -e ".[dev]"`, Playwright Chromium for WebRTC).
- **Preflight:** Each run resolves exit IPv4 first, skips duplicate benchmarks for the same provider + exit IP unless `--force`, and (by default) **auto-detects** location id/label via ipwho.is when `--locations` is omitted.
- **Suite per location:** Multi-source exit IP, DNS (local + IPLeak HTML), IPv6 (curl + test-ipv6 page), WebRTC (Playwright ICE), optional fingerprint, **RIPEstat + Team Cymru + PeeringDB** attribution, **privacy policy** fetch + SHA-256 + keyword summary ([vpn_leaks/policy/fetch_policy.py](vpn_leaks/policy/fetch_policy.py): browser-like httpx headers; **Playwright** when the response is a Cloudflare interstitial or a thin JS shell such as Nord Account; Nord config uses [my.nordaccount.com legal privacy URL](https://my.nordaccount.com/legal/privacy-policy/) because `nordvpn.com/privacy-policy/` is often blocked for automated clients).
- **Artifacts:** Under `runs/<run_id>/` (gitignored): `run.json`, `raw/preflight.json`, per-location `raw/<location_id>/` (ip-check, dnsleak, webrtc, ipv6, attribution, policy HTML), and `locations/<location_id>/normalized.json`.
- **Docs:** [README.md](README.md), [docs/spec.md](docs/spec.md), [docs/methodology.md](docs/methodology.md), [docs/data-dictionary.md](docs/data-dictionary.md), canonical [vpn-leaks.md](vpn-leaks.md).

**Not in scope for the harness itself:** Proving what NordVPN stores on servers; automating the Nord macOS app (you connect manually, then `vpn-leaks run --provider nordvpn --skip-vpn`).

---

## NordVPN benchmark runs you collected

You ran **`vpn-leaks run --provider nordvpn --skip-vpn`** (auto location) after switching the **NordVPN macOS client** to each destination. That produced **five separate run directories** — one **location / exit** per run — listed **oldest to newest** below.

| # | Run id (folder under `runs/`) | Auto location id | Label (ipwho) | Exit IPv4 | Exit ASN | ASN holder (attribution) | DNS leak | WebRTC leak | IPv6 leak |
|---|------------------------------|------------------|-----------------|-----------|----------|---------------------------|----------|-------------|-----------|
| 1 | `nordvpn-20260410T014115Z-192ddf81` | `us-california-san-francisco-67` | San Francisco, California, United States | 185.187.168.67 | 212238 | CDNEXT - Datacamp Limited | false | false | false |
| 2 | `nordvpn-20260410T020850Z-06046ac5` | `gb-england-london-102` | London, England, United Kingdom | 2.58.73.102 | 62240 | CLOUVIDER - Clouvider Limited | false | false | false |
| 3 | `nordvpn-20260410T020935Z-8559f9bc` | `ca-british-columbia-vancouver-153` | Vancouver, British Columbia, Canada | 45.90.222.153 | 147049 | PACKETHUBSA-AS-AP PacketHub S.A. | false | false | false |
| 4 | `nordvpn-20260410T021013Z-3db4d1ec` | `de-hamburg-hamburg-127` | Hamburg, Hamburg, Germany | 185.161.202.127 | 207137 | PACKETHUBSA - PacketHub S.A. | false | false | false |
| 5 | `nordvpn-20260410T021116Z-5cf8e0dc` | `us-new-mexico-albuquerque-136` | Albuquerque, New Mexico, United States | 66.179.156.136 | 136787 | PACKETHUBSA-AS-AP PacketHub S.A. | false | false | false |

**What each run stored (per location):**

- **`normalized.json`:** Full structured record: `exit_ip_sources`, `dns_servers_observed`, WebRTC candidates, IPv6 status, `attribution` (confidence + sources), `policies` (Nord privacy URL + content hash + heuristic bullets), `services_contacted`, `extra.exit_geo` (ipwho snapshot when auto-location was used).
- **`raw/<location_id>/`:** `ip-check.json`, `dnsleak/` (e.g. `ipleak_dns.html`, `dns_summary.json`), `webrtc/webrtc_candidates.json`, `ipv6/` (curl output, test-ipv6 HTML, summary JSON), `attribution.json`, `policy/` (fetched HTML).
- **`raw/preflight.json`:** Preflight IPv4 and whether auto-location was used for that run.

**Config updated:** [configs/vpns/nordvpn.yaml](configs/vpns/nordvpn.yaml) now lists the six location entries (including the older `sf-usa` placeholder) plus the five auto-derived ids above.

**Aggregated markdown reports:** Generate locally with `vpn-leaks report --provider nordvpn` (writes under `VPNs/`, gitignored by default). Underlay-specific report: `vpn-leaks report --provider nordvpn --asn <asn>` if you want a file per ASN.

**Historical note (2026-04-10 runs):** Those five `normalized.json` files record **`fetch error: 403`** for the old policy URL (`https://nordvpn.com/privacy-policy/`). New runs after the fetch + config change above should populate `policies[].sha256` and keyword bullets; re-run benchmarks if you need on-disk policy HTML under `raw/.../policy/` for Nord.

---

## Quick reference paths

```text
runs/nordvpn-20260410T014115Z-192ddf81/locations/us-california-san-francisco-67/normalized.json
runs/nordvpn-20260410T020850Z-06046ac5/locations/gb-england-london-102/normalized.json
runs/nordvpn-20260410T020935Z-8559f9bc/locations/ca-british-columbia-vancouver-153/normalized.json
runs/nordvpn-20260410T021013Z-3db4d1ec/locations/de-hamburg-hamburg-127/normalized.json
runs/nordvpn-20260410T021116Z-5cf8e0dc/locations/us-new-mexico-albuquerque-136/normalized.json
```

If you delete `runs/` later, this table is the snapshot of what was collected on **2026-04-10**; re-run the commands above to regenerate data.
