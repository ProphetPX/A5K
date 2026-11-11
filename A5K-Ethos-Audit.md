# A5K — Ethos Audit

**What this is.** A candid comparison between the Amiga’s engineering ethos, its
platform ethos, and what A5K keeps, changes, or breaks. It is not a claim of
purity. It is the map that lets the project say what it is without pretending to
be more than it is.

**Status:** documentation, 11 November 2026, Rev. AW (B49). No design claim
changes. Nothing here is measured; no hardware exists.

---

## 1. The question

> Is A5K still entirely within the original and latest “true Amiga ethos” in
> every way?

**No.** A5K keeps the **engineering ethos** and deliberately breaks most of the
**platform ethos**. That is the honest answer, and the rest of this document is
the evidence.

The project’s own sentence already says it:

> “It is not a 1990s Amiga and not a clone, but it **is** a deliberate attempt to
> define what future Amiga-like hardware should be able to be and do — the
> method, not the product.” — `README.md`

This audit turns that sentence into a table.

---

## 2. The two value systems

The Amiga had **two value systems**, and they are easy to conflate.

### The engineering ethos

How the machine was built:

- **Chipset-first co-design** — custom chips for video, audio and DMA, not a
  general-purpose CPU doing everything.
- **Deterministic beam timing** — the Copper and the DMA slots tie events to the
  video beam, so software can reason about *when* something happens.
- **Fixed-function parallelism** — Agnus, Denise, Paula, the blitter and the
  Copper work alongside the CPU.
- **Separable compute** — the CPU is one part of the system, not the whole
  system; Lorraine’s cartridge port and the A2000 CPU slot are the early
  expressions of the idea.
- **More with less** — line buffers, the blitter, bandwidth discipline and
  clever scheduling instead of brute force.
- **Legibility** — documented hardware, expandable machines, a community that
  could learn and push the design.

### The platform ethos

What the machine was *for*:

- **Backward compatibility** — A500 software ran on later Amigas; AGA ran
  OCS/ECS software; the 68k and Kickstart were the contract.
- **A software library** — AmigaOS, applications, games, tools.
- **An affordable whole computer** — the A500 was the mass-market model; the
  A1000 was not.
- **A community and a consumer culture** — demoscene, user groups, magazines,
  shops.
- **A business** — Commodore’s proprietary, closed model, for better and worse.

A5K is faithful to the first list. It breaks most of the second. That is not a
betrayal; it is the project’s actual shape.

---

## 3. The audit

| Ethos strand | What the Amiga did | What A5K does | Verdict | Reversible? |
|---|---|---|---|---|
| **Chipset-first co-design** | Agnus / Denise / Paula; AAA’s Andrea / Monica / Mary / Linda | FPGA chipset logic: slot scheduler, Copper, planar scanout, blitter, audio | **Kept** | n/a |
| **Deterministic beam timing** | Copper + DMA slots, with priority arbitration | Static per-line rota; exact Copper retirement | **Kept, strengthened** | n/a |
| **Fixed-function parallelism** | Display, blitter, Copper, audio, CPU share the chip bus | Display, blitter, Copper, audio, host share the scheduled fabric | **Kept** | n/a |
| **Separable compute** | Lorraine cartridge port; A2000 CPU slot | PCIe host; CPU-agnostic; the chipset outlives the CPU | **Kept, extended** | n/a |
| **Video/audio first-class** | Genlock, Video Toaster, Scala, deterministic audio | The whole card is built around deterministic display and audio | **Kept** | n/a |
| **More with less** | Line buffers, blitter, bandwidth discipline | 32-byte bursts, line buffers, §4.3 budget | **Kept** | n/a |
| **Legible and hackable** | Hardware reference manuals; demoscene reverse engineering | Open documents, frailty register, simulator spec, published contract | **Kept** (community strand) | n/a |
| **Backward compatibility** | OCS/ECS/AGA, 68k, Kickstart | No 68k, no Kickstart, no Amiga software | **Broken** | Only as a separate multi-year compatibility project |
| **Platform and software library** | AmigaOS and a large application/game library | AROS is the intended open path; no existing library | **Broken / partial** | Partially, with AROS plus an ecosystem; years |
| **Affordable mass-market whole computer** | A500-class machine for ordinary people | Niche PCIe card; a few dozen units per batch | **Broken** | Not with this BOM and FPGA class; a different product |
| **Whole-system co-design** | Chipset + CPU + OS + case + price | Component card; host supplies CPU, OS, case and PSU | **Broken** | Possible as a reference system; a larger project |
| **Custom silicon** | Custom ASICs / chips | Commodity FPGA | **Changed** | Not an ASIC; FPGA is the feasible medium |
| **Games and consumer culture** | Huge games library and mass-market culture | Explicitly excluded | **Narrowed** | Deliberate |
| **Proprietary / closed business** | Commodore’s closed model | Open hardware and documents | **Changed — an improvement, but not Commodore’s ethos** | n/a |
| **“Ahead of its time” mass wow** | A visible gap over 1985 home computers | A niche deterministic instrument | **Narrowed** | Not a product claim; a different kind of wow |

