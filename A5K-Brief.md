# A5K — a plain-language brief

**For engineers outside the Amiga world.** This is the one-page answer to the
questions raised by the r/FPGA thread: what A5K is, what the schedule means, what
the Copper is, what the numbers are, and what review is actually wanted.

## What it is

A5K is a **PCIe card that generates video and audio from a deterministic,
line-by-line schedule**. A host CPU sets up the schedule; the card executes it
against the video beam. It is not a computer, not a GPU, not an Amiga clone, and
it makes no Amiga compatibility claim.

No hardware has been built. The repository is a design study: documents,
arithmetic, and a simulator specification.

## Who it is for, and how it attaches

The card is a **PCIe endpoint** — for an x86-64 host today, RISC-V or ARM later,
or a system-on-module with PCIe. The host writes registers through BAR0, can map
a Chip RAM aperture through BAR2, and can DMA. The card does not need a host CPU
on board; a small supervisory core is optional.

It is **not** a standalone computer and **not** a console.

## What a "fixed slot schedule" means

It is **not** "assign every bus cycle, every frame, in software." That would be
absurd, and the critique is right about that.

The schedule is a **repeating per-line rota**. The bus is divided into slots of
6.734 ns. Each slot has one owner: display fetch, blitter, host, Copper, audio.
At 1080p a line has about 2,200 slots. The same rota repeats every line. The host
writes the line schedule **once per mode**, and the hardware cycles it.

At 60 Hz a frame is about 2.5 million bus cycles, but the schedule is not 2.5
million assignments. It is a line schedule repeated 1,125 times. Only a mode
change, or a new Copper list, rewrites it.

## What the Copper is

The Amiga Copper is a **coprocessor that executes a list of instructions
synchronised to the video beam**. The instructions are MOVE, WAIT, SKIP, JUMP,
CALL, RET, END and IRQ. It writes chipset registers — not framebuffer pixels
directly.

A5K's Copper is the same idea at a **7.0714 MHz tick** (148.5 ÷ 21). It fetches
and retires one instruction per tick, can WAIT on a `(line, tick)` position, and
owns slot 0 of every tick so its fetch cannot queue behind a burst.

"Copper-style" is not a new term; it is the Amiga coprocessor. A non-Amiga reader
can think of it as a **beam-synchronised register sequencer**, distinct from a
GPU command processor because its retirement time is fixed by the slot table, not
by a scheduler.

## What "deterministic" means

The word is doing specific work here, and it is easy to answer the wrong question.

**It does not mean:**

- that a host command finishes in a fixed number of cycles — PCIe latency is variable, and the host is **not in the timing path**;
- that every pixel changes on the same cycle as the register write — the pixel pipeline has a fixed, nonzero delay;
- that the whole machine is hard real-time — the host OS, the driver and the application are not;
- that memory access is fixed-latency — DDR3L has refresh, row misses and turnaround.

**It does mean:**

1. **Slot ownership is fixed per line.** Each line is a repeating rota of slots, one owner per slot. The host writes the rota once per mode; the hardware cycles it.
2. **Copper retirement is exact.** A `WAIT (line, tick)` followed by a `MOVE` retires at that slot. Under saturated blitter and host traffic, the slot index does not move. Test T3 asserts this over 1,000 frames.
3. **The line time is fixed.** The beam never stalls. If a display fetch misses, the last pixel repeats; line time varies by less than 0.01% under induced misses (test T4). Three consecutive misses raise a fault.
4. **The pixel pipeline delay is fixed.** A register change at line *N* appears at a known line offset, set by the line-buffer depth. That is a design constant; no measured number is claimed yet.
5. **The host is decoupled.** The host writes Copper lists and registers ahead of time. List swaps apply at frame boundaries. A host round-trip is never asked to meet a scanline deadline.

The guarantee is therefore **asymmetric**:

| Path | Guarantee |
|---|---|
| Copper register write | exact slot, every frame |
| Video line timing | fixed; never stalls; hold on miss |
| Display fetch | slot-scheduled; DDR latency absorbed by the line buffer; bounded, not zero |
| Audio DMA / sample clock | the card's audio clock (or an external master) is the reference; fixed DMA schedule; the host fills buffers ahead of time |
| Host → card register write | scheduled in the host window; PCIe latency variable; not scanline-exact |
| Host ↔ card readback | best-effort within the host window |
| Host OS / application | not deterministic |

A concrete example: a palette write scheduled at line 214 retires at line 214’s tick 40, every frame. The pixels using the new palette appear after the fixed pipeline delay. A host write over PCIe that arrives “sometime around line 214” is not the same guarantee, and the design does not claim it is.

