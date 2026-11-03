# Where this is most likely wrong

**A register of the assumptions this project rests on.**

> Nothing here has been built, simulated or measured. Every number in these
> documents is arithmetic from datasheets, standards and clock rates. This file
> lists what that arithmetic assumes, in the order a reviewer should attack it.
>
> **This is the real test of the design.** A specification that cannot name its
> own weak points is a brochure.

## How to read it

| Class | Meaning | If it is wrong |
|---|---|---|
| **Undefined** | we know we have not decided | blocks everything downstream |
| **Unverified** | decided, but only on paper | a number or a part changes |
| **Assumed** | a defensible choice, not a proof | the constraint changes, not the arithmetic |

**Severity.** *Blocking* changes a number that other numbers depend on, or the
architecture. *Major* changes a price, a part or a constraint. *Minor* affects
only itself.

If you find one of these, quote its identifier. Every revision of the documents
cites the identifiers it answers.

---

## A. Undefined

### A1. Dual-pipe arbitration

**Was.** No rule existed for two beams sharing one slot table. The family
document said the Studio has two beams; the slot table specified one.

**Now.** Written in `A5K-Dual-Pipe-Arbitration.md`: a superframe, three tiers of
claim, and stated starvation bounds.

**Remaining risk.** The superframe bound, the refusal of mixed pixel-clock
standards, and the assumption that a second register file is affordable are
policy choices, not proofs. The page is a specification, not a simulation.

**Test.** The three tests in §7 of that document.

**Severity.** Closed on paper; **blocking** until simulated.

---

## B. Unverified

### B1. 4K is assumed to use CEA-861 timing

**Claim.** 4,400 × 2,250 dots, 1,100 64-bit slots per line, 560 dots of blanking
— 943 ns — and therefore room for two refreshes.

**If it fails.** CVT-RB is 4,000 × 2,222 at 533.25 MHz: **1,114 slots per line**
and **160 dots of blanking, 300 ns** — 44.6 slots against the 52 one refresh
needs. About 0.96 refreshes per line must therefore spill roughly **7 slots into
the active region, 0.6% of the line**, where the 350 ns line buffers already
cover them. The per-line numbers move by 1.3% and the table is regenerated; the
display band goes from 44% to 43%, not up.

**Test.** Read the EDID of the target displays, confirm CEA support, and re-run
the budget with CVT-RB timings.

**Severity.** Major — a table regeneration, not a redesign. It was recorded as
blocking until the arithmetic was redone; the correction is in Rev. Z.

### B2. tRFC is taken as 350 ns

**Claim.** Refresh blocks the bus for 350 ns, 52 slots, 4.5% of the time.

**Problem already known.** 350 ns is the **8 Gb** figure. The bill of materials
uses **4 Gb** devices, whose tRFC is **260 ns**.

**If corrected.** Refresh falls to 3.3%, total overhead to 12.3%, and every line
buffer shrinks. The error is in the safe direction, which is why it has not been
changed in a hurry — but it is an error and it is recorded here rather than
quietly fixed.

**Test.** Confirm the exact ordering part number.

**Severity.** Minor.

### B3. 148.5 MHz closes at 256 bits

**Claim.** A 256-bit slot path closes timing at 148.5 MHz on a Kintex-7 **-2**.

**If it fails.** A -3 speed grade, +20–25% on the FPGA. If 512 bits also fails,
the Pro II is not buildable on this board at all.

**Test.** Place and route with the MIG attached. Report worst negative slack.

**Severity.** Major.

### B4. The DDR3L overheads are budgets

**Claim.** Refresh 4.5%, turnaround 6%, row misses 3% — 86.5% of raw bandwidth.

**If it fails.** Row misses are the softest: 3% assumes one open page per plane
with banks interleaved. A poor address map doubles it, and DRAM load moves from
43% to 46%. The fabric limit does not move, which is why the design survives.

**Test.** MIG simulation with the real address map.

**Severity.** Major.

### B5. Line buffers sized to tRFC are enough

**Claim.** A FIFO holding tRFC worth of the stream's own pixels never underruns.

**If it fails.** The beam holds pixels every 7.8 µs, permanently. A visible,
periodic artefact — the worst kind, because it looks like a software bug.

