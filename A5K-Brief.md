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

## What "promise" means

Deterministic retirement. If the list says *WAIT until line 214, tick 40, then
MOVE*, the write retires at that beam position within the fixed schedule. There is
no queue, no best-effort GPU scheduler, no "usually around vblank."

The guarantee is only for the **slot and line contract**. Memory latency is
absorbed by line buffers; it is not allowed to move the register write.

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
| **MIG** | Xilinx Memory Interface Generator (DDR controller) |
| **Line buffer** | On-chip FIFO holding a line of pixels to absorb DDR latency |
| **Fabric** | The FPGA's programmable logic and routing |
