# VPN Leaks — operational spec

Canonical product and threat-model specification: [vpn-leaks.md](../vpn-leaks.md) (project root).

## What this project measures

Client-side observable privacy: leaks, fingerprints, exit attribution, and policy text—not claims about what a VPN stores internally.

## Implementation (this repository)

| Piece | Location / entry |
|-------|------------------|
| CLI | `vpn-leaks` (see `pyproject.toml`), implemented in [`vpn_leaks/cli.py`](../vpn_leaks/cli.py) |
| Python package | [`vpn_leaks/`](../vpn_leaks/) — checks, adapters, attribution, policy, reporting |
| Provider configs | [`configs/vpns/<slug>.yaml`](../configs/vpns/) |
| Tool configs | [`configs/tools/leak-tests.yaml`](../configs/tools/leak-tests.yaml), [`configs/tools/attribution.yaml`](../configs/tools/attribution.yaml) |
| Run artifacts | `runs/<run_id>/` (gitignored): [`run.json`](data-dictionary.md#runsrun_idrunjson), [`raw/preflight.json`](data-dictionary.md#runsrun_idraw-layout), per-location [`raw/<location_id>/`](data-dictionary.md#runsrun_idraw-layout), [`locations/<location_id>/normalized.json`](data-dictionary.md#runsrun_idlocationslocation_idnormalizedjson), `summary.md` |
| Aggregated reports | `VPNs/*.md`, `PROVIDERS/*.md` (generated; gitignored by default) |
| Exposure graph | `vpn-leaks graph-export` → JSON (`exposure-graph.json` by default); optional [viewer/README.md](../viewer/README.md) |

## Run behavior (summary)

1. **Preflight:** quick exit IPv4 (first IP endpoint in leak-test config).
2. **Duplicate guard:** if that IPv4 already appears in any prior `normalized.json` for the same `vpn_provider`, the command exits successfully without creating a new run (use `--force` to run anyway).
3. **Location:** omit `--locations` for **auto** id/label via ipwho.is (optional YAML append); or pass explicit `--locations` (see [README](../README.md)).
4. **Suite:** IP check, DNS, IPv6, WebRTC, optional fingerprint, attribution, policy fetch—then `normalized.json` per location.

Further detail: [methodology.md](methodology.md), field reference: [data-dictionary.md](data-dictionary.md), usage: [README](../README.md).
