# The simulator specification

**Phase 0 of `TODO.md`. Status: proposal, to be written before any code.**

This document defines the behavioural model that must exist before any RTL, and
the five tests it has to pass. It targets **A5K (C+) only** — the frozen reference
model — so that the target cannot move while the model is being written.

> The simulator is the golden model. If it and the paper disagree, the paper is
> wrong until proven otherwise.

---

## 1. What it is

A **slot-accurate, deterministic, event-driven model** of the C+ machine: the slot
scheduler, the DDR3L memory behind it, the display pipeline that drains it, and the
Copper that rides on top.

| | |
|---|---|
| **Granularity** | one slot (6.734 ns). No sub-slot events, no floating-point time |
| **Determinism** | same inputs, same trace, bit for bit, on any machine |
| **Language** | Python 3, standard library only |
| **Wall clock** | never consulted. A run takes as long as it takes |
| **Purpose** | prove the schedule, then serve as the reference for RTL |

## 2. What it is not

- **Not gate-level, not cycle-accurate silicon.** It models the *contract*, not
  the implementation.
- **Not an HDMI or DisplayPort model.** It produces pixels; it does not encode
  them.
- **Not a PCIe model.** The host is a traffic generator with a bandwidth budget.
- **Not a blitter.** The blitter is a slot consumer with a size, not a pixel ALU.
  Its correctness is a separate problem.

## 3. The clock, and why everything is integers

There is exactly one unit: the slot. Time is an integer count of slots.

| Quantity | Value |
|---|---|
| Slot | 1 unit = 6.734 ns |
| Tick | 21 units |
| Burst | 4 units (32 bytes) |
| Refresh interval | 1,158 units (7.8 µs) |
| Refresh duration | 52 units (350 ns) |

Modes arrive as integers, not as frequencies:

| Mode | Slots/line | Lines/frame | Tick positions |
|---|---|---|---|
| 640×480 @ 60 | 4,720 | 525 | 225 |
| 1024×768 @ 60 | 3,071 | 806 | 147 |
| 1080p60 | 2,200 | 1,125 | 105 |
| 4K60 | 1,100 | 2,250 | 53 |

No number in this table may be hard-coded in the model. They come from the mode
file, because the same table must hold CVT-RB, 1080p240 and the /1.001 rates
without a code change.

## 4. The objects

| Object | What it owns | What it must never do |
|---|---|---|
| **Scheduler** | the rota for one line: who owns each slot | invent a slot, or let two owners hold one |
| **Memory** | bursts, rows, latency, refresh | complete a burst in the slot it was requested |
| **Display** | one FIFO per stream, and the drain rate | read memory directly; it reads its FIFO |
| **Copper** | fetch, decode, retire, WAIT | retire two instructions in one tick |
| **Blitter** | a slot budget and a size | borrow from the display band |
| **Host** | a slot budget and a burst cap | exceed its window |
| **Beam** | line and tick position | move while the line is stalled — there is no stall |

Each object exposes a step function called once per slot, in a fixed order:
`scheduler → memory → display → copper → beam`. Fixed order is what makes the
trace reproducible.

## 5. Memory model

The only part that matters for the tests:

- A request is **one 32-byte burst**, never smaller, never unaligned.
- Latency from grant to the last byte: **2 slots** on a row hit, **6 slots** on a
  row miss. Counted from the grant, not from the request.
- **Refresh** blocks the whole bus for 52 slots every 1,158, always starting on a
  burst boundary. It may not be moved to suit a stream; the streams must cover it.
- **Turnaround**: a direction change costs 2 slots. Eight bursts in one direction
  before turning.
- **ECC off.** If enabled, the burst becomes 40 bytes and the test for
  "no transaction smaller than 32 bytes" becomes 40.

The memory is intentionally crude — a queue, a bank/row table and a timer. Its job
is to be *pessimistic and repeatable*, not to model a MIG.

## 6. Scheduler model

The rota is generated from registers exactly as §4.6 of the slot table describes:

1. **Copper lane** — slot 0 of every tick.
2. **Display reservations** — per stream, spread across the line.
3. **Pool** — blitter floor 10%, host floor 5%, round-robin at burst granularity,
   maximum four consecutive bursts per master.

The scheduler must be able to answer, for any slot: *who owns it, and why*. That
"why" goes into the trace.

## 7. Copper model

MC-1 only: MOVE, WAIT, SKIP, JUMP, CALL, RET, END, IRQ.

- One instruction fetched and retired per tick, from the lane.
- WAIT compares `(V << 12) | H`, where **H is a tick position**, not a dot.
- The fetched instruction is available *before* the tick in which it retires, so
  the lane can be lent when the Copper is idle.
