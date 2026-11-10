# Resuming this project

**Model-agnostic handover.** If you are a new assistant, a new collaborator, or the
same author months later, read this first. It exists because the AI session is
rented and the repository is not.

---

## State, at Rev. AW (B49), documentation through 10 November 2026

| | |
|---|---|
| Revision | **AW** (B49), tagged `rev-aw` |
| Documents | 19-page study, 4-page addendum, 6-page specification card, plus the markdown set |
| Later documents | `A5K-Brief.md`, `A5K-AROS-68K-Plan.md`, `A5K-Bus-Technology.md`, `A5K-Market-Signals.md` — documentation, not a revision |
| Design changes since AW | **none** — no number, constraint, part or rule has moved |
| Latest commit | `trunk` — see `git log -1`; documentation through 10 November 2026 |
| Hardware | **none.** No RTL, no board, no measurement |
| Frozen models | **none** — frozen by author decision only |
| Public repo | `github.com/ProphetPX/A5K`, branch `trunk` |
| Private folder | `~/Documents/A5K_Project_PRIVATE` — **not in git** |

## Read these first, in this order

1. `RESUME.md` — this file.
2. `TODO.md` — the live task list, the review campaign, and the open findings.
3. `A5K-Frailties.md` — what is weak, with identifiers (A1, B1, C11…).
4. `A5K-Brief.md` — the plain-language version, for engineers outside the Amiga world.
5. `A5K-Lineage.md` — AAA in its own words, Lorraine, and the camps that exist today.
6. `A5K-Slot-Table.md` — the timing contract.
7. `A5K-Family.md` — the product line.
8. `A5K-AROS-68K-Plan.md` — what is and is not being promised about AROS and 68k.
9. `A5K-Market-Signals.md` — informal feedback and the small-batch product shape.
10. `A5K-Bus-Technology.md` — bus reference; why the internal fabric, not PCIe, is the limit.

## Where the truth lives

- **The documents are the specification.** Every "the card does X" means "the
  design requires X". Nothing has been built.
- **The private folder holds** the legal memo, the conversation archive, the ad
  copy, the historical research, the author's capability note, and the questions
  drafted for Dave Haynie.
- **The conversation is disposable; the repo is not.** Anything that mattered was
  written into a file.

## How to rebuild the PDFs

```sh
cd ~/Documents/A5K_Project
python3 build_proposition.py     # 19 pp
python3 build_specifications.py  # 6 pp
python3 build_addendum.py        # 4 pp
```

Requires `chromium` and `pymupdf`. The scripts create their own temporary
directories and do not depend on any session.

Refresh the private archive with:

```sh
cd ~/Documents/A5K_Project_PRIVATE
python3 export_conversation.py   # CONVERSATION*.{txt,md}, raw jsonl
python3 build_legal_notes.py     # the memo
```

## The rules that must survive the handover

1. **Revision letters:** A–Z, then AA–AZ, BA–BZ (ASME Y14.35). Every revision is
   tagged. Housekeeping — README, TODO, changelog, formatting — does **not** bump.
2. **No revision without a finding.** A number that changes in a chat and not in a
   document is a bug. Log it in `TODO.md`, then batch it.
3. **Nothing is measured.** Do not write "supports", "achieves" or "measured"
   without a test. "Fitted, not yet measured" is the honest form.
4. **No compatibility obligation.** No Kickstart, no Amiga branding, and no
   compatibility claim. A 68k legacy core is **reserved on every model but not
   built**; the card remains CPU-agnostic and OS-agnostic.
5. **One block at a time.** Do not "redo every chip". AAA died of scope.
6. **The model wins.** If the simulator and the paper disagree, the paper is wrong
   until proven otherwise.

## Author capability — do not over-assign

The author is a retired PC repair technician, not an electronics engineer.
Programming background: **MS BASIC 2.0** (mastered), a little C++ and Perl 5,
and **no Python**. Strengths: specification, documentation, debugging by
elimination, and review discipline.

Do **not** assign RTL, timing closure, PCB layout, EMC, verification, or
unassisted Python implementation. When Python is needed, provide complete scripts
and line-by-line explanation, or pair with an engineer. The author's role is
architect/specifier/publisher; implementation needs a collaborator.

