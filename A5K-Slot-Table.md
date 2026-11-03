# The slot table

**Why this document exists.** Every modern description of the A5K says "the slot
table is the machine's timing contract" and then moves on. This document
explains what that means, how it differs from the Amiga, and what a builder or a
programmer has to know to use it.

*This document describes the single-pipeline machine. The dual-pipeline
variants, and what changes about arbitration when there are two beams, are in
`A5K-Family.md`.*

**This document specifies A5K (C+), the frozen reference model** — one beam, one
Copper, one slot table. The dual-pipeline variants and their arbitration are in
`A5K-Family.md`.

**Status: proposal, not measurement.** The figures below are arithmetic from
clock rates, bus widths and pixel formats. Nothing has been simulated or built.
Where a number is a design choice rather than a consequence, it is marked.

---

## 1. What a slot is

A computer's memory bus can be shared in two ways. Most modern machines share it
*between requests*: whoever asks first wins, and the loser waits. The Amiga — and
this design — shares it *by time*: every fixed interval belongs to a named
owner in advance, and everyone knows whose turn it is.

That fixed interval is a **slot**. In the original it was one cycle of the 7.09
MHz chip bus — **141 nanoseconds**. In 141 ns, light travels about 42 metres; a
modern CPU executes a few hundred instructions; and on an Amiga, one bitplane
word is fetched.

The **slot table** is the rota: for every slot in a scanline, which unit owns the
bus. It is written before the frame begins, not negotiated during it.

Why bother? Because a rota can be *counted*. If the Copper says "wait until line
214, slot 40", that is a promise the hardware can keep, every frame, forever. A
request-based bus can only promise "soon, usually". Everywhere this design claims
deterministic timing, it is really claiming that the rota exists and is honest.

## 2. What the original did

The Amiga's numbers, for reference:

| | Amiga (PAL) |
|---|---|
| Line time | 64 µs |
| Line rate | 15.625 kHz |
| Chip bus | 7.09 MHz, 16-bit |
| Bus ticks per line | ~454 |
| Colour clocks per line | 227.5 |
| Max bitplanes | 8 (AGA) |
| Sprites | 8, fetched by their own DMA |

At 640 pixels wide and 8 planes, a line needs 5,120 bits — **320 words**. Against
454 ticks, that is about 70% of the bus, which is why an 8-plane AGA screen left
so little room for anything else.

The elegance was the *borrowing rule*: the blitter used slots the display did not
need, and the Copper could wait on a blitter-finished flag. Demoscene code was
written against those exact rules, which is why "cycle exact" means something
specific to Amiga people.

## 3. What changes here, and why

| | Amiga | A5K | Why |
|---|---|---|---|
| Line time at 60 Hz | 64 µs (50 Hz) | **14.8 µs** | 1,125 lines instead of 313 |
| Ticks per line | ~454 | **~105** | four times fewer, four times more lines |
| Bus width | 16-bit | **64-bit proposed** | 8 planes at HD need the width |
| Slot clock | 7.09 MHz | **148.5 MHz fixed** | a PLL output, not the pixel clock |
| Tick | 7.09 MHz, from the colour clock | **7.0714 MHz** (148.5 ÷ 21) | an exact integer ratio to the bus |
| Planes | 8 sprites, 16 px wide | **planes, arbitrary width** | the modern equivalent, per Appendix A.5 |
| Borrowing | blitter takes idle slots | **explicit window** | predictability beats opportunism |

The line-time change is the one that matters most, and it is not obvious:

> At 60 Hz a scanline lasts 14.8 µs. At a 7.0714 MHz tick that is **105 Copper
> positions per line** — against 454 on a PAL Amiga. Four times fewer ticks
> per line, but 1,125 lines instead of 313.

So a Copper list written for PAL timing has roughly four times less room per
line, and nearly four times more lines to play with. Nothing written for the
original will "just work"; everything has to be re-timed. That is a real
incompatibility and this document exists partly to say so plainly.

## 4. The table itself

### 4.1 Two currencies

Builders and programmers need different units, and confusing them is the most
common mistake:

| Unit | Length | Counts |
|---|---|---|
| **Tick** | 141.4 ns (7.0714 MHz) | Copper instructions, beam position |
| **Slot** | 6.73 ns (148.5 MHz); 64-bit on C+, 256-bit on Studio | Bus transfers |

