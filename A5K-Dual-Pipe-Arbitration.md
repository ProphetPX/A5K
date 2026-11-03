# Dual-pipe arbitration

**Status: proposal, not measurement.** Arithmetic from clock rates and line
timings. Nothing here has been simulated or built.

This document answers the one question `A5K-Slot-Table.md` left open: **when two
beams share one slot table and one DRAM, who gets which slot, and what is the
worst case?**

It applies to A5K Studio and Studio Pro. A5K (C+) has one beam and needs none of
it; nothing here changes the C+ specification.

---

## 1. What is shared, and what is not

| Resource | Shared | Per beam |
|---|---|---|
| Slot fabric (148.5 MHz) | **yes** | — |
| DRAM and controller | **yes** | — |
| Copper lane (slots) | **yes**, time-multiplexed | — |
| Copper program counter and list | — | **yes** |
| Register file and palette | — | **yes** |
| Line buffers | — | **yes** |
| Tick oscillator (7.0714 MHz) | **yes** | H counter **per beam** |
| Blitter | **yes** | — |

**The register file must be per beam.** Two beams writing one palette is not a
scheduling problem, it is a correctness problem: beam A's raster split would
repaint beam B's screen. A second palette is 256 × 32 bits = 1 KiB, plus a few
hundred control registers — nothing. Duplicating them is what makes the beams
independent; sharing them would need banking and would make ownership the hard
problem instead of bandwidth.

The blitter is deliberately **global**. It writes to memory; both beams read it.
A per-beam blitter would double the logic to halve the usefulness.

## 2. The superframe

Both beams' line lengths are whole numbers of slots. Their reservations therefore
repeat together over

> **S = lcm(N_A, N_B)** slots, where N is slots per line.

| Pair | N_A | N_B | S | Time |
|---|---|---|---|---|
| 4K60 + 1080p60 | 1,100 | 2,200 | **2,200** | **14.8 µs** |
| 4K60 + 4K60 | 1,100 | 1,100 | 1,100 | 7.4 µs |
| 1080p60 + 1080p60 | 2,200 | 2,200 | 2,200 | 14.8 µs |
| 4K60 + 1080p50 | 1,100 | 2,640 | 13,200 | 88.8 µs |

The common case is exact and small: 4K60 and 1080p60 are both 60 Hz, so a 1080p
line is exactly two 4K lines. **The two beams are commensurate by construction**,
which is what makes a static table possible at all.

**Bound: S ≤ 16,384 slots (110 µs).** A mode pair that exceeds it is rejected
with a status bit rather than scheduled badly. Mixed 50/60 pairs fit; most other
mixtures do not.

## 3. Three tiers of claim

### 3.1 The Copper lane

Each beam gets one Copper fetch per its own tick, but the lane is *amortised* to
the slot width:

| Slot width | Instructions per slot | Lane per beam |
|---|---|---|
| 64-bit (C+) | 1 | 1 slot per tick |
| 256-bit (Studio) | 4 | **1 slot per 4 ticks** |
| 512-bit (Pro II) | 8 | 1 slot per 8 ticks |

At 256 bits, two beams consume one slot in 42 — **2.4% of the bus** — and each
still retires one instruction per tick. The lanes are placed at fixed positions
in the superframe and never overlap a burst.

### 3.2 Reserved display

Each beam's worst-case display band is reserved inside its **own** line and
mapped into the superframe, spread evenly. A beam cannot spend another beam's
reservation, and cannot be displaced from its own.

This is the tier that makes the picture provable: a display fetch never
arbitrates, because its slot was assigned before the frame began.

### 3.3 The pool

Everything left. Two masters:

- **Blitter** — floor **10%** of S, at most four consecutive bursts per grant.
- **Host** — floor **5%** of S, bursts of 8 to 256 bytes.

Round-robin at burst granularity. A master that does not use its floor cannot
bank it beyond one superframe, which stops a sleeping master from monopolising
the bus when it wakes.

The table is **generated from registers** — line lengths, plane counts, mode — not
stored per mode. Only overrides are written by software.

## 4. Worst cases, stated as numbers

| Class | Worst case |
|---|---|
| Display | **never waits.** Reserved, and the line buffer covers tRFC |
| Copper | fetch delayed by at most 4 ticks = **565 ns** |
| Blitter, saturated | first grant within **1 superframe** (14.8 µs); sustained ≥ 10% |
| Host, saturated | first grant within **2 superframes** (29.6 µs); sustained ≥ 5% |

These are the numbers a driver may rely on. Anything tighter is a bug; anything
looser is a revision.

## 5. Mode changes

A change of resolution on either beam regenerates the table. It may happen only
at a **frame boundary of the slower beam** — the same rule as the Copper list
swap, for the same reason: a schedule that changes mid-line is not a schedule.

Regeneration cost is at most S clocks, one descriptor per clock:

| Pair | Regeneration | Slower beam's vblank |
|---|---|---|
| 4K60 + 1080p60 | 14.8 µs | 430 µs |
| 4K60 + 1080p50 | 88.8 µs | 800 µs |

Fits with room. The old table keeps running until the new one is complete.

## 6. Not supported, and why

- **Two different pixel-clock standards.** 59.94 Hz needs a 148.35 MHz slot clock
  and 60.00 needs 148.50. One PLL, one standard per configuration. Mixed 59.94
  and 60.00 is refused, not approximated.
- **S > 16,384 slots.** The table stops being generable in a vblank.
- **A per-beam blitter.** See §1.
- **Independent power or colour management per output** in this revision. One
  LUT bank, applied after the beams.

## 7. Tests

1. **Starvation.** Saturate the blitter and host. Assert that neither beam's
   display reservation is ever missed and that no H counter jumps.
2. **Lane.** Assert lane slots never overlap a burst, and that no beam gets more
   than one fetch per four ticks.
3. **Superframe.** At 4K60 + 1080p50 (S = 13,200), assert the pattern repeats
   exactly, that regeneration completes inside vblank, and that the old table is
   used until it does.

## 8. Still open

- Whether mixed 50/60 is worth a 13,200-slot table, or should simply be refused.
- Whether the second Copper can share one register file with ownership bits
  instead of duplicating it. Duplication is simpler and costs 1 KiB; that is the
  recommendation, but it has not been costed in LUTs.
- Whether the Pro II's 512-bit fabric changes the lane amortisation to one in
  eight, which is arithmetic, or needs a different scheduler, which is not.

---

*Proposal, 2 November 2026. Arithmetic, not measurement. The three tests in §7
are the price of calling it a specification.*

---

*Rev. Y · 2 November 2026 · project started 30 October 2026*
