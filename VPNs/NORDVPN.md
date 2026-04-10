# NordVPN (nordvpn)

- **Report generated:** 2026-04-10T23:16:49.726379+00:00
- **Runs included:** nordvpn-20260410T221659Z-5dfe011f
- **Normalized locations:** 1

## Matrix

| Field | Value |
|-------|-------|
| Connection modes observed | manual_gui |
| Locations covered | 1 |

## Leak summary

| Location | DNS leak | WebRTC leak | IPv6 leak |
|----------|----------|-------------|-----------|
| Santa Clara, California, United States | False | False | False |


## Underlay (ASNs)


- **AS141039:** PACKETHUBSA-AS-AP PacketHub S.A.


---

## Detailed runs

Each section mirrors `normalized.json`. Large API blobs (**attribution**, **competitor_surface**) use generous caps; if anything still hits the safety limit, see **Complete normalized record** at the bottom of each run (verbatim JSON, up to ~2 MiB).



### nordvpn-20260410T221659Z-5dfe011f / us-california-santa-clara-160

- **vpn_provider:** nordvpn
- **Label:** Santa Clara, California, United States
- **Path:** `runs/nordvpn-20260410T221659Z-5dfe011f/locations/us-california-santa-clara-160/normalized.json`
- **schema_version:** 1.2
- **timestamp_utc:** 2026-04-10T22:18:59.196360+00:00
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
| exit_ip_v4 | 185.169.0.160 |
| exit_ip_v6 | None |

**exit_ip_sources**

```json
[
  {
    "url": "https://api.ipify.org",
    "ipv4": "185.169.0.160",
    "ipv6": null,
    "raw_excerpt": "185.169.0.160",
    "error": null
  },
  {
    "url": "https://api64.ipify.org",
    "ipv4": "185.169.0.160",
    "ipv6": null,
    "raw_excerpt": "185.169.0.160",
    "error": null
  },
  {
    "url": "https://api.ipify.org?format=json",
    "ipv4": "185.169.0.160",
    "ipv6": null,
    "raw_excerpt": "{\"ip\":\"185.169.0.160\"}",
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
      "185.169.0.156"
    ]
  },
  {
    "tier": "external",
    "detail": "ipleak_dns",
    "servers": [
      "185.169.0.160"
    ]
  }
]
```

#### WebRTC

| Field | Value |
|-------|-------|
| webrtc_leak_flag | False |
| webrtc_notes | Exit IP appears in candidate set (expected for tunneled public) |



| type | protocol | address | port | raw (truncated) |
|------|----------|---------|------|-----------------|
| host | udp | 3a9dc72f-16c2-4ed4-b37a-1599824e6884.local | 60346 | `candidate:1711279333 1 udp 2113937151 3a9dc72f-16c2-4ed4-b37a-1599824e6884.local 60346 typ host generation 0 ufrag CHPW network-cost 999` |
| srflx | udp | 185.169.0.160 | 45967 | `candidate:1937844965 1 udp 1677729535 185.169.0.160 45967 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag CHPW network-cost 999` |


#### IPv6

| Field | Value |
|-------|-------|
| ipv6_status | unsupported_or_no_ipv6 |
| ipv6_leak_flag | False |
| ipv6_notes | No IPv6 observed via curl or IP endpoints |

#### Fingerprint


*(empty)*


#### Attribution

