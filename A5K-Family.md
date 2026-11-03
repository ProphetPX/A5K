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

Independent outputs require two beams. There is no way around it — but two
beams are necessary, not sufficient. At 4K HDR the memory can afford one
composited beam, so what the second one may be is bounded by §5.3.

How the two share the bus — the superframe, the three tiers of claim, and the
worst case a driver may rely on — is specified in
`A5K-Dual-Pipe-Arbitration.md`.

## 5. The line

| | **A5K (C+)** | **A5K Studio** | **A5K Studio Pro** |
|---|---|---|---|
| FPGA | Artix-7 100T | Kintex-7 160T | Kintex-7 325T |
| Transceivers | 4 | 8 | 16 |
| Pipelines | **1** | **2** | **2** |
| Fabric | **64-bit** (1.19 GB/s) | **256-bit** (4.75 GB/s) | **256-bit** (4.75 GB/s); 512-bit in the Pro II |
| Copper tick | **7.0714 MHz**, fixed | 7.0714 MHz | 7.0714 MHz; a faster domain is reserved, not built |
| HDMI out | 4K60 **SDR**, 8-bit 4:4:4 | 4K60 **HDR10**, 10-bit 4:2:2 | 4K60 HDR10, 10-bit 4:2:2 |
| DP out | 1080p60 SDR | 4K60 **HDR10**, 10-bit **4:4:4** | 4K60 HDR10, 10-bit **4:4:4** |
| Capture | none | 1080p60 **10-bit 4:2:2** | 1080p60 **10-bit 4:4:4** |
| Both outputs at once | mirrored, 1080p on DP | **one graphics + one video or derived** | same; two independent graphics needs the Pro II |
| PCIe | ×1 | ×2 | ×4 |
| Memory | **2 × 16-bit** (32-bit, 1 GB) | **4 × 16-bit** (64-bit, 2 GB) | **4 × 16-bit** (64-bit, 2 GB) |
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

The earlier **Studio Pro ISO** idea — two 32-bit memory channels instead of one
64-bit — is withdrawn. It moved the same 12.8 GB/s into two narrower controllers,
which buys isolation, not capacity; and isolation now belongs in the burst
scheduler's QoS rather than in a second DRAM channel.

### 5.2 One tick, and room for another

Every model runs the Copper at **7.0714 MHz** — 148.5 ÷ 21, exactly twenty-one
slots of the bus. It is 0.26% slower than the Amiga's 7.09 MHz on PAL and 1.2%
slower than NTSC's 7.16 — and, unlike either, it divides the bus exactly. An approximate ratio would drift five slots per line,
which is the one thing a machine built on countable timing cannot afford.

The Studio class reserves a **second, faster tick domain** as a future hardware
mode. What is fixed now is the rule rather than the rate:

- **C+ never gains it.** The reference model stays at one tick.
- **A tick is always a whole number of slots**, so exact doubling is unavailable:
  21 ÷ 2 = 10.5. The usable rates are integer divisors — 14.85, 21.214 or 29.7 MHz.
- **It changes only at frame end**, like the Copper list swap.
- **It costs bandwidth.** A Copper instruction costs one slot, so the Copper's
  ceiling is 1/N of the bus: 4.8% today, 14.3% at 3×.

`BEAMCON0[3:1]` selects it and reads `000` on everything shipping today. The rate,
and whether the two beams share one domain, remain open. See *A5K — The Slot
Table*, §7.

The Pro is the only model with 4K DisplayPort, because it is the only one with
enough transceivers to generate DP natively. Every other model uses a 1080p DP
bridge — a part that certainly exists, which removes the main supply risk from the
line.

### 5.3 What the second output can be

The limit is the slot fabric, not the memory. At 256 bits the fabric moves
4.75 GB/s and 4.52 of it reaches bursts; the 64-bit DDR3L behind it can supply
12.8, so the memory sits at 43%.

| Configuration at 4K60 | Traffic | Share of 4.52 GB/s |
|---|---|---|
| graphics + video + capture | 3.70 GB/s | 82% |
| graphics + derived 4K output + capture | 2.46 GB/s | 54% |
| graphics + independent 1080p graphics + capture | 2.96 GB/s | 66% |
| two independent 4K graphics + capture | 4.45 GB/s | **98%** |

So on a Studio or a Pro the second output is one of three things: **video**
(4:2:2, passthrough or scaled), a **derived** output (a crop, a scaled region or a
colour variant of the same frame), or **independent graphics up to 1080p**. What
it is not is a second fully independent 4K HDR graphics raster.

Said the other way: both connectors run 4K60 HDR at the same time, but only one of
them can be composited graphics.

### 5.4 The Pro II path

Doubling the slot to 512 bits doubles the fabric to 9.5 GB/s and leaves the DRAM,
its pins and the PCB alone. The memory then runs at 86% instead of 43%. Two
independent 4K HDR graphics beams, capture, a 1.5 GB/s blitter and a 1.0 GB/s host
come to 6.95 GB/s — 77% of the fabric and 63% of the memory.

**A5K Studio Pro II** is therefore a -3 speed grade and a wider fit on the same
board: roughly +$250, not a respin. That is also why the Studio ships 64-bit
memory although 32 bits would have met today's budget — width is the one thing
that cannot be added later.

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
3. **A5K Studio Pro** — same RTL, larger part, two 4K60 HDR outputs: one
   composited graphics beam and one video or derived beam.
4. **A5K Studio Pro II** — 512-bit fabric on the same board, when two
   *independent* 4K HDR graphics streams are worth a speed grade.

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

## 11. Where this is most likely wrong

Nothing in this document has been built or measured. The assumptions behind it —
video timing, timing closure, memory overheads, buffer depth, prices — are listed
with severity and consequence in `A5K-Frailties.md`, and that register is the
honest version of this page.

The four that would change *this* document most:

| # | Assumption | If it fails |
|---|---|---|
| A1 | two beams share a superframe | the Studio cannot be built as specified — it is a rule now, not a simulation |
| B1 | 4K uses CEA-861 timing | CVT-RB leaves 300 ns of blanking; about seven slots of refresh spill into the line — a table regeneration, not a redesign |
| B3 | 256-bit closes at 148.5 MHz on a -2 | a -3 part, and the Studio's price moves |
| C4 | the bill of materials | ±20% is normal; the wedge stops being a wedge at +25% |

---

*Proposal, 2 November 2026. C+ frozen as of this document; changes to it require
a new model designation.*

---

*Rev. Y · 2 November 2026 · project started 30 October 2026*