**Test.** Slot-table test 2: refresh forced to the worst phase.

**Severity.** Major.

### B6. One Copper lane is enough

**Claim.** One slot in twenty-one — amortised to one in four ticks at 256 bits —
serves a deterministic Copper.

**If it fails.** WAIT positions drift by a tick, and the timing contract is void.

**Test.** Slot-table test 3.

**Severity.** **Blocking.**

### B7. Sequential fetching wastes nothing

**Claim.** Planar lines are contiguous, so bursts span line boundaries and a
240-byte line is never rounded up to 256.

**If it fails.** 6.7% waste on 1080p bitplanes, sixteen slots per line.

**Test.** Implement the straddle and measure.

**Severity.** Minor.

### B8. Sideband ECC keeps the payload

**Claim.** A 40-bit bus of five devices carries the same 6.4 GB/s of data, at the
cost of one device and eight pins.

**If it fails.** The burst becomes 40 bytes and a tick holds four bursts instead
of five — a 20% cut in bursts per tick.

**Test.** MIG with ECC enabled.

**Severity.** Minor, because ECC is optional.

---

## C. Assumed

### C1. The slot clock is 148.5 MHz

**Claim.** One fixed PLL, one tick, 148.5 ÷ 21.

**If it fails.** 59.94 Hz needs 148.35 MHz. That moves the tick to 7.0643 MHz and
every number in these documents by 0.1%, and the tick stops being an exact
division of the *video* clock unless the PLL moves with it.

**Test.** Decide whether 59.94 is supported. If it is, the PLL needs two settings
and the tick follows the slot clock, not a fixed constant.

**Severity.** Major.

### C2. Host throttling is acceptable

**Claim.** At 4K HDR with capture, 18% of the fabric — about 0.8 GB/s — is left
for the host.

**If it fails.** A driver tuned to PCIe ×4 throughput will time out under full
display load, and it will look like a hardware fault.

**Test.** Bulk readback while both outputs and capture are saturated.

**Severity.** Major, and it is a software contract, not a hardware one.

### C3. Planar-first content at 4K

**Claim.** At 4K the background is planar and overlays are partial width, because
a full-width ARGB plane is 175% of a line.

**If it fails.** The hardware is wrong for a compositor-driven desktop. It is not
wrong for video, which is the market.

**Severity.** Major, product.

### C4. The bill of materials

**Claim.** $255 / $540 / $1,200 at Q4 2026 single-unit distributor pricing.

**If it fails.** ±20% is normal. The wedge stops being a wedge at +25%.

**Test.** Three quotes at five and one hundred units.

**Severity.** Major, product.

### C5. The AROS port

**Claim.** Months, and the longest pole in the schedule.

**If it fails.** It is years, and the card has no operating system. No amount of
hardware work fixes that.

**Severity.** **Blocking**, schedule.

### C6. 60 Hz only

**Claim.** The ceilings fix the machine at 60 Hz; the rota is regenerated once per
frame.

**Consequence.** 50 Hz material is converted, not displayed natively, and PAL-era
software timing cannot be reproduced. For a workstation aimed at European
production, that is a real limit.

**Why it is a choice, not a limit.** A 50 Hz mode is a regenerated table, not new
silicon: 1,320 slots per line at 4K50, 2,640 at 1080p50. The cost is validation —
a second schedule to prove — not hardware.

**Test.** Decide whether 50 Hz is in scope. If it is, it doubles the test matrix.

**Severity.** Minor technically, major commercially in PAL markets.

---

## D. What not to bother reporting

These have been considered and rejected; the reasoning is in the documents.

- **"Just use a GPU."** §9 of the design proposition. The point is deterministic
  timing, not throughput.
- **"Use DDR4 or DDR5."** The FPGA family that drives it costs more than the rest
  of the card. Specification card, §6.
- **"Add HDMI 2.1."** A different transceiver class and an FRL protocol this
  design does not implement.
- **"Make the Copper faster."** It is a ruler, not an engine. A faster domain is
  reserved and costs bandwidth, §7 of the slot table.
- **"It is not Amiga-compatible."** Correct, and stated on page one.

---

*Rev. Z · 2 November 2026 · project started 30 October 2026*
