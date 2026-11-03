# The slot table

**Why this document exists.** Every modern description of the A5K says "the slot
table is the machine's timing contract" and then moves on. This document
explains what that means, how it differs from the Amiga, and what a builder or a
programmer has to know to use it.

**This document specifies A5K (C+), the frozen reference model** — one beam, one
Copper, one slot table. The dual-pipeline variants are in `A5K-Family.md`, and
their arbitration is specified in `A5K-Dual-Pipe-Arbitration.md`.

**Status: proposal, not measurement.** The figures below are arithmetic from
clock rates, bus widths and pixel formats. Nothing has been simulated or built.
Where a number is a design choice rather than a consequence, it is marked.

---

## 1. What a slot is

A computer's memory bus can be shared in two ways. Most modern machines share it
*between requests*: whoever asks first wins, and the loser waits. The Amiga — and
this design — shares it *by time*: every fixed interval belongs to a named
owner in advance, and everyone knows whose turn it is.

That fixed interval is a **slot**. In the original it was one cycle of the chip
bus — **141 nanoseconds on PAL (7.09 MHz), 140 on NTSC (7.16 MHz)**. In that
time light travels about 42 metres; a modern CPU executes a few hundred
instructions; and on an Amiga, one bitplane word is fetched.

The **slot table** is the rota: for every slot in a scanline, which unit owns the
bus. It is written before the frame begins, not negotiated during it.

Why bother? Because a rota can be *counted*. If the Copper says "wait until line
214, slot 40", that is a promise the hardware can keep, every frame, forever. A
request-based bus can only promise "soon, usually". Everywhere this design claims
deterministic timing, it is really claiming that the rota exists and is honest.

## 2. What the original did

The Amiga's numbers, for reference:

| | Amiga (PAL) | Amiga (NTSC) |
|---|---|---|
| Line time | 64.0 µs | 63.56 µs |
| Line rate | 15.625 kHz | 15.734 kHz |
| Lines per frame | 312.5 at 50 Hz | 262.5 at 60 Hz |
| Visible lines | 256 | 200 |
| Chip bus | 7.094 MHz, 16-bit | 7.159 MHz, 16-bit |
| Bus cycles per line | ≈454 | ≈455 |
| Colour clocks per line | 227.5 | 227.5 |
| Max bitplanes | 8 (AGA) | 8 (AGA) |
| Sprites | 8, by their own DMA | 8, by their own DMA |

At 640 pixels wide and 8 planes, a line needs 5,120 bits — **320 words**. Against
454 ticks (PAL) or 455 (NTSC), that is about 70% of the bus either way, which is
why an 8-plane AGA screen left so little room for anything else.

The two standards carry **almost exactly the same number of bus cycles per line**,
because the faster NTSC clock compensates for its shorter line. Only the number
of lines differs: 312.5 against 262.5. That is why a Copper list written for one
usually fits the other — and why "PAL timing" and "NTSC timing" differ far less
than the names suggest.

The elegance was the *borrowing rule*: the blitter used slots the display did not
need, and the Copper could wait on a blitter-finished flag. Demoscene code was
written against those exact rules, which is why "cycle exact" means something
specific to Amiga people.

## 3. What changes here, and why

| | Amiga | A5K | Why |
|---|---|---|---|
| Line time | 64.0 µs PAL / 63.56 µs NTSC | **14.8 µs** | 4.3× shorter, at NTSC's own 60 Hz |
| Ticks per line | ≈454 / ≈455 | **105** | 4.3× fewer |
| Lines per frame | 312.5 / 262.5 | **1,125** | 3.6× more than PAL, 4.3× more than NTSC |
| Bus width | 16-bit | **64-bit** on C+, 256-bit on Studio | 8 planes at HD need the width |
| Transfer quantum | one 16-bit word per cycle | **32 bytes, four slots** | DDR3L cannot do less (§4.3) |
| Slot clock | 7.09 MHz PAL / 7.16 NTSC | **148.5 MHz fixed** | a PLL output, not the pixel clock |
| Tick | 7.09 / 7.16 MHz, from the colour clock | **7.0714 MHz** (148.5 ÷ 21) | an exact integer ratio to the bus |
| Planes | 8 sprites, 16 px wide | **planes, arbitrary width** | the modern equivalent, per Appendix A.5 |
| Borrowing | blitter takes idle slots | **explicit window** | predictability beats opportunism |

