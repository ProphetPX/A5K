# The A5K family

**A video and audio workstation card. Not a games console, and not a GPU.**

This document defines the product line: what is settled, what the Studio models
add, how the output is chosen, and what order to build it in.

Status: proposal. No model has been built.

---

## 1. A5K (C+) Rev 2 — the reference machine

**Rev 2 replaces the first C+ and is not frozen yet.** The audio path is the
reason: the original C+ topped out at stereo, and a card sold to video and audio
people cannot ship that. Rev 2 is the working baseline, and it freezes only when the author says so —
not when a checklist completes, and not before the remaining questions in
`TODO.md` are answered.

| | A5K (C+) Rev 2 |
|---|---|
| FPGA | Artix-7 100T (4 GTP) |
| Pipelines | **1** — one beam, one Copper, one slot table |
| **Primary output** | **4K60 HDMI**, straight from fabric |
| **Secondary output** | **1080p60 DisplayPort**, via a commodity bridge |
| **Audio** | **8 channels, 24-bit** — 4 stereo jacks, TOSLINK, HDMI LPCM |
| Input | **None** — capture begins with the Studio models |
| HDCP | none, by design |
| PCIe | ×1 (500 MB/s) |
| Memory | 1 × 32-bit DDR3L, 1 GB (2 GB max) |
| Host | x86-64, PCIe ×1 or larger slot |
| BOM | **~$280** |

**Promises:** one Amiga-like machine — deterministic, documented, open, under
$300 in parts, with eight channels of audio.

**Does not promise:** independent outputs, 4K input, 4K DisplayPort, HDCP, or two
of anything.

**The first C+ (~$255, stereo DAC) is retired and will never be built.** It was
correct as a timing study and wrong as a product.

## 2. What this card is for

Not to run old games, although it will. It is a **display and timing engine for
people who make things**: video editors, live-production operators, audio
engineers, instrument builders, and anyone who needs an image to appear at a
known instant rather than eventually.

### 2.1 Two machines, one bus

The card is not a peripheral in the sense a sound card or a GPU is. It is a
**second machine** on the far side of the PCIe link: its own processor, its own
memory, its own clocks, its own display and audio engines. The host supplies
power, a slot, and — when it wants to — data.

There is **no shared clock and no timing protocol across the link.** Standard
PCIe, standard DMA in both directions: Copper lists, frames and audio go in;
captured frames and telemetry come out. The host's video and audio and the card's
video and audio are separate endpoints, and software decides which one plays
what.

**When synchronisation is needed, the card is the clock master.** It drives word
clock out and external converters follow. The card never chases the host's clock;
a user who wants that can resample in software, where the cost is visible and
reversible.

That is the whole paradigm: **the host does the thinking, the card does the
timing.**

And one consequence worth stating early: **the card is CPU-agnostic by
construction.** It has no ISA, no emulation and no operating system of its own.
The question that consumed Commodore's last years — which processor, and how to
keep software portable across it — does not arise here, because the answer belongs
to the host.

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
| Audio out | **8 ch**, 24-bit: 4 jacks + TOSLINK + HDMI; front-panel HP/mic header | same, plus S/PDIF/ADAT in and word clock | same, plus **USB UAC2 host** |
| Both outputs at once | mirrored, 1080p on DP | **one graphics + one video or derived** | same; two independent graphics needs the Pro II |
| Refresh | up to **1080p240** on HDMI; DP 60 | up to **1080p240**, 1440p144; 4K60. **No VRR** | same |
| PCIe | ×1 **Gen2** | ×2 **Gen2** | ×4 — generation **not yet decided** |
| Memory | **2 × 16-bit** (32-bit, 1 GB) | **4 × 16-bit** (64-bit, 2 GB) | **4 × 16-bit** (64-bit, 2 GB) |
| BOM | **~$280** | **~$565** | **~$1,225** |

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

### 5.5 Audio

**Eight channels, 24-bit, on every model — and stereo is what comes out of the
box, on every output.** The channel mode is one setting, not a per-port switch:

| Mode | HDMI / DisplayPort | TOSLINK | Jacks |
|---|---|---|---|
| **Stereo** — factory default | 2-channel LPCM | 2-channel PCM | downmix on jack 1, 2–4 silent |
| **5.1** | 6-channel LPCM | 2-channel PCM, or a bitstream | 3 jacks discrete |
| **7.1** | 8-channel LPCM | 2-channel PCM, or a bitstream | 4 jacks discrete |

The mode is stored in the configuration flash. Change it once and **that becomes
the power-on default from then on**; a factory reset returns it to stereo. TOSLINK
stays at two channels in every mode, because S/PDIF has no room for more — in 5.1
and 7.1 it carries either the downmix or a compressed bitstream for a receiver.

**Sensing detects plugs, not speakers.** A switching jack knows that something is
inserted; it cannot know whether a speaker is on the other end, whether it is
powered, or how many channels it can reproduce. Plug presence is therefore a
*hint*: the driver may offer surround when a surround jack is occupied, and the
user decides. HDMI is the one place where capability is genuinely negotiated,
because the sink declares its formats in EDID — the card offers 8-channel LPCM
there only when the display says it accepts it.

