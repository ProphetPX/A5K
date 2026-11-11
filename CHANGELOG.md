# Changelog

One line per revision. **The letter is a label; the date and this table carry the
information.** Sort by date, or by the canonical integer below — sorting by letter
alone puts `Z` after `AA`.

The scheme is ASME Y14.35: A–Z, then AA–AZ, BA–BZ. `Rev. 1.0` is reserved for the
first freeze, when hardware exists; after it, numbering is semantic and letters do
not return.

**Canonical numbers.** Every revision also has an integer: its index in this table,
which is exactly the bijective base-26 value of the letters (A=1 … Z=26, AA=27 …
AZ=52, BA=53 …). The integer is the canonical key and the letter is its display
alias, so `AV` is **B48** and `AW` is **B49**. Artefacts cite the pair — `Rev. AW (B49)` — and the
integer is what sorts, indexes and cross-references without the `Z`-after-`AA`
trap. `Rev. 1.0`, when it arrives, is a milestone mapping (`B<n> → 1.0`), not a
new series; the integer keeps counting.

**Revisions A–J predate the repository.** They were made in the earlier working
folders — `/home/prophetpx/Modern-Amiga` and, before that, the home directory —
and have no commits and no tags, because the repository did not exist yet. They
are nonetheless real design revisions: the working folder and the session were
renamed (`Modern-Amiga` → `A5K_Project`, *"Greeting"* → *"A5K_Project"*) at the
**K** boundary. Their record is this table, the private conversation archive, and
one surviving artefact — a 16-page **Rev. E** PDF kept in the private folder at
`sources/historical/Rev-E-A5K-Design-Proposition.pdf`. The public git history
therefore begins at **K**, which is where the project was published, not where it
started. No tags are invented for A–J.

Finding identifiers in the last column refer to `A5K-Frailties.md`, which exists
from Rev. W. Earlier revisions have no identifiers to cite.

