# The A5K family

**C+ is frozen. Everything above it is a departure, and says so.**

This document defines the product line around the reference machine. The first
section is a specification that should not change; the rest is an exploration of
what a card with *two* pipelines can do that one cannot.

Status: proposal. No model has been built.

---

## 1. A5K — the reference machine (C+), frozen

This is the design described in the rest of the repository. It does not gain
features. If a change would alter any line below, it is a new model, not a
revision.

| | A5K (C+) |
|---|---|
| FPGA | Artix-7 200T (4 GTP) |
| Pipelines | **1** — one beam, one Copper, one slot table |
| Output | 4K60 on HDMI and DisplayPort, **mirrored** |
| Input | 1080p60 HDMI, unencrypted sources only |
| HDCP | none, by design |
| PCIe | ×1 (500 MB/s) |
| Memory | 1 × 32-bit DDR3L, 1 GB (2 GB max) |
| Host | x86-64, PCIe ×4 physical slot |
| BOM | **~$195** |

**What C+ promises:** one Amiga-like machine, deterministic, documented, open,
under $200 in parts.

**What C+ does not promise:** independent outputs, 4K input, HDCP, PCIe
bandwidth for frame grabbing, or two of anything.

That is the definition of "Amiga-like" in this project. Everything else is a
different product that borrows the chipset.

## 2. Why climb above it

A single pipeline is one machine doing one thing at one rate. A second pipeline
lets a card **capture, process and present at the same time** — the workflow a
video mixer, a kiosk player, a simulator or a live-production rig actually needs:

```
capture ──► process ──► present          pipeline A
                  └────► preview          pipeline B
```

With one pipeline that sequence has to be serialised: grab a frame, stop
displaying, process, resume. With two, the display never stops while the next
frame is being built.

## 3. The line

| | **A5K (C+)** | **A5K Duo (D−)** | **A5K Duo Pro (D)** | **Duo Pro VRAM (D+)** |
|---|---|---|---|---|
| FPGA | Artix-7 200T | Kintex-7 160T | Kintex-7 325T | Kintex-7 325T |
| Transceivers | 4 | 8 | 16 | 16 |
| Pipelines | **1** | **2** | **2** | **2** |
| Outputs | 4K60, mirrored | **4K60 + 1080p60** | **4K60 + 4K60** | 4K60 + 4K60 |
| Input | 1080p60 | 1080p60 | 1080p60 | 1080p60 |
| PCIe | ×1 | ×2 | ×4 | ×4 |
| Memory | 1 × 32-bit | 1 × 64-bit | 1 × 64-bit | **2 × 32-bit + capture** |
| BOM | **~$195** | **~$500** | **~$1,150** | **~$1,250** |

The mid model exists because eight transceivers cannot carry two 4K streams and
PCIe ×4. It can carry 4K60 on one pipe, 1080p60 on the other, and PCIe ×2 — which
is the shape a mixer wants: programme at 4K, preview at HD.

The VRAM variant is a board change, not a redesign: same RTL, same part, two
memory channels for physical isolation. Build it only if a customer needs the
guarantee that a capture burst can never delay a scanout.

## 4. What "dual pipeline" means in hardware

| Resource | Single | Dual |
|---|---|---|
| Beam counter | 1 | **2** |
| Denise scanout | 1 | **2** |
| Copper | 1 | **2** |
| Blitter | 1 | **2** (or 1 with two contexts) |
| Slot table | 1 | **2**, arbitrating one memory |
| Palette | 1 | **2** |

Two blitters matter more than they look: a shared blitter makes each pipe wait
for the other, which defeats the purpose.

The arbiter is the hard part. Two periodic clients with different line rates
sharing one memory controller need **deadline scheduling with hard QoS**, not
best-effort sharing. The six reliability rules from the slot table apply per
pipe, plus:

- each pipe's display band is reserved before the other pipe's blitter;
- a capture burst may not preempt either display band;
- starvation of either pipe is a design failure, not a performance issue.

## 5. The three primitives that make it a pipeline

Without these, "two pipes" is just two devices in one slot:

1. **Cross-blit.** Blitter source in pipe A's memory, destination in pipe B's.
   A compositor without a CPU.
2. **Genlock.** A shared frame clock (locked outputs), or independent clocks
   with a defined relationship (free-running, with a resync point).
3. **Frame-pass.** Pipe B consumes pipe A's completed frame as a plane. Picture-
   in-picture, preview, and feedback effects, all in hardware.

These should be specified in the register map before any RTL exists, because they
determine the memory model.

## 6. What the departure costs

- **RTL:** roughly double the display side (two beams, two Coppers, two
  blitters). The blitter and Copper are small; the scanout and arbiter are not.
- **Driver:** one device with two CRTCs, two Copper contexts, two buffer sets.
  Linux DRM models this natively; AROS does not, and would need work.
- **Power and thermal:** a 325T with two pipes needs a fan and a proper VRM. The
  card stops being passive.
- **Software:** nothing exists that uses two pipelines. The first application has
  to be written, or the second pipe is just a second monitor.
- **Meaning:** the single beam *is* the Amiga model. Dual-pipe keeps the memory
  shared but breaks the single timing contract. A Copper list belongs to pipe A
  or pipe B; a demo must choose.

That last point is the one to write down, in the same place the documents say
"not a clone". It is a deliberate divergence, not an oversight.

## 7. What is not promised, on any model

- 4K60 **input** — bandwidth and HDCP both say no.
- HDCP of any version.
- Composite, S-Video, SCART or coaxial output — future options, not designed.
- Binary compatibility with Amiga software, on any model.
- A shipping date.

## 8. Build order

1. **A5K (C+)** — validate the chipset, the slot table and the driver.
2. **A5K Duo (D−)** — add the second pipeline on the cheaper part; prove the
   arbiter with two different line rates.
3. **Duo Pro (D)** — same RTL, bigger part, two 4K streams.
4. **Duo Pro VRAM (D+)** — only on request.

C+ is the machine. The Duo line is the studio.

---

*Proposal, 2 November 2026. C+ frozen as of this document; changes to it require
a new model designation.*
