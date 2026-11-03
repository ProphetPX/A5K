#!/usr/bin/env python3
"""Build the A5K technical specification card."""
import os, re, subprocess
import atexit, shutil, tempfile
import pymupdf

BASE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(BASE, "A5K-Design-Proposition.html")
HTML = os.path.join(BASE, "A5K-Technical-Specifications.html")
PDF = os.path.join(BASE, "A5K-Technical-Specifications.pdf")

# Per-run scratch directory: no assumption about the host harness, and it
# cleans itself up even if the build fails.
_TMPDIR = tempfile.mkdtemp(prefix="a5k-build-")
atexit.register(shutil.rmtree, _TMPDIR, ignore_errors=True)

TMP = os.path.join(_TMPDIR, "spec_pass.pdf")

main = open(MAIN, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", main, re.S).group(1)

extra = """
  .spec-head {
    border-bottom: 2.5pt solid #b03030;
    padding-bottom: 9pt;
    margin-bottom: 12pt;
  }
  .spec-head h1 { font-size: 24pt; margin: 2pt 0 5pt 0; }
  .spec-head .kicker { margin-bottom: 4pt; }
  .statusline {
    background: #f6f1e7;
    border-left: 2.5pt solid #b03030;
    padding: 6pt 9pt;
    font-size: 8.4pt;
    line-height: 1.45;
    margin: 0 0 12pt 0;
    font-family: "DejaVu Sans", Helvetica, Arial, sans-serif;
    color: #333;
  }
  .spec h2 { margin-top: 16pt; }
  .spec table { font-size: 7.5pt; margin: 4pt 0 10pt 0; }
  .spec td, .spec th { padding: 3.2pt 4.5pt; }
  .spec .num { text-align: right; font-variant-numeric: tabular-nums; }
  .spec .note { font-size: 8.4pt; color: #555; }
"""

body = r"""
<div class="spec-head">
  <p class="kicker">Reference card &middot; Rev. AK</p>
  <h1>A5K — Technical Specifications</h1>
  <p class="subtitle">Clocks, memory, processors, bandwidth and the limits they impose</p>
  <p class="meta">Rev. AK &nbsp;·&nbsp; 2 November 2026 &nbsp;·&nbsp; Companion to the design proposition &nbsp;·&nbsp; Figures are targets, not measurements</p>
</div>

<div class="statusline">
  <strong>Design study.</strong> Nothing described here has been built or measured. Clock rates are synthesis estimates for the named device families; bandwidth figures are arithmetic from bus width and data rate; processor core counts are what the logic can hold, not what the software needs.
</div>

<div class="spec">

<h2 id="sp1">1. What this is — and what it is not</h2>

<p><strong>This document specifies A5K (C+), the frozen reference model.</strong> It is a PCIe add-in card. It is not a computer, not a single-board machine, and not a replacement for a motherboard. It has no CPU, no boot firmware and no operating system of its own. It is a display and timing device that plugs into a host PC, in the same mechanical and electrical class as a graphics card.</p>

<table>
<caption><strong>Table S1.</strong> Product classes, and which one exists.</caption>
<thead>
<tr><th style="width:22%">Product</th><th style="width:20%">Status</th><th style="width:30%">Requires</th><th>Provides</th></tr>
</thead>
<tbody>
<tr><td><strong>A5K card</strong></td><td><strong>the current design</strong></td><td>An x86-64 host with a free PCIe slot</td><td>Chipset, Chip RAM, HDMI scanout</td></tr>
<tr><td>A5K module (SoM)</td><td>not designed</td><td>A carrier board</td><td>The same chipset in a socket</td></tr>
<tr><td>A5K mainboard</td><td>mentioned as a form factor only</td><td>Mains power and a case</td><td>A complete machine</td></tr>
</tbody>
</table>

<p>The host supplies the CPU, the memory the OS runs in, the storage and the operating system. The card supplies the chipset, its own Chip RAM and its own display output. Unplug the host and the card is a board with a power LED.</p>

<p><strong>The small RISC-V core on the card is not an application processor.</strong> It is housekeeping — timers, GPIO, the SD card and interrupt aggregation — running bare-metal firmware at 50–150 MHz, with no MMU and no loader. Applications and drivers run on the host, compiled for the host's architecture. The card contributes the chipset, not the CPU.</p>

<p><strong>It cannot be plugged into a Commodore Amiga.</strong> The A2000 has Zorro II, the A3000 and A4000 have Zorro III, the A1200 has a trapdoor and PCMCIA. None of them has PCIe, and no bridge exists that would make a modern card enumerate on a 68k bus.</p>

<h2 id="sp2">2. Host requirements</h2>

<p>Today the card requires an <strong>x86-64 PC</strong>. Other host architectures are technically possible — the interface is standard PCIe — but they are untested, and some RISC-V boards expose only a single lane.</p>

<table>
<caption><strong>Table S2.</strong> Minimum host, and the recommended build.</caption>
<thead>
<tr><th style="width:26%">Item</th><th style="width:32%">Minimum</th><th>Recommended</th></tr>
</thead>
<tbody>
<tr><td>Architecture</td><td>x86-64</td><td>any recent desktop CPU</td></tr>
<tr><td>Processor</td><td>2 cores at 2 GHz</td><td>4 cores, anything from the last decade</td></tr>
<tr><td>System RAM</td><td>4 GB</td><td>8 GB or more</td></tr>
<tr><td>Free slot</td><td>PCIe ×1 electrical or larger, Gen2+</td><td>×4 or ×16 length, Gen3</td></tr>
<tr><td>Slot power</td><td>25 W from the slot, no auxiliary connector</td><td>as minimum</td></tr>
<tr><td>Firmware</td><td>UEFI with Above 4G Decoding enabled</td><td>Resizable BAR also enabled</td></tr>
<tr><td>Operating system</td><td>Linux 6.x with DRM/KMS</td><td>a current distribution</td></tr>
<tr><td>Disk</td><td>20 GB free for tooling</td><td>—</td></tr>
<tr><td>Displays</td><td>one monitor for the host, one for the card</td><td>two inputs on one monitor</td></tr>
<tr><td>Case</td><td>clearance for a low-profile card</td><td>full-height bracket</td></tr>
</tbody>
</table>

<p class="note"><strong>Notes.</strong> A laptop requires a Thunderbolt-to-PCIe enclosure, because the card needs a real slot. Above 4G Decoding must be enabled in UEFI for the 64-bit BAR that maps Chip RAM; on some consumer boards this is the only setting that has to be changed. The card draws roughly 5 W, so a ×4 slot is ample and no power cable is needed.</p>

<h2 id="sp3">3. Why ×1 on the reference card, and ×4 on the Studio Pro</h2>

<p>The reference card is <strong>electrically ×1</strong>. The display is fetched from the card's own DDR3L; PCIe carries Copper lists, register writes and the occasional frame readback. Half a gigabyte per second is already an order of magnitude more than control traffic needs. The Studio Pro uses ×4 because two pipelines and a capture stream want real bandwidth.</p>

<table>
<caption><strong>Table S3.</strong> Slot options, and what each would cost.</caption>
<thead>
<tr><th style="width:14%">Slot</th><th style="width:10%" class="num">Lanes</th><th style="width:22%" class="num">Gen2 / Gen3</th><th style="width:26%">Fits</th><th>Cost</th></tr>
</thead>
<tbody>
<tr><td><strong>×1</strong></td><td class="num">1</td><td class="num">0.5 / 1.0 GB/s</td><td>every slot, including ×1</td><td><strong>C+ reference</strong></td></tr>
<tr><td>×2</td><td class="num">2</td><td class="num">1.0 / 2.0 GB/s</td><td>×2 and larger slots</td><td>Studio variant</td></tr>
<tr><td><strong>×4</strong></td><td class="num">4</td><td class="num">2.0 / 3.9 GB/s</td><td>×4, ×8 and ×16 slots</td><td><strong>Studio Pro</strong></td></tr>
<tr><td>×8 / ×16</td><td class="num">8 / 16</td><td class="num">4–16 GB/s</td><td>rare on desktops</td><td>not used</td></tr>
</tbody>
</table>

<p><strong>The lane budget decides it.</strong> An Artix-7 100T has exactly four GTP transceivers, and 4K60 output consumes three of them for HDMI. One is left, and that is the PCIe link: ×1. The Studio Pro moves to a Kintex-7 325T, where sixteen transceivers allow two 4K60 transmitters and ×4 to the host.</p>

<p><strong>A ×1 card still fits any slot.</strong> A ×1 card seats in ×1, ×2, ×4, ×8 and ×16 connectors, including the ×4 slot a desktop usually has free. The physical connector on the reference card is ×4-length for mechanical stability; the link is ×1.</p>

<h2 id="sp4">4. Clock domains</h2>

<table>
<caption><strong>Table S4.</strong> The domains a card would run in.</caption>
<thead>
<tr><th style="width:26%">Domain</th><th style="width:22%">Rate</th><th>Purpose</th></tr>
</thead>
<tbody>
<tr><td>Copper / chip bus</td><td>7.0714 MHz (141.4 ns)</td><td>One instruction per tick; exactly 21 slots of the 148.5 MHz bus. The machine's timing contract</td></tr>
<tr><td>Pixel clock, 1080p60</td><td>148.5 MHz</td><td>Scanout</td></tr>
<tr><td>Pixel clock, 4K60</td><td>594 MHz (4 lanes)</td><td>Scanout, above the fabric's comfort zone</td></tr>
<tr><td>DDR3L</td><td>800 MHz (1600 MT/s)</td><td>Chip RAM</td></tr>
<tr><td>PCIe reference</td><td>100 MHz</td><td>Link training and packet clock</td></tr>
<tr><td>Host CPU</td><td>external</td><td>Whatever the host provides</td></tr>
</tbody>
</table>

<h2 id="sp5">5. Memory</h2>

<table>
<caption><strong>Table S5.</strong> Chip RAM configurations.</caption>
<thead>
<tr><th style="width:20%">Configuration</th><th style="width:24%">Devices</th><th style="width:14%" class="num">Capacity</th><th style="width:16%" class="num">Bandwidth</th><th>Note</th></tr>
</thead>
<tbody>
<tr><td>Base</td><td>2 × 4 Gb DDR3L, 32-bit</td><td class="num">1 GB</td><td class="num">6.4 GB/s</td><td>as costed in the BOM</td></tr>
<tr><td>Upgrade</td><td>2 × 8 Gb DDR3L, 32-bit</td><td class="num">2 GB</td><td class="num">6.4 GB/s</td><td>same package, drop-in</td></tr>
<tr><td>Maximum</td><td>4 × 8 Gb, two ranks</td><td class="num">4 GB</td><td class="num">6.4 GB/s</td><td>top of the 32-bit space</td></tr>
<tr><td>Architectural ceiling</td><td>32-bit byte addressing</td><td class="num">4 GiB</td><td class="num">—</td><td>~3.5 GB usable after registers and apertures</td></tr>
<tr><td>64-bit variant</td><td>4 × 16 Gb DDR4</td><td class="num">8–32 GB</td><td class="num">12.8–25 GB/s</td><td>wider bus and 40-bit pointers; new part</td></tr>
</tbody>
</table>

<p><strong>Why DDR3L, and not DDR5.</strong> The target families cannot drive DDR5 at all — it needs an UltraScale+ or Versal part, at roughly ten times the FPGA cost. DDR3L is still in production for industrial and networking equipment, is stocked by every distributor, and costs about $7 per 512 MB. A 32-bit DDR3L bus supplies 6.4 GB/s, which is more than the slot table can consume. DDR5 would solve a bandwidth problem this machine does not have, at a price it cannot pay.</p>

<p><strong>Upgrade path.</strong> 1 GB to 2 GB is a device swap in the same footprint — 4 Gb parts for 8 Gb. 2 GB to 4 GB needs two ranks and rank support in the memory controller. Beyond 4 GiB the obstacle is not the memory but the pointer width: the 64-bit variant widens both, and moves to DDR4.</p>

<p class="note"><strong>ECC</strong> is the more valuable upgrade for instrumentation work than capacity: on a 32-bit bus it means 40 bits and five x8 devices instead of two x16. DDR3 tops out at 8 Gb per device, which is why 4 GB is the wall for the 32-bit design. Host memory is reached by DMA over PCIe and is not limited by the card.</p>

<h2 id="sp6">6. Processors</h2>

<p>There are two CPU positions in this design, and they are not interchangeable.</p>

<table>
<caption><strong>Table S6.</strong> Processor options, clock and cores.</caption>
<thead>
<tr><th style="width:24%">Option</th><th style="width:12%">Kind</th><th style="width:14%" class="num">Max clock</th><th style="width:14%" class="num">Cores</th><th>Where it runs</th></tr>
</thead>
<tbody>
<tr><td>VexRiscv on ECP5-85</td><td>soft</td><td class="num">~50 MHz</td><td class="num">1–4</td><td>On the card; housekeeping</td></tr>
<tr><td>VexRiscv on Artix-7 200T</td><td>soft</td><td class="num">100–150 MHz</td><td class="num">1–8</td><td>On the card; practical sweet spot</td></tr>
<tr><td>Microblaze on Artix-7</td><td>soft</td><td class="num">~200 MHz</td><td class="num">1–8</td><td>Vendor core, closed toolchain</td></tr>
<tr><td>Rocket / CVA6</td><td>soft</td><td class="num">50–100 MHz</td><td class="num">1–4</td><td>Needs a larger part</td></tr>
<tr><td>PolarFire SoC</td><td>hard</td><td class="num">667 MHz</td><td class="num">4 + 1</td><td>Hardened cluster beside the fabric</td></tr>
<tr><td>x86-64 host</td><td>hard</td><td class="num">4–6 GHz</td><td class="num">4–256</td><td>PC, outside the card</td></tr>
<tr><td>RISC-V host (P670 class)</td><td>hard</td><td class="num">~2–2.5 GHz</td><td class="num">1–16</td><td>Host board</td></tr>
</tbody>
</table>

<p class="note"><strong>The on-card core is a supervisor, not an engine.</strong> It runs CIA timers, GPIO and interrupt aggregation. Whether it runs at 50 MHz or 667 MHz changes almost nothing, because it does not draw pixels — the Copper, blitter and planes do. Spending fabric on clock speed here is spending it in the wrong place. The heavy work belongs on the host, on the other side of PCIe.</p>

<h2 id="sp7">7. Bandwidth budget at 4K60</h2>

<p>3840 × 2160 = 8.29 megapixels. The 32-bit DDR3L bus supplies 6.4 GB/s of raw memory, but the <strong>64-bit slot fabric supplies only 1.19 GB/s</strong> — the fabric, not the memory, is the limit, and it is the same on every model. The slot table must also fit the Copper, the blitter and audio into the same schedule. Slot width differs by model: <strong>64 bits on C+</strong> (1.19 GB/s) and <strong>256 bits on the Studio models</strong> (4.75 GB/s), which is what makes 10-bit HDR and 10-bit capture possible together.</p>

<table>
<caption><strong>Table S7.</strong> What 4K60 costs, per content type.</caption>
<thead>
<tr><th style="width:40%">Content</th><th style="width:16%" class="num">Per frame</th><th style="width:14%" class="num">At 60 Hz</th><th style="width:15%" class="num">Of 1.19 GB/s</th><th>Verdict</th></tr>
</thead>
<tbody>
<tr><td>8 planar bitplanes (1 bit/px)</td><td class="num">8.3 MB</td><td class="num">0.5 GB/s</td><td class="num">42%</td><td>Comfortable</td></tr>
<tr><td>1 full-screen ARGB8888 plane</td><td class="num">33 MB</td><td class="num">2.0 GB/s</td><td class="num">168%</td><td>Does not fit</td></tr>
<tr><td>2 ARGB planes</td><td class="num">66 MB</td><td class="num">4.0 GB/s</td><td class="num">336%</td><td>No</td></tr>
<tr><td>4 ARGB planes</td><td class="num">133 MB</td><td class="num">8.0 GB/s</td><td class="num">672%</td><td>No</td></tr>
<tr><td>8 ARGB planes</td><td class="num">265 MB</td><td class="num">15.9 GB/s</td><td class="num">1,336%</td><td>No</td></tr>
</tbody>
</table>

<p class="note">This is the quiet argument for planar graphics: at 4K60, eight bitplanes cost 42% of the bus and one full-screen ARGB plane costs 168%. The Amiga's bitmap format was a bandwidth strategy, not a limitation — and on this machine the limit is the slot fabric, not the DRAM behind it.</p>

<h2 id="sp8">8. Parallelism</h2>

<table>
<caption><strong>Table S8.</strong> What runs simultaneously, and what does not.</caption>
<thead>
<tr><th style="width:22%">Unit</th><th style="width:12%" class="num">Count</th><th>Nature</th></tr>
</thead>
<tbody>
<tr><td>Copper</td><td class="num">1</td><td>One sequencer, one instruction per tick; parallel with everything else, serial within itself</td></tr>
<tr><td>Blitter</td><td class="num">1</td><td>One operation at a time, by design</td></tr>
<tr><td>Planes</td><td class="num">8 (16 optional)</td><td>Fetched in parallel each line</td></tr>
<tr><td>Audio channels</td><td class="num">4–8</td><td>Independent DMA streams</td></tr>
<tr><td>Slot table</td><td class="num">1</td><td>Fixed schedule; every cycle allocated before the frame</td></tr>
<tr><td>Host cores</td><td class="num">unbounded</td><td>Outside the card, over PCIe</td></tr>
</tbody>
</table>

<p><strong>Parallelism here is spatial, not threaded.</strong> Roughly twenty independent units run at once because each does one thing forever at a fixed rate — not because anything is scheduled. Adding CPU cores does not add throughput; it adds contention on the same memory. The bound is bandwidth: at 1.19 GB/s of slot fabric, the display pipeline is the budget, and the slot table is the ledger.</p>

<h2 id="sp9">9. Links and ceilings</h2>

<table>
<caption><strong>Table S9.</strong> The buses that bound the design.</caption>
<thead>
<tr><th style="width:34%">Link</th><th style="width:22%" class="num">Bandwidth</th><th>Binds</th></tr>
</thead>
<tbody>
<tr><td>PCIe Gen2 ×1</td><td class="num">0.5 GB/s</td><td>Host ↔ card, A5K (C+)</td></tr>
<tr><td>PCIe Gen2 ×4</td><td class="num">2.0 GB/s</td><td>Host ↔ card, Studio Pro</td></tr>
<tr><td>PCIe Gen3 ×4</td><td class="num">3.9 GB/s</td><td>Host ↔ card, preferred</td></tr>
<tr><td>PCIe Gen4 ×4</td><td class="num">7.9 GB/s</td><td>Host ↔ card, beyond current parts</td></tr>
<tr><td>DDR3L 32-bit</td><td class="num">6.4 GB/s</td><td>Raw; the 64-bit fabric draws 1.19 GB/s of it</td></tr>
<tr><td>Address space</td><td class="num">4 GiB</td><td>Chip RAM ceiling</td></tr>
</tbody>
</table>

<p><strong>What would have to change for more.</strong> More planes at 4K means a wider memory bus before it means more logic. A faster on-card CPU means a hard core, not a bigger soft one. More host bandwidth means Gen3 or Gen4, which means an Artix-7 with GTP or a larger part. Each is a different board, not a different setting.</p>

<h2 id="sp10">10. Video modes, and the way back</h2>

<p>Timings are generated from registers, so a mode is a row in a table, not a circuit. Three tiers matter:</p>

<table>
<caption><strong>Table S10.</strong> The floor, the default and the normal case.</caption>
<thead>
<tr><th style="width:17%">Tier</th><th style="width:25%">Mode</th><th>Why</th></tr>
</thead>
<tbody>
<tr><td><strong>Floor</strong></td><td><strong>640×480 @ 60</strong></td><td>The lowest signal HDMI and DisplayPort can carry — 25.175 MHz. It is also the modern equivalent of Amiga “hi-res”: 640 pixels wide. A 15 kHz Amiga mode cannot be put on either port at all.</td></tr>
<tr><td><strong>Default</strong></td><td><strong>1024×768 @ 60</strong></td><td>XGA: accepted by essentially every display since 1990, and what the card falls back to when there is no EDID to ask. The user may change it; the setting lives in the configuration flash.</td></tr>
<tr><td><strong>Normal</strong></td><td>display preferred, up to 4K60</td><td>On a 4K panel the EDID asks for 4K60, and that is what the card drives.</td></tr>
</tbody>
</table>

<p><strong>The ceiling is a pixel rate, not a list.</strong> Any CEA or VESA timing at or below 594 MHz that the EDID declares is legal: the standard video rates 23.976–60 on two slot clocks (148.35 MHz for the 1000/1001 family), high refresh to 1080p240 and 1440p144, and 4K at 60. <strong>1080p240 costs the same as 4K60</strong> — 497.7 megapixels per second either way — so the budget is per pixel rate, not per resolution.</p>

<p><strong>No variable refresh.</strong> FreeSync, G-Sync Compatible and Intel’s Adaptive Sync only operate when the source offers them; a source that does not leaves the panel at fixed refresh, which every panel accepts. It is a ceiling, like no 8K.</p>

<p><strong>Four rules keep it out of trouble.</strong> Never emit a timing the EDID does not declare; use the preferred timing at boot; implement DPMS D0/D3 only, waking on hotplug and never idling the link; and debounce hotplug for 100 ms, because monitors chatter on power-save. Those four are what separate a card that works with every panel from a card that works with the one on the bench.</p>

<p><strong>First power-on.</strong> Read the EDID and use its preferred timing. No EDID, or nothing readable: come up at <strong>1024×768 @ 60</strong>. Every mode comes from the same registers, so adding one costs a row, not a redesign.</p>

<p><strong>Recovery, for a blank screen.</strong> Four routes, layered, and all four ship:</p>

<ol>
<li><strong>Host register.</strong> PCIe configuration space is independent of video, so a driver can force defaults even when the display is wrong.</li>
<li><strong><code>SAFE_MODE</code> on the microSD.</strong> Drop the file on the card and power-cycle — it comes up at 1024×768 with no host involved.</li>
<li><strong>Button or jumper.</strong> One second at power-on selects safe video; ten seconds restores factory defaults. About $0.15 for a bracket button, $0.02 for a jumper.</li>
<li><strong>Automatic.</strong> No EDID, or no hotplug for ten seconds, and the card cycles 1024×768 → 800×600 → 640×480 until one locks — what a PC BIOS does.</li>
</ol>

<p>Precedence at power-on: button or jumper, then the SD file, then the stored default, then the display’s EDID, then the automatic cycle. The button does not violate the “no physical switch” rule — that rule is about the Auto/HDMI/DP selector, not about recovery.</p>

<h2 id="sp11">11. Quick reference</h2>

<table>
<caption><strong>Table S12.</strong> The numbers worth memorising.</caption>
<thead>
<tr><th style="width:34%">Item</th><th>Figure</th></tr>
</thead>
<tbody>
<tr><td>Product class</td><td>PCIe add-in card — requires a host PC</td></tr>
<tr><td>Host, minimum</td><td>x86-64, 4 GB RAM, free PCIe ×4 slot</td></tr>
<tr><td>Card power</td><td>~5 W from the slot; no auxiliary connector</td></tr>
<tr><td>Chip RAM, base</td><td>1 GB DDR3L, 32-bit, 1600 MT/s</td></tr>
<tr><td>Chip RAM, upgrade</td><td>2 GB — 8 Gb devices, same footprint</td></tr>
<tr><td>Chip RAM, maximum</td><td>4 GB, two ranks</td></tr>
<tr><td>Architectural ceiling</td><td>4 GiB, about 3.5 GB usable</td></tr>
<tr><td>Memory bandwidth</td><td>6.4 GB/s DRAM; 1.19 GB/s usable through the fabric</td></tr>
<tr><td>Copper tick</td><td>7.0714 MHz (148.5 ÷ 21), 141.4 ns per instruction</td></tr>
<tr><td>Scanout</td><td>4K60 at a 594 MHz pixel clock, four lanes</td></tr>
<tr><td>Host link</td><td>PCIe Gen2 ×1 (0.5 GB/s) on C+; ×4 on the Studio Pro</td></tr>
<tr><td>On-card CPU</td><td>VexRiscv, 50 MHz (ECP5) to 150 MHz (Artix-7)</td></tr>
<tr><td>Host CPU</td><td>anything with PCIe; 2–6 GHz, 4–256 cores</td></tr>
<tr><td>Planes</td><td>8, optionally 16</td></tr>
<tr><td>Outputs</td><td>4K60 SDR HDMI (primary), 1080p60 DP (secondary); HDMI sensed first. HDR10 on the Studio models</td></tr>
<tr><td>Mode floor</td><td>640×480 @ 60 — the lowest either port can carry</td></tr>
<tr><td>Refresh</td><td>Fixed only. 24–60 standard rates, 1080p to 240 Hz, 1440p to 144; no VRR</td></tr>
<tr><td>First power-on</td><td>EDID preferred timing; 1024×768 @ 60 when there is no EDID</td></tr>
<tr><td>Fabric</td><td>64-bit slots (C+), 256-bit (Studio), 512-bit reserved (Pro II) — all at 148.5 MHz</td></tr>
<tr><td>Blitters</td><td>1</td></tr>
<tr><td>Audio</td><td>8 channels, 24-bit; factory default 2.0 on every output; 4 jacks, TOSLINK, HDMI/DP LPCM; front-panel HP/mic header; internal clock only (word clock is Studio and above)</td></tr>
<tr><td>4K60 cost, planar</td><td>0.5 GB/s for eight bitplanes</td></tr>
<tr><td>4K60 cost, ARGB</td><td>2.0 GB/s per full-screen plane</td></tr>
</tbody>
</table>

<p class="note">Sources: datasheet figures for the ECP5-85 and Artix-7 200T families, DDR3L at 1600 MT/s, and arithmetic from bus width and pixel format. No figure here has been measured on hardware, because there is no hardware.</p>

</div>
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>A5K — Technical Specifications (Rev. AK)</title>
<style>{css}{extra}</style>
</head>
<body>
{body}
</body>
</html>
"""
open(HTML, "w", encoding="utf-8").write(html)

subprocess.run(["chromium", "--headless=new", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", "--print-to-pdf=" + TMP,
                "file://" + HTML], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

doc = pymupdf.open(TMP)

heads = [("1. What this is", "1. What this is - and what it is not"),
         ("2. Host requirements", "2. Host requirements"),
         ("3. Why ×4", "3. Why x4, and not x8 or x16"),
         ("4. Clock domains", "4. Clock domains"),
         ("5. Memory", "5. Memory"),
         ("6. Processors", "6. Processors"),
         ("7. Bandwidth budget", "7. Bandwidth budget at 4K60"),
         ("8. Parallelism", "8. Parallelism"),
         ("9. Links and ceilings", "9. Links and ceilings"),
         ("10. Quick reference", "10. Quick reference")]

toc = [[1, "Title", 1]]
for needle, label in heads:
    for i, page in enumerate(doc):
        if needle in page.get_text():
            toc.append([1, label, i + 1])
            break

for i, page in enumerate(doc):
    w, h = page.rect.width, page.rect.height
    page.draw_line(pymupdf.Point(w * 0.10, h - 30),
                   pymupdf.Point(w * 0.90, h - 30),
                   color=(0.80, 0.80, 0.80), width=0.5)
    page.insert_text((w * 0.10, h - 19),
                     "Rev. AK \u00b7 3 Nov 2026 \u00b7 start 30 Oct 2026",
                     fontname="helv", fontsize=6.8, color=(0.45, 0.45, 0.45))
    title = "A5K \u00b7 Technical Specifications"
    tw = pymupdf.get_text_length(title, fontname="helv", fontsize=7.2)
    page.insert_text(((w - tw) / 2, h - 19), title,
                     fontname="helv", fontsize=7.2, color=(0.45, 0.45, 0.45))
    label = str(i + 1)
    tw = pymupdf.get_text_length(label, fontname="helv", fontsize=8)
    page.insert_text((w * 0.90 - tw, h - 19), label,
                     fontname="helv", fontsize=8, color=(0.2, 0.2, 0.2))

doc.set_toc(toc)
doc.set_metadata({
    "title": "A5K - Technical Specifications (Rev. AK)",
    "author": "Design study",
    "subject": "Clocks, memory, processors, bandwidth and limits of the A5K design",
    "keywords": "A5K, Amiga-like, FPGA, DDR3L, RISC-V, bandwidth, specification",
})
doc.save(PDF, deflate=True, garbage=4)
doc.close()
print("wrote %s (%d pages)" % (PDF, pymupdf.open(PDF).page_count))