| Rev | Date | Tag | What changed | Findings |
|---|---|---|---|---|
| **AW** (B49) | 4 Nov 2026 | `rev-aw` | Storage, USB and legacy policy settled: microSD recovery on every model; M.2 NVMe on Studio and above, host-visible and two-way, behind a Gen4-capable switch with a Gen2 FPGA; UAC2 fitted on Studio but firmware-dark until fit and measurement, enabled on Pro and above; converters dual-footprint; 68k core reserved on every model with no compatibility claim; 3D and AI deferred on every model. Line framing: three build points and a halo | F-06, F-08 |
| **AV** (B48) | 3 Nov 2026 | `rev-av` | The two camps distinguished: emulation advances packaging, FPGA compatibility advances silicon under a compatibility constraint, this design advances neither and says so | — |
| **AU** (B47) | 3 Nov 2026 | `rev-au` | `A5K-Lineage.md` published: AAA from Haynie’s 1993 document, Hombre, the convergence table, what is deliberately not copied, and the two camps that exist today | C11 |
| **AT** (B46) | 3 Nov 2026 | `rev-at` | Positioning names both existing camps — Vampire/A6000 FPGA compatibility and AmigaKit NG emulation appliances — and states that this card is neither | C11 |
| **AS** (B45) | 3 Nov 2026 | `rev-as` | Dave Haynie’s critique of a similar proposal answered in the documents: "not a Vampire" positioning, C11 market risk, and the card stated as CPU-agnostic by construction | C11 |
| **AR** (B44) | 3 Nov 2026 | `rev-ar` | Studio explicitly Gen2 (×2); the Pro and above left undecided on PCIe generation; the capture-recorder switch is a proposal, not a commitment | — |
| **AQ** (B43) | 3 Nov 2026 | `rev-aq` | Capture storage specified for the Pro: optional M.2 behind a Gen3 PCIe switch, FPGA port Gen2 ×4, ~1.7 GB/s usable; recorder only, not a disk controller | — |
| **AP** (B42) | 3 Nov 2026 | `rev-ap` | BOM note corrected: an alternate with a different pinout is a board revision, not a part swap; the same caveat recorded in the private memo | — |
| **AO** (B41) | 3 Nov 2026 | `rev-ao` | AKM AK4458 and AK5720 as primary converters, Cirrus CS4385/CS5368 named as alternates; alternate-part policy recorded; C+ at ~$280 | — |
| **AN** (B40) | 3 Nov 2026 | `rev-an` | Direct monitoring documented (ADC → mixer → DAC, under 1 ms at 96 kHz); converter class and its group-delay cost named | — |
| **AM** (B39) | 3 Nov 2026 | `rev-am` | Audio capped at 96 kHz: 44.1 default, 48 standard, 88.2/96 fitted and claimed only when measured; nothing above 96 offered | F-07 |
| **AL** (B38) | 3 Nov 2026 | `rev-al` | Sample rates clarified: 24.576 MHz covers 48/96/192 and 22.5792 covers 44.1/88.2/176.4; 44.1 and 48 are the working set, the rest fitted and unclaimed | — |
| **AK** (B37) | 3 Nov 2026 | `rev-ak` | The fit rule written down: synthesise before claiming; if a feature does not fit, disable it in firmware rather than uprating the part | F-06 |
| **AJ** (B36) | 3 Nov 2026 | `rev-aj` | UAC2 PHY footprint on the Studio board from the first revision, enabled by firmware; 48 kHz documented as fitted and not yet measured; no model is frozen | F-06, F-07 |
| **AI** (B35) | 3 Nov 2026 | `rev-ai` | Storage clarified: no controller on any model; the microSD is private to the card and never exposed to the host; AROS hosted first, native later | — |
| **AH** (B34) | 2 Nov 2026 | `rev-ah` | Three clocking modes behind one register — independent (default), card master, external master — reset at every power-on; no BIOS setting and no switch; the host is never slaved | — |
| **AG** (B33) | 2 Nov 2026 | `rev-ag` | Host and card documented as independent timing domains: standard PCIe, DMA both ways, no timing coupling; the card is the clock master and never follows the host | — |
| **AF** (B32) | 2 Nov 2026 | `rev-af` | Front-panel HD-Audio header, headphone DAC with independent volume, mic ADC on front and rear; the rear 8-channel path is never broken | — |
| **AE** (B31) | 2 Nov 2026 | `rev-ae` | The channel mode is one setting covering HDMI, TOSLINK and the jacks; stereo at first power-on; the user’s choice persists and a factory reset returns to stereo | C10 |
| **AD** (B30) | 2 Nov 2026 | `rev-ad` | Stereo downmix is the default on the jacks; discrete 8-channel on jack presence or user setting; plug sensing is a hint, not capability | C10 |
| **AC** (B29) | 2 Nov 2026 | `rev-ac` | C+ Rev 2 retires C+; eight-channel audio, 4 jacks + TOSLINK + HDMI LPCM, two clock families, UAC2 host on Studio+ | F-05 |
| **AB** (B28) | 2 Nov 2026 | `rev-ab` | Simulator specification: Phase 0 model, trace format, five tests and a negative test that proves they can fail | planned work |
| **AA** (B27) | 2 Nov 2026 | `rev-aa` | Video rates 23.976–60 on two slot clocks, high refresh to 1080p240, VRR explicitly excluded, CEA labelling | C1, C6, C7 |
| **Z** (B26) | 2 Nov 2026 | `rev-z` | Mode floor 640×480, first power-on default 1024×768, and four recovery routes (host, SD, button, automatic) | — |
| **Y** (B25) | 2 Nov 2026 | `rev-y` | B1 corrected: CVT-RB costs 0.6% of a line, not 11 points of display band; severity Blocking → Major | B1 |
| **X** (B24) | 2 Nov 2026 | `rev-x` | PAL and NTSC reference statistics side by side; 50 Hz recorded as an out-of-scope ceiling | C6 |
| **W** (B23) | 2 Nov 2026 | `rev-w` | Dual-pipe arbitration specified; `A5K-Frailties.md` created; review campaign planned; Appendix D added to the study | A1 |
| **V** (B22) | 2 Nov 2026 | `rev-v` | The fabric, not the DRAM, identified as the bandwidth limit; 64-bit memory on Studio; second output defined; 512-bit Pro II path; ISO withdrawn | — |
| **U** (B21) | 2 Nov 2026 | `rev-u` | Bus rebuilt on DDR3L bursts; refresh, turnaround and ECC priced; 1080p line schedule; five acceptance tests | — |
| **T** (B20) | 2 Nov 2026 | `rev-t` | Copper tick fixed at 148.5 ÷ 21 on every model; H counted in ticks; faster Studio tick domain reserved | — |
| **S** (B19) | 2 Nov 2026 | `rev-s` | C+ loses capture; Studio gains HDR10, 10-bit capture and a 256-bit fabric | — |
| **R** (B18) | 2 Nov 2026 | `rev-r` | "Duo" renamed Studio; HDMI-first output sensing; DP bridge supply risk removed | — |
| **Q** (B17) | 2 Nov 2026 | `rev-q` | BOM reconciled with the 4K60 requirement; PCIe ×1 corrected; C+ frozen in the slot table | — |
| **P** (B16) | 2 Nov 2026 | `rev-p` | Slot table published, with the explanation it needed | — |
| **O** (B15) | 2 Nov 2026 | `rev-o` | Host versus on-card processor clarified; section 5 retitled | — |
| **N** (B14) | 1 Nov 2026 | `rev-n` | Product class stated in section 4 | — |
| **M** (B13) | 1 Nov 2026 | `rev-m` | Processor, bandwidth and parallelism figures; technical specification card added | — |
| **L** (B12) | 1 Nov 2026 | `rev-l` | Memory stated precisely: 1 GB DDR3L, 2 GB upgrade, 4 GiB ceiling | — |
| **K** (B11) | 1 Nov 2026 | `rev-k` | Claims narrowed — "targets RISC-V", "intends" — so the documents stop promising what is not demonstrated | — |
| **J** (B10) | 1 Nov 2026 | — | Integration-agreement template; private memo at Rev. 7 | — |
| **I** (B9) | 1 Nov 2026 | — | Publisher clause and closing legal page; the study reaches 18 pages | — |
| **H** (B8) | 1 Nov 2026 | — | Cover variant B — centred, +4 pt | — |
| **G** (B7) | 1 Nov 2026 | — | Guru-style cover | — |
| **F** (B6) | 1 Nov 2026 | — | Page 1 records the originating question; 64-bit address-path variant sketched | — |
| **E** (B5) | 1 Nov 2026 | — | Renamed **A5K**; new title, tagline and cover legal line | — |
| **D** (B4) | 1 Nov 2026 | — | Renamed **A5000**; new title, cover and file names | — |
| **C** (B3) | 1 Nov 2026 | — | 15 pages; adds "why not just use a GPU"; comparative addendum created | — |
| **B** (B2) | 31 Oct 2026 | — | 12 pages; chipset mapping and bus options expanded | — |
| **A** (B1) | 31 Oct 2026 | — | First draft — *A New, Modern Amiga: Architecture Proposal* | — |

