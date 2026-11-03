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

*Rev. AG · 2 November 2026 · project started 30 October 2026*
