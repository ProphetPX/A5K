# Lineage

**What the last Amiga team was building, and what this design inherited.**

This is not a history chapter for its own sake. It exists because the most common
objection to this project is *"that is just another Vampire"* — and the answer is
in the primary documents. Several things the A5K arrived at independently were
already being built by Commodore in 1993. That is convergence, not imitation, and
it is worth being able to show.

## Sources

| Source | What it is |
|---|---|
| *An Overview of the Advanced Amiga Architecture and Other Future Directions*, Rev 1.0, 1993 Developer's Conference, **Dave Haynie** | **Primary.** The last Amiga team describing AAA in its own words |
| Bambi Amiga History, *Lorraine* (2001), [bambi-amiga.co.uk](http://bambi-amiga.co.uk/amigahistory/prototypes/lorraine.html) | Secondary: the 1984 prototype, CES demonstration, breadboards |
| Wikipedia, *Advanced Amiga Architecture chipset*; Bambi Amiga history; Big Book of Amiga Hardware (*Nyx*) | Secondary: dates, configurations, the stop-gap machine |
| Wikipedia, *Amiga Hombre chipset* | Secondary, and thin |

The AAA document is Commodore-confidential material that is publicly mirrored. It
is cited here, not reproduced.

## Lorraine, 1984

The origin point is earlier than AAA. **Lorraine** was the 1984 Hi-Toro/Amiga
Corp. breadboard prototype that became the Amiga 1000. It was not a recent Amiga
model and it is not an A5K predecessor in the product sense.

- **1984 — Lorraine** — Hi-Toro/Amiga Corp. breadboard prototype
- **1985 — Amiga** — launched as the “Amiga”; later renamed **Amiga 1000** after
  the A500 arrived
- **1987 — Amiga 500 / 2000**
- **1990 — Amiga 3000**
- **1992 — Amiga 1200 / 4000**
- **1993 — CD32**
- later: Amiga Technologies, AmigaOne/PowerPC, and the modern Amiga ecosystem

The prototype was **four breadboards cabled together**, not a PCB: 128K RAM
(expandable to 512K internally), 64K ROM, Apple-compatible BASIC, a keyboard
interface, a 5.25-inch disk drive, a **cartridge port intended for a CPU upgrade
or PC emulator**, and a built-in 300-bps modem. It was demonstrated at the January
1984 CES in a “secret enclosure” that was not actually secret. Commodore’s
purchase removed the modem and cartridge port, raised memory to 256K, standardized
a 3.5-inch drive, discarded CAOS in favour of TripOS/Intuition, and finalized the
logic into OCS.

The often-repeated line that the motherboard “became Zorro” is loose: **Zorro is
the expansion bus**, not the machine. The prototype was Lorraine; the product
became the Amiga/A1000.

**What A5K inherits.** The method, not the hardware: chipset-first design, a
separable compute path, and the discipline of prototyping early. Lorraine’s
cartridge port was an early “swap the CPU, keep the chipset” idea; A5K expresses
the same instinct through PCIe.

**What A5K does not inherit.** The cartridge port, the 68k, the 5.25-inch drive,
the modem, or any Amiga compatibility claim. **Lorraine was the A1000’s
predecessor, not a modern model; A5K is not a continuation of the Amiga product
line.** It is a modern design study that borrows the chipset method — fixed slots,
Copper-style beam control, separable compute — not the Lorraine or A1000 hardware.

**The breadboard lesson.** Four cabled breadboards beat a beautiful PCB that never
exists. A5K is still at the paper stage; the next honest step is the simulator, then
a single-block prototype, not a finished board.

## AAA, 1993

Four new VLSI chips, not three:

| Chip | Role | Replaced |
|---|---|---|
| **Andrea** | chip bus controller, chip RAM, DMA | Agnus / Alice |
| **Monica** | display controller | Denise / Lisa |
| **Mary** | I/O | Paula |
| **Linda** | double-buffers **full display lines** | — new |

- **Bus:** 32-bit, a four-cycle burst to Chip RAM, extended bursts of up to
  **512 words** for high-resolution displays. Fast-Page DRAM **or VRAM**, mixable
  per bank; VRAM's serial port frees the parallel bus from display fetches.
- **Priority:** a fixed list — graphics overlay, DRAM refresh, interrupt transfer,
  disk, high-priority external, audio, display, sprite, coprocessor, processor,
  blitter. When demand exceeds supply, **the graphics fetch is what starves**, and
  it raises an overrun interrupt telling software to quieten down.
- **Display:** up to **16 bitplanes**, 256 CLUT entries of 25 bits, sprites 128 px
  wide; bitplane, half-chunky (2/4/8-bit), chunky (8/16-bit) and hybrid pixels;
  HAM8 and HAM10. **The pixel clock is no longer tied to the bus clock**, so
  standard resolutions can be generated and screen promotion works by scaled
  clocks.
- **Blitter:** pixel addressing instead of masks and modulos; bitplanes or chunky;
  clip-rect mode; arithmetic operations for sort and tally.
- **Copper:** 32-bit operations, **move-multiple** for blocks of consecutive
  registers, and an interrupt input so it can chain blits without the CPU.
- **Audio:** eight channels, 16-bit, better than 50 kHz, on-chip DACs.

## Hombre

A later, separate direction: **64-bit, PA-RISC-based 3D**, described in some
sources as a 3D accelerator on a PCI card, cancelled with Commodore in 1994. Far
less is documented than AAA and much of what circulates is recollection. Treat it
as a direction, not a specification.

## What we derived independently, and AAA already had

| A5K | AAA, 1993 |
|---|---|
| Line buffers per stream | **Linda**, double-buffering full display lines |
| 32-byte bursts into buffers | four-cycle bursts, up to 512 words |
| Fixed priority for every slot | a fixed priority list |
| Width in the Copper instruction | **move-multiple** |
| Pixel clock independent of the bus | stated explicitly |
| 16 bitplanes as a ceiling | 16 bitplanes |

The same problem produces the same answers. Line buffers and burst scheduling are
not modern ideas bolted onto an Amiga; they are where the last team was heading
when the company died.

## What we do not copy — and what is deferred

- **VRAM.** Its serial port solved display fetch in 1993. DDR3L plus line buffers
  solves it now, and VRAM is long dead.
- **The 512-word burst.** Excellent for display latency, terrible for everything
  else's. Our eight-burst cap is the modern trade.
- **Starving graphics on overload.** AAA raised an interrupt and let the picture
  break; the A5K holds the last pixel and never stalls the beam.
- **Hombre's 3D — deferred, not rejected.** It is not in this revision, but every
  model leaves room for a 3D block as later work. The ethos is kept; the pipeline
  comes when the schedule and the parts allow it.

## The two camps that exist today

Both sell the **software library**. Neither sells a timing contract.

| | **Apollo A6000** (Vampire V4) | **AmigaKit A4000NG** |
|---|---|---|
| Technology | FPGA, AC68080 softcore | ARM single-board computer |
| Compatibility | native 68k | emulation (AmiBench, UAE-derived) |
| Display | HDMI to 1080p | commodity SoC |
| Status | shipping | prototype, specs TBA |

**What each camp actually advances.** An emulation appliance advances
*packaging and setup*: a modern ARM SoC running a UAE-derived environment, sold as
a finished machine. An FPGA compatibility machine advances *silicon*, but every
decision is bounded by the need to run existing software at existing timings.
Neither targets 4K60 HDR, a 96 kHz audio path, or a published slot schedule — not
because it would be impossible, but because their buyers are asking a different
question.

**This card is neither.** It has no host CPU and no Kickstart; a 68k core is
**reserved but not built**, and no binary compatibility is claimed or shipped. What
it shares with them is the silicon class — an FPGA, DDR and an HDMI output — and
nothing else.

## What the lineage claim actually is

Not *"the next Amiga"*. **The AAA direction, continued without the compatibility
burden**: a fixed schedule, line buffers, bursts, a sequencer that owns the beam —
at 4K60 with HDR, on a PCIe card, for people who need a pixel at a known time.

---

*Rev. AW (B49) · 4 November 2026 · project started 30 October 2026*