```json
{
  "asn": 141039,
  "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
  "country": null,
  "confidence": 0.7,
  "confidence_notes": "ASNs seen: [141039]",
  "supporting_sources": [
    {
      "name": "ripestat",
      "asn": 141039,
      "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
      "country": null,
      "raw": {
        "prefix_overview": {
          "messages": [
            [
              "warning",
              "Given resource is not announced but result has been aligned to first-level less-specific (185.169.0.0/24)."
            ]
          ],
          "see_also": [],
          "version": "1.3",
          "data_call_name": "prefix-overview",
          "data_call_status": "supported",
          "cached": false,
          "query_id": "20260410221717-93701f96-6a6c-49f1-b1ec-bcc2210c2b50",
          "process_time": 78,
          "server_id": "app162",
          "build_version": "v0.9.7-thriftpy2-2026.04.10",
          "pipeline": "1223136",
          "status": "ok",
          "status_code": 200,
          "time": "2026-04-10T22:17:17.626675",
          "data": {
            "is_less_specific": true,
            "announced": true,
            "asns": [
              {
                "asn": 141039,
                "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
              }
            ],
            "related_prefixes": [],
            "resource": "185.169.0.0/24",
            "type": "prefix",
            "block": {
              "resource": "185.0.0.0/8",
              "desc": "RIPE NCC (Status: ALLOCATED)",
              "name": "IANA IPv4 Address Space Registry"
            },
            "actual_num_related": 0,
            "query_time": "2026-04-10T16:00:00",
            "num_filtered_out": 0
          }
        }
      }
    },
    {
      "name": "team_cymru",
      "asn": 141039,
      "holder": null,
      "country": null,
      "raw": {
        "asn": 141039,
        "raw_line": "141039 | 185.169.0.0/24 | DE | ripencc | 2016-09-20",
        "parts": [
          "141039",
          "185.169.0.0/24",
          "DE",
          "ripencc",
          "2016-09-20"
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
            "id": 25841,
            "org_id": 28491,
            "name": "PacketHub AS141039",
            "aka": "",
            "name_long": "",
            "website": "https://www.packethub.net/",
            "social_media": [
              {
                "service": "website",
                "identifier": "https://www.packethub.net/"
              }
            ],
            "asn": 141039,
            "looking_glass": "",
            "route_server": "",
            "irr_as_set": "APNIC::AS-PACKETHUB",
            "info_type": "",
            "info_types": [],
            "info_prefixes4": 5000,
            "info_prefixes6": 5000,
            "info_traffic": "",
            "info_ratio": "Not Disclosed",
            "info_scope": "Global",
            "info_unicast": true,
            "info_multicast": false,
            "info_ipv6": false,
            "info_never_via_route_servers": false,
            "ix_count": 3,
            "fac_count": 5,
            "notes": "",
            "netixlan_updated": "2021-11-08T09:10:50Z",
            "netfac_updated": "2021-09-30T12:02:07Z",
            "poc_updated": "2022-10-06T09:30:24Z",
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
            "created": "2021-02-01T12:14:24Z",
            "updated": "2024-07-04T10:29:30Z",
            "status": "ok"
          }
        ],
        "meta": {}
      }
    }
  ],
  "disclaimers": [
    "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
  ]
}
```

#### Policies

```json
[
  {
    "role": "vpn",
    "url": "https://my.nordaccount.com/legal/privacy-policy/",
    "fetched_at_utc": "2026-04-10T22:17:21.272920+00:00",
    "sha256": "897b30f99923471c6b1bbf590dab5cd88b9f632fa4ea34049d3c911bdd2261e6",
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




- `competitor_probe:enabled`

- `dns:lookup:nordaccount.com`

- `dns:lookup:nordvpn.com`

- `https://api.ipify.org`

- `https://api.ipify.org?format=json`

- `https://api.nordvpn.com/v1/servers/count`

- `https://api64.ipify.org`

- `https://ipleak.net/`

- `https://ipwho.is/185.169.0.160`

- `https://my.nordaccount.com/`

- `https://my.nordaccount.com/config.json`

- `https://my.nordaccount.com/data.json`

- `https://my.nordaccount.com/legal/privacy-policy/`

- `https://nordvpn.com/`

- `https://nordvpn.com/config.json`

- `https://nordvpn.com/data.json`

- `https://test-ipv6.com/`

- `policy:playwright_chromium`

- `transit:local_traceroute`

- `webrtc:local_playwright_chromium`

- `yourinfo.ai:playwright_chromium`


#### Artifacts (paths)

```json
{
  "connect_log": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/connect.log",
  "ip_check_json": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/ip-check.json",
  "dnsleak_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/dnsleak",
  "webrtc_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/webrtc",
  "ipv6_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/ipv6",
  "fingerprint_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/fingerprint",
  "attribution_json": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/attribution.json",
  "policy_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/policy",
  "competitor_probe_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe",
  "yourinfo_probe_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/yourinfo_probe"
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
  "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/yourinfo_probe/yourinfo.har",
  "cdn_headers": {},
  "error": null
}
```