## Not revisions

Housekeeping does not take a letter: this file, the README prose, the tags, and
formatting commits. A revision is required only when a **design claim** changes —
a number, a constraint, a part, or a rule.

Examples already in the history: the footer standardisation, the project-name
disambiguation, and the TODO updates all sit inside Rev. S without taking a letter
of their own. This changelog itself is housekeeping.

### Documentation and market notes (not revisions)

Between Rev. AW and the next revision, the following were added or reframed. None
changes a design claim — no number, constraint, part or rule moved — so none takes
a letter. They are recorded here so the public timeline shows when the argument
changed shape.

| Date | Artefact | What changed |
|---|---|---|
| 10 Nov 2026 | `A5K-Brief.md` | Plain-language brief for engineers outside the Amiga world; answers the r/FPGA finding that the campaign post assumed Copper/Amiga knowledge |
| 10 Nov 2026 | `A5K-Lineage.md` | Lorraine (1984) added; related modern projects table added; "Amiga-inspired display/audio card" positioning clarified |
| 10 Nov 2026 | `A5K-AROS-68K-Plan.md` | Three paths separated: native AROS on the host, host-emulated 68k, and an on-card 68k soft core; recommendation recorded |
| 10 Nov 2026 | `A5K-Bus-Technology.md` | PCIe 1.0–7.0, CXL, NVLink, UALink, UCIe, UltraFusion, Infinity Fabric/UPI, HBM; conclusion that A5K's internal fabric, not PCIe, is the limit |
| 10 Nov 2026 | `A5K-Market-Signals.md` | HeatDeath's niche/small-batch estimate, Dave Haynie's "interesting" (explicitly not a review), and the "Mad Max Amiga" community nickname |
| 10 Nov 2026 | `A5K-Frailties.md` | HeatDeath critique recorded as civil Discord feedback, distinct from the r/FPGA thread; follow-ups added |
| 10 Nov 2026 | `README.md` | Reframed as an Amiga-inspired deterministic display/audio card; "What A5K is not" and "Who it is for" added; social preview image placed at the top |
| 10 Nov 2026 | `CITATION.cff` | Title and abstract aligned with the current framing |
| 10 Nov 2026 | Review campaign | r/FPGA thread effectively closed: ~7,400 views, 13 recorded replies, **no class-A findings**. No further cross-posts. |
| 10 Nov 2026 | Search/AI framing (F-10) | Proposition retitled to *An Amiga-Inspired Deterministic Display and Audio Card*; cover, citation, `NOTICE`, `LEGAL.md`, `LICENSE-docs` and `TRADEMARKS.md` aligned; "Destination: RISC-V" replaced with "Host: any PCIe machine; RISC-V is one example"; README "Project facts" and "Quick answers"; `llms.txt`; GitHub About and topics. Documentation only — no design claim changed |
| 11 Nov 2026 | `A5K-Brief.md`, `README.md`, `llms.txt` | Added "What 'deterministic' means": exact slot versus bounded window, the host is not in the timing path, fixed pixel-pipeline delay, hold-on-miss, what is and is not guaranteed, and the simulator → RTL → logic-analyser test path. Documentation only |

### Review campaign posts (not revisions)

Putting a question to reviewers does not change a design claim, so a post takes no
letter. Posts are logged here so the public record shows when each question was put.

| Date | Channel | Post | Answers | Status |
|---|---|---|---|---|
| 4 Nov 2026 | r/FPGA | [Does 256-bit at 148.5 MHz close on a Kintex-7 325T -2?](https://www.reddit.com/r/FPGA/comments/1xo9dak/does_256bit_at_1485_mhz_close_on_a_kintex7_325t_2/) | **B3** | Posted — 72-hour wait before any revision |

---

*Rev. AW (B49) · 4 November 2026 · documentation through 11 November 2026 · project started 30 October 2026*
