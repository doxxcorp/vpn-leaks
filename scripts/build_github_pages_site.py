#!/usr/bin/env python3
"""Stage a static tree for GitHub Pages: VPNs/, style/icons/, index.html."""
from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    site = root / "site"
    if site.exists():
        shutil.rmtree(site)
    site.mkdir(parents=True)

    vpn_src = root / "VPNs"
    if vpn_src.is_dir():
        shutil.copytree(vpn_src, site / "VPNs")
    else:
        (site / "VPNs").mkdir()
        print("Warning: VPNs/ missing — empty site/VPNs/", file=sys.stderr)

    icons_src = root / "style" / "icons"
    if not icons_src.is_dir():
        print("Error: style/icons/ not found (required for report icons).", file=sys.stderr)
        return 1
    (site / "style").mkdir(parents=True)
    shutil.copytree(icons_src, site / "style" / "icons")

    vpn_dir = site / "VPNs"
    items = sorted(vpn_dir.glob("*.html")) if vpn_dir.is_dir() else []

    lines = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8"/>',
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>',
        "<title>VPN Leaks reports</title>",
        "<style>"
        "body{font-family:system-ui,sans-serif;max-width:48rem;margin:2rem auto;padding:0 1rem}"
        "ul{line-height:1.8}"
        "code{font-size:0.9em}"
        "</style>",
        "</head><body>",
        "<h1>VPN Leaks reports</h1>",
        "<p>Static HTML from <code>vpn-leaks report</code> (SPEC coverage, exposure graph).</p>",
    ]
    if not items:
        lines.append("<p>No <code>VPNs/*.html</code> files yet.</p>")
    else:
        lines.append("<ul>")
        for p in items:
            rel = f"VPNs/{p.name}"
            label = html.escape(p.stem.replace("_", " "))
            lines.append(
                f'<li><a href="{html.escape(rel)}">{label}</a></li>'
            )
        lines.append("</ul>")
    lines.append("</body></html>")
    (site / "index.html").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Avoid Jekyll processing on github.io
    (site / ".nojekyll").touch()

    print(f"Wrote {site / 'index.html'} ({len(items)} report(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