| Output | What it carries |
|---|---|
| **HDMI / DisplayPort** | 8-channel LPCM, or a compressed bitstream passed through untouched |
| **TOSLINK** | 2-channel PCM, or a compressed Dolby/DTS stream — **not** 8-channel LPCM. S/PDIF has no room for it, and no design can change that |
| **Analogue** | 4 × 3.5 mm stereo jacks — front, surround, rear, centre/LFE — from an 8-channel DAC. **Stereo downmix by default; discrete channels when the mode is raised** |

The TOSLINK limit is worth stating plainly: optical gives 7.1 only as a
*bitstream*, decoded by a receiver. It is a compatibility port, not a
multichannel one. Multichannel LPCM goes over HDMI, DisplayPort, or the jacks.

**Headphones, microphone, and the front panel.** The card carries a standard
**10-pin HD-Audio front-panel header**, so any ATX case works: headphone L/R, mic,
ground, presence and the sense returns. The rear carries the four line-outs and
its own mic jack.

The headphone path is **not a passive tee**. A switched jack in series with the
rear output is how PCs did it — insertion physically breaks the path to the back —
and it costs independent volume and puts a long unshielded stub on the analogue
output. Instead the card fits a **second, stereo DAC** for the front panel, with
its own volume in the mixer:

- Plugging in headphones switches the card to **stereo mode**, routes the downmix
  to the headphones, and mutes the rear jacks.
- Unplugging restores the previous mode.
- The rear 8-channel path is never broken, and a card with no front panel fitted
  behaves normally — the header's presence pin says so.

The microphone is an **ADC with two inputs**, front and rear. If both are plugged,
the front wins and the driver reports which. Bias for electret microphones is
supplied on both.

**Direct monitoring.** The ADC can be mixed straight to the DAC inside the card,
bypassing the host and the operating system entirely. At 96 kHz, with converters
that offer a low-latency filter mode, the round trip is **under a millisecond** —
which is the number a musician actually feels. The host path adds USB framing and
OS buffering on top of that; it is for recording and playback, not for monitoring.

**Inputs on the Studio models:** line-in, plus S/PDIF or ADAT with **word clock in
and out**, so an external converter can be the clock master. That is what
professional users actually want, and it costs a connector and a comparator.

**Clocks.** Two families, because neither divides the 148.5 MHz video clock:
22.5792 MHz for 44.1/88.2/176.4 and 24.576 MHz for 48/96/192. The **default is
the 44.1 family**; the 48 family exists because video and broadcast are 48 kHz,
and resampling every video timeline is exactly the kind of hidden arithmetic
this project exists to avoid. Both crystals are fitted.

One crystal covers a whole family: 24.576 MHz is 512 × 48 kHz and 256 × 96 kHz,
so **96 needs no extra part** — only a divider setting. **The card is capped at
96 kHz.** 44.1 is the default, 48 is the video standard, and 88.2/96 are fitted
and claimed once measured. Nothing above 96 is offered: the converter stops there,
the data rate triples for no audible gain, and several converters measure *worse*
at 192 than at 96.

**Clocking modes.** The card's clock is its own unless told otherwise. Three
modes, selected by a register and **never stored across a power cycle**:

| Mode | Register | What actually happens |
|---|---|---|
| **Independent** — default | 0 | The card free-runs on its own crystals; word clock in is ignored |
| **Card master** | 1 | The card drives **word clock out**; external converters follow it |
| **External master** | 2 | The card locks to **word clock in**; a status bit reports lock and frequency |

Word clock connectors exist on the **Studio models**; C+ has none, so it is a
mode-0 machine. Mode resets to 0 at every power-on and on factory reset. It is **not a BIOS
setting and not a switch**: a PCIe card has no business in the host's firmware,
and a switch is a part that can be set wrong and left wrong. The driver sets the
register; the register map is public, so any driver can.

The reason it does not persist is that a wrong clock mode presents as silence or
a pitch error — which reads as a hardware fault. The safe state has to return by
itself.

There is no mode that slaves the host. The host's codec has no clock input, and
no add-in card can give it one. If an application wants the host's stream to
follow the card, it **resamples on the host**, in software, where the cost is
visible — and that is the user opt-in you asked for, not a hardware default.

**USB.** A UAC2 host port appears on the **Studio and above**, never on C+. The
**PHY footprint — pads and connector — is on the board from the first revision**,
whether or not the firmware is ready; enabling it later is a firmware update, not
a board change. The scope is narrow on purpose: one interface, playback and
capture, no hubs, no HID. The PHY is cheap; the firmware is not, and a $280 wedge
does not need it.

**If it does not fit, the feature is disabled — the chip is never uprated.**
*Build it in the tool before promising it on the box.* If the UAC2 host will not
fit the Studio's 160T alongside both beams, the port ships dark: pads on the
board, firmware never enabling it. The Studio stays at ~$565. Uprating to a 325T
to rescue one feature would turn the Studio into a Pro at ~$1,100 and delete the
tier — so that is not an option, at any point.

