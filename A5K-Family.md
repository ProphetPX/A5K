# The A5K family

**A video and audio workstation card. Not a games console, and not a GPU.**

This document defines the product line: what is frozen, what the Studio models
add, how the output is chosen, and what order to build it in.

Status: proposal. No model has been built.

---

## 1. A5K (C+) — the reference machine, frozen

This is the design described in the rest of the repository. It does not gain
features. If a change would alter any line below, it is a new model, not a
revision.

| | A5K (C+) |
|---|---|
| FPGA | Artix-7 100T (4 GTP) |
| Pipelines | **1** — one beam, one Copper, one slot table |
| **Primary output** | **4K60 HDMI**, straight from fabric |
| **Secondary output** | **1080p60 DisplayPort**, via a commodity bridge |
| Input | **None** — capture begins with the Studio models |
| HDCP | none, by design |
| PCIe | ×1 (500 MB/s) |
| Memory | 1 × 32-bit DDR3L, 1 GB (2 GB max) |
| Host | x86-64, PCIe ×1 or larger slot |
| BOM | **~$255** |

**Promises:** one Amiga-like machine — deterministic, documented, open, under
$300 in parts.

**Does not promise:** independent outputs, 4K input, 4K DisplayPort, HDCP, or two
of anything.

## 2. What this card is for

Not to run old games, although it will. It is a **display and timing engine for
people who make things**: video editors, live-production operators, audio
engineers, instrument builders, and anyone who needs an image to appear at a
known instant rather than eventually.

## 3. Positioning, not emulation

Two tiers, one architecture — the way Commodore sold the A500 and the A3000.

| Tier | Amiga ancestor | Why it fits |
|---|---|---|
| **A5K (C+)** | **A500** | The wedge: one beam, one output, the lowest price at which the machine makes sense |
| **A5K Studio** | **A3000 / A4000** | The workstation: two beams, a wider host link, more memory — capability, not slots |

The A2000 is deliberately absent. Its identity was **expansion** — Zorro II slots,
a CPU slot, a video slot, SCSI — and none of these models have them.

> *Two tiers, one architecture. The A5K is the wedge. The Studio is the
> workstation. The comparison is one of position, not of compatibility.*

Three rules for using this in public: say "positioned like", never "compatible
with"; no model-number styling and no logos; never pair the analogy with a
compatibility claim.

## 4. Can one beam drive two outputs?

**Yes, but only if both show the same picture.**

- One beam, two connectors, same image = **mirrored**. That is C+.
- One beam, two connectors, different images at different timings = impossible.
  Two timings need two rasters, and a raster is a beam.
- The middle case: one beam, second output a crop, a scaled region or a colour
  variant of the same frame. Same timing, different pixels. Useful, not independent.

Independent outputs require two beams. There is no way around it.

## 5. The line

| | **A5K (C+)** | **A5K Studio** | **A5K Studio Pro** |
|---|---|---|---|
| FPGA | Artix-7 100T | Kintex-7 160T | Kintex-7 325T |
| Transceivers | 4 | 8 | 16 |
| Pipelines | **1** | **2** | **2** |
| Fabric | **64-bit** (1.19 GB/s) | **256-bit** (4.75 GB/s) | **256-bit** (4.75 GB/s) |
| HDMI out | 4K60 **SDR**, 8-bit 4:4:4 | 4K60 **HDR10**, 10-bit 4:2:2 | 4K60 HDR10, 10-bit 4:2:2 |
| DP out | 1080p60 SDR | 4K60 **HDR10**, 10-bit **4:4:4** | 4K60 HDR10, 10-bit **4:4:4** |
| Capture | none | 1080p60 **10-bit 4:2:2** | 1080p60 **10-bit 4:4:4** |
| PCIe | ×1 | ×2 | ×4 |
| Memory | 1 × 32-bit | 1 × 64-bit | 1 × 64-bit |
| BOM | **~$255** | **~$540** | **~$1,200** |

### 5.1 The HDMI wall, stated plainly

4K60 10-bit 4:4:4 needs a 742 MHz TMDS clock. HDMI 2.0 tops out at 600 MHz; only
HDMI 2.1's FRL carries it, and that needs a different transceiver class and a
protocol this design does not implement.

> **4K60 HDR10 is 10-bit 4:2:2 over HDMI 2.0 and 10-bit 4:4:4 over DisplayPort
> 1.2. 4:4:4 at 4K60 does not exist on HDMI on any model, because it requires
> HDMI 2.1 — a different transceiver class and a protocol this design does not
> implement.**

