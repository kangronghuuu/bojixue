#!/usr/bin/env python3
"""Lightweight repository check: page manifest, art references, placeholders, page count."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "assets" / "art"

def main():
    manifest = json.loads((ROOT / "BOOK.json").read_text(encoding="utf-8"))
    html = ""
    for f in manifest["pages"]:
        p = ROOT / f
        if not p.exists():
            print(f"missing page file: {f}"); return 1
        html += p.read_text(encoding="utf-8")

    if "fig-missing" in html:
        print("placeholder art found (fig-missing)"); return 1

    arts = sorted(set(re.findall(r'data-art="([^"]+)"', html)))
    missing = [a for a in arts if not (ART / f"{a}.svg").exists()]
    if missing:
        print("missing art:", ", ".join(missing)); return 1

    pages = len(re.findall(r'<section class="page', html))
    if pages < 50:
        print(f"unexpected page count: {pages}"); return 1

    illustration_prefixes = ("ch-open-", "atlas-", "mascot-")
    for svg in ART.glob("*.svg"):
        if svg.name.startswith(illustration_prefixes) and "<text" in svg.read_text(encoding="utf-8"):
            print(f"warning: <text> inside illustration: {svg.name}")

    print(f"OK pages={pages} art_refs={len(arts)} svg_files={len(list(ART.glob('*.svg')))}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
