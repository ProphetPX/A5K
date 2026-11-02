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
| Slot clock | 7.09 MHz | **148.5 MHz proposed** | locked to the pixel clock |
| Planes | 8 sprites, 16 px wide | **planes, arbitrary width** | the modern equivalent, per Appendix A.5 |
| Borrowing | blitter takes idle slots | **explicit window** | predictability beats opportunism |

The line-time change is the one that matters most, and it is not obvious:

> At 60 Hz a scanline lasts 14.8 µs. At a 7.09 MHz tick that is **105 Copper
> instructions per line** — against 454 on a PAL Amiga. Four times fewer ticks
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
| **Tick** | 141 ns (7.09 MHz) | Copper instructions, beam position |
| **Slot** | 6.73 ns (148.5 MHz), 64-bit | Bus transfers |

One tick = **21 slots**. The Copper runs on ticks; the memory runs on slots. A
WAIT position is a tick; the data a WAIT protects arrives in slots.

### 4.2 The budget

Proposed: slot clock locked to the pixel clock at 148.5 MHz, 64 bits wide
(1.19 GB/s peak, about 18% of the DDR3L's 6.4 GB/s).

| Mode | Line time | Slots/line | Ticks/line | 8-plane fetch | Utilisation |
|---|---|---|---|---|---|
| 640×512 @ 50 Hz | 64.0 µs | 9,504 | 454 | 80 slots | 0.8% |
| 1080p60 | 14.8 µs | 2,200 | 105 | 240 slots | 11% |
| 4K60 | 7.4 µs | 1,100 | 52 | 480 slots | 44% |

The pattern is worth pausing on: at 640×512 the bus is almost idle, at 1080p it
is comfortable, and at 4K the display alone takes nearly half the line before
the blitter, the planes or the Copper have asked for anything.

### 4.3 What full-width ARGB costs

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

### 4.4 Allocation policy (proposed)

A line is divided into four bands:

1. **Display band** — slots reserved for bitplane and plane fetches, positioned
   immediately ahead of the beam so the shifter never starves.
2. **Blitter window** — a guaranteed 25% of slots (550 at 1080p), so a blit has a
   predictable worst case.
3. **Service band** — Copper fetches (2 slots per instruction), audio DMA,
   refresh, SD.
4. **Host window** — whatever remains, offered to PCIe DMA.

The blitter may borrow from the host window but never from the display band.
That single rule is what makes "the picture never tears because of a blit"
provable rather than hopeful.

### 4.5 The descriptor

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

### 4.6 What is still open

- Whether 64 bits is right, or 128 bits at half the clock. Both meet the budget;
  the choice hinges on FPGA pin count.
- Whether the blitter window should scale with the frame rate.
- Whether the Copper's fetches belong in the service band or get their own.
- What happens when a display fetch misses its slot — stall the beam, or repeat
  the last pixel? The original repeated; a modern machine might prefer a stall.

## 5. For programmers

### 5.1 WAIT is in ticks, not pixels

An MC-1 WAIT takes a packed `(V << 12) | H`, where H is a **dot-clock** position.
Dots are pixel clocks, not slots. At 1080p there are 2,200 dots per line and
2,200 slots, so they coincide; at 640×512 they do not.

Rule of thumb: **one tick is 21 dots at 1080p**, so a Copper instruction that
takes one tick advances the beam by about 21 pixels. A list that changes a colour
every 16 pixels is not possible at 1080p; every 32 pixels is comfortable.

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
| Copper (2 slots × 105 ticks) | 210 | 10% |
| Audio, refresh, SD | 96 | 4% |
| Blitter window | 550 | 25% |
| Remaining for host | 976 | 44% |

The picture is honest: at 1080p there is room to spare. At 4K the same list needs
480 slots for the bitplanes alone, and the blitter window has to shrink to about
15% to keep the display fed — which is exactly the kind of trade this document
exists to make visible before anyone writes RTL.

---

*Proposal, 2 November 2026. Figures are arithmetic, not measurements. Corrections
welcome — particularly on the 4K allocation, which is the tightest case.*