One tick = **exactly 21 slots**, because 148.5 ÷ 21 = 7.0714. This is the one
place the design deliberately leaves the Amiga behind: 7.09 does not divide
148.5, and the nearest whole-slot approximation drifts five slots per line. The
tick is therefore **0.26% slower than the Amiga's** — one part in 380, below the
tolerance of any timing constant that matters — in exchange for an exact ratio.
A drift of 5 slots per line is not a rounding error; it is the machine counting
wrong.

The Copper runs on ticks; the memory runs on slots. A WAIT position is a tick;
the data a WAIT protects arrives in slots.

A line is not a whole number of ticks. At 1080p it is 104 full ticks and a
16-slot tail; the H counter resets at the start of every line and the trailing
partial tick is truncated, so the tail falls in horizontal blanking and **every
line presents the same tick positions, 0 to 104**. Line-invariant timing is
worth more than 108 ns of Copper time.

### 4.2 The budget

The slot clock is a **fixed 148.5 MHz PLL output**, not the pixel clock. The two
coincide only where a mode happens to use 148.5 MHz dots: 1080p has 2,200 dots
and 2,200 slots per line, and 4K has 1,100 of each. At 640×512 the dot clock is
about 25 MHz and the bus still runs at 148.5 MHz — which is why the table below
lists 9,504 slots for that mode and not 1,600.