**How it is measured.** Phase 0 simulator trace first — T1 (tick ratio), T3 (Copper determinism under load), T4 (miss behaviour) — then the RTL testbench, then a logic analyser on the board comparing the Copper write strobe to the video timing. No hardware exists, so nothing is measured; the claim is a specification with tests that can fail.

**What would falsify it.** A WAIT whose slot index moves under load; a line time that varies beyond the budget; a display fetch that stalls the beam; a register write that misses its slot when the blitter and host window are saturated. Any of those is a defect, not a nuance.

## Reads and writes

The schedule includes **both**:

- display fetch (reads from memory into line buffers),
- blitter reads and writes,
- host reads and writes,
- Copper instruction fetch,
- audio fetch.

The original post emphasised register **writes** because the Copper's
deterministic part is a register write at a known scanline. It did not mean the
design ignores reads. The line buffers are written by DMA and read by scanout;
the host can read Chip RAM. Every one of those is a slot owner.

## The numbers

- **256-bit slot path at 148.5 MHz** = 256 ÷ 8 × 148.5 MHz = **4.752 GB/s**.
  That is the Studio fabric.
- **64-bit DDR3L at 1600 MT/s** = 8 bytes × 1.6 GT/s = **12.8 GB/s** raw.
  Studio uses 64-bit; the C+ uses 32-bit, or 6.4 GB/s.
- The **fabric is the limit** because 4.75 GB/s is less than 12.8 GB/s. After
  refresh, turnaround and the Copper lane, about **4.52 GB/s** reaches bursts.
- The percentages in the documents are **budget arithmetic**, not measured
  utilisation. No synthesis has been run, so no utilisation or timing number is
  claimed.
- The first fit check targets a **Kintex-7 325T -2**. The question is whether the
  256-bit path closes with the MIG attached, and if not, which element is the
  limiter: the MIG's 256-bit user interface, the arbiter's fan-out, the FIFO
  read/write ports, or routing congestion.

## What is and is not claimed

**Claimed:** the documents, the arithmetic, the slot contract, and the simulator
plan.

**Not claimed:** hardware, measured bandwidth, timing closure, utilisation,
Amiga compatibility, or games.

The "frailty register" is a **self-critique list** — the assumptions most likely
to be wrong. It is not a list of known bugs being outsourced, and it is not a
substitute for reading the datasheets and user guides. It exists so a reviewer
can aim a correction instead of writing a general critique.

## Ethos: kept and broken

A5K keeps the Amiga’s **engineering ethos** and breaks most of its **platform
ethos**. That is deliberate, and it is worth stating plainly before a reviewer
assumes the project is claiming more than it is.

| Engineering ethos | Kept? | Platform ethos | Kept? |
|---|---|---|---|
| Chipset-first co-design | **Yes** | Backward compatibility | **No** |
| Deterministic beam timing | **Yes, strengthened** | Software library | **No** (AROS is the path) |
| Fixed-function parallelism | **Yes** | Affordable whole computer | **No** |
| Separable compute | **Yes** | Whole-system co-design | **No** |
| More-with-less | **Yes** | Consumer scale | **No** |
| Legibility / open docs | **Yes** | Proprietary model | **No** (open instead) |

The deepest inversion: the Amiga used custom chips to make a **whole computer**
affordable — the A500 was the mass-market expression. A5K uses the custom-chip
**method** to make a **component** deterministic. The method has become the end.

The full audit, including the AAA/Hombre comparison and the three routes to close
the gap, is in `A5K-Ethos-Audit.md`.

## What review is wanted

One of these:

1. A specific answer: **does 256-bit at 148.5 MHz close on a Kintex-7 325T -2
   with the MIG attached?** If not, what is the limiter?
2. A correction to a number or assumption, with a datasheet, user guide, or
   standard citation.
3. A note that the schedule is unsound, with the specific slot or line where it
   breaks.

Not wanted: "build it for me", "validate the whole project", or a general
argument about AI. The repository is the record; the question is deliberately
narrow.

## Glossary

| Term | Meaning |
|---|---|
| **Slot** | 6.734 ns bus unit; one owner per slot |
| **Tick** | 21 slots; the Copper's instruction interval |
| **Line** | One video scanline; contains many slots |
| **Frame** | One complete picture; contains many lines |
| **Copper** | Beam-synchronised register sequencer |
| **Deterministic** | A named unit retires at a named slot or line, every frame — not a bounded average and not host-command latency |
| **MIG** | Xilinx Memory Interface Generator (DDR controller) |
| **Line buffer** | On-chip FIFO holding a line of pixels to absorb DDR latency |
| **Fabric** | The FPGA's programmable logic and routing |