The line-time change is the one that matters most, and it is not obvious:

> At 60 Hz a scanline lasts 14.8 µs. At a 7.0714 MHz tick that is **105 Copper
> positions per line** — against 455 on an NTSC Amiga at the same 60 Hz, and 454
> on a PAL one at 50. Four times fewer ticks per line, but 1,125 lines instead
> of 262 or 313.

So a Copper list written for PAL or NTSC timing has roughly four times less room
per line, and nearly four times more lines to play with. Nothing written for the
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

**Slot width differs by model** — 64 bits on C+, 256 on the Studio models, and
512 reserved for the Pro II — giving 1.19, 4.75 and 9.5 GB/s at the slot clock.
The memory behind them is deliberately wider still: 32-bit DDR3L on C+
(6.4 GB/s) and 64-bit on the Studio (12.8 GB/s). **The fabric is the bottleneck on
every model, not the DRAM** — C+ uses 19% of its memory and the Studio 43%.

That is the right way round, and it is what makes the next model cheap: widening
the internal fabric to 512 bits doubles the bus without touching the DRAM, the
pins or the board (§4.4).

| Mode | Line time | Slots/line | Tick positions | 8-plane fetch | Utilisation |
|---|---|---|---|---|---|
| 640×480 @ 60 Hz | 31.8 µs | 4,720 | 225 | 80 slots | 1.7% |
| 1024×768 @ 60 Hz | 20.7 µs | 3,071 | 147 | 128 slots | 4.2% |
| 640×512 @ 50 Hz | 64.0 µs | 9,504 | 453 | 80 slots | 0.8% |
| 1080p60 | 14.81 µs | 2,200 | 105 | 240 slots | 11% |
| 1080p240 | 3.70 µs | 550 | 27 | 240 slots | 44% |
| 4K60 (CEA-861) | 7.41 µs | 1,100 | 53 | 480 slots | 44% |

"Tick positions" counts the truncated tail tick as one position: 104 full ticks
plus a short one at 1080p, 52 at 4K, and the same rule everywhere. 640×480 is the
floor the ports can carry and 1024×768 is the first power-on default — see the
technical specification card, §10.

The pattern is worth pausing on: at 640×512 the bus is almost idle, at 1080p it
is comfortable, and at 4K the display alone takes nearly half the line before
the blitter, the planes or the Copper have asked for anything.

### 4.3 The memory is not a slot machine

A slot is 8 bytes. **DDR3L has no 8-byte transaction.** Its smallest is a burst
of eight transfers on a 32-bit bus — **32 bytes, four slots** — and the first
word does not come back in the slot it was asked for. The earlier revision of
this document assumed a fetch occupied one slot and returned in it; no DRAM ever
built behaves that way. The budget has to be rebuilt on what the part actually
does.

| Event | Time | Slots | Consequence |
|---|---|---|---|
| Row hit, first word (CL 11) | 13.75 ns | 2.0 | two slots per burst are latency, not transfer |
| Row miss (tRP + tRCD + CL) | 41.25 ns | 6.1 | hidden by buffers, never by priority |
| Refresh, all banks (tRFC, 4 Gb) | 350 ns | **52** | the entire bus stops — blanking only |
| Write→read turnaround (tWTR) | 7.5 ns | 1.1 | batched, budgeted at 6% |
| Read→write turnaround | ~12 ns | 1.8 | batched, budgeted at 6% |

Four rules follow, and none of them is optional:

1. **32 bytes is the quantum.** Nothing smaller ever reaches the DRAM, and every
   burst is 32-byte aligned. Software still sees 8-byte slots; the controller
   coalesces. Without ECC a partial write is free — DDR3 has byte masks. With
   ECC it costs a read-modify-write unless all 32 bytes are written, which is
   why the ECC option in this section is priced rather than assumed.
2. **A tick is five bursts and one Copper slot**: 5 × 4 + 1 = 21. This is why 21
   is the right divisor rather than a convenient one. Bursts never straddle a
   tick boundary, the Copper's slot is always in the same place, and the burst
   grid cannot drift against the tick — which is exactly what broke at 7.09.
3. **Every display stream has a line buffer** deep enough to survive a refresh:
   **at least 350 ns of its own pixels.** A stream that cannot cover tRFC will
   starve every 7.8 µs, and no amount of priority fixes it.

   | Stream | 1080p (350 ns = 52 px) | 4K (350 ns = 208 px) |
   |---|---|---|
   | 1-bit plane | 52 bits = 7 B → **32 B** | 208 bits = 26 B → **32 B** |
   | ARGB8888 overlay | 208 B → **256 B** | 832 B → **1,024 B** |

   One burst ahead is enough for a bitplane; a 32-bit overlay needs twenty-six
   bursts of cover at 4K, rounded to a kilobyte — which is why the wide streams
   are the ones that cost BRAM. The number is not a guess: it is tRFC times the
   pixel rate.
4. **Direction changes are batched.** Eight consecutive bursts (256 B) in one
   direction before turning the bus around. A round trip of 16 bursts is 64
   slots; the two turnarounds cost about 19.5 ns, or 4.5% — budgeted at 6% below
   for headroom. A controller that interleaved single bursts would lose most of
   the bus to turnaround alone.

#### Refresh lives in the blanking interval

A refresh stops the whole bus for 350 ns — 52 slots — and it is needed every
7.8 µs, which is 1.90 times per 1080p line and 0.95 times per 4K line. There is
no way to hide it behind other work, so it goes where the display does not need
the bus:

| Mode | Blanking | Two refreshes | Margin |
|---|---|---|---|
| 1080p60 | 1,886 ns | 700 ns | 1,186 ns |
| 4K60 | 943 ns | 700 ns | **243 ns** |

Both fit. 4K is the tight one, and it is why **the Copper's last tick positions
each line are not guaranteed**: they fall in blanking, and blanking belongs to
refresh. In practice the Copper has **92 guaranteed positions in a 1080p line**
and **46 in a 4K line** — the active region, divided by 21. Copper work has to
finish inside the picture.

#### What ECC actually costs

The common claim is that ECC costs 25% of bandwidth. That is true only for
*inline* ECC. Sideband ECC — a 40-bit bus of five x8 devices instead of four —
carries **the same 6.4 GB/s of payload**, because the extra 8 bits per transfer
are the check bits:

| Option | Payload | Burst | Real cost |
|---|---|---|---|
| None | 6.4 GB/s | 32 B / 4 slots | baseline |
| **Sideband, 40-bit** | **6.4 GB/s** | 40 B / 5 slots | +1 DRAM device, +8 pins; four bursts per tick instead of five |
| Inline | 5.6 GB/s | 32 B / 4 slots | 12.5% of capacity and bandwidth, no extra pins |

C+ ships without ECC. Sideband ECC is the option worth having, because it buys
protection for a device and eight pins rather than for a twelfth of the machine.

#### What actually limits the bus

| Overhead | Share | Source |
|---|---|---|
| Refresh | 4.5% | 350 ns per 7.8 µs |
| Turnaround | 6.0% | 8-burst runs; arithmetic gives 4.5%, budgeted at 6% |
| Row misses | 3.0% | one page per plane, banks interleaved |
| **DRAM usable** | **86.5%** | |