**Drivers.** ALSA upstream, AHI on AROS, OSS4 out-of-tree and explicitly invited.
The register map is public, so the third one can be written by the people who
want it.

### 5.6 Storage and filesystems

**No model is a storage controller.** The card is a display and audio engine with
a supervisor CPU, not a computer; the host owns the disks, the burners, the card
readers and the filesystems.

**One exception, on the Pro only and optional: a capture recorder.** A single M.2
NVMe slot behind a PCIe switch, so the capture engine can record without sending
the stream through the host. The switch is **proposed** as Gen3-capable, so the host and
the drive could negotiate Gen3 ×4; the Pro's PCIe generation is **not yet
decided**. **The FPGA's own port is Gen2 ×4 either way**, because 7-series PCIe
hard blocks stop there. That is about 1.7 GB/s into the drive — enough for 4K60 10-bit
4:2:2 (1.24 GB/s), not for 4:4:4 (1.87 GB/s). Gen3 straight from the FPGA means an
UltraScale part and a different price class: a future model, not this one.

**The microSD socket is private to the card.** It holds firmware and a `SAFE_MODE`
file, it is read at boot, and it is **never exposed to the host** as a block
device. It is a recovery device, not a system disk. If the picture is wrong or
dark, that file is one of the ways back — the others are the host register, the
button, and the automatic mode cycle.

Filesystems are **operating-system middleware**, not hardware. The card's only
obligation is the block contract it presents to a host driver, and it presents
none: the card has no block device at all.

**AROS can meet the card two ways.**

| | What runs | Filesystems it sees |
|---|---|---|
| **Hosted** | AROS as a process on Linux | inherits Linux's — ext4, XFS, Btrfs, ZFS, HFS+, Amiga `affs` |
| **Native** | AROS installed on the host's disk | its own — FFS/OFS, SFS, PFS3, FAT |

Hosted is the first step, because it lets the driver be written before committing
to a native install. Native is the destination: AROS with a HIDD for the card,
running on the host's own disks.

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

### 6.1 First power-on, and the way back

Every model comes up on the display's preferred timing. With no EDID it comes up
at **1024×768 @ 60** — XGA, which every display since 1990 accepts — and the user
may change that default; it is stored in the configuration flash.

The floor is **640×480 @ 60**, the lowest HDMI or DisplayPort can carry
(25.175 MHz) and the modern equivalent of Amiga "hi-res", 640 pixels wide. A
15 kHz Amiga mode cannot be put on either port at all, so the old CRT monitors
are out of reach without an external converter.

Four ways back from a blank screen, all fitted: a **host register** (PCIe config
space does not depend on video), a **`SAFE_MODE` file on the microSD**, a
**button or jumper** at power-on (one second for safe video, ten for factory
defaults), and an **automatic cycle** of 1024×768 → 800×600 → 640×480 after ten
seconds without a hotplug. Precedence is button, SD file, stored default, EDID,
automatic.

**Rates, not just resolutions.** Every model presents a fixed set: the standard
video rates 23.976–60 on two slot clocks, high refresh to **1080p240** and
**1440p144**, and 4K at 60. There is **no variable refresh** — a FreeSync or
G-Sync panel simply runs at the fixed rate it is given, which every panel
accepts. And 1080p240 costs exactly what 4K60 costs, because the budget is per
pixel rate, not per resolution.

Four rules keep it out of trouble, and they matter more than the mode list: never
emit a timing the EDID does not declare, use the preferred timing at boot,
implement DPMS D0/D3 with a hotplug wake and no idling link, and debounce hotplug
for 100 ms. A display is the authority on what it can do; the card only asks for
what it has been told is legal.

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
- **Not a Vampire, and not an Amiga.** A Vampire V4+ or an A6000 is a computer
  that runs Amiga software on an FPGA. This card has no CPU, no 68K, no Kickstart
  and no binary compatibility: it cannot run an Amiga program and does not try.
  What it shares with those machines is the silicon class — an FPGA, DDR and an
  HDMI output — and nothing else. If that distinction is not obvious in one
  sentence, the design has a positioning problem, not a technical one.

What it can do is **deterministic work at video rate**: encrypt or watermark a
stream in step with the beam, scale and composite in fixed time, timestamp every
frame.

## 9. Build order

1. **A5K (C+) Rev 2** — validate the chipset, the slot table, the driver and the eight-channel audio path.
2. **A5K Studio** — add the second pipeline; prove the arbiter with two line rates.
3. **A5K Studio Pro** — same RTL, larger part, two 4K60 HDR outputs: one
   composited graphics beam and one video or derived beam.
4. **A5K Studio Pro II** — 512-bit fabric on the same board, when two
   *independent* 4K HDR graphics streams are worth a speed grade.

The sequencing is what keeps the family from becoming three half-finished
projects.

## 10. What is not promised, on any model

- 4K60 **input** — bandwidth and HDCP both say no.
- **Variable refresh** — FreeSync, G-Sync Compatible, Adaptive Sync. A variable
  line time would invalidate the rota and every WAIT position in it.
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

*Rev. AS · 3 November 2026 · project started 30 October 2026*