## Open items, in priority order

| | Item | Where |
|---|---|---|
| 1 | **F-09:** specification card calls Gen3/Gen4 "a bigger 7-series part"; it needs GTH/GTY, a different transceiver class and board. Batch into Rev. AX | `TODO.md` |
| 2 | Chip modernisation study, **Copper first**, one page per block | not started |
| 3 | Simulator: Phase 0, M1 = clock/modes/beam/scheduler | `A5K-Simulator-Specification.md` |
| 4 | UAC2 fit gate on the Studio's 160T (F-06) | `TODO.md` |
| 5 | 48 kHz measurement (F-07) — documentation now, bench later | `TODO.md` |
| 6 | Small-batch manufacturing note: BOM, PCBWay-class process, test rig, 10/25/50-unit cost | `A5K-Market-Signals.md` |
| 7 | One narrow question to Dave Haynie — only if a concrete number is ready | private `Haynie-questions.md` |
| 8 | Capture storage: **Studio and above**; Gen4-capable switch, Gen2 FPGA | `TECHNICAL-CONSIDERATIONS.md` §15 |

## Where the project actually is (10 November 2026)

The position that survived review is **not** “the next Amiga” and **not** a
mass-market Apple competitor. It is:

> an open, deterministic display/audio PCIe card with a published timing
> contract, for people who need a register write at a known scanline without a
> GPU scheduler or OS compositor in the path.

The card is the primary form factor. A Thunderbolt/USB4 enclosure is an optional
way to use the same card on machines without a slot — packaging, not a different
product. It is not an eGPU; if the requirement is graphics throughput, a GPU wins.

The plausible first scale is **a few dozen units per batch**, using PCBWay-class
fabrication — HeatDeath's estimate, not a market study. The Ultimate II small-batch
model is a better reference than “next Amiga”.

The broader ambition — an affordable Amiga-like A/V workstation or home
supercomputer — remains a system-level goal, not a claim about this card. 68k
compatibility remains a separate, multi-year project.

## Active reminder — review campaign is closed

The r/FPGA thread was the only channel posted. It drew ~**7,400 views** and **13
recorded replies**; none produced a class-A finding. The thread turned hostile at
the end (a labour/AI objection, not a technical claim), and the author has stopped
engaging. **Do not add cross-posts or reopen the argument.** The campaign's
remaining value is the reply notes in `TODO.md`, not more traffic.

The exit criteria — three independent reviewers with no class-A defect, or thirty
days without one — are effectively met by silence, not by endorsement. Record it
that way.

## What not to do

- Do not start RTL before the simulator.
- Do not buy parts; there is no budget.
- Do not build the 68k legacy core yet; it is reserved, not shipped.
- Do not freeze a model because a checklist completed.
- Do not publish the author's private opinions as project claims.
- Do not claim mass-market reach through PCIe. PCIe buys desktop/workstation
  installability; Thunderbolt/USB4 buys reach. Say which one is meant.
- Do not conflate HeatDeath's Discord critique with the hostile r/FPGA thread.
- Do not reopen the Reddit argument. It is closed.
- If the author pauses: leave the tree clean, record the last commit here, and do
  not manufacture work to fill the gap.

## Cold-start prompt

Paste this into any new session:

> You are continuing the **A5K** design study — an Amiga-inspired, CPU-agnostic
> PCIe deterministic display and audio engine with a published, slot-exact timing
> contract. Nothing has been built. Read `RESUME.md`, `TODO.md`, `A5K-Frailties.md`,
> `A5K-Brief.md`, `A5K-Lineage.md`, `A5K-Slot-Table.md` and
> `A5K-Market-Signals.md` before proposing anything. Follow the rules in
> `RESUME.md`: one block at a time, no revision without a finding, nothing measured
> until a board exists, no compatibility burden. The r/FPGA campaign is closed; do
> not reopen it. Then ask what to work on.

## If the token budget is about to end

1. Run `export_conversation.py` in the private folder.
2. `git add -A && git commit && git push` in the public one.
3. Open `RESUME.md` in a new session with any model.
4. Nothing else is required. The repository is the memory.

---

*Rev. AW (B49) · 4 November 2026 · documentation through 10 November 2026 · project started 30 October 2026*