Those three are **DRAM-side costs**. They reduce what the memory can supply, not
what the fabric can carry — and on every model the fabric is the narrower of the
two:

| | C+ | Studio | Pro II |
|---|---|---|---|
| Slot fabric | 1.19 GB/s | **4.75** | **9.50** |
| Less the Copper lane (1 slot in 21) | 1.13 | **4.52** | 9.05 |
| DRAM, raw | 6.40 | 12.80 | 12.80 |
| DRAM after the 13.5% above | 5.54 | 11.07 | 11.07 |
| **Binding limit** | **1.13** | **4.52** | **9.05** |
| DRAM load at full fabric | 19% | 43% | 86% |

C+ is limited by its 64-bit fabric, not by its memory: 1.13 GB/s of burst capacity
against 5.54 GB/s of usable DRAM. The Studio is limited the same way, 4.52 against
11.07. **Every bandwidth figure in §4.4 and §4.5 is a share of burst capacity —
4.52 GB/s on the Studio, not 4.75.**

That is the most useful fact in this section: the machine is not short of memory,
it is short of slot width. And slot width is internal logic, which is why the next
model does not need a new board.

### 4.4 What HDR and capture cost on the Studio models

256-bit slots give 4.75 GB/s of fabric, of which **4.52 GB/s** is available to
bursts once the Copper lane is reserved. That is what makes 10-bit HDR and 10-bit
capture possible — and it is why the second output has a shape:

| Traffic at 4K60 | Bandwidth | Share of 4.52 GB/s |
|---|---|---|
| 10-bit 4:4:4 graphics | 1.99 GB/s | 44% |
| 10-bit 4:2:2 video | 1.24 GB/s | 27% |
| 1080p60 10-bit 4:4:4 capture | 0.47 GB/s | 10% |
| **as shipped: graphics + video + capture** | **3.70 GB/s** | **82%** |
| graphics + derived 4K output + capture | 2.46 GB/s | 54% |
| graphics + independent 1080p graphics + capture | 2.96 GB/s | 66% |
| **two independent 4K graphics + capture** | **4.45 GB/s** | **98% — not viable** |

The shipped configuration leaves 18%, or 0.8 GB/s, for the blitter and the host.
Two independent 4K HDR graphics rasters leave 0.07 GB/s, which is not a blitter —
it is a queue. That is the line to draw: **the Studio and the Pro can drive two
4K HDR outputs, but only one of them can be composited graphics.** The other is
video, or a crop, a scale or a colour variant of the same frame, or graphics at
1080p.

#### The 512-bit path

Doubling the slot to 512 bits doubles the fabric to 9.5 GB/s — 9.05 for bursts —
and leaves the DRAM untouched. The memory then runs at 86% instead of 43%, which
is the balance a display engine actually wants. Two independent 4K HDR graphics
beams, plus capture, plus a 1.5 GB/s blitter and a 1.0 GB/s host, come to
6.95 GB/s: **77% of the fabric and 63% of the memory.**

The cost is not a board. The fabric is internal FPGA logic; the DRAM, its pins and
the PCB do not change. **A5K Studio Pro II is a -3 speed grade and a wider fit on
the same board** — about +$250, not a respin. It is also why the Studio ships
64-bit memory although 32 bits would have met today's budget: width is the one
thing that cannot be added later.

So 256-bit is not a luxury on the Studio line — it is the minimum that meets the
shipped specification, and 512-bit is the minimum that meets the *other* one.

### 4.5 What full-width ARGB costs

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

### 4.6 Allocation policy

A line is divided into five things, in this order of precedence:

1. **Copper lane** — **slot 0 of every tick**, one slot in twenty-one. Not a
   window and not a band: a fixed position, so a Copper fetch can never queue
   behind a burst. When the Copper has no fetch pending — it is executing a
   satisfied WAIT, or idling — the lane is lent to the blitter for that tick and
   taken back at the next one, decided at tick start. The Copper's priority is
   therefore absolute and the waste is bounded at 4.8%.
