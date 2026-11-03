#!/usr/bin/env python3
"""Crop transparent padding from chapter-opener SVGs by measuring rendered bbox."""
import re, subprocess, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BG = (0xFB,0xF5,0xE5)

def bbox(svg_path):
    html = ROOT/"build"/"_op.html"
    html.write_text(f'<!doctype html><html><head><style>body{{margin:0;background:#FBF5E5}}img{{display:block}}</style></head><body><img src="../assets/art/{svg_path.name}" width="1100"></body></html>')
    png = ROOT/"build"/"_op.png"
    subprocess.run([CHROME,"--headless=new","--disable-gpu",f"--screenshot={png}","--window-size=1100,620","--hide-scrollbars",f"file://{html}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    im = Image.open(png).convert("RGB"); w,h=im.size; px=im.load()
    minx,miny,maxx,maxy = w,h,0,0
    for y in range(h):
        for x in range(w):
            r,g,b=px[x,y]
            if abs(r-BG[0])+abs(g-BG[1])+abs(b-BG[2])>24:
                minx=min(minx,x); maxx=max(maxx,x); miny=min(miny,y); maxy=max(maxy,y)
    return minx,miny,maxx,maxy

def crop(name):
    p = ROOT/"assets"/"art"/f"{name}.svg"
    s = p.read_text()
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"[^>]*width="(\d+)" height="(\d+)"', s)
    if not m:
        m = re.search(r'width="(\d+)" height="(\d+)"[^>]*viewBox="0 0 (\d+) (\d+)"', s)
    W,H = int(m.group(1)), int(m.group(2))
    minx,miny,maxx,maxy = bbox(p)
    pad = 18
    x = max(0,minx-pad); y = max(0,miny-pad)
    w = min(W, maxx+pad) - x; h = min(H, maxy+pad) - y
    s2 = re.sub(r'viewBox="0 0 \d+ \d+"', f'viewBox="{x} {y} {w} {h}"', s, count=1)
    s2 = re.sub(r'width="\d+" height="\d+"', f'width="{w}" height="{h}"', s2, count=1)
    p.write_text(s2)
    print(name, 'crop ->', x,y,w,h)

if __name__ == "__main__":
    for n in sys.argv[1:]:
        crop(n)