---

## 4. The deepest inversion

The Amiga used custom chips to make a **whole computer** affordable to ordinary
people — the A500 was the mass-market expression. The custom silicon was a means
to that end.

A5K uses the custom-chip **method** to make a **component** deterministic, for a
niche. The method has become the end.

That is the inversion. It is coherent, and the documents say it plainly — “the
method, not the product” — but it is not the original whole-system ethos.

The original ethos asked:

> What whole machine can we build that ordinary people can buy, that changes what
> a home computer is?

A5K asks:

> What timing contract can a card publish that a GPU cannot?

Both are legitimate questions. They are not the same question.

---

## 5. The AAA / Hombre test

The “latest true Amiga” matters here, and it cuts against the stronger claim.

- **AAA (1993)** was explicitly designed to be **largely register-compatible
  with ECS**. The last Amiga team kept the software library and the platform.
  AAA was a full chipset for a computer, not a card.
- **Hombre (1994)** moved toward **PCI and 3D**, but the documented direction is
  still a system chipset, and the primary documentation is thin. Treat it as a
  direction, not a specification.
- **A5K** is closer to **Hombre in form** (a PCI card) and **AAA in method**
  (line buffers, wider buses, independent pixel clock), but it breaks the
  compatibility that both would have preserved.

That is the precise historical gap: **A5K keeps the method of AAA and the form
factor of Hombre, and drops the compatibility of both.**

---

## 6. What is kept, in engineering terms

A5K’s claim is not “we rebuilt the Amiga.” It is “we kept the part that can be
specified and tested.”

| Kept idea | Where it lives in A5K |
|---|---|
| Slot-based bus ownership | `A5K-Slot-Table.md` — 148.5 MHz slot clock, 6.734 ns slots, 21 slots per tick |
| Beam-locked sequencer | Copper at 7.0714 MHz; `WAIT (line, tick)`; slot 0 of every tick |
| Planar display | Denise-class scanout from line buffers, not a linear framebuffer |
| Blitter | Minterm ALU and line draw, scheduled in a fixed window |
| Deterministic audio | Card audio clock / external master; fixed DMA schedule; host buffers ahead |
| Separable compute | PCIe host; CPU-agnostic; no application CPU on the card |
| More-with-less | 32-byte bursts, line buffers, refresh/turnaround budget |
| Legibility | Open documents, frailty register, simulator specification |

The guarantee is asymmetric, and that is deliberate:

- **Copper register write:** exact slot, every frame.
- **Video line timing:** fixed; the beam never stalls; a missed fetch holds the
  last pixel.
- **Display fetch:** slot-scheduled; DDR latency absorbed by line buffers;
  bounded, not zero.
- **Host → card write:** variable PCIe latency; **not** scanline-exact.
- **Host OS / application:** not deterministic.

See `A5K-Brief.md` → “What ‘deterministic’ means” for the long form.

---

## 7. What is broken, and why

### 7.1 Backward compatibility

**Broken.** No 68k, no Kickstart, no Amiga software. AROS is the intended open
OS path. A 68k legacy core is reserved as later work and is not built.

**Why:** compatibility is a platform-scale, multi-year obligation. It would
swamp the card’s actual claim, and it would invite the “another Vampire”
comparison. The project chose the timing contract instead.

**Reversible?** Only as a separate project. The AROS/68k plan records three
paths: native AROS on the host, host-emulated 68k, and an on-card 68k core.

### 7.2 Platform and software library

**Broken / partial.** There is no existing Amiga application library. AROS is a
plan, not a shipped ecosystem.

**Why:** the card is a component, not a computer. The host OS and application
stack are outside its scope.

**Reversible?** Partially, with AROS plus drivers plus time. It is not a
documentation task.

