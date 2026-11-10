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
- **No revision without a finding.** A number that changes in a forum reply and
  not in the document is a bug.

---

## Money and hardware

**There is no budget for hardware.** No dev board, no PCB, no parts, no lab time.
The project is a design study in the literal sense — documents, arithmetic and
review — until that changes.

That is not a limitation to apologise for; it decides which questions can be
closed and which cannot:

| Question | Closable with no money? |
|---|---|
| Consistency of the documents | **yes** — reading and arithmetic |
| The slot schedule, Copper, line buffers | **yes** — the simulator, on a laptop |
| Clock synthesis and FPGA fit | **yes** — free vendor toolchain, synthesis report |
| Timing closure at 148.5 MHz | **yes** — same toolchain, utilisation and slack report |
| Real DDR3L behaviour | no — needs a board |
| Audio jitter and THD+N | no — needs a board and an analyser |
| HDMI/DP interoperability | no — needs a board and panels |

Nothing may be called *measured* until a board exists. The point of the table is
that three of the seven can still be **closed by reasoning or by free tools**, and
those are the ones to do next.

**Alternates before a board is ordered.** Every scarce part needs a named second
source — the audio converters first (AKM AK4458 ↔ Cirrus CS4385, AKM AK5720 ↔
Cirrus CS5368), then the USB PHY and the headphone amp. The two converters are
**not pin-compatible**, so the policy is: **dual footprint where the packages
allow it**, so a supply swap is not a respin; where they do not, the alternate is a
documented contingency, not a drop-in.

**Author capability, stated so it cannot be forgotten.** The author is a retired
PC repair technician who writes well — *not* an electronics engineer. Programming
background: **MS BASIC 2.0** (mastered), a little C++ and Perl 5, and **no
Python**. What that gives: debugging by elimination, reading a datasheet for what
it omits, and documentation. What it does **not** give: RTL, timing closure, PCB
layout, EMC, verification, fabrication, or unassisted Python implementation.

**Consequence:** the documents are a specification, not an implementation, and
nothing is measured until a board exists. The review campaign is how the missing
engineer is found. When Python is needed, provide complete scripts and line-by-line
explanation, or pair with an engineer. The author's role is
architect/specifier/publisher, not implementer. The full note is
`ABOUT-THE-AUTHOR.md` in the private folder.

**Scope discipline — the rule that keeps this alive.** Do **not** try to redo every
chip. That is how AAA died: scope, not technology. Pick one block (the Copper),
write one page — what it is, what is heritage, what is stale, what changing it
costs, what it buys, how it is tested — then the next. No block is "improved"
without a number.

**No model is frozen.** The first C+ was frozen too early; Rev 2 stays open until
the author says otherwise, not until a checklist completes.

---

## Next: the review campaign

*Weeks. £0. The cheapest experiment available, and the only one that finds the
class of error self-review cannot.*

**Objective.** Convert paper claims into independently checked claims before
anyone builds from them. Every defect found so far — the tick ratio, the burst
model, the bandwidth limit — was found by self-review. That source is now
exhausted: a sixth pass will find the sixth thing already believed.

### Artefacts to publish

| # | Artefact | Why |
|---|---|---|
| 1 | Repository URL | the whole thing, citable |
| 2 | `A5K-Design-Proposition.pdf` | the argument, 19 pages |
| 3 | `A5K-Slot-Table.md` | the timing contract |
| 4 | `A5K-Frailties.md` | **what to attack**, so reviewers start where it matters |

### Channels, and what each is for

| Channel | Audience | Ask them about | Expect |
|---|---|---|---|
| r/FPGA | FPGA engineers | closure, MIG, BRAM, CDC | the most useful replies |
| r/hardware | general hardware | concept, BOM, thermals | mixed |
| EEVblog forum | board-level engineers | DDR3L layout, power, EMC | slow, high quality |
| Hacker News (Show HN) | technical generalists | the idea | volume; "just use a GPU" |
| Amiga forums (EAB, amigaworld) | domain experts | Copper semantics, planar model | "not compatible" and one good correction |
| Xilinx forums | vendor-specific | 7-series memory and timing | narrow, authoritative |

Read each channel's self-promotion rules first. One post per channel, not a
cross-posted blast.

### The post

150 words, one block diagram, one question, one link. Not *"what do you think"* —
that invites opinion. *"Does 256-bit close at 148.5 MHz on a -2 325T?"* invites an
answer.

### The five questions

1. Does 256-bit at 148.5 MHz close on a Kintex-7 325T **-2**?
2. Is a 32-byte burst quantum with `tick = 5 bursts + 1 Copper slot` a sane way
   to schedule DDR3L?
3. Does 4K60 CEA-861 leave enough blanking for two 350 ns refreshes?
4. Is tRFC 260 ns or 350 ns for the 4 Gb parts in the BOM?
5. Is one Copper slot in twenty-one enough for deterministic WAIT retirement?

### Triage — classify before answering

| Class | Test | Action |
|---|---|---|
| **A. Factual defect** | cites a number, a datasheet or a standard | opens a finding with an ID; may open a revision |
| **B. Design preference** | "I would have…" | record in DECLINED with a reason; do not argue |
| **C. Misreading** | answers a different design | one clarifying reply, then stop |
| **D. Noise** | no content | ignore |

A class-A finding is not a defeat; it is the document doing its job. The register
in `A5K-Frailties.md` exists so that reviewers spend their time on A, not C.

### Cadence

- Publish once, then wait **72 hours** before revising anything.
- **One revision per week**, maximum. Batch findings.
- Never argue in a thread. Record, answer once, move on.
- Every revision names the finding IDs it answers.

### Exit criteria

The campaign is over when either:

- three independent reviewers have responded and none produced a class-A defect;
- or thirty days pass with no class-A defect.

Then tag the result and stop revising until hardware exists.

### Open findings, awaiting a revision

Findings are logged here and batched into the next revision — not fixed on the
day they arrive, per the cadence rule above.

| ID | Finding | Consequence | Status |
|---|---|---|---|
| **F-01** | The target monitor advertises **50.00, 59.94 and 60.00 Hz**; the ceilings fixed 60.000 only. | Resolved in Rev. AV: video rates on two slot clocks, high refresh to 1080p240, VRR out. | Closed in Rev. AV |
| **F-02** | B1 cannot be tested on a 1080p panel. | Withdrawn: the card is the source, HDMI 2.0 4K60 *is* CEA-861, and the generator takes line length as a register. No 4K panel is required to close it. | Withdrawn |
| **F-03** | B1 closed by labelling the 4K example as CEA rather than the definition. | Applied in Rev. AV: §4.2 and §5.5 say CEA-861; CVT-RB is another row in the same generator. | Closed in Rev. AV |
| **F-04** | Mode floor, first power-on default and recovery policy were undefined. | Applied in Rev. Z: 640×480 floor, 1024×768 default, four recovery routes. | Closed in Rev. Z |
| **F-05** | The reference BOM fits a stereo DAC (PCM5102) but lists **no audio connector**. | Resolved in Rev. AV: 8-channel DAC, four jacks, TOSLINK, two audio clocks; C+ Rev 2 replaces C+. | Closed in Rev. AV |
| **F-06** | UAC2 host: open stacks are thin and the Studio's 160T has less room than the Pro's 325T. | **Decided:** C+ never. **Studio carries the complete UAC2 circuit** (PHY, connector and fabric logic) but **ships firmware-disabled** until the host controller fits beside both beams and a board measures it. **Pro and Pro II carry it enabled.** Scope: one interface, playback and capture, no hubs or HID. Enabling on Studio is a firmware update, not a board change. | Open — hardware fitted; Studio dark |
| **F-07** | The 48 kHz family is fitted but unmeasured. It is a **documentation claim**, not a hardware fault — the ID is only a label. | **Decided:** both crystals on the board; 44.1 is the default; the documents say "48 kHz is fitted and not yet measured". Closed by that sentence now, and reopened only when a board can measure it. The clock synthesis itself can be checked in the free toolchain. | Documented; measurement deferred |
| **F-08** | The 68k soft core was discussed, then cut in conversation, and **the cut was never recorded** — at the time, the main study still listed it and five documents still said "no 68K". | **Decided:** an open-core 68k block is **reserved on every model**, as the CPU half of a future legacy stack; it is **not** being built, and **no Amiga compatibility is shipped or claimed**. The public sentences were reconciled in Rev. AW. | Documented; deferred |
| **F-09** | The specification card says *"More host bandwidth means Gen3 or Gen4, which means an Artix-7 with GTP or a larger part."* Artix-7 GTP is Gen2 (6.6 Gb/s); Gen3/Gen4 needs GTH/GTY, i.e. an UltraScale-class part. | The sentence is a factual error about the part class. Correct it in the next revision: Gen3/Gen4 means a different transceiver class and a different board, not a bigger 7-series part. The FPGA-per-model table is unaffected. | Open — found in the 4 Nov audit; batch it |

