# TODO — from paper to hardware

A working plan for turning the A5K design into something that runs. Ordered by
cost of being wrong: the cheapest experiments come first, the irreversible ones
last.

**Current state:** design study, no HDL, no board, no driver. Everything below
is unstarted.

---

## Ground rules

- **Do not start with a PCB.** A board locks in decisions that haven't been
  tested, and a respin costs more than every dev board combined.
- **Do not ship a Kickstart ROM.** Ever. AROS needs none.
- **Do not put "Amiga" on a silkscreen, a box, or a store page.** Describe;
  don't brand. See `TRADEMARKS.md`.
- **Do not chase an ASIC.** Gate arrays and shuttle runs are for projects with
  a market, not a proposition.
- **Do not port AROS before the driver works.** It depends on phases 3–5.

---

## Phase 0 — Behavioural simulator

*Weeks. £0. Proves the specification before it becomes RTL.*

- [ ] Write the simulator specification: the exact register subset, the frame
      loop, the Copper interpreter, the plane compositor, acceptance tests
- [ ] Implement the beam counter at 7.0714 MHz (148.5 ÷ 21)
- [ ] Implement the MC-1 Copper: MOVE / WAIT / SKIP / JUMP / CALL / RET / END / IRQ
- [ ] Implement planar fetch from a slot table
- [ ] Implement the plane merge, priority and palette
- [ ] Implement the blitter: minterms, shifts, line draw
- [ ] Render to a window (SDL or similar)
- [ ] Capture reference frames for the RTL testbench

**Done when:** a raster split renders at the correct scanline, and a plane
moves under Copper control.

---

## Phase 1 — RTL and simulation

*Weeks. £0. Finds the timing bugs while they are still free.*

- [ ] Choose the HDL approach (Migen/LiteX, or plain Verilog)
- [ ] Agnus: slot table, beam counter, DMA arbitration
- [ ] Denise: planar fetch, planes, priority, palette
- [ ] Blitter: minterm ALU, line draw
- [ ] Copper: microsequencer per Appendix A
- [ ] Paula: audio DMA (SD card and UART can wait)
- [ ] Register file and bus decode
- [ ] Verilator testbench comparing against the Phase 0 frames

**Done when:** the RTL and the simulator produce identical frames for a set of
Copper lists.

---

## Phase 2 — First dev board

*Weeks to months. $150–400. No custom hardware yet.*

- [ ] Pick a board: **Artix-7 100T for C+** (4 GTP); an ECP5 board only for a
      1080p variant
- [ ] Bring up DDR
- [ ] Bring up one video mode: 640 × 512 planar, DVI or HDMI out
- [ ] Run a Copper list from DDR
- [ ] Blit into the visible buffer
- [ ] Measure the slot table against the theoretical schedule

**Done when:** a stable picture, generated entirely by the chipset, with no CPU
touching the framebuffer after setup.

---

## Phase 3 — PCIe path

*Months. $300–800. Proves the host interface.*

- [ ] Bring up the PCIe endpoint (x1 first)
- [ ] Implement BAR0: register window
- [ ] Implement BAR2: Chip RAM aperture (64-bit prefetchable if possible)
- [ ] Implement bus-master DMA to host memory
- [ ] Add MSI-X interrupts
- [ ] Write a smoke-test tool: poke Copper registers, read back frames

**Done when:** a host process can upload a Copper list over PCIe and read the
resulting frame back out of Chip RAM.

---

## Phase 4 — Driver

*Months. £0. The first genuinely useful software.*

- [ ] Linux DRM/KMS driver: modeset, one plane, vblank
- [ ] Expose the beam-synchronous fence
- [ ] Optionally: AROS HIDD for graphics
- [ ] Document the ioctl surface

**Done when:** a standard Linux desktop can appear on the card's HDMI output.

---

## Phase 5 — Custom PCB

*Weeks of layout + one build. ~$200–400 for five.*

- [ ] Schematic capture from the validated design
- [ ] 4-layer layout, low-profile PCIe or M.2 2280
- [ ] Power tree, decoupling, ESD
- [ ] Bring-up plan and test points
- [ ] Order five; expect one to work
- [ ] EMC pre-check if it will ever be sold

**Done when:** the board enumerates, displays, and survives a soak test.

---

## Phase 6 — AROS

*Months. £0. Depends on 3–5.*

