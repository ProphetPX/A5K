#!/usr/bin/env python3
"""Compose, render and stamp the comparative addendum."""
import os, re, subprocess, sys
import atexit, shutil, tempfile
import pymupdf

BASE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(BASE, "A5K-Design-Proposition.html")
HTML = os.path.join(BASE, "A5K-Comparative-Addendum.html")
PDF = os.path.join(BASE, "A5K-Comparative-Addendum.pdf")

# Per-run scratch directory: no assumption about the host harness, and it
# cleans itself up even if the build fails.
_TMPDIR = tempfile.mkdtemp(prefix="a5k-build-")
atexit.register(shutil.rmtree, _TMPDIR, ignore_errors=True)

TMP = os.path.join(_TMPDIR, "addendum_pass.pdf")

# ---------------------------------------------------------------- css ----
main = open(MAIN, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", main, re.S).group(1)

extra = """
  /* ---------- addendum specifics ---------- */
  .add-head {
    border-bottom: 2.5pt solid #b03030;
    padding-bottom: 10pt;
    margin-bottom: 14pt;
  }
  .add-head h1 {
    font-size: 25pt;
    line-height: 1.08;
    margin: 2pt 0 6pt 0;
  }
  .scope {
    background: #f3f5f7;
    border-left: 2.5pt solid #4a5568;
    padding: 8pt 10pt 6pt 10pt;
    margin: 6pt 0 14pt 0;
    font-size: 9.2pt;
    line-height: 1.45;
  }
  .scope .slabel {
    font-family: "DejaVu Sans", Helvetica, Arial, sans-serif;
    font-size: 7pt;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4a5568;
    font-weight: 700;
    display: block;
    margin-bottom: 3pt;
  }
  .scope p { margin: 0 0 6pt 0; }
  .scope p:last-child { margin-bottom: 4pt; }
  table.eras { font-size: 6.9pt; }
  table.eras th, table.eras td { padding: 3pt 4pt; }
  table.eras td:first-child { white-space: normal; }
  .verdict { margin-top: 4pt; }
  .bpl {
    margin-top: 18pt;
    border-top: 1.2pt solid #b03030;
    padding-top: 8pt;
    font-family: "DejaVu Sans", Helvetica, Arial, sans-serif;
    font-size: 7.3pt;
    line-height: 1.46;
    color: #666;
    page-break-inside: avoid;
  }
  .bpl .bplabel {
    display: block; font-size: 6.8pt; letter-spacing: 0.14em; text-transform: uppercase;
    font-weight: 700; color: #b03030; margin-bottom: 3pt;
  }
  .bpl p { margin: 0 0 3pt 0; text-align: left; }
  .bpl p:last-child { margin-bottom: 0; }
  .legalnote {
    font-family: "DejaVu Sans", Helvetica, Arial, sans-serif;
    font-size: 6.5pt;
    line-height: 1.4;
    color: #8a8a8a;
    margin: 10pt 0 0 0;
  }
"""

# --------------------------------------------------------------- body ----
body = r"""
<div class="add-head">
  <p class="kicker">Addendum to <em>A5K</em> · Rev. AG</p>
  <h1>Where This Design Sits</h1>
  <p class="subtitle">AAA, Hombre, the shipped Amiga eras, and a 2026 scientific workstation — compared honestly</p>
  <p class="meta">Rev. AG &nbsp;·&nbsp; 2 November 2026 &nbsp;·&nbsp; Comparative analysis &nbsp;·&nbsp; 5 sections &nbsp;·&nbsp; 4 tables</p>
  <p class="legalnote">Amiga and Commodore are trademarks of their respective owners. This is an independent design study, not affiliated with, endorsed by, or sponsored by any rights holder. Comparisons are estimates and opinion, not statements of fact about any company. See LEGAL.md.</p>
</div>

<div class="scope">
  <span class="slabel">Scope and ground rules</span>
  <p>This addendum does not restate the design; it places it. It compares the A5K concept against the two Amiga architectures that were designed but never built — <strong>AAA</strong> (1994) and <strong>Hombre</strong> (1995) — against the three that shipped, and against a current top-end scientific workstation.</p>
  <p>One asymmetry governs everything below. <strong>OCS, ECS, AGA and the workstation are real, shipping hardware. AAA and Hombre were cancelled before volume silicon, and the A5K is a paper design with a bill of materials.</strong> Every comparison involving the Amigas is therefore design-target against design-target, and every number is an estimate derived from public specifications, datasheets and the BOM in Appendix C of the main document. Where a figure is a range, the range <em>is</em> the answer.</p>
</div>

<h2 id="c1">1. Why the A5K is better than AAA — and by how far</h2>

<p>AAA (1993–94) was a <strong>2D evolution of the Amiga chipset</strong>: 32-bit paths, 16-bit chunky as well as planar, more bitplanes, 8-channel 16-bit audio, a 64-bit blitter, a wider Copper, and a display ceiling around 1280×1024. It was the right architectural answer to AGA’s limits, and it was cancelled because Commodore ran out of money before it could tape out.</p>

<p>The A5K beats it in five ways and loses in one.</p>

<table>
<caption><strong>Table A1.</strong> The A5K against the AAA target specification.</caption>
<thead>
<tr><th style="width:20%">Axis</th><th style="width:33%">AAA (target, ~1995 silicon)</th><th style="width:33%">A5K (2026, FPGA)</th><th style="width:14%">Ratio</th></tr>
</thead>
<tbody>
<tr><td>Configurable logic</td><td>~50–150k gates across 3–4 chips</td><td>215k logic cells ≈ 2–4M gate-equivalents</td><td>~20–60×</td></tr>
<tr><td>Clock domain</td><td>~14–28 MHz chip bus</td><td>100–200 MHz core; 148.5 MHz pixel</td><td>~5–10×</td></tr>
<tr><td>Chip RAM</td><td>~2–16 MB (never fixed)</td><td>512 MB – 2 GB DDR3/LPDDR4</td><td>~100–1000×</td></tr>
<tr><td>Memory bandwidth</td><td>~50–100 MB/s</td><td>6.4–12.8 GB/s</td><td>~100×</td></tr>
<tr><td>Host link</td><td>Zorro III, ~37 MB/s</td><td>PCIe Gen1/2 ×4, 1–2 GB/s</td><td>~30–50×</td></tr>
<tr><td>Scanout</td><td>1280 × 1024</td><td>4K (3840 × 2160)</td><td>~6× pixels</td></tr>
<tr><td>Native 68k software</td><td>Yes, by construction</td><td>No — AROS or emulation</td><td>AAA wins</td></tr>
</tbody>
</table>

<p><strong>By how far:</strong> roughly <strong>1.5 orders of magnitude in silicon, and 2–3 in memory and bandwidth</strong>. That is not a new class of machine — it is the AAA concept executed on a 2026 FPGA with twenty-five extra years of process, memory and I/O. The real difference is not the ratio but the fact that <strong>one shipped and the other didn’t.</strong> AAA needed a fab, a CPU, an OS team, a factory and a market; the A5K needs a $264 BOM and a laptop.</p>

<p>The one place AAA is strictly better: it would have run 1994 Amiga software natively. The A5K cannot, and should not pretend otherwise.</p>

<h2 id="c2">2. Why it is better than Hombre — and where Hombre was ahead</h2>

<p>Hombre (1995) was a different animal: a <strong>PA-RISC CPU plus a fixed-function 3D chipset</strong>, aimed at a CD32 successor — a games console rather than a computer. It was cancelled in 1995–96.</p>

<p>Against Hombre, the A5K wins on:</p>

<ul>
  <li><strong>Openness.</strong> PA-RISC is dead; the design would have been closed, single-vendor and unmaintainable. The A5K is RISC-V or x86 plus LiteX and AROS, all readable.</li>
  <li><strong>Memory and I/O.</strong> Hombre would have had a few megabytes and a cartridge or CD bus. The A5K has 2 GB and PCIe.</li>
  <li><strong>Survivability.</strong> Hombre depended on winning a console war against PlayStation. The A5K depends on nobody.</li>
  <li><strong>Tools.</strong> Yosys, nextpnr and Verilator, versus 1995 proprietary everything.</li>
</ul>

<p>But be honest about the 3D: <strong>Hombre had a 3D pipeline; the A5K has none.</strong> Its likely target was 10<sup>5</sup>–10<sup>6</sup> polygons per second — three to four orders below a 2026 GPU — so the correct comparison is not “ours is faster” but “ours declines the contest and borrows a GPU as a plane source” (§9.6 of the main document). Hombre tried to win a race it was already losing; the A5K refuses to enter it.</p>

<p><strong>By how far:</strong> the same 1.5–3 orders in memory and logic, plus qualitative wins in openness and cost — but <em>minus</em> the one thing Hombre actually had, which is 3D silicon.</p>

<h2 id="c3">3. The three Amiga eras, side by side</h2>

<table class="eras">
<caption><strong>Table A2.</strong> Shipped Amigas, cancelled Amigas, and the paper design.</caption>
<thead>
<tr>
  <th style="width:15%"></th>
  <th style="width:14%">OCS (1985)</th>
  <th style="width:13%">ECS (1990)</th>
  <th style="width:14%">AGA (1992)</th>
  <th style="width:14%">AAA (1994, ✝)</th>
  <th style="width:13%">Hombre (1995, ✝)</th>
  <th style="width:17%">A5K (2026, paper)</th>
</tr>
</thead>
<tbody>
<tr><td>CPU</td><td>68000 @ 7.1 MHz</td><td>68000 / 020</td><td>020 / 030 / 040</td><td>040 / 060</td><td>PA-RISC</td><td>RISC-V or x86 host</td></tr>
<tr><td>Chip RAM</td><td>256–512 KB</td><td>1–2 MB</td><td>2 MB</td><td>~2–16 MB</td><td>a few MB</td><td>0.5–2 GB</td></tr>
<tr><td>Planes / colour</td><td>6 / 4,096</td><td>6 / 4,096</td><td>8 / 262k (HAM8)</td><td>16-bit chunky</td><td>3D</td><td>8-planar + ARGB planes</td></tr>
<tr><td>Blitter</td><td>16-bit</td><td>16-bit</td><td>16-bit</td><td>64-bit</td><td>3D</td><td>64-bit equivalent</td></tr>
<tr><td>Audio</td><td>4 × 8-bit</td><td>4 × 8-bit</td><td>4 × 8-bit</td><td>8 × 16-bit</td><td>CD-class</td><td>N × 24-bit I²S DMA</td></tr>
<tr><td>Display</td><td>640 × 512</td><td>640 × 512</td><td>1280 × 512</td><td>~1280 × 1024</td><td>TV</td><td>4K</td></tr>
<tr><td>Bus</td><td>custom</td><td>custom</td><td>custom</td><td>custom</td><td>custom</td><td>PCIe / AXI</td></tr>
<tr><td>Software</td><td>AmigaOS</td><td>AmigaOS</td><td>AmigaOS</td><td>—</td><td>—</td><td>AROS / Linux</td></tr>
<tr><td>Exists?</td><td><strong>yes</strong></td><td><strong>yes</strong></td><td><strong>yes</strong></td><td>no</td><td>no</td><td>no</td></tr>
</tbody>
</table>

<p>The A5K is not the next Amiga era. It is <strong>AAA’s architecture, Hombre’s ambition minus the 3D, and neither one’s market</strong> — instantiated on hardware that exists.</p>

<h2 id="c4">4. Against a cutting-edge scientific workstation</h2>

<p>Take a realistic top-end mathematics-lab node: dual 128-core EPYC or Xeon 6, 2–3 TB of DDR5, eight H100/B200-class accelerators, 100+ TB of NVMe and 400 Gb InfiniBand — or, for a single seat, an HP Z8 or a Mac Studio Ultra, which is the “professional workstation” version of the same thing.</p>

<table>
<caption><strong>Table A3.</strong> A 2026 lab node against the A5K.</caption>
<thead>
<tr><th style="width:22%">Axis</th><th style="width:36%">2026 lab node</th><th style="width:28%">A5K</th><th style="width:14%">Ratio</th></tr>
</thead>
<tbody>
<tr><td>FP64 throughput</td><td>20 TFLOPS CPU + 270–320 TFLOPS GPU ≈ 300 TFLOPS</td><td>≈ 0 in the chipset; host does 10–50 GFLOPS</td><td>~10<sup>4</sup>–10<sup>5</sup>×</td></tr>
<tr><td>Memory</td><td>2–3 TB DDR5 + ~1 TB HBM</td><td>2 GB</td><td>~10<sup>3</sup>×</td></tr>
<tr><td>Bandwidth</td><td>~1 TB/s DDR5 + 3–8 TB/s HBM</td><td>~13 GB/s</td><td>~10<sup>2</sup>–10<sup>3</sup>×</td></tr>
<tr><td>Storage</td><td>100+ TB NVMe</td><td>microSD</td><td>~10<sup>5</sup>×</td></tr>
<tr><td>Cores</td><td>256 CPU + ~10<sup>5</sup> GPU lanes</td><td>1 RISC-V + fixed-function blocks</td><td>~10<sup>5</sup>×</td></tr>
<tr><td>Software</td><td>NumPy, PETSc, FFTW, CUDA, MPI, every compiler</td><td>AROS, a demo scene, no BLAS</td><td>not comparable</td></tr>
<tr><td>Worst-case display latency</td><td>Unbounded: compositor, driver, scheduler</td><td>One scanline, by construction</td><td>A5K wins</td></tr>
<tr><td>Display-path power</td><td>5–30 W for the GPU alone, plus platform</td><td>1–2 W for the chipset</td><td>A5K wins</td></tr>
<tr><td>Lines of code to understand it</td><td>~10<sup>8</sup></td><td>~10<sup>4</sup></td><td>A5K wins</td></tr>
</tbody>
</table>

<p><strong>By how far:</strong> on the workload a mathematics lab actually runs — dense linear algebra, PDE solvers, FFTs, Monte Carlo — the workstation is <strong>four to five orders of magnitude faster</strong>, with a thousand times the memory and a software stack that has no counterpart at all. This is not close, and no amount of clever chipset design changes it.</p>

<p>Where it is not absurd: a laboratory also has <em>instruments</em>. Laser sync, ADC and DAC capture, camera triggers, optical benches, real-time control loops. There the question is not how many FLOPs but <strong>when exactly a sample lands, and whether that can be proven</strong>. A Linux box with a compositor and a fair scheduler gives statistical timing; this chipset gives a contract. That is a real, narrow, defensible niche — and precisely why §9.7 of the main document lists genlock and instrumentation rather than numerical work.</p>

<h2 id="c5">5. The honest bottom line</h2>

<ul>
  <li><strong>Versus AAA:</strong> better by ~1.5 orders in silicon and 2–3 in memory and bandwidth, mainly because it is <em>buildable</em>. Worse in one respect: no native 68k.</li>
  <li><strong>Versus Hombre:</strong> better in openness, cost, memory and survivability; worse in that Hombre had 3D and this does not.</li>
  <li><strong>Versus a 2026 lab workstation:</strong> behind by 4–5 orders of magnitude on compute, 3 on memory, 2–3 on bandwidth, and effectively infinite on software. Ahead on exactly one axis — bounded display and timing latency — and on power and comprehensibility.</li>
</ul>

<p>The truthful framing is not “a competitor to a modern PC”. It is: <strong>the fastest, cheapest, most open way to own a machine whose display timing you can prove</strong> — a 1994 architecture given 2026 memory and I/O, and a 1985 timing contract given a reason to still exist. At a mathematics lab it is not the computer that does the mathematics; at best it is the instrument that tells you, to the scanline, when the mathematics was displayed.</p>

<table class="verdict">
<caption><strong>Table A4.</strong> The verdict at a glance.</caption>
<thead>
<tr><th style="width:22%">Compared with</th><th style="width:28%">A5K ahead on</th><th style="width:28%">The other ahead on</th><th style="width:22%">Net</th></tr>
</thead>
<tbody>
<tr><td>AAA (1994, ✝)</td><td>Buildability; ~10<sup>2</sup>–10<sup>3</sup>× memory and I/O; openness; 4K</td><td>Native 68k compatibility</td><td>A5K, by 1.5–3 orders</td></tr>
<tr><td>Hombre (1995, ✝)</td><td>Openness, cost, memory, survivability, tools</td><td>An integrated 3D pipeline</td><td>A5K, except in 3D</td></tr>
<tr><td>OCS / ECS / AGA (shipped)</td><td>~10<sup>3</sup>× memory, 4K, PCIe, open toolchain</td><td>Shipped software, real 68k, a market</td><td>Different machines, not successors</td></tr>
<tr><td>2026 lab workstation</td><td>Bounded display latency, power, comprehensibility</td><td>10<sup>4</sup>–10<sup>5</sup>× FP64, 10<sup>3</sup>× memory, the entire software stack</td><td>The workstation, by 4–5 orders</td></tr>
</tbody>
</table>

<h2 id="cm">How these numbers were derived</h2>

<ul>
  <li><strong>OCS / ECS / AGA:</strong> published hardware reference manuals and contemporary datasheets; figures are nominal, not measured on a specific board.</li>
  <li><strong>AAA and Hombre:</strong> contemporary documentation and press coverage. Neither specification was ever frozen, so ranges are given rather than points, and the cancelling decisions mean no benchmark exists.</li>
  <li><strong>A5K:</strong> the bill of materials in Appendix C of the main document, plus vendor datasheet figures for the ECP5-85 / Artix-7 200T families and DDR3L at 1600 MT/s.</li>
  <li><strong>Workstation:</strong> current-generation vendor figures for a dual-socket, 128-core-per-socket node with eight accelerators. A single-seat workstation is roughly one order slower and half a terabyte smaller; the ratios do not change by more than that.</li>
  <li><strong>All ratios</strong> are order-of-magnitude and rounded deliberately. A factor of two is noise at this scale; the arguments rest on orders, not decimals.</li>
</ul>

<div class="bpl">
  <span class="bplabel">Legal notice</span>
  <p><strong>Not a clone.</strong> This work contains no Commodore code, ships no Kickstart ROM and offers no binary compatibility with Amiga software. It is an independent re-issue of the architecture’s ideas; the relevant patents expired by 2012 and the mask-work term is ten years.</p>
  <p>Amiga and Commodore are trademarks of their respective owners. This is an independent design study, not affiliated with, endorsed by or sponsored by any rights holder. Comparisons are estimates and opinion, not statements of fact about any company. Provided “as is”, without warranty of any kind, and not for safety-critical, medical, life-support, aviation or aerospace use. To the maximum extent permitted by law the author accepts no liability for any loss arising from its use. <strong>The author publishes information and does not manufacture or sell goods.</strong> Full notice: LEGAL.md. Not legal advice.</p>
</div>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Where This Design Sits — Addendum</title>
<style>{css}{extra}</style>
</head>
<body>
{body}
</body>
</html>
"""
open(HTML, "w", encoding="utf-8").write(html)

# ------------------------------------------------------------- render ----
subprocess.run(["chromium", "--headless=new", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--print-to-pdf=" + TMP,
                "file://" + HTML], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

doc = pymupdf.open(TMP)

heads = [("1. Why the A5K is better than AAA", "1. Why the A5K is better than AAA - and by how far"),
         ("2. Why it is better than Hombre", "2. Why it is better than Hombre - and where Hombre was ahead"),
         ("3. The three Amiga eras", "3. The three Amiga eras, side by side"),
         ("4. Against a cutting-edge scientific workstation", "4. Against a cutting-edge scientific workstation"),
         ("5. The honest bottom line", "5. The honest bottom line"),
         ("How these numbers were derived", "How these numbers were derived")]

toc = [[1, "Title", 1]]
for needle, label in heads:
    for i, page in enumerate(doc):
        if needle in page.get_text():
            toc.append([1, label, i + 1])
            break

# ------------------------------------------------------------------ folios
for i, page in enumerate(doc):
    w, h = page.rect.width, page.rect.height
    page.draw_line(pymupdf.Point(w * 0.10, h - 30),
                   pymupdf.Point(w * 0.90, h - 30),
                   color=(0.80, 0.80, 0.80), width=0.5)
    page.insert_text((w * 0.10, h - 19),
                     "Rev. AG \u00b7 2 Nov 2026 \u00b7 start 30 Oct 2026",
                     fontname="helv", fontsize=6.8, color=(0.45, 0.45, 0.45))
    title = "A5K \u00b7 Addendum \u2014 Comparative Analysis"
    tw = pymupdf.get_text_length(title, fontname="helv", fontsize=7.2)
    page.insert_text(((w - tw) / 2, h - 19), title,
                     fontname="helv", fontsize=7.2, color=(0.45, 0.45, 0.45))
    tw = pymupdf.get_text_length(label, fontname="helv", fontsize=8)
    page.insert_text((w * 0.90 - tw, h - 19), label,
                     fontname="helv", fontsize=8, color=(0.2, 0.2, 0.2))

doc.set_toc(toc)
doc.set_metadata({
    "title": "Where This Design Sits - Addendum to A5K (Rev. AG)",
    "author": "Design study",
    "subject": "Comparative analysis: AAA, Hombre, the shipped Amiga eras, and a 2026 scientific workstation",
    "keywords": "Amiga, AAA, Hombre, OCS, ECS, AGA, RISC-V, FPGA, workstation, comparison",
    "creator": "LiteX-inspired design study",
})
doc.save(PDF, deflate=True, garbage=4)
doc.close()
print("wrote %s (%d pages)" % (PDF, pymupdf.open(PDF).page_count))