**Visible text excerpt** (may be truncated in this report):

~~~
RESEARCHING YOUR INFORMATION...
20
Querying intelligence databases...

Concerned about your digital privacy?

doxx.net - Secure networking for humans
 
~~~




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
        "error": null
      },
      "nordaccount.com": {
        "ns": [
          "lily.ns.cloudflare.com",
          "seth.ns.cloudflare.com"
        ],
        "a": [
          "104.18.42.225",
          "172.64.145.31"
        ],
        "aaaa": [
          "2a06:98c1:3101::6812:2ae1",
          "2a06:98c1:3107::ac40:911f"
        ],
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
        "cf-ray": "9ea52160ccd2c8bd-SJC",
        "server": "cloudflare"
      },
      "scripts": [
        "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ea52160ccd2c8bd"
      ],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe/har/d945f098fbd5bb50.har"
    },
    {
      "url": "https://api.nordvpn.com/v1/servers/count",
      "error": null,
      "status": 200,
      "final_url": "https://api.nordvpn.com/v1/servers/count",
      "cdn_headers": {
        "cf-ray": "9ea52161da8525c3-SJC",
        "server": "cloudflare"
      },
      "scripts": [],
      "images": [],
      "captcha_third_party": false,
      "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe/har/5396776ec51664e8.har"
    }
  ],
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
        "cf-ray": "9ea5216459d74c7c-SJC",
        "server": "cloudflare"
      },
      "error": null
    }
  ],
  "transit": {
    "target": "185.169.0.160",
    "command": [
      "traceroute",
      "-n",
      "-m",
      "15",
      "-w",
      "2",
      "185.169.0.160"
    ],
    "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
    "stderr": "traceroute to 185.169.0.160 (185.169.0.160), 15 hops max, 40 byte packets\n",
    "hops": [],
    "returncode": 0
  },
  "stray_json": [
    {
      "url": "https://nordvpn.com/data.json",
      "status": 403,
      "content_type": "text/html; charset=UTF-8",
      "body_excerpt": "<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\"><meta name=\"robots\" content=\"noindex,nofollow\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>*{box-sizing:border-box;margin:0;padding:0}html{line-height:1.15;-webkit-text-size-adjust:100%;color:#313131;font-family:system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,\"Noto Sans\",sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\",\"Noto Color Emoji\"}body{display:flex;flex-direction:column;height:100vh;min-height:100vh}.main-content{margin:8rem auto;padding-left:1.5rem;max-width:60rem}@media (width <= 720px){.main-content{margin-top:"
    },
    {
      "url": "https://nordvpn.com/config.json",
      "status": 403,
      "content_type": "text/html; charset=UTF-8",
      "body_excerpt": "<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\"><meta name=\"robots\" content=\"noindex,nofollow\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>*{box-sizing:border-box;margin:0;padding:0}html{line-height:1.15;-webkit-text-size-adjust:100%;color:#313131;font-family:system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,\"Noto Sans\",sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\",\"Noto Color Emoji\"}body{display:flex;flex-direction:column;height:100vh;min-height:100vh}.main-content{margin:8rem auto;padding-left:1.5rem;max-width:60rem}@media (width <= 720px){.main-content{margin-top:"
    },
    {
      "url": "https://my.nordaccount.com/data.json",
      "status": 403,
      "content_type": "text/html; charset=UTF-8",
      "body_excerpt": "<!DOCTYPE html>\n<!--[if lt IE 7]> <html class=\"no-js ie6 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 7]>    <html class=\"no-js ie7 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 8]>    <html class=\"no-js ie8 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class=\"no-js\" lang=\"en-US\"> <!--<![endif]-->\n<head>\n<title>Attention Required! | Cloudflare</title>\n<meta charset=\"UTF-8\" />\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\" />\n<meta name=\"robots\" content=\"noindex, nofollow\" />\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n<link rel=\"stylesheet\" id=\"cf_styles-css\" href=\"/cdn-cgi/styles/cf.errors.css\" />\n<!--[if lt IE 9]><link rel=\"stylesheet\" id='cf_styles-ie-css' href=\"/cdn-cgi"
    },
    {
      "url": "https://my.nordaccount.com/config.json",
      "status": 403,
      "content_type": "text/html; charset=UTF-8",
      "body_excerpt": "<!DOCTYPE html>\n<!--[if lt IE 7]> <html class=\"no-js ie6 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 7]>    <html class=\"no-js ie7 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 8]>    <html class=\"no-js ie8 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class=\"no-js\" lang=\"en-US\"> <!--<![endif]-->\n<head>\n<title>Attention Required! | Cloudflare</title>\n<meta charset=\"UTF-8\" />\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\" />\n<meta name=\"robots\" content=\"noindex, nofollow\" />\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n<link rel=\"stylesheet\" id=\"cf_styles-css\" href=\"/cdn-cgi/styles/cf.errors.css\" />\n<!--[if lt IE 9]><link rel=\"stylesheet\" id='cf_styles-ie-css' href=\"/cdn-cgi"
    }
  ],
  "errors": []
}
```


#### Extra

```json
{
  "exit_geo": {
    "source": "ipwho.is",
    "ip": "185.169.0.160",
    "country_code": "US",
    "region": "California",
    "city": "Santa Clara",
    "connection": {
      "asn": 141039,
      "org": "Packethub S.A.",
      "isp": "Packethub S.A.",
      "domain": "packethub.net"
    },
    "location_id": "us-california-santa-clara-160",
    "location_label": "Santa Clara, California, United States"
  }
}
```

#### Complete normalized record (verbatim)

Full JSON for this location (same as `normalized.json`; capped only at ~2 MiB for safety).

```json
{
  "schema_version": "1.2",
  "run_id": "nordvpn-20260410T221659Z-5dfe011f",
  "timestamp_utc": "2026-04-10T22:18:59.196360+00:00",
  "runner_env": {
    "os": "Darwin 25.4.0",
    "kernel": "25.4.0",
    "python": "3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 10:07:17) [Clang 14.0.6 ]",
    "browser": null,
    "vpn_protocol": "manual_gui",
    "vpn_client": null
  },
  "vpn_provider": "nordvpn",
  "vpn_location_id": "us-california-santa-clara-160",
  "vpn_location_label": "Santa Clara, California, United States",
  "connection_mode": "manual_gui",
  "exit_ip_v4": "185.169.0.160",
  "exit_ip_v6": null,
  "exit_ip_sources": [
    {
      "url": "https://api.ipify.org",
      "ipv4": "185.169.0.160",
      "ipv6": null,
      "raw_excerpt": "185.169.0.160",
      "error": null
    },
    {
      "url": "https://api64.ipify.org",
      "ipv4": "185.169.0.160",
      "ipv6": null,
      "raw_excerpt": "185.169.0.160",
      "error": null
    },
    {
      "url": "https://api.ipify.org?format=json",
      "ipv4": "185.169.0.160",
      "ipv6": null,
      "raw_excerpt": "{\"ip\":\"185.169.0.160\"}",
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
        "185.169.0.156"
      ]
    },
    {
      "tier": "external",
      "detail": "ipleak_dns",
      "servers": [
        "185.169.0.160"
      ]
    }
  ],
  "dns_leak_flag": false,
  "dns_leak_notes": "Heuristic: no obvious public resolver IPs parsed from external page",
  "webrtc_candidates": [
    {
      "candidate_type": "host",
      "protocol": "udp",
      "address": "3a9dc72f-16c2-4ed4-b37a-1599824e6884.local",
      "port": 60346,
      "raw": "candidate:1711279333 1 udp 2113937151 3a9dc72f-16c2-4ed4-b37a-1599824e6884.local 60346 typ host generation 0 ufrag CHPW network-cost 999"
    },
    {
      "candidate_type": "srflx",
      "protocol": "udp",
      "address": "185.169.0.160",
      "port": 45967,
      "raw": "candidate:1937844965 1 udp 1677729535 185.169.0.160 45967 typ srflx raddr 0.0.0.0 rport 0 generation 0 ufrag CHPW network-cost 999"
    }
  ],
  "webrtc_leak_flag": false,
  "webrtc_notes": "Exit IP appears in candidate set (expected for tunneled public)",
  "ipv6_status": "unsupported_or_no_ipv6",
  "ipv6_leak_flag": false,
  "ipv6_notes": "No IPv6 observed via curl or IP endpoints",
  "fingerprint_snapshot": {},
  "attribution": {
    "asn": 141039,
    "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
    "country": null,
    "confidence": 0.7,
    "confidence_notes": "ASNs seen: [141039]",
    "supporting_sources": [
      {
        "name": "ripestat",
        "asn": 141039,
        "holder": "PACKETHUBSA-AS-AP PacketHub S.A.",
        "country": null,
        "raw": {
          "prefix_overview": {
            "messages": [
              [
                "warning",
                "Given resource is not announced but result has been aligned to first-level less-specific (185.169.0.0/24)."
              ]
            ],
            "see_also": [],
            "version": "1.3",
            "data_call_name": "prefix-overview",
            "data_call_status": "supported",
            "cached": false,
            "query_id": "20260410221717-93701f96-6a6c-49f1-b1ec-bcc2210c2b50",
            "process_time": 78,
            "server_id": "app162",
            "build_version": "v0.9.7-thriftpy2-2026.04.10",
            "pipeline": "1223136",
            "status": "ok",
            "status_code": 200,
            "time": "2026-04-10T22:17:17.626675",
            "data": {
              "is_less_specific": true,
              "announced": true,
              "asns": [
                {
                  "asn": 141039,
                  "holder": "PACKETHUBSA-AS-AP PacketHub S.A."
                }
              ],
              "related_prefixes": [],
              "resource": "185.169.0.0/24",
              "type": "prefix",
              "block": {
                "resource": "185.0.0.0/8",
                "desc": "RIPE NCC (Status: ALLOCATED)",
                "name": "IANA IPv4 Address Space Registry"
              },
              "actual_num_related": 0,
              "query_time": "2026-04-10T16:00:00",
              "num_filtered_out": 0
            }
          }
        }
      },
      {
        "name": "team_cymru",
        "asn": 141039,
        "holder": null,
        "country": null,
        "raw": {
          "asn": 141039,
          "raw_line": "141039 | 185.169.0.0/24 | DE | ripencc | 2016-09-20",
          "parts": [
            "141039",
            "185.169.0.0/24",
            "DE",
            "ripencc",
            "2016-09-20"
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
              "id": 25841,
              "org_id": 28491,
              "name": "PacketHub AS141039",
              "aka": "",
              "name_long": "",
              "website": "https://www.packethub.net/",
              "social_media": [
                {
                  "service": "website",
                  "identifier": "https://www.packethub.net/"
                }
              ],
              "asn": 141039,
              "looking_glass": "",
              "route_server": "",
              "irr_as_set": "APNIC::AS-PACKETHUB",
              "info_type": "",
              "info_types": [],
              "info_prefixes4": 5000,
              "info_prefixes6": 5000,
              "info_traffic": "",
              "info_ratio": "Not Disclosed",
              "info_scope": "Global",
              "info_unicast": true,
              "info_multicast": false,
              "info_ipv6": false,
              "info_never_via_route_servers": false,
              "ix_count": 3,
              "fac_count": 5,
              "notes": "",
              "netixlan_updated": "2021-11-08T09:10:50Z",
              "netfac_updated": "2021-09-30T12:02:07Z",
              "poc_updated": "2022-10-06T09:30:24Z",
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
              "created": "2021-02-01T12:14:24Z",
              "updated": "2024-07-04T10:29:30Z",
              "status": "ok"
            }
          ],
          "meta": {}
        }
      }
    ],
    "disclaimers": [
      "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs."
    ]
  },
  "policies": [
    {
      "role": "vpn",
      "url": "https://my.nordaccount.com/legal/privacy-policy/",
      "fetched_at_utc": "2026-04-10T22:17:21.272920+00:00",
      "sha256": "897b30f99923471c6b1bbf590dab5cd88b9f632fa4ea34049d3c911bdd2261e6",
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
    "competitor_probe:enabled",
    "dns:lookup:nordaccount.com",
    "dns:lookup:nordvpn.com",
    "https://api.ipify.org",
    "https://api.ipify.org?format=json",
    "https://api.nordvpn.com/v1/servers/count",
    "https://api64.ipify.org",
    "https://ipleak.net/",
    "https://ipwho.is/185.169.0.160",
    "https://my.nordaccount.com/",
    "https://my.nordaccount.com/config.json",
    "https://my.nordaccount.com/data.json",
    "https://my.nordaccount.com/legal/privacy-policy/",
    "https://nordvpn.com/",
    "https://nordvpn.com/config.json",
    "https://nordvpn.com/data.json",
    "https://test-ipv6.com/",
    "policy:playwright_chromium",
    "transit:local_traceroute",
    "webrtc:local_playwright_chromium",
    "yourinfo.ai:playwright_chromium"
  ],
  "artifacts": {
    "connect_log": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/connect.log",
    "ip_check_json": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/ip-check.json",
    "dnsleak_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/dnsleak",
    "webrtc_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/webrtc",
    "ipv6_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/ipv6",
    "fingerprint_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/fingerprint",
    "attribution_json": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/attribution.json",
    "policy_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/policy",
    "competitor_probe_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe",
    "yourinfo_probe_dir": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/yourinfo_probe"
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
          "error": null
        },
        "nordaccount.com": {
          "ns": [
            "lily.ns.cloudflare.com",
            "seth.ns.cloudflare.com"
          ],
          "a": [
            "104.18.42.225",
            "172.64.145.31"
          ],
          "aaaa": [
            "2a06:98c1:3101::6812:2ae1",
            "2a06:98c1:3107::ac40:911f"
          ],
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
          "cf-ray": "9ea52160ccd2c8bd-SJC",
          "server": "cloudflare"
        },
        "scripts": [
          "https://nordvpn.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1?ray=9ea52160ccd2c8bd"
        ],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe/har/d945f098fbd5bb50.har"
      },
      {
        "url": "https://api.nordvpn.com/v1/servers/count",
        "error": null,
        "status": 200,
        "final_url": "https://api.nordvpn.com/v1/servers/count",
        "cdn_headers": {
          "cf-ray": "9ea52161da8525c3-SJC",
          "server": "cloudflare"
        },
        "scripts": [],
        "images": [],
        "captcha_third_party": false,
        "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/competitor_probe/har/5396776ec51664e8.har"
      }
    ],
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
          "cf-ray": "9ea5216459d74c7c-SJC",
          "server": "cloudflare"
        },
        "error": null
      }
    ],
    "transit": {
      "target": "185.169.0.160",
      "command": [
        "traceroute",
        "-n",
        "-m",
        "15",
        "-w",
        "2",
        "185.169.0.160"
      ],
      "stdout": " 1  * * *\n 2  * * *\n 3  * * *\n 4  * * *\n 5  * * *\n 6  * * *\n 7  * * *\n 8  * * *\n 9  * * *\n10  * * *\n11  * * *\n12  * * *\n13  * * *\n14  * * *\n15  * * *\n",
      "stderr": "traceroute to 185.169.0.160 (185.169.0.160), 15 hops max, 40 byte packets\n",
      "hops": [],
      "returncode": 0
    },
    "stray_json": [
      {
        "url": "https://nordvpn.com/data.json",
        "status": 403,
        "content_type": "text/html; charset=UTF-8",
        "body_excerpt": "<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\"><meta name=\"robots\" content=\"noindex,nofollow\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>*{box-sizing:border-box;margin:0;padding:0}html{line-height:1.15;-webkit-text-size-adjust:100%;color:#313131;font-family:system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,\"Noto Sans\",sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\",\"Noto Color Emoji\"}body{display:flex;flex-direction:column;height:100vh;min-height:100vh}.main-content{margin:8rem auto;padding-left:1.5rem;max-width:60rem}@media (width <= 720px){.main-content{margin-top:"
      },
      {
        "url": "https://nordvpn.com/config.json",
        "status": 403,
        "content_type": "text/html; charset=UTF-8",
        "body_excerpt": "<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title><meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\"><meta name=\"robots\" content=\"noindex,nofollow\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>*{box-sizing:border-box;margin:0;padding:0}html{line-height:1.15;-webkit-text-size-adjust:100%;color:#313131;font-family:system-ui,-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,\"Noto Sans\",sans-serif,\"Apple Color Emoji\",\"Segoe UI Emoji\",\"Segoe UI Symbol\",\"Noto Color Emoji\"}body{display:flex;flex-direction:column;height:100vh;min-height:100vh}.main-content{margin:8rem auto;padding-left:1.5rem;max-width:60rem}@media (width <= 720px){.main-content{margin-top:"
      },
      {
        "url": "https://my.nordaccount.com/data.json",
        "status": 403,
        "content_type": "text/html; charset=UTF-8",
        "body_excerpt": "<!DOCTYPE html>\n<!--[if lt IE 7]> <html class=\"no-js ie6 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 7]>    <html class=\"no-js ie7 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 8]>    <html class=\"no-js ie8 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class=\"no-js\" lang=\"en-US\"> <!--<![endif]-->\n<head>\n<title>Attention Required! | Cloudflare</title>\n<meta charset=\"UTF-8\" />\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\" />\n<meta name=\"robots\" content=\"noindex, nofollow\" />\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n<link rel=\"stylesheet\" id=\"cf_styles-css\" href=\"/cdn-cgi/styles/cf.errors.css\" />\n<!--[if lt IE 9]><link rel=\"stylesheet\" id='cf_styles-ie-css' href=\"/cdn-cgi"
      },
      {
        "url": "https://my.nordaccount.com/config.json",
        "status": 403,
        "content_type": "text/html; charset=UTF-8",
        "body_excerpt": "<!DOCTYPE html>\n<!--[if lt IE 7]> <html class=\"no-js ie6 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 7]>    <html class=\"no-js ie7 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if IE 8]>    <html class=\"no-js ie8 oldie\" lang=\"en-US\"> <![endif]-->\n<!--[if gt IE 8]><!--> <html class=\"no-js\" lang=\"en-US\"> <!--<![endif]-->\n<head>\n<title>Attention Required! | Cloudflare</title>\n<meta charset=\"UTF-8\" />\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" />\n<meta http-equiv=\"X-UA-Compatible\" content=\"IE=Edge\" />\n<meta name=\"robots\" content=\"noindex, nofollow\" />\n<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />\n<link rel=\"stylesheet\" id=\"cf_styles-css\" href=\"/cdn-cgi/styles/cf.errors.css\" />\n<!--[if lt IE 9]><link rel=\"stylesheet\" id='cf_styles-ie-css' href=\"/cdn-cgi"
      }
    ],
    "errors": []
  },
  "yourinfo_snapshot": {
    "url": "https://yourinfo.ai/",
    "final_url": "https://yourinfo.ai/",
    "status": 200,
    "title": "YourInfo.ai",
    "text_excerpt": "RESEARCHING YOUR INFORMATION...\n20\nQuerying intelligence databases...\n\nConcerned about your digital privacy?\n\ndoxx.net - Secure networking for humans\n ",
    "text_excerpt_truncated": false,
    "har_path": "runs/nordvpn-20260410T221659Z-5dfe011f/raw/us-california-santa-clara-160/yourinfo_probe/yourinfo.har",
    "cdn_headers": {},
    "error": null
  },
  "extra": {
    "exit_geo": {
      "source": "ipwho.is",
      "ip": "185.169.0.160",
      "country_code": "US",
      "region": "California",
      "city": "Santa Clara",
      "connection": {
        "asn": 141039,
        "org": "Packethub S.A.",
        "isp": "Packethub S.A.",
        "domain": "packethub.net"
      },
      "location_id": "us-california-santa-clara-160",
      "location_label": "Santa Clara, California, United States"
    }
  }
}
```

---



## Appendix

- Canonical JSON per location: `runs/<run_id>/locations/<location_id>/normalized.json`
- Raw captures: `runs/<run_id>/raw/<location_id>/` (including `yourinfo_probe/`, `competitor_probe/` when present)
- Regenerate this file: `vpn-leaks report --provider nordvpn`