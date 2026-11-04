# Changelog

One line per revision. **The letter is a label; the date and this table carry the
information.** Sort by date, not by letter — in ASCII, `Z` sorts after `AA`.

The scheme is ASME Y14.35: A–Z, then AA–AZ, BA–BZ. `Rev. 1.0` is reserved for the
first freeze, when hardware exists; after it, numbering is semantic and letters do
not return.

**Revisions A–J predate the repository.** They were made in the earlier working
folders — `/home/prophetpx/Modern-Amiga` and, before that, the home directory —
and have no commits and no tags. Their record is this table and the private
conversation archive. The public git history therefore begins at **K**, which is
where the project was published, not where it started.

Finding identifiers in the last column refer to `A5K-Frailties.md`, which exists
from Rev. W. Earlier revisions have no identifiers to cite.

| Rev | Date | Tag | What changed | Findings |
|---|---|---|---|---|
| **AV** | 3 Nov 2026 | `rev-av` | The two camps distinguished: emulation advances packaging, FPGA compatibility advances silicon under a compatibility constraint, this design advances neither and says so | — |
| **AU** | 3 Nov 2026 | `rev-au` | `A5K-Lineage.md` published: AAA from Haynie’s 1993 document, Hombre, the convergence table, what is deliberately not copied, and the two camps that exist today | C11 |
| **AT** | 3 Nov 2026 | `rev-at` | Positioning names both existing camps — Vampire/A6000 FPGA compatibility and AmigaKit NG emulation appliances — and states that this card is neither | C11 |
| **AS** | 3 Nov 2026 | `rev-as` | Dave Haynie’s critique of a similar proposal answered in the documents: "not a Vampire" positioning, C11 market risk, and the card stated as CPU-agnostic by construction | C11 |
| **AR** | 3 Nov 2026 | `rev-ar` | Studio explicitly Gen2 (×2); the Pro and above left undecided on PCIe generation; the capture-recorder switch is a proposal, not a commitment | — |
| **AQ** | 3 Nov 2026 | `rev-aq` | Capture storage specified for the Pro: optional M.2 behind a Gen3 PCIe switch, FPGA port Gen2 ×4, ~1.7 GB/s usable; recorder only, not a disk controller | — |
| **AP** | 3 Nov 2026 | `rev-ap` | BOM note corrected: an alternate with a different pinout is a board revision, not a part swap; the same caveat recorded in the private memo | — |
| **AO** | 3 Nov 2026 | `rev-ao` | AKM AK4458 and AK5720 as primary converters, Cirrus CS4385/CS5368 named as alternates; alternate-part policy recorded; C+ at ~$280 | — |
| **AN** | 3 Nov 2026 | `rev-an` | Direct monitoring documented (ADC → mixer → DAC, under 1 ms at 96 kHz); converter class and its group-delay cost named | — |
| **AM** | 3 Nov 2026 | `rev-am` | Audio capped at 96 kHz: 44.1 default, 48 standard, 88.2/96 fitted and claimed only when measured; nothing above 96 offered | F-07 |
| **AL** | 3 Nov 2026 | `rev-al` | Sample rates clarified: 24.576 MHz covers 48/96/192 and 22.5792 covers 44.1/88.2/176.4; 44.1 and 48 are the working set, the rest fitted and unclaimed | — |
| **AK** | 3 Nov 2026 | `rev-ak` | The fit rule written down: synthesise before claiming; if a feature does not fit, disable it in firmware rather than uprating the part | F-06 |
| **AJ** | 3 Nov 2026 | `rev-aj` | UAC2 PHY footprint on the Studio board from the first revision, enabled by firmware; 48 kHz documented as fitted and not yet measured; no model is frozen | F-06, F-07 |
| **AI** | 3 Nov 2026 | `rev-ai` | Storage clarified: no controller on any model; the microSD is private to the card and never exposed to the host; AROS hosted first, native later | — |
| **AH** | 2 Nov 2026 | `rev-ah` | Three clocking modes behind one register — independent (default), card master, external master — reset at every power-on; no BIOS setting and no switch; the host is never slaved | — |
| **AG** | 2 Nov 2026 | `rev-ag` | Host and card documented as independent timing domains: standard PCIe, DMA both ways, no timing coupling; the card is the clock master and never follows the host | — |
| **AF** | 2 Nov 2026 | `rev-af` | Front-panel HD-Audio header, headphone DAC with independent volume, mic ADC on front and rear; the rear 8-channel path is never broken | — |
| **AE** | 2 Nov 2026 | `rev-ae` | The channel mode is one setting covering HDMI, TOSLINK and the jacks; stereo at first power-on; the user’s choice persists and a factory reset returns to stereo | C10 |
| **AD** | 2 Nov 2026 | `rev-ad` | Stereo downmix is the default on the jacks; discrete 8-channel on jack presence or user setting; plug sensing is a hint, not capability | C10 |
| **AC** | 2 Nov 2026 | `rev-ac` | C+ Rev 2 retires C+; eight-channel audio, 4 jacks + TOSLINK + HDMI LPCM, two clock families, UAC2 host on Studio+ | F-05 |
| **AB** | 2 Nov 2026 | `rev-ab` | Simulator specification: Phase 0 model, trace format, five tests and a negative test that proves they can fail | planned work |
| **AA** | 2 Nov 2026 | `rev-aa` | Video rates 23.976–60 on two slot clocks, high refresh to 1080p240, VRR explicitly excluded, CEA labelling | C1, C6, C7 |
| **Z** | 2 Nov 2026 | `rev-z` | Mode floor 640×480, first power-on default 1024×768, and four recovery routes (host, SD, button, automatic) | — |
| **Y** | 2 Nov 2026 | `rev-y` | B1 corrected: CVT-RB costs 0.6% of a line, not 11 points of display band; severity Blocking → Major | B1 |
| **X** | 2 Nov 2026 | `rev-x` | PAL and NTSC reference statistics side by side; 50 Hz recorded as an out-of-scope ceiling | C6 |
| **W** | 2 Nov 2026 | `rev-w` | Dual-pipe arbitration specified; `A5K-Frailties.md` created; review campaign planned; Appendix D added to the study | A1 |
| **V** | 2 Nov 2026 | `rev-v` | The fabric, not the DRAM, identified as the bandwidth limit; 64-bit memory on Studio; second output defined; 512-bit Pro II path; ISO withdrawn | — |
| **U** | 2 Nov 2026 | `rev-u` | Bus rebuilt on DDR3L bursts; refresh, turnaround and ECC priced; 1080p line schedule; five acceptance tests | — |
| **T** | 2 Nov 2026 | `rev-t` | Copper tick fixed at 148.5 ÷ 21 on every model; H counted in ticks; faster Studio tick domain reserved | — |
| **S** | 2 Nov 2026 | `rev-s` | C+ loses capture; Studio gains HDR10, 10-bit capture and a 256-bit fabric | — |
| **R** | 2 Nov 2026 | `rev-r` | "Duo" renamed Studio; HDMI-first output sensing; DP bridge supply risk removed | — |
| **Q** | 2 Nov 2026 | `rev-q` | BOM reconciled with the 4K60 requirement; PCIe ×1 corrected; C+ frozen in the slot table | — |
| **P** | 2 Nov 2026 | `rev-p` | Slot table published, with the explanation it needed | — |
| **O** | 2 Nov 2026 | `rev-o` | Host versus on-card processor clarified; section 5 retitled | — |
| **N** | 1 Nov 2026 | `rev-n` | Product class stated in section 4 | — |
| **M** | 1 Nov 2026 | `rev-m` | Processor, bandwidth and parallelism figures; technical specification card added | — |
| **L** | 1 Nov 2026 | `rev-l` | Memory stated precisely: 1 GB DDR3L, 2 GB upgrade, 4 GiB ceiling | — |
| **K** | 1 Nov 2026 | `rev-k` | Claims narrowed — "targets RISC-V", "intends" — so the documents stop promising what is not demonstrated | — |
| **J** | 1 Nov 2026 | — | Integration-agreement template; private memo at Rev. 7 | — |
| **I** | 1 Nov 2026 | — | Publisher clause and closing legal page; the study reaches 18 pages | — |
| **H** | 1 Nov 2026 | — | Cover variant B — centred, +4 pt | — |
| **G** | 1 Nov 2026 | — | Guru-style cover | — |
| **F** | 1 Nov 2026 | — | Page 1 records the originating question; 64-bit address-path variant sketched | — |
| **E** | 1 Nov 2026 | — | Renamed **A5K**; new title, tagline and cover legal line | — |
| **D** | 1 Nov 2026 | — | Renamed **A5000**; new title, cover and file names | — |
| **C** | 1 Nov 2026 | — | 15 pages; adds "why not just use a GPU"; comparative addendum created | — |
| **B** | 31 Oct 2026 | — | 12 pages; chipset mapping and bus options expanded | — |
| **A** | 31 Oct 2026 | — | First draft — *A New, Modern Amiga: Architecture Proposal* | — |

## Not revisions

Housekeeping does not take a letter: this file, the README prose, the tags, and
formatting commits. A revision is required only when a **design claim** changes —
a number, a constraint, a part, or a rule.

Examples already in the history: the footer standardisation, the project-name
disambiguation, and the TODO updates all sit inside Rev. S without taking a letter
of their own. This changelog itself is housekeeping.

---

*Rev. AV · 3 November 2026 · project started 30 October 2026*
