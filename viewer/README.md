# Exposure graph (3D viewer)

Offline-friendly static page that visualizes JSON from **`vpn-leaks graph-export`**.

## Generate graph data

From the repository root (with benchmarks under `runs/`):

```bash
vpn-leaks graph-export --provider nordvpn -o exposure-graph.json
# or all providers:
vpn-leaks graph-export -o exposure-graph.json
```

## View locally

Browsers block `fetch()` for `file://`, so serve the folder:

```bash
cd viewer
python3 -m http.server 8765
```

Open:

- [http://127.0.0.1:8765/?url=../exposure-graph.json](http://127.0.0.1:8765/?url=../exposure-graph.json)  
  (adjust path if you placed `exposure-graph.json` elsewhere)

Or copy `exposure-graph.json` into `viewer/` and open `http://127.0.0.1:8765/?url=exposure-graph.json`.

Nodes are colored by `type` (vpn, domain, ns, ip, asn, policy_url). Edges carry `relation` and `run_id` / `location_id` for provenance.

## Dependencies

The page loads **3d-force-graph** from a CDN (ESM); no `npm install` required.