- END re-arms from COP2LC and raises VBlank.

## 8. Display model

Per stream: a FIFO sized by the rule in §4.3 of the slot table (tRFC of its own
pixels), refilled in bursts, drained at the mode's pixel rate expressed in slots.

Miss policy, and it is a test:

- A fetch that misses its slot **holds the last pixel**. The beam does not stall.
- A miss counter increments.
- Three consecutive misses raise the fault interrupt.

## 9. Inputs

| Input | Format |
|---|---|
| Mode | name, slots/line, lines/frame, pixel rate as a rational |
| Rota | generated, not supplied — but overridable for negative tests |
| Copper list | text assembler (the syntax in Appendix A) or binary |
| Scene | plane base pointers, widths, formats, one overlay rectangle |
| Load | blitter bytes/frame, host bytes/frame, capture on/off |
| Length | frames |

## 10. Outputs

| Output | Why |
|---|---|
| `trace.csv` | one row per slot: owner, request, FIFO level, line, tick |
| `lines.csv` | one row per line: slots per owner, misses, underruns |
| `frame_%04d.ppm` | the actual picture, so a wrong pixel is visible |
| `report.json` | counters, first failure, timings |

The trace is the primary artefact. A disagreement with the paper should be a diff
of two CSVs, not a discussion.

## 11. The five tests

These are §6 of the slot table, made executable.

### T1 — tick ratio
Run 1,000 lines at 1080p. Assert **105 tick positions per line**, H never exceeds
104, and the tick count at line 1,000 is exactly **105,000**.

### T2 — refresh never starves the beam
Force refresh to start at its worst phase (first slot of blanking) at 4K60. Run
10,000 frames. Assert **zero FIFO underruns** on every stream and a measured
refresh duty of 4.5 ± 0.1%.

### T3 — Copper determinism under load
Saturate the blitter and the host. Assert a WAIT at *(line 500, tick 40)* retires
at the **same slot index on all 1,000 frames**, and that no fetch waits more than
one tick.

### T4 — miss behaviour
Inject five lines of induced misses on one plane. Assert the line time varies by
**less than 0.01%**, the last pixel repeats rather than the beam stalling, the miss
counter increments, and the fault interrupt fires on the third consecutive miss.

### T5 — budget conformance
Load the §5.4 worked example. Measure slots per owner per line. Assert every
figure is within **1%** of the table, and that no transaction smaller than 32
bytes, or crossing a 32-byte boundary, ever reaches memory.

### T6 — the tests have teeth
Deliberately break the model three ways — remove the Copper lane, remove the
refresh, let the blitter take a display slot — and assert T1, T2 and T5 **fail**.
A test suite that cannot fail is a decoration.

## 12. What a failure means

| Failure | Reading |
|---|---|
| T1 | the tick rule is wrong, or the line table is |
| T2 | a buffer is too small, or refresh is misplaced |
| T3 | the Copper lane is not exclusive |
| T4 | the miss policy stalls the beam somewhere |
| T5 | the paper's budget is optimistic |
| T6 | the tests are not testing |

In every case the **model wins**, and the paper is revised with a finding ID.

## 13. Structure

```
sim/
  a5k/
    clock.py        slot counter, tick derivation
    modes.py        the mode table, CVT-RB and /1.001 included
    memory.py       bursts, rows, refresh, turnaround
    scheduler.py    rota generation and grants
    copper.py       MC-1 assembler and interpreter
    display.py      FIFOs, drain, miss policy
    beam.py         line and tick position
    trace.py        CSV writers, PPM writer
  tests/
    t1_tick.py … t6_teeth.py
  run.py            one run, one report
  README.md         how to run, and what the numbers should be
```

Every module maps one-to-one onto a future Migen module. No base classes, no
dependency injection, no cleverness: the point is that an RTL engineer can read it
and disagree.

## 14. Milestones

| | Deliverable | Proves |
|---|---|---|
| **M1** | clock, modes, beam, scheduler | T1 |
| **M2** | memory and display FIFOs | T2, most of T5 |
| **M3** | Copper | T3 |
| **M4** | miss injection and faults | T4 |
| **M5** | negative tests, CI | T6, regression for everything |

M1 is a week. If it is not, the specification is not understood well enough to
build the rest.

## 15. What would make this a failure

- Hard-coding 1,100 or 2,200 instead of reading the mode table.
- Using floats for time, so two runs disagree in the last digit.
- Modelling the MIG instead of the contract.
- Passing T1–T5 by construction — testing the model against itself.
- Never running T6.

---

*Rev. AI · 3 November 2026 · project started 30 October 2026*
