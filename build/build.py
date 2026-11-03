#!/usr/bin/env python3
"""薄肌学 book build: assemble page fragments -> index.html, inject art + footers + TOC numbers.

Usage:
  python3 build/build.py                              # full book from BOOK.json
  python3 build/build.py --fragments pages/03-ch2.html --out build/preview-ch2.html --pdf /tmp/ch2.pdf --audit
"""
import json, os, re, sys, subprocess, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART_DIR = ROOT / "assets" / "art"
CHROME = os.environ.get("CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

def read(p): return p.read_text(encoding="utf-8")

def svg_for(name):
    p = ART_DIR / f"{name}.svg"
    if p.exists():
        return read(p)
    return f'<div class="fig-missing">缺图 · {name}</div>'

fig_re = re.compile(r'(<figure\b[^>]*\bdata-art="([^"]+)"[^>]*>)', re.I)
def inject_art(html):
    return fig_re.sub(lambda m: m.group(1) + svg_for(m.group(2)), html)

page_split = re.compile(r'(<section\b[^>]*class="[^"]*\bpage\b[^"]*"[^>]*>)', re.I)
def split_pages(text):
    parts = page_split.split(text)
    pages, i = [], 1
    while i < len(parts):
        pages.append((parts[i], parts[i] + (parts[i+1] if i+1 < len(parts) else "")))
        i += 2
    return pages

def attr(name, tag):
    m = re.search(name + r'="([^"]*)"', tag)
    return m.group(1) if m else None

def build(fragments, out_html, css_rel="css/book.css", with_audit=False):
    pages = []
    for f in fragments:
        pages.extend(split_pages(read(ROOT / f)))

    printed, keymap, numbered = 0, {}, []
    for tag, html in pages:
        cls = attr("class", tag) or ""
        is_front = any(c in cls for c in ("page--front", "page--cover", "page--backcover"))
        if not is_front:
            printed += 1
        numbered.append((tag, html, printed if not is_front else None))
        k = attr("data-key", tag)
        if k and printed:
            keymap[k] = printed

    def repl_pn(html):
        return re.sub(r"\{\{PN:([^}]+)\}\}", lambda m: str(keymap.get(m.group(1), "??")), html)

    out = []
    for tag, html, num in numbered:
        html = inject_art(repl_pn(html))
        if num and "pg-foot" not in html:
            ch, sec = attr("data-ch", tag) or "", attr("data-sec", tag) or ""
            foot = '<div class="pg-foot"><span class="foot-l">'
            if ch: foot += f'<span class="foot-ch">{ch}</span>'
            if sec: foot += f'<span class="foot-sec">{sec}</span>'
            foot += f'</span><span class="foot-r">{num}</span></div>'
            foot += '<span class="pg-wm">kangrong_hu</span>'
            html = html.replace("</section>", foot + "</section>")
        out.append(html)

    audit = '''
<script>
(function(){
  function run(){
    var bad=[];
    document.querySelectorAll('.page').forEach(function(p,i){
      if(p.scrollHeight > p.clientHeight + 2){
        var k = p.getAttribute('data-key') || p.querySelector('[data-key]') && p.querySelector('[data-key]').getAttribute('data-key') || ('page'+(i+1));
        bad.push((i+1)+':'+k);
      }
    });
    document.title = 'AUDIT ' + (bad.length? bad.join(' | '):'OK');
    var d=document.createElement('div'); d.id='audit-result'; d.textContent=document.title; d.style.cssText='position:fixed;left:-9999px';
    document.body.appendChild(d);
  }
  if(document.readyState==='complete') run(); else window.addEventListener('load', run);
  setTimeout(run, 1000);
})();
</script>
'''
    head = f'<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><title>薄肌学 · 必修 第一册</title><meta name="author" content="kangrong_hu"><link rel="stylesheet" href="{css_rel}"></head><body>\n'
    extra = audit if with_audit else ""
    (ROOT / out_html).write_text(head + "\n".join(out) + "\n" + extra + "\n</body></html>\n", encoding="utf-8")
    return len(out), keymap

def chrome_pdf(html_rel, pdf_path):
    url = "file://" + str((ROOT / html_rel).resolve())
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=6000", f"--print-to-pdf={pdf_path}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    return pdf_path

def chrome_audit(html_rel):
    url = "file://" + str((ROOT / html_rel).resolve())
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=6000",
                        "--dump-dom", url], capture_output=True, text=True)
    m = re.search(r"<title>(AUDIT [^<]*)</title>", r.stdout)
    return m.group(1) if m else "AUDIT ?"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragments", help="comma separated page fragment files")
    ap.add_argument("--out", default="index.html", help="output html path (relative to project)")
    ap.add_argument("--pdf", help="also render PDF to this path")
    ap.add_argument("--audit", action="store_true", help="check page overflow")
    a = ap.parse_args()

    if a.fragments:
        frags = [f.strip() for f in a.fragments.split(",") if f.strip()]
    else:
        frags = json.loads(read(ROOT / "BOOK.json"))["pages"]
    css_rel = os.path.relpath(ROOT / "css/book.css", (ROOT / a.out).parent)
    n, keys = build(frags, a.out, css_rel, with_audit=a.audit)
    print(f"pages={n} keys={len(keys)} -> {a.out}")
    if a.pdf:
        chrome_pdf(a.out, a.pdf)
        print("pdf:", a.pdf)
    if a.audit:
        print(chrome_audit(a.out))