And 10-bit is not the same as HDR. Full HDR10 also needs a PQ or HLG transfer
function, static metadata (ST 2086, MaxCLL/MaxFALL), and a wide-gamut pipeline
(Rec.2020). Ten bits with an sRGB curve is simply deeper SDR.

A variant of the Pro is documented and not built: **A5K Studio Pro ISO**, with two
32-bit memory channels instead of one 64-bit, for installations where a capture
burst must never delay a scanout. ~$1,250, and a board change rather than a
redesign.

The Pro is the only model with 4K DisplayPort, because it is the only one with
enough transceivers to generate DP natively. Every other model uses a 1080p DP
bridge — a part that certainly exists, which removes the main supply risk from the
line.

## 6. Choosing the output

**HDMI is the default on every model.** The card then falls through a sensing
chain:

```
HDMI  ──►  DisplayPort  ──►  (reserved: DVI, S-Video, composite)
 1st          2nd                        not implemented
```

The rules:

1. **Sense hot-plug detect** on HDMI, debounced for 100 ms — monitors chatter
   during power-save and must not cause a mode change.
2. **If HDMI is present, it is primary.** Its EDID selects the mode: 4K60 where
   the display supports it, lower where it does not.
3. **Otherwise sense DisplayPort.** If present, it is primary, at 1080p60 (4K60 on
   the Pro).
4. **If neither is present**, the card keeps scanning out to an internal sink and
   sets a status bit. Nothing is lost when a monitor sleeps.
5. **Software can override** with `OUT_PREF = AUTO | HDMI | DP`. AUTO follows the
   chain; the others force a connector. The chain is the default, not a cage.

Every connector is driven simultaneously on single-beam models, so there is
nothing to "switch between" — the sensing decides *which display defines the mode*,
and which one is reported as primary.

**No physical switch on the A5K or Studio.** A 3-position **Auto / HDMI / DP**
switch is offered as an option on Studio Pro, for rack installations where the
operator wants to force an output regardless of what is plugged in. It is a
convenience, not a mechanism.

## 7. What two beams buy a professional

- **Programme and preview.** HDMI to air, DP for the next shot or scopes.
- **Capture while presenting.** One pipe scans out while the other ingests.
- **Genlock.** Frame-locked outputs, or locked to house sync.
- **Cross-blit.** Blitter reads pipe A, writes pipe B — a compositor with no CPU.
- **Frame-pass.** One pipe consumes the other's finished frame as a plane.
- **Audio.** A 60 Hz UI on one pipe, a waveform locked to the audio clock on the
  other.

## 8. What this card is not

| | A5K Studio Pro (325T) | A mid-range GPU (2026) |
|---|---|---|
| Compute | ~0.3 TOPS, 840 DSP slices | 100+ TOPS |
| Memory bandwidth | 12.8 GB/s | 300–1,000 GB/s |
| Shader cores | none | thousands |
| 3D pipeline | none | full, with texturing |
| SHA-256 | ~1–2 GH/s | ASICs: ~100 TH/s |

- **Not a 3D GPU.** No rasteriser, no texture unit, no depth buffer.
- **Not an AI accelerator.** Three orders of magnitude short.
- **Not a miner.** Five orders short, and loses money on power.

What it can do is **deterministic work at video rate**: encrypt or watermark a
stream in step with the beam, scale and composite in fixed time, timestamp every
frame.

## 9. Build order

1. **A5K (C+)** — validate the chipset, the slot table and the driver.
2. **A5K Studio** — add the second pipeline; prove the arbiter with two line rates.
3. **A5K Studio Pro** — same RTL, larger part, two 4K streams.
4. **Variants** — ISO memory, the output switch, only when a customer asks.

The sequencing is what keeps the family from becoming three half-finished
projects.

## 10. What is not promised, on any model

- 4K60 **input** — bandwidth and HDCP both say no.
- HDCP of any version.
- HDMI 4:4:4 at 4K60, on any model — see §5.1.
- DVI, S-Video, composite or coaxial output — reserved in the sensing chain,
  not designed.
- Binary compatibility with Amiga software.
- 3D acceleration or AI compute.
- A shipping date.

---

*Proposal, 2 November 2026. C+ frozen as of this document; changes to it require
a new model designation.*

---

*Revision: R, 2 November 2026. Living document; changes tracked in the private memo.*