**External review to seek.** Dave Haynie's critique of a similar proposal is
recorded in the private memo (Rev. 25). One narrow question to him is still worth
asking — not a document review, one question with one number; drafts are in the
private folder. Record any answer verbatim, with its date, and treat it as
outweighing the author's opinion.

### After the campaign

Write one page: **what the reviewers found**. It is the only credible evidence
that the design was tested, and it is worth more than another appendix. Link it
from the README.

### Campaign log

One row per channel. Classify every reply before answering: **A** factual defect,
**B** preference, **C** misreading, **D** noise. Only class A opens a revision.

| # | Channel | Posted | Post | Replies | Class-A | Status |
|---|---|---|---|---|---|---|
| 1 | r/FPGA | 4 Nov 2026 | [post](https://www.reddit.com/r/FPGA/comments/1xo9dak/does_256bit_at_1485_mhz_close_on_a_kintex7_325t_2/) | 13 (nixiebunny, alexforencich ×3, tux2603 ×3, OnYaBikeMike ×4, FVjake ×1, gerhardt_von_goll ×1) | none (13 method notes) | posted — 72 h closed; triage continuing |
| 2 | EEVblog forum | — | — | — | — | not posted |
| 3 | Xilinx forums | — | — | — | — | not posted |
| 4 | r/hardware | — | — | — | — | not posted |
| 5 | Hacker News | — | — | — | — | not posted |
| 6 | Amiga forums (EAB, amigaworld) | — | — | — | — | not posted |

**Reach (10 Nov 2026):** the r/FPGA post has ~**7,400 views** and **13 recorded replies**; no class-A findings yet. Views are reach, not review — the exit criteria still depend on independent technical responses, not traffic.

**Thread access:** [old.reddit view](https://old.reddit.com/r/FPGA/comments/1xo9dak/does_256bit_at_1485_mhz_close_on_a_kintex7_325t_2/) · [short link](https://redd.it/1xo9dak) · [RSS feed](https://www.reddit.com/r/FPGA/comments/1xo9dak.rss). The RSS feed is the reliable machine-readable fallback when the HTML page is blocked.

**Reply notes** (classify before answering):

- **4 Nov — *nixiebunny*:** implementation-dependent; a large Virtex-7 design closed at 320 MHz. Not a defect — recorded as a data point under **B3**. It supports "148.5 MHz is not aggressive as a clock" but not "256-bit closes on a Kintex-7 −2 with the MIG"; different family, width and placement. Reply sent: asked for the widest register-to-register path and whether the memory controller shared the clock domain.
- **4 Nov — *alexforencich*:** the question is underspecified — width alone does not determine closure; logic depth, fan-out and placement do. Correct, and it is a criticism of **how the post asked**, not of the document (B3 already specifies place-and-route with the MIG). Two reviewers independently made the same point: treat as a **consensus concern about the question**, not a design defect. Reply drafted: define the 256-bit datapath precisely and ask which element is the likely limiter. No Frailties edit during the 72-hour window.
- **4 Nov — *alexforencich* (second reply):** routing congestion on a wide bus is a real risk, distinct from logic depth; the "AI generates everything" premise is wrong — there is no RTL, and AI assisted the documents. Class **C** (misreading) with a technical kernel. Congestion/placement logged as a **B3 review concern** (consensus with nixiebunny's "spread out"). One correction, then stop.
- **4 Nov — *tux2603*:** pipeline depth vs latency. Technical kernel: a **fixed** number of stages is absorbed by the line buffers; **variable** latency is what the slot table removes. Second-order point: the buffer floor should be **tRFC + pipeline latency**, not tRFC alone — logged as a **B5 note**. The "throwing Claude at a wall" clause is a preference, not a claim; no response. Reply drafted: state the fixed-latency argument and ask whether he would pipeline at the slot boundary.
- **4 Nov — *OnYaBikeMike*:** variable off-chip memory latency and read/write contention are missing from the question. Correct about the **post**; the design covers them in §4.3 (row misses, refresh in blanking, batched turnarounds, 6% budget) and in **B4/B5**, and the simulator is meant to test them. Class **B** with a technical kernel. The second clause — "expertise taken and sold back" — is a labour opinion; answer once with the fact that nothing is for sale, do not argue. **Third reviewer to call the question under-specified: consensus.**
- **4 Nov — *tux2603* (second reply):** don't pre-plan pipeline stages; run the math, synthesise, look at the critical path, then decide. **Method endorsement** of the project's own "fit before claims" plan. No defect; no design change.
- **4 Nov — *OnYaBikeMike* (second reply):** suggests absorbing latency in a **"gojong structure"**. Term unknown — likely a typo or a structure not in the literature we have. Reply asks for clarification and compares it to the line-buffer FIFO. Do not bluff it.
- **10 Nov — *FVjake*:** *"Gojong structures are the obvious choice here. They will definitely minimize the impact of the copper lanes interleaving latencies."* Class **B/C** — no definition, citation, mechanism, or number. The term remains unresolved; "obvious choice" is not a finding. Action: one clarifying reply asking for a reference/definition and the mechanism by which it reduces Copper-lane interleaving latency. Do not adopt it or edit `A5K-Slot-Table.md`. If a citation or number follows, reclassify as **A**.
- **10 Nov — *tux2603* (third reply):** *"Like I said, if you know what you're doing and are willing to break down wide operations into multiple steps (even something as 'simple' as 256-bit addition could easily eat up half of your setup time), it will probably close. If you have no experience with FPGAs and HDL, then good luck."* Class **B** with a technical kernel: wide operations must be pipelined/decomposed, and setup time is the real limiter. It is a conditional opinion, not a number or a cited defect; "good luck" is tone, not a claim. Reinforces the existing consensus that the original question was under-specified. No reply needed; record and close.
- **10 Nov — *gerhardt_von_goll*:** *"I did a lot of design work for optical sensor systems. My approach was always to buffer image lines in block memory before transfer to off-chip DRAM. The block RAM line buffers mitigate the DDR latency. This works whether you are receiving or generating the image data."* Class **B** with a strong technical kernel: independently corroborates the existing line-buffer rule (§4.3 / B5) — absorb variable DDR latency in BRAM line buffers instead of exposing it to the pixel path. No number or citation, so not a class-A finding. No design change; record as external corroboration. One brief acknowledgement is enough.
- **10 Nov — *OnYaBikeMike* (third reply):** *"I don't want any money from you, But your repo and your posts are all AI-genersted text. ... Whenever somebody suggests something, you seem to be well informed on the topic you know nothing about a few seconds ago. There is no 'give' in such. interactions, only take. You are just burning the goodwill of others here."* Class **D** — no technical claim, number, datasheet, or standard; a labour/community objection to AI-assisted writing. The "all AI-generated" premise is a misreading of the repo (documents and build scripts are authored; AI assisted). Record, do not argue. Author sent one defensive reply; **no further response**. Do not delete the reply; let the thread close.
- **10 Nov — *OnYaBikeMike* (fourth reply):** long line-by-line critique. Class **C** overall, with useful **B** kernels: the post assumed Amiga/Copper knowledge and did not explain the slot table, reads, or where 4.75/12.8 GB/s came from. His "over two million cycles to assign every frame" is a misreading — the schedule is a hardware rota per line, not a per-frame software assignment of every bus cycle; only a mode change rewrites it. "Google doesn't know Copper" is false in the Amiga context, but the point that a non-Amiga reader needs a definition is valid. The closing "nothing of value / learn to help themselves" is **D** opinion. Action: no argument; treat it as a **writing finding** — write a one-page plain-language brief for engineers outside the Amiga world. No design change; no class-A.
- **4 Nov — *alexforencich* (third comment):** *"Why are you pasting AI responses here? Just have Claude do everything for you. Don't forget to tell it to make no mistakes."* **Class D** — no technical content; pure bait. **Do not reply.**

**Documentation gap the thread is pointing at:** there is no explicit **latency and contention** section (off-chip variable latency, read/write turnaround, fetch → FIFO → scanout → pixel). Three reviewers have now asked for it in different words. Add one after the 72-hour window; it belongs next to the line-buffer rule in `A5K-Slot-Table.md` §4.3.

**Checking the thread (daily, until 8 November 2026):**

- A **number** — a slack figure, clock rate, LUT count, datasheet page — → send it;
  it is a **class A** finding.
- A **repeat** of the same objection → **consensus**, not noise; note it even without
  a citation.
- A **hostile reply with no technical claim** → **class D**; ignore it.
- A **hostile reply with a specific claim** → **class A** if it cites a number,
  otherwise **class C**; one reply, then stop.
- Do not edit the post, do not revise the documents, and do not start the next
  channel before the window closes.

**Cadence.** 72 hours between posting and revising; one revision per week; never
argue in a thread; every revision names the finding IDs it answers.

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
- [x] ~~64, 128 or 256-bit slots?~~ — 64 on C+, 256 on Studio, 512 for the Pro II
- [x] ~~Memory width?~~ — **32-bit (2 × 16-bit) on C+, 64-bit (4 × 16-bit) on
      Studio and Pro**. The fabric is the binding limit; the DRAM runs at 19% /
      43% / 86% of capacity, so the next model doubles the slots, not the memory
- [x] ~~What may the second output be?~~ — video, a derived crop/scale/LUT, or
      independent graphics to 1080p. Two independent 4K HDR graphics rasters need
      512 bits (§5.3 of the family document)
- [x] ~~Is the ISO second channel needed?~~ — **withdrawn**; it moved the same
      12.8 GB/s into two controllers, buying isolation rather than capacity
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
- [x] ~~Re-run the 4K and two-beam checks~~ — §4.4: the Pro as shipped is 82% of
      the fabric; two independent 4K graphics rasters are 98% and need 512 bits
- [x] ~~Five acceptance tests~~ — §6
- [x] ~~Specify dual-pipe arbitration~~ — **done**: `A5K-Dual-Pipe-Arbitration.md`
      (superframe, three tiers, starvation bounds)
- [ ] Decide when the **Pro II** (512-bit) ships — same board, -3 speed grade

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

1. Run the review campaign — r/FPGA first; triage replies by class and log findings.
2. Build the simulator, **M1**: clock, modes, beam and scheduler; pass test T1.
3. Decide the HDL language.

## Open questions

- Which board is actually in budget and in stock?
- Is 640 × 512 enough for a first light, or should the first mode be 1080p?
- Does the simulator need a debugger view (registers, beam position, slot trace)?
- Who writes the AROS HIDD — the author, or a contributor under CLA?

---

*Design study. Nothing here is built, and nothing here is a promise. See
`TECHNICAL-CONSIDERATIONS.md` for what exists and `LEGAL.md` for the notices.*

---

*Rev. AW (B49) · 4 November 2026 · project started 30 October 2026*