2. **Display band** — bursts into per-stream line buffers, sized as in §4.3 and
   fetched ahead of the beam. The beam reads a buffer, never the DRAM, so a
   refresh or a page miss costs latency that the buffer already covers.
3. **Service band** — refresh, audio DMA, SD. Refresh is placed in the blanking
   interval by construction (§4.3), so it costs no active-line slots.
4. **Blitter window** — a guaranteed fraction of the whole line, set per mode in
   the generator: **25% at 1080p** (550 slots) and **15% at 4K** (165 slots). The
   4K figure is lower because the display band has already taken 44%; keeping 25%
   there would leave the host 10% of the line. It is a default that software may
   change. What software may not do is take a slot from the display band.
5. **Host window** — whatever is left, in bursts of at least 8 and at most one
   line, so a 33 MB readback cannot hold the bus for 28 ms.

The blitter may borrow from the host window, and from the Copper lane when it is
idle, but **never from the display band**. That single rule is what makes "the
picture never tears because of a blit" provable rather than hopeful.

**Does the window scale with frame rate? No, and it should not.** There is only
one frame rate (60 Hz, see §8) and the line length is what changes between modes.
The window is defined as a fraction of the line, so it already scales with the
thing that actually varies. Scaling it with a refresh rate the machine does not
have would be a rule with no case behind it.

### 4.7 The descriptor

Each slot is described by a 32-bit word, held in a small table in fabric:

| Bits | Field |
|---|---|
| 7:0 | Owner ID (bitplane n, plane n, blitter, Copper, audio n, refresh, host) |
| 15:8 | Burst count, in 4-slot units (1–255); a burst is 32 bytes |
| 23:16 | Flags (borrowable, stealable, must-complete) |
| 31:24 | Reserved |

The table is **generated from registers**, not stored per mode: line length,
plane count and plane widths determine the display band, and the rest follows a
fixed pattern. Only the override window is written by software.

### 4.8 What is settled, and what is not

**Settled.** Slot width — 64 bits on C+, 256 on Studio, 512 on the Pro II. Memory
— 32-bit on C+, 64-bit on the Studio and Pro. The fabric is the binding limit on
every model, and the DRAM is deliberately wider: 19%, 43% and 86% loaded at full
fabric. Tick — 148.5 ÷ 21 everywhere. H — counted in ticks, twelve bits, never
widened. Quantum — 32 bytes, four slots, and a tick is five bursts plus the
Copper lane. Refresh — in blanking, always. Buffer depth — tRFC of the stream's
own pixels. Turnarounds — batched at 8 bursts. Blitter — 25% of the line at
1080p, 15% at 4K. Miss behaviour — hold, never stall. Arbitration between two
beams — a superframe with three tiers, in `A5K-Dual-Pipe-Arbitration.md`. Ceilings
— §8.

**Still open.**

- Whether 256 bits closes timing at 148.5 MHz on a -2 Kintex-7, or whether the
  Studio needs a -3 speed grade — and whether 512 bits closes on a -3. Both are
  synthesis questions, not design ones, and they are the only items here that
  could change a price.
- The rate of the reserved second tick domain (§7), and whether both beams share
  it.
- Whether the Pro II ships as its own model or as a speed-grade variant of the
  Pro on the same board.

**Answered, and the answers are above:** the blitter window does not scale with
frame rate (§4.6); the Copper does not get a band, it gets a lane (§4.6, §4.3);
a missed display fetch holds the last pixel and raises a flag, because a stalled
beam would break the video timing that every other guarantee rests on (§5.5).

## 5. For programmers

### 5.1 WAIT is in ticks, not pixels

