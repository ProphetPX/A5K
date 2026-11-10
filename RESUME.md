# Resuming this project

**Model-agnostic handover.** If you are a new assistant, a new collaborator, or the
same author months later, read this first. It exists because the AI session is
rented and the repository is not.

---

## State, at Rev. AW (B49), 4 November 2026

| | |
|---|---|
| Revision | **AW** (B49), tagged `rev-aw` |
| Documents | 19-page study, 4-page addendum, 6-page specification card, plus the markdown set |
| Hardware | **none.** No RTL, no board, no measurement |
| Frozen models | **none** — frozen by author decision only |
| Public repo | `github.com/ProphetPX/A5K`, branch `trunk` |
| Private folder | `~/Documents/A5K_Project_PRIVATE` — **not in git** |

## Read these first, in this order

1. `RESUME.md` — this file.
2. `TODO.md` — the live task list, the review campaign, and the open findings.
3. `A5K-Frailties.md` — what is weak, with identifiers (A1, B1, C11…).
4. `A5K-Lineage.md` — AAA in its own words, and the two camps that exist today.
5. `A5K-Slot-Table.md` — the timing contract.
6. `A5K-Family.md` — the product line.

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
| 1 | Review campaign: triage replies as class A/B/C/D | `TODO.md` |
| 2 | Chip modernisation study, **Copper first**, one page per block | not started |
| 3 | UAC2 fit gate on the Studio's 160T (F-06) | `TODO.md` |
| 4 | 48 kHz measurement (F-07) — documentation now, bench later | `TODO.md` |
| 5 | Simulator: Phase 0, M1 = clock/modes/beam/scheduler | `A5K-Simulator-Specification.md` |
| 6 | One narrow question to Dave Haynie | private `Haynie-questions.md` |
| 7 | Capture storage: **Studio and above**; Gen4-capable switch, Gen2 FPGA | `TECHNICAL-CONSIDERATIONS.md` §15 |

## Active reminder — review campaign (until 8 November 2026)

The **r/FPGA post on B3 is live**. Until the 72-hour window closes, **no revision**.

Triage every reply before answering: **A** factual defect (number, datasheet,
standard or measurement) → log a finding; **B** preference → record and close;
**C** misreading → one clarifying reply, then stop; **D** noise → ignore. Do not
start a second channel until this one has had its window. Log replies in
`TODO.md` → Campaign log. The daily card is
`A5K_Project_PRIVATE/CAMPAIGN-REMINDER.md`.

## What not to do

- Do not start RTL before the simulator.
- Do not buy parts; there is no budget.
- Do not build the 68k legacy core yet; it is reserved, not shipped.
- Do not freeze a model because a checklist completed.
- Do not publish the author's private opinions as project claims.

## Cold-start prompt

Paste this into any new session:

> You are continuing the **A5K** design study — an Amiga-like, CPU-agnostic PCIe
> display and audio engine with a published, slot-exact timing contract. Nothing
> has been built. Read `RESUME.md`, `TODO.md`, `A5K-Frailties.md`,
> `A5K-Lineage.md` and `A5K-Slot-Table.md` before proposing anything. Follow the
> rules in `RESUME.md`: one block at a time, no revision without a finding, nothing
> measured until a board exists, no compatibility burden. Then ask what to work on.

## If the token budget is about to end

1. Run `export_conversation.py` in the private folder.
2. `git add -A && git commit && git push` in the public one.
3. Open `RESUME.md` in a new session with any model.
4. Nothing else is required. The repository is the memory.

---

*Rev. AW (B49) · 4 November 2026 · project started 30 October 2026*
