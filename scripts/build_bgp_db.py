#!/usr/bin/env python3
"""CLI wrapper: download Route Views RIB and build .cache/vpn_leaks/bgp_prefixes.db."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from vpn_leaks.attribution.bgp_build import _ROUTEVIEWS_BASE, build_bgp_db
from vpn_leaks.attribution.bgp_lookup import _default_db_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Build BGP prefix SQLite DB from Route Views MRT RIB")
    ap.add_argument("--url", default=None, help="Override RIB .bz2 URL")
    ap.add_argument("--rib-file", default=None, metavar="PATH", help="Use local .bz2 file")
    ap.add_argument("--db", default=None, metavar="PATH", help="Output DB path")
    ap.add_argument(
        "--base-url", default=_ROUTEVIEWS_BASE, help="Route Views archive base URL"
    )
    args = ap.parse_args()

    db_path = Path(args.db).resolve() if args.db else _default_db_path()
    rib_file = Path(args.rib_file).resolve() if args.rib_file else None

    try:
        result = build_bgp_db(
            db_path,
            rib_url=args.url,
            rib_file=rib_file,
            base_url=args.base_url,
            progress=True,
        )
        print(f"prefixes={result['prefix_count']:,}  db={result['db_path']}  "
              f"size={result['db_size_mb']:.0f}MB  elapsed={result['elapsed_s']:.0f}s")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