An MC-1 WAIT takes a packed `(V << 12) | H`. H is a **tick** position within the
line, not a pixel: at 1080p the positions run 0–104 (0–91 inside the active
picture), at 4K 0–52 (0–45), at 640×512 0–452. Twelve bits address every mode in the family with room to spare, and the
field does not widen when the fast tick of §7 is enabled — which is the whole
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
3. **Do not port PAL or NTSC timing arithmetic.** A list that fits in 454 ticks
   (PAL) or 455 (NTSC) does not fit in 105. Re-derive the positions from the mode
   you are actually running.

### 5.4 A worked example

1080p, 8 planar bitplanes, one 256-pixel overlay, a 50,000-pixel fill during
vblank:

| Item | Bursts | Slots | Share |
|---|---|---|---|
| 8 bitplanes | 60 | 240 | 11% |
| 1 overlay, 256 px ARGB8888 | 32 | 128 | 6% |
| Blitter window | 137 | 548 | 25% |
| Host window | 269 | 1,076 | 49% |
| *burst path, subtotal* | **498** | **1,992** | 91% |
| Copper lane | — | 105 | 4.8% |
| Refresh, audio, SD | — | 100 | 4.5% |
| Spare | — | 3 | — |

498 bursts × 4 slots, plus 105 Copper slots, plus 100 for refresh and audio, plus
3 spare slots of alignment, is exactly 2,200. Every slot is owned, and the three
spare slots are the price of 32-byte alignment against a 2,200-slot line.

The picture is honest: at 1080p there is room to spare. At 4K the same list needs
480 slots for the bitplanes alone, and the blitter window has to shrink to about
15% to keep the display fed — which is exactly the kind of trade this document
exists to make visible before anyone writes RTL.

### 5.5 The 1080p line, in bursts

The schedule is not a list of 2,200 entries. It is one 21-slot unit repeated 105
times, and a short tail:

```
  tick 0              tick 1                        tick 104 (short)
  ┌─┬──────────────┐  ┌─┬──────────────┐            ┌─┬────────┐┌───┐
  │C│BB BB BB BB BB│  │C│BB BB BB BB BB│     ...    │C│BB BB BB││ 3 │
  └─┴──────────────┘  └─┴──────────────┘            └─┴────────┘└───┘
   1      20 slots      1      20 slots               1    12       3
```

That is the whole contract. Everything else is which owner fills which burst:

| Slots | Owner | Rule |
|---|---|---|
| `0` of every tick (105) | Copper | absolute priority; lent to the blitter at tick start when no fetch is pending |
| the other 20 of each tick (2,080) | bursts | display first, then refresh (blanking only), then blitter, then host |
| tail 12 (3 bursts) | bursts | same order |
| tail 3 | spare | alignment; audio or SD |

At 4K the same unit repeats **52 times** with an 8-slot tail, giving 53 Copper
slots and 249 bursts. The numbers are CEA-861 (4,400 × 2,250); CVT-RB is another
row in the same generator, 1,114 slots, and the tables do not change shape — 120 for eight planes, 32 for a 256-pixel overlay, 41 for
the blitter and 56 for the host.

**When a display fetch misses its slot, the beam holds and repeats the last
pixel.** It never stalls. A stalled beam changes the line time, and the line time
is the one thing every other guarantee is built on: the Copper's WAIT positions,
the monitor's sync, the buffer depths, the whole contract. A repeated pixel is a
local, bounded, visible error; a stalled line is a broken frame and a lost lock.

Three consecutive misses on one stream increment a fault counter and raise an
interrupt. One miss is a scheduling event; three is a bug, and the driver should
be told.

## 6. Tests a simulator must pass

Five, each stated so it can be automated. Until these pass, the schedule is a
claim rather than a specification.

1. **Tick ratio.** Run 1,000 lines at 1080p. Assert exactly 105 tick positions per
   line, that H never exceeds 104, and that the tick count at line 1,000 is
   exactly 105,000 — no drift, ever.
2. **Refresh never starves the beam.** Force refresh to start at the worst phase,
   the first slot of blanking, at 4K. Run 10,000 frames. Assert zero FIFO
   underruns on every display stream and a measured refresh duty of 4.5 ± 0.1%.