### 7.3 Affordable mass-market whole computer

**Broken.** A5K is a niche card. The plausible first scale is a few dozen units
per batch through PCBWay-class fabrication.

**Why:** the FPGA, DDR3L, converters and connectors put it in a different price
class from a consumer appliance. The project has no company, no funding and no
factory.

**Reversible?** Not with this design. A mass-market product would be a different
board, a different BOM and a different business.

### 7.4 Whole-system co-design

**Broken.** A5K is a card. The host supplies CPU, memory, OS, case and PSU.

**Why:** the card is the deliberate packaging choice. It keeps power and heat in
the host, avoids a custom case and PSU, and lets the same board live in a desktop
slot or a Thunderbolt enclosure.

**Reversible?** Yes — as a reference system that uses the card. That is a larger
project, not a revision.

### 7.5 Custom silicon → FPGA

**Changed.** The Amiga used custom chips; A5K uses a commodity FPGA.

**Why:** an ASIC is out of reach for an unfunded one-person project. The FPGA is
the feasible medium. “Custom logic” is not “custom silicon.”

**Reversible?** Not needed. The method is the logic and the schedule, not the
mask set.

### 7.6 Games and consumer culture

**Narrowed.** A5K is not a games machine. A host may drive it, and a game could
appear on a host, but that is not the target.

**Why:** the target is deterministic display/audio work, not nostalgia or a
mass-market game platform.

**Reversible?** Deliberate, not a defect.

### 7.7 Proprietary → open

**Changed — an improvement, but not Commodore’s ethos.** The Amiga was a closed,
proprietary product. A5K is open hardware and open documents.

**Why:** the project’s purpose is to be forkable, testable and buildable by
anyone. That is a new value, not the original one.

### 7.8 “Ahead of its time” mass wow

**Narrowed.** The 1985 Amiga created a visible gap over home computers. A5K is a
niche instrument, not a mass-cultural shock.

**Why:** the baseline is too strong, and the gap is too small. A niche “wow” is
still possible for the engineer or artist who needs deterministic timing.

---

## 8. The three routes to close the gap

If the goal is to be closer to the whole Amiga ethos, there are only three real
routes. None is current.

| Route | What it would require | Why it is not this project |
|---|---|---|
| **Whole-system** | A reference host + card + AROS machine, with a case, PSU and support | A different, larger project; the card is the component |
| **Compatibility** | 68k/AROS emulation or an on-card legacy core, plus the software library | Multi-year; reserved, not built |
| **Affordability** | A lower-cost board, a smaller FPGA, a mass-market BOM and a business | Not supported by the current BOM or the project’s resources |

A5K is coherent without them. It is the **method** without the **platform**.

---

## 9. For the general reader (age 15)

### The big idea

Imagine a school art room. One student mixes paint. One draws the lines. One
runs the music. One keeps the clock. They all share one big table.

If everyone grabs the table at once, nothing gets done. The Amiga’s trick was to
give every job a **turn**, in a fixed order, so the picture and the sound always
arrived on time.

That is the “ethos”: not a pile of fast parts, but a **team with a schedule**.

### What A5K is

A5K is a design for a card that plugs into a PC. It does the same trick as the
Amiga: it gives the picture and sound jobs a fixed schedule, so the computer knows
exactly when things will happen — not just “soon.”

It is **not** an Amiga. It does **not** run old Amiga games. It is **not** a
graphics card for gamers. It is a design study: no hardware has been built yet.

### What it keeps from the Amiga

- **Special jobs for pictures and sound**, instead of making one chip do
  everything.
- **A schedule you can count**, so a change can happen on an exact line of the
  picture.
- **A brain you can swap** — the PC supplies the CPU; the card keeps the
  chipset.
- **Open plans**, so other people can read, test and build it.

### What it leaves behind

- **Old Amiga software.** No 68k, no Kickstart, no compatibility.
- **Being a whole computer.** It is a card, not a case with a keyboard.
- **Being cheap and everywhere.** It is a niche design, not a mass-market
  product.
- **Custom silicon.** It uses an FPGA, not a factory-made ASIC.
- **Nostalgia.** It is not a museum piece or a retro console.

### Why it is interesting

Most fast computers are fast **on average**. A5K is trying to be **on time**.

If you need a colour to change on line 214 of the picture, every single frame,
a normal graphics card cannot promise that. It can say “probably very soon.” A5K
is trying to say “exactly here.”

### The honest one-liner

