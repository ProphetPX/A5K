#!/usr/bin/env python3
"""Build the PDF: resolve TOC folios with temporary markers, then render a
clean source (no markers), stamp folios, bookmarks and metadata."""
import re, subprocess, sys, os
import atexit, shutil, tempfile
import pymupdf

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "A5K-Design-Proposition.html")
PDF = os.path.join(BASE, "A5K-Design-Proposition.pdf")

# Per-run scratch directory: no assumption about the host harness, and it
# cleans itself up even if the build fails.
_TMPDIR = tempfile.mkdtemp(prefix="a5k-build-")
atexit.register(shutil.rmtree, _TMPDIR, ignore_errors=True)

TMP_HTML = os.path.join(_TMPDIR, "_markers.html")
TMP_PDF = os.path.join(_TMPDIR, "pass.pdf")

MARKERS = ["zzS1zz","zzS2zz","zzS3zz","zzS4zz","zzS5zz","zzS6zz",
           "zzS7zz","zzS8zz","zzS9zz","zzSazz","zzSbzz","zzSczz","zzSdzz"]

# table/figure references: located by their printed caption, not by anchors
SPECIAL = {"zzT1zz":"Table 1.","zzT2zz":"Table 2.","zzT3zz":"Table 3.",
           "zzT4zz":"Table 4.","zzT5zz":"Table 5.","zzT6zz":"Table 6.",
           "zzF1zz":"Figure 1."}

names = {
 "zzS1zz":"1. What the latest model of that era actually was",
 "zzS2zz":"2. The design ethos, distilled",
 "zzS3zz":"3. Chip-by-chip: the modern re-issue",
 "zzS4zz":"4. Getting it onto a modern bus",
 "zzS5zz":"5. Which host processor?",
 "zzS6zz":"6. A concrete reference build",
 "zzS7zz":"7. Software",
 "zzS8zz":"8. What you'd lose",
 "zzS9zz":"9. Why not just use a GPU?",
 "zzSazz":"Appendix A - The Copper, specified",
 "zzSbzz":"Appendix B - Implementation skeleton",
 "zzSczz":"Appendix C - Bill of materials",
 "zzSdzz":"Appendix D - Where this is most likely wrong",
}
order = ["zzS1zz","zzS2zz","zzS3zz","zzS4zz","zzS5zz","zzS6zz",
         "zzS7zz","zzS8zz","zzS9zz","zzSazz","zzSbzz","zzSczz","zzSdzz"]

def render(path, out):
    subprocess.run(["chromium","--headless=new","--disable-gpu","--no-sandbox",
                    "--no-pdf-header-footer","--print-to-pdf="+out,
                    "file://"+path], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def locate_special(pdf):
    doc = pymupdf.open(pdf); found = {}
    for i, page in enumerate(doc):
        if i < 2:            # skip cover and contents
            continue
        t = page.get_text()
        for k, needle in SPECIAL.items():
            if k not in found and needle in t:
                found[k] = i - 1
    doc.close(); return found


def locate(pdf):
    doc = pymupdf.open(pdf); found = {}
    for i, page in enumerate(doc):
        t = page.get_text()
        for m in MARKERS:
            if m in t and m not in found:
                found[m] = i
    doc.close(); return found

# ---- pass 1: resolve page numbers ---------------------------------------
src = open(HTML, encoding="utf-8").read()

# self-heal: re-inject the invisible anchors if the source was already stripped
ids = {"s1":"zzS1zz","s2":"zzS2zz","s3":"zzS3zz","s4":"zzS4zz","s5":"zzS5zz",
       "s6":"zzS6zz","s7":"zzS7zz","s8":"zzS8zz","s9":"zzS9zz",
       "appA":"zzSazz","appB":"zzSbzz","appC":"zzSczz","appD":"zzSdzz"}
for hid, mk in ids.items():
    if (">%s</span>" % mk) not in src:
        pat = r'(<h2 id="%s"[^>]*>)(.*?)(</h2>)' % hid
        src, n = re.subn(pat, lambda mo, mk=mk: mo.group(1) + mo.group(2)
                         + '<span class="mk">%s</span>' % mk + mo.group(3),
                         src, count=1, flags=re.S)
        if n != 1:
            sys.exit("could not inject marker for %s" % hid)
prev = None
for it in range(8):
    open(TMP_HTML, "w", encoding="utf-8").write(src)
    render(TMP_HTML, TMP_PDF)
    found = locate(TMP_PDF)
    missing = [m for m in MARKERS if m not in found]
    if missing:
        sys.exit("markers not found: %s" % missing)
    pages = {m: found[m] - 1 for m in MARKERS}
    pages.update(locate_special(TMP_PDF))
    if pages == prev:
        break
    prev = pages
    for m, p in pages.items():
        src, n = re.subn(r'(data-mk="%s"[^>]*>)\s*\d+\s*(<)' % m,
                         r'\g<1>%d\g<2>' % p, src)
        if not n:
            sys.exit("placeholder not found for %s" % m)
else:
    sys.exit("did not stabilise")
print("folios:", pages)

# ---- pass 2: strip markers, render clean --------------------------------
clean = re.sub(r'<span class="mk">zzS\w+zz</span>', '', src)
open(HTML, "w", encoding="utf-8").write(clean)
render(HTML, TMP_PDF)

doc = pymupdf.open(TMP_PDF)
if doc.page_count != 14:
    print("note: page count is", doc.page_count)

# ---- folios -------------------------------------------------------------
for i, page in enumerate(doc):
    if i == 0:
        continue
    label = "ii" if i == 1 else str(i - 1)
    w, h = page.rect.width, page.rect.height
    page.draw_line(pymupdf.Point(w * 0.10, h - 30),
                   pymupdf.Point(w * 0.90, h - 30),
                   color=(0.80, 0.80, 0.80), width=0.5)
    page.insert_text((w * 0.10, h - 19),
                     "Rev. AN \u00b7 3 Nov 2026 \u00b7 start 30 Oct 2026",
                     fontname="helv", fontsize=6.8, color=(0.45, 0.45, 0.45))
    title = "A5K \u00b7 Design Study"
    tw = pymupdf.get_text_length(title, fontname="helv", fontsize=7.2)
    page.insert_text(((w - tw) / 2, h - 19), title,
                     fontname="helv", fontsize=7.2, color=(0.45, 0.45, 0.45))
    tw = pymupdf.get_text_length(label, fontname="helv", fontsize=8)
    page.insert_text((w * 0.90 - tw, h - 19), label,
                     fontname="helv", fontsize=8, color=(0.2, 0.2, 0.2))

doc.set_toc([[1, "Cover", 1], [1, "Contents", 2]] +
            [[1, names[m], pages[m] + 2] for m in order])
doc.set_metadata({
    "title": "A5K - A Theoretical Design Proposition for an Amiga 5000-Like System - Rev. AN",
    "author": "Design study",
    "subject": "Re-issuing the Amiga custom-chipset design ethos on a modern bus, in open silicon",
    "keywords": "Amiga, Copper, Agnus, Denise, Blitter, Paula, PCIe, CXL, RISC-V, LiteX, Migen, AROS, FPGA",
    "creator": "LiteX-inspired design study",
})
doc.save(PDF, deflate=True, garbage=4)
doc.close()
print("wrote %s" % PDF)
