# The A5K family

**A video and audio workstation card. Not a games console, and not a GPU.**

This document defines the product line around the reference machine: what is
frozen, what the second model adds, what is deliberately left out, and what order
to build it in.

Status: proposal. No model has been built.

---

## 1. A5K (C+) — the reference machine, frozen

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

**Promises:** one Amiga-like machine — deterministic, documented, open, under
$200 in parts.

**Does not promise:** independent outputs, 4K input, HDCP, PCIe bandwidth for
frame grabbing, or two of anything.

C+ is the definition of "Amiga-like" in this project. Everything above it is a
different product that borrows the same core.

## 2. What this card is for

The purpose is not to run old games, although it will. It is a **display and
timing engine for people who make things**: video editors, live-production
operators, audio engineers, instrument builders, and anyone who needs an image to
appear at a known instant rather than eventually.

The distinction matters because it decides what the second model is for. A games
machine wants one output and lots of compatibility. A workstation wants capture,
compositing, preview and programme — often at the same time.

### 2.1 Positioning, not emulation

Two tiers, one architecture — the way Commodore sold the A500 and the A3000.

| Tier | Amiga ancestor | Why it fits |
|---|---|---|
| **A5K (C+)** | **A500** | The wedge: one beam, one output, the lowest price at which the machine makes sense |
| **A5K Duo (D)** | **A3000 / A4000** | The workstation: two beams, a wider host link, more memory — capability, not slots |

The A2000 is deliberately absent from that table. Its identity was **expansion**
— Zorro II slots, a CPU slot, a video slot, SCSI — and the Duo has none of them.
Invoking the A2000 invites a buyer to expect slots, and there are none.

> *Two tiers, one architecture — the way Commodore sold the A500 and the A3000.
> The C+ is the wedge. The Duo is the workstation. The comparison is one of
> position, not of compatibility or features.*

Three rules for using this in public:

1. **Say "positioned like", never "compatible with".** The analogy is about market
   tier, not software or hardware.
2. **No model-number styling and no logos.** Do not render "A5K" in a Commodore
   typeface, and do not use the checkmark.
3. **Never combine the analogy with a compatibility claim.** "The A3000 of the
   family" is descriptive; "A3000-class compatibility" is a misrepresentation.

## 3. Can one beam drive two outputs?

**Yes, but only if both show the same picture.**

- One beam, two transmitters = **mirrored**. Same image, same timing, two
  connectors. That is what C+ does, and it is genuinely useful.
- One beam, two outputs showing *different* content = impossible. Different
  content at different timings needs two rasters, and a raster is a beam.

There is a middle case — one beam feeding two outputs where the second is a crop,
a scaled region, or a different colour treatment of the same frame. Same timing,
different pixels. Useful, but not "independent".

So: **independent outputs require two beams.** There is no clever way around it,
because the beam *is* the thing that defines when each pixel exists.

## 4. The two models, one core

| | **A5K (C+)** | **A5K Duo (D)** |
|---|---|---|
| FPGA | Artix-7 200T | Kintex-7 325T |
| Transceivers | 4 | 16 |
| Pipelines | **1** | **2** |
| Output | 4K60 mirrored | **4K60 + 4K60, independent** |
| Input | 1080p60 | 1080p60 |
| PCIe | ×1 | **×4** |
| Memory | 1 × 32-bit, 1 GB | **1 × 64-bit, 2 GB** |
| BOM | **~$195** | **~$1,150** |

One RTL tree, one register map, one driver. The Duo instantiates the display side
twice and gives each pipe its own Copper, blitter and slot table. A capability
register tells the driver which configuration it is talking to.

### Documented variants (not designed)

| Variant | What changes | BOM | Build when |
|---|---|---|---|
| **Duo −** | Kintex-7 160T, 4K60 + 1080p60, PCIe ×2 | ~$500 | if the Duo proves demand and price matters |
| **Duo VRAM** | two 32-bit channels instead of one 64-bit | ~$1,250 | only if a customer needs physical isolation |

Neither is a redesign: both are the same RTL on different silicon or a different
memory layout.

## 5. What two beams buy a professional

- **Programme and preview.** Output A goes to air; output B shows the next shot,
  a multiview, or scopes — at a different resolution if that is cheaper.
- **Capture while presenting.** Pipe A scans out the finished frame while pipe B
  ingests the next one. With one beam, capture means freezing the display.
- **Genlock.** Two beams can be frame-locked to each other or to house sync. That
  is the difference between a monitor and a broadcast device.
- **Cross-blit.** The blitter reads from pipe A's memory and writes into pipe B's.
  A compositor with no CPU and no GPU.
- **Frame-pass.** Pipe B consumes pipe A's completed frame as a plane. Picture-in-
  picture and feedback effects in hardware.
- **Audio.** The same argument applies to sample-accurate timing: one pipe can
  present a 60 Hz UI while the other drives a waveform display locked to the
  audio clock, without either waiting on the other.

## 6. What this card is not

Worth stating with numbers, because "FPGA card" invites the wrong expectations:

| | A5K Duo (Kintex-7 325T) | A mid-range GPU (2026) |
|---|---|---|
| Compute | ~0.3 TOPS equivalent, 840 DSP slices | 100+ TOPS |
| Memory bandwidth | 12.8 GB/s | 300–1,000 GB/s |
| Shader cores | none | thousands |
| 3D pipeline | none | full, with texturing |
| Crypto hashing | ~1–2 GH/s SHA-256 | ASICs do 100 TH/s |

So, plainly:

- **Not a 3D GPU.** There is no rasteriser, no texture unit, no depth buffer. A
  simple flat-shaded polygon engine could be added in fabric, and it would look
  like 1995, not 2025.
- **Not an AI accelerator.** 840 DSP slices is three orders of magnitude short of
  a modern GPU for training, and still far short for serious inference.
- **Not a miner.** An FPGA is 100,000× slower than an ASIC at hashing, and loses
  money on power alone.

What it *can* do is **deterministic work at video rate**: encrypt or watermark a
4K stream in line with the beam, scale and composite in fixed time, timestamp
every frame. That is a real niche, and it is where the design is strong.

## 7. Build order

1. **A5K (C+)** — validate the chipset, the slot table and the driver.
2. **A5K Duo (D)** — add the second pipeline, prove the arbiter with two
   different line rates.
3. **Variants** — only when a customer asks, and only as documented changes.

The sequencing is what keeps the family from becoming three half-finished
projects.

## 8. What is not promised, on any model

- 4K60 **input** — bandwidth and HDCP both say no.
- HDCP of any version.
- Composite, S-Video, SCART or coaxial output — future options, not designed.
- Binary compatibility with Amiga software.
- 3D acceleration or AI compute.
- A shipping date.

---

*Proposal, 2 November 2026. C+ frozen as of this document; changes to it require
a new model designation.*