> A5K is an open design study for a PCIe card that draws pictures and plays sound
> on a schedule you can predict — inspired by the Amiga’s custom chips, but not
> an Amiga and not a clone.

---

## 10. For the electronics engineer

### Architecture in one paragraph

A5K is a PCIe endpoint. The host supplies the application CPU, OS and storage.
The card supplies a deterministic display/audio pipeline: a 148.5 MHz slot clock,
6.734 ns slots, a 32-byte burst quantum (four 64-bit slots on C+, one 256-bit slot
on Studio/Pro), a 7.0714 MHz Copper tick (21 slots), planar scanout from line
buffers, a minterm blitter, and audio DMA. The display is fetched from the card’s
own DDR3L; PCIe carries Copper lists, register writes and occasional readback, not
scanout.

### Timing contract

| Item | Value / property |
|---|---|
| Slot clock | 148.5 MHz; 6.734 ns per slot |
| Tick | 7.0714 MHz = 148.5 ÷ 21; 21 slots |
| 1080p line | 105 ticks ≈ 2,205 slots |
| Copper | one instruction per tick; owns slot 0; `WAIT (line, tick)` |
| Copper guarantee | exact slot retirement; T3 repeats over 1,000 frames |
| Line timing | fixed; the beam never stalls |
| Miss behaviour | hold the last pixel; <0.01% line-time variation; fault on the third consecutive miss |
| Display fetch | slot-scheduled; DDR3L latency absorbed by line buffers |
| Host path | variable PCIe latency; not scanline-exact |

### Bandwidth

| Model | Slot width | Fabric | DDR3L |
|---|---:|---:|---:|
| C+ | 64-bit | 1.19 GB/s | 6.4 GB/s (32-bit) |
| Studio | 256-bit | 4.75 GB/s | 12.8 GB/s (64-bit) |
| Studio Pro | 256-bit | 4.75 GB/s | 12.8 GB/s (64-bit) |

The fabric is the limit, not the DRAM. After refresh, turnaround and the Copper
lane, about 4.52 GB/s reaches bursts on the 256-bit models.

### FPGA and open items

| Item | Status |
|---|---|
| C+ FPGA | Artix-7 100T (4 GTP) |
| Studio / Pro | Kintex-7 160T / 325T; 256-bit closure at 148.5 MHz is **B3**, open |
| F-09 | Specification card’s Gen3/Gen4 wording is wrong: GTH/GTY, not a bigger 7-series part. Batch into Rev. AX |
| F-02 | tRFC 260 vs 350 ns, open |
| Hardware | none; no RTL, no board, no measurement |
| Test path | Phase 0 simulator → RTL testbench → logic analyser on hardware |

### What “deterministic” means here

Not host-command latency, and not a window. A Copper instruction tied to a beam
position retires at that slot, every frame. The pixel pipeline has a fixed delay
set by the line-buffer depth. DDR latency is absorbed by the line buffers, and a
missed fetch holds the last pixel rather than stalling the line. The host is
outside the contract.

### The ethos, in engineering terms

A5K keeps the **method** — slot-based arbitration, beam-locked sequencing,
fixed-function parallelism, separable compute, line buffers, open documentation.
It does not keep the **platform** — no 68k/Kickstart compatibility, no Amiga
software library, no whole-system product, no mass-market price, no custom ASIC.

That is a deliberate subset, not an accident.

---

## 11. The accurate sentence

Use this:

> A5K keeps the Amiga’s **engineering ethos** — chipset-first, deterministic,
> parallel, separable, legible — and deliberately does not claim the **platform
> ethos** of compatibility, mass-market affordability, or a whole-system product.

Do **not** use:

- “the true Amiga in every way”
- “the next Amiga”
- “an Amiga 5000”
- “Amiga-compatible”
- “mass-market”
- “a whole computer”

Those claims are false, and they invite exactly the arguments the project has
already lost.

---

## 12. Related documents

- `A5K-Lineage.md` — AAA, Hombre, Lorraine, and the two camps.
- `A5K-Brief.md` — the plain-language and engineering brief.
- `A5K-Slot-Table.md` — the timing contract and the five tests.
- `A5K-AROS-68K-Plan.md` — the compatibility paths.
- `A5K-Market-Signals.md` — the niche/small-batch product shape.
- `README.md` — the public framing.

---

*Documentation only · Rev. AW (B49) · 11 November 2026 · no hardware exists · no
measurement is claimed.*