**Slot width differs by model** — 64 bits on C+ (1.19 GB/s, about 18% of the
DDR3L's 6.4 GB/s) and 256 bits on the Studio models (4.75 GB/s, about 74%).

| Mode | Line time | Slots/line | Tick positions | 8-plane fetch | Utilisation |
|---|---|---|---|---|---|
| 640×512 @ 50 Hz | 64.0 µs | 9,504 | 453 | 80 slots | 0.8% |
| 1080p60 | 14.81 µs | 2,200 | 105 | 240 slots | 11% |
| 4K60 | 7.41 µs | 1,100 | 53 | 480 slots | 44% |

"Tick positions" counts the truncated tail tick as one position: 104 full ticks
plus a short one at 1080p, 52 plus a short one at 4K, 452 plus a short one at
640×512.

The pattern is worth pausing on: at 640×512 the bus is almost idle, at 1080p it
is comfortable, and at 4K the display alone takes nearly half the line before
the blitter, the planes or the Copper have asked for anything.

### 4.3 What HDR and capture cost on the Studio models

256-bit slots give 4.75 GB/s. That is what makes 10-bit HDR and 10-bit capture
possible at the same time:

| Traffic at 4K60 | Bandwidth | Share of 4.75 GB/s |
|---|---|---|
| 10-bit 4:4:4 output | 1.87 GB/s | 39% |
| 10-bit 4:2:2 output | 1.24 GB/s | 26% |
| 1080p60 10-bit capture | 0.47 GB/s | 10% |
| **4:4:4 out + capture** | **2.34 GB/s** | **49%** |
| **two 4:4:4 pipelines + capture** | **4.21 GB/s** | **89%** |

Two independent 4K60 HDR pipes plus capture is the tightest case in the family and
it still fits — with 11% left for the blitter and the Copper. That margin is thin,
which is why the Studio Pro uses a 325T and a -3 speed grade.

At 128 bits the same traffic would be 98% and 177%: the first leaves no room for a
blit, the second is impossible. **256-bit is not a luxury on the Studio line; it is
the minimum that meets the specification.**

### 4.4 What full-width ARGB costs

A plane is not free just because it is fetched rather than blitted:

| Plane width | Bytes/line | Slots | At 1080p | At 4K |
|---|---|---|---|---|
| 256 px, ARGB8888 | 1,024 | 128 | 6% | 12% |
| 1,920 px, ARGB8888 | 7,680 | 960 | **44%** | — |
| 3,840 px, ARGB8888 | 15,360 | 1,920 | — | **175%, impossible** |

Which gives a design rule rather than a limitation: **full-screen ARGB planes
work at 1080p and do not work at 4K.** At 4K the background must be planar, and
overlays must be partial-width — exactly the trade the original made for
different reasons.

### 4.5 Allocation policy (proposed)

A line is divided into four bands:

1. **Display band** — slots reserved for bitplane and plane fetches, positioned
   immediately ahead of the beam so the shifter never starves.
2. **Blitter window** — a guaranteed 25% of slots (550 at 1080p), so a blit has a
   predictable worst case.
3. **Service band** — Copper fetches (**1 slot per instruction**: an MC-1
   instruction is 64 bits, exactly one slot), audio DMA, refresh, SD. Refresh
   is not free and not optional: at 350 ns every 7.8 µs it costs **4.5% of the
   bus in every mode**, because it is a property of the DRAM and not of the
   display timing.
4. **Host window** — whatever remains, offered to PCIe DMA.

The blitter may borrow from the host window but never from the display band.
That single rule is what makes "the picture never tears because of a blit"
provable rather than hopeful.

### 4.6 The descriptor

Each slot is described by a 32-bit word, held in a small table in fabric:

| Bits | Field |
|---|---|
| 7:0 | Owner ID (bitplane n, plane n, blitter, Copper, audio n, refresh, host) |
| 15:8 | Burst length in slots |
| 23:16 | Flags (borrowable, stealable, must-complete) |
| 31:24 | Reserved |

The table is **generated from registers**, not stored per mode: line length,
plane count and plane widths determine the display band, and the rest follows a
fixed pattern. Only the override window is written by software.

### 4.7 What is still open

- Slot width is settled: 64 bits on C+, 256 bits on Studio. What remains open is
  whether 256 bits closes timing at 148.5 MHz on a -2 part, or whether the Studio
  needs a -3 speed grade.
- The tick is settled: 148.5 ÷ 21 on every model, with a second domain reserved
  but not built (§6). The rate of that second domain is deliberately still open.
- Whether the blitter window should scale with the frame rate.
- Whether the Copper's fetches belong in the service band or get their own.
- What happens when a display fetch misses its slot — stall the beam, or repeat
  the last pixel? The original repeated; a modern machine might prefer a stall.

## 5. For programmers

### 5.1 WAIT is in ticks, not pixels

An MC-1 WAIT takes a packed `(V << 12) | H`. H is a **tick** position within the
line, not a pixel: at 1080p the positions run 0–104, at 4K 0–52, at 640×512
0–452. Twelve bits address every mode in the family with room to spare, and the
field does not widen when the fast tick of §6 is enabled — which is the whole
reason H is counted in ticks rather than dots. A dot-clock H field would need
13 bits to reach the 4,400 dots of a 4K line, and would then need 14 or more at
the fast tick.

The beam is therefore addressable to **one tick**: 21 dots at 1080p, 8 at 4K.
Rule of thumb: a Copper instruction that takes one tick advances the beam by
about 21 pixels at 1080p, so a list that changes a colour every 16 pixels is not
possible; every 32 pixels is comfortable.

### 5.2 The blitter is never instantaneous

A blit does not complete at a fixed time. It completes when its slots have been
granted, which depends on what else is fetching. Two consequences:

- Poll the **blitter-busy** flag, or use a Copper WAIT with the blitter flag set.
  Do not assume a blit finished because N microseconds passed.
- A large blit during the visible line will stretch, because the display band
  takes priority. Schedule big fills for vblank.

### 5.3 Three rules that prevent most bugs

1. **Never write a buffer the beam is reading.** Double-buffer, and swap at
   `END`, which the hardware defers to vblank.
2. **Compute your budget before you ship.** Count the slots your planes need per
   line; if the display band is above ~60%, the blitter window will starve and
   your effects will jitter.
3. **Do not port PAL timing arithmetic.** A list that fits in 454 ticks does not
   fit in 105. Re-derive the positions from the mode you are actually running.

### 5.4 A worked example

1080p, 8 planar bitplanes, one 256-pixel overlay, a 50,000-pixel fill during
vblank:

| Item | Slots/line | Share |
|---|---|---|
| 8 bitplanes | 240 | 11% |
| 1 overlay, 256 px | 128 | 6% |
| Copper (1 slot × 105 positions) | 105 | 5% |
| Refresh, audio, SD | 100 | 5% |
| Blitter window | 550 | 25% |
| Remaining for host | 1,077 | 49% |

The picture is honest: at 1080p there is room to spare. At 4K the same list needs
480 slots for the bitplanes alone, and the blitter window has to shrink to about
15% to keep the display fed — which is exactly the kind of trade this document
exists to make visible before anyone writes RTL.

## 6. The second tick domain, reserved

Every model ships **one** tick, and it is 7.0714 MHz. Nothing in the family
executes a Copper instruction at any other rate today.

The Studio class is designed to be able to add a **second, faster tick domain**
later, as a hardware mode selected at run time. What is reserved now is not the
rate. It is the four things that would be expensive to change afterwards:

1. **C+ never gets it.** The reference model is frozen at one tick. If a fast
   domain ever appears, it appears above C+, and C+ remains valid as written.
2. **A tick is always an integer number of slots.** This is the rule that made
   the tick 7.0714 MHz in the first place, and it binds the fast domain too. It
   has a consequence worth stating plainly: **exact doubling is unavailable.**
   21 ÷ 2 = 10.5 slots, which is not a whole number. The usable rates are the
   integer divisors, and they are not the ratios a marketing sheet would pick:

   | Slots/tick | Tick | vs C+ | Positions at 1080p | at 4K | Copper ceiling |
   |---|---|---|---|---|---|
   | 21 | 7.0714 MHz | 1.00× | 105 | 53 | 4.8% |
   | 10 | 14.85 MHz | 2.10× | 220 | 110 | 10.0% |
   | 7 | 21.214 MHz | 3.00× | 315 | 158 | 14.3% |
   | 5 | 29.7 MHz | 4.20× | 440 | 220 | 20.0% |
   | 3 | 49.5 MHz | 7.00× | 734 | 367 | 33.3% |

3. **The Copper's ceiling is exactly 1/N of the bus**, because an instruction
   costs one slot and a tick is N slots. At the shipping tick that is 4.8% —
   which is why the Copper in §5.4 costs 105 slots and not 2,200. A 3× domain
   raises that ceiling to 14.3%, and 14.3% of a 4K line is more than the
   bitplane fetch. **The fast tick is a bandwidth purchase, not a free speed-up**,
   and the budget has to be re-run before it is switched on.
4. **The domain changes only at `END`.** A WAIT whose meaning changes mid-frame
   is not a contract. The swap follows the same rule as the Copper list swap:
   queued, applied at the frame boundary, never during a line.

The register space is reserved now, and costs nothing:

| Bits | Register | Meaning |
|---|---|---|
| `BEAMCON0[3:1]` | 0x0018 | Tick divisor select. `000` = 21 slots (7.0714 MHz), the only value implemented |
| `BEAMCON0[3:1]` writes | 0x0018 | Ignored on C+ and on the current Studio models; reads back `000` |

Software that wants to know probes the field: write, read back, restore. On every
model shipping today it reads `000`, which is the truth.

**Deliberately deferred:** the rate; whether one domain serves both beams or each
beam has its own, which follows the arbitration question in §4.7; whether a fast
domain adds a sub-tick H counter for finer WAIT granularity. None of those
constrains C+, and all of them are cheaper to decide with a simulator than with a
board.

## 7. Ceilings

Better stated than discovered:

| Bound | Value | Why |
|---|---|---|
| Frame rate | **60 Hz fixed** | the rota and the Copper list are regenerated once per frame; variable refresh would invalidate both |
| Resolution | **4K** (3,840 × 2,160) | V is 12 bits, 4,095 lines; 8K needs 4,320 and does not fit |
| Frame rate at 4K | **60 Hz** | 1,100 slots per line, 480 taken by eight planes; 4K120 halves the line to 550 slots and the display alone would be 87% |
| Planes at 4K | planar, plus partial overlays | a full-width ARGB plane is 175% of a line (§4.4) |
| Copper | one instruction per tick | 4.8% of the bus at 7.0714 MHz; a faster domain is a bandwidth trade (§6) |

C+ is a 60 Hz, 4K, fixed-timing machine. That is a constraint, not a shortcoming,
and every one of these ceilings is the price of the property the machine exists
for: the schedule is countable because it never has to be renegotiated.

---

*Proposal, 2 November 2026. Figures are arithmetic, not measurements. Corrections
welcome — particularly on the 4K allocation, which is the tightest case.*

**Still outstanding in this document:** the memory schedule is written in slots
of 8 bytes, but DDR3L transfers in 32-byte bursts with 16 ns latency and 30–40 ns
page misses. Until the display band is rewritten as bursts into line buffers,
with FIFO depth and fetch-ahead distance stated, the per-line schedule cannot be
implemented as drawn. That is the next revision, and it is a change of model
rather than a correction of arithmetic.

---

*Rev. T · 2 November 2026 · project started 30 October 2026*