- [ ] Platform layer: timers, interrupts, memory map
- [ ] Graphics HIDD
- [ ] Boot monitor or firmware payload loader
- [ ] Boot AROS from SD
- [ ] Fix what breaks

**Done when:** AROS reaches a desktop on real hardware, drawn by the chipset.

---

## Slot table — remaining work

`A5K-Slot-Table.md` is now a specification in structure and a proposal in its
numbers. Every timing question except dual-pipe arbitration is closed.

- [x] ~~C+ captures at all?~~ — **no capture** (Rev. S)
- [x] ~~Capture format?~~ — 10-bit ARGB2101010; 4:2:2 on Studio, 4:4:4 on Pro
- [x] ~~64, 128 or 256-bit slots?~~ — 64 on C+, 256 on Studio
- [x] ~~Tick rate and its ratio to the slot clock?~~ — 7.0714 MHz = 148.5 ÷ 21
- [x] ~~Reserve a faster tick domain?~~ — reserved, not built (`BEAMCON0[3:1]`)
- [x] ~~Burst model, latency and line buffers?~~ — §4.3: 32-byte quantum, tick =
      5 bursts + 1 Copper slot, buffer = tRFC of the stream's own pixels
- [x] ~~Refresh, ECC and turnarounds as line items?~~ — §4.3: 4.5% + 6% + 3%,
      86.5% usable; ECC costs a device and eight pins, not 25% of bandwidth
- [x] ~~Does the blitter window scale with frame rate?~~ — no; fraction of the
      line, floor 10%
- [x] ~~Do Copper fetches get their own band?~~ — a lane, slot 0 of every tick
- [x] ~~What happens on a missed display fetch?~~ — hold the pixel, never stall;
      fault after three consecutive misses
- [x] ~~Per-line schedule at 1080p60~~ — §5.5
- [x] ~~Re-run the 4K and two-beam checks on usable bandwidth~~ — §4.4: the Pro as
      shipped is 87%; two 4:4:4 beams are 102% and need the ISO's second channel
- [x] ~~Five acceptance tests~~ — §6
- [ ] Specify **dual-pipe arbitration** for Studio and Studio Pro

---

## Legal position, by artefact

| Artefact | Whose | Licence / obligation |
|---|---|---|
| HDL, constraints, testbenches | Yours | CERN-OHL-S v2 — publish complete source on distribution |
| PCB, schematic, Gerbers | Yours | CERN-OHL-S v2 |
| Drivers, simulator, tools | Yours | MIT (or GPL if you prefer) |
| Documents | Yours | CC BY 4.0 |
| FPGA vendor IP (PCIe block, DDR controller) | Vendor | Used under the tool licence; the bitstream is yours |
| A board you sell | Yours | Seller liability, EMC, insurance — see `LEGAL.md` |

**Contribution rule:** a CLA or DCO before accepting outside code, or the
option to dual-license disappears.

---

## The emulator question

Yes — and it is the best next artefact, because it doubles as the golden model
for Phase 1.

| Approach | What it is | Licence shape |
|---|---|---|
| **Own simulator (recommended)** | Your chipset, your semantics, no ROMs | MIT or GPL — your choice |
| **Fork UAE / FS-UAE** | Full Amiga emulation | GPLv2+; the fork stays GPL; needs a Kickstart or the AROS ROM |
| **Copper playground** | Type a list, watch the beam draw it | MIT; small and teachable |

Name it **A5K Simulator**, never "Amiga emulator".

**Done when:** a user can type a Copper list and see the raster split appear at
the right line.

---

## Immediate next actions

1. Close the remaining slot-table decisions (three open questions, per-line
   schedule, capture band, dual-pipe arbitration, acceptance tests).
2. Write the simulator specification — register subset, frame loop, acceptance
   tests — now that C+ has no capture and the Studio models are 256-bit.
3. Decide the HDL language and the first dev board (Artix-7 100T).

## Open questions

- Which board is actually in budget and in stock?
- Is 640 × 512 enough for a first light, or should the first mode be 1080p?
- Does the simulator need a debugger view (registers, beam position, slot trace)?
- Who writes the AROS HIDD — the author, or a contributor under CLA?

---

*Design study. Nothing here is built, and nothing here is a promise. See
`TECHNICAL-CONSIDERATIONS.md` for what exists and `LEGAL.md` for the notices.*

---

*Rev. U · 2 November 2026 · project started 30 October 2026*