3. **Copper determinism under load.** Saturate the blitter and the host window.
   Assert that a WAIT at *(line 500, tick 40)* retires at the same slot index on
   all 1,000 frames, and that no instruction fetch waits more than one tick.
4. **Miss behaviour.** Inject five lines of induced misses on one plane. Assert
   the line time varies by less than 0.01%, the last pixel repeats rather than
   the beam stalling, the miss counter increments, and the fault interrupt fires
   on the third consecutive miss.
5. **Budget conformance.** Load the §5.4 example and measure slots per owner per
   line. Assert every figure is within 1% of the table, and that no transaction
   smaller than 32 bytes, or crossing a 32-byte boundary, ever reaches the DRAM.

## 7. The second tick domain, reserved

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
beam has its own, which follows the arbitration question in §4.8; whether a fast
domain adds a sub-tick H counter for finer WAIT granularity. None of those
constrains C+, and all of them are cheaper to decide with a simulator than with a
board.

## 8. Ceilings

Better stated than discovered:

| Bound | Value | Why |
|---|---|---|
| Frame rate | **a fixed set**, 24–240 Hz | each rate is its own table; a variable one would invalidate every WAIT position in it |
| Resolution | **4K** (3,840 × 2,160) | V is 12 bits, 4,095 lines; 8K needs 4,320 and does not fit |
| Frame rate at 4K | **60 Hz** | 1,100 slots per line, 480 taken by eight planes; 4K120 halves the line to 550 slots and the display alone would be 87% |
| Planes at 4K | planar, plus partial overlays | a full-width ARGB plane is 175% of a line (§4.5) |
| Copper | one instruction per tick | 4.8% of the bus at 7.0714 MHz; a faster domain is a bandwidth trade (§7) |
| Independent 4K HDR beams | **1** at 256-bit, **2** at 512-bit | two independent 4K HDR graphics rasters plus capture is 98% of a 256-bit fabric (§4.4) |

C+ is a 4K, fixed-timing machine: 24 to 240 Hz depending on resolution, 60 at
4K, and never a variable one. That is a constraint, not a shortcoming, and every
one of these ceilings is the price of the property the machine exists for: the
schedule is countable because it never has to be renegotiated.

## 9. This is where the real test is

> **Nothing here has been built or measured.** The arithmetic is internally
> consistent; that is not the same as correct. Every assumption this document
> stands on is listed, with severity and consequence, in `A5K-Frailties.md`.
> The five that would change *this* document most:

| # | Assumption | If it fails |
|---|---|---|
| A1 | dual-pipe arbitration is a written rule | it is, in `A5K-Dual-Pipe-Arbitration.md` — but it has not been simulated |
| B1 | 4K uses CEA-861 timing | CVT-RB leaves 300 ns of blanking; ~7 slots of refresh spill into the line, 0.6%, and the per-line numbers move 1.3% |
| B2 | tRFC is 350 ns | it is probably 260 ns for the 4 Gb parts; the budget improves |
| B3 | 256-bit closes at 148.5 MHz on a -2 | -3 speed grade, +20–25% on the FPGA |
| B5 | buffers sized to tRFC are enough | a permanent pixel-hold every 7.8 µs |

A specification that cannot name its own weak points is a brochure. This one can,
and §6 is the list of tests that would settle them.

---

*Proposal, 2 November 2026. Every number here is arithmetic, not measurement —
corrections welcome, particularly on the 4K allocation, which is the tightest
case.*

**What would make it a measurement:** the latency figures are JEDEC typicals for
DDR3L-1600 at CL 11; the overheads are budgets; and no line buffer has been sized
against a real controller's arbitration. §6 is the list of tests that would turn
this from a proposal into a specification, and building the simulator against them
is the next step.

---

*Rev. AI · 3 November 2026 · project started 30 October 2026*
