# Decisions taken

**What this file is.** A one-line record of the decisions the design rests on, so a
reviewer does not have to rediscover them in a changelog, a conversation or a
document's older wording. It is **append-only**: a decision is superseded by a new
row, never deleted.

The canonical revision is the integer in `CHANGELOG.md` (B1–B49), with the letter as
its display alias. Rows cite the baseline at which the decision took effect.

| # | Decision | At | Detail |
|---|---|---|---|
| **0** | **Scope** | B49 | A5K is the open, modern continuation of the AAA/Hombre multi-chip lineage on one FPGA. The published C+ Rev 2 / Studio family is the **first slice**; other blocks are **deferred, not denied**. Lineage is inspiration, not obligation. No third-party hardware: Vampire, Apollo and MiSTer are market comparisons only. |
| **1** | **Host** | B22 | The card is a PCIe endpoint, CPU-agnostic by construction. Reference host x86-64; RISC-V is the destination; Mac later. |
| **2** | **AROS** | B23 | AROS runs on the **host**, driving the card over PCIe. The card has no OS of its own. A standalone RISC-V machine is a future product, not this card. |
| **3** | **FPGA per model** | B47 | 100T / 160T / 325T / 325T −3, chosen by cumulative feature load (beams, HDR, capture, UAC2 logic), not by a single global choice. |
| **4** | **Line framing** | B49 | Three build points and a halo: C+ (A500), Studio (A3000), Studio Pro (A4000), Pro II (no ancestor, theoretical). |
| **5** | **Storage** | B49 | microSD recovery on **all** models — private, firmware-owned, no PCIe host controller. M.2 **NVMe on Studio and above only**, host-visible, two-way, asymmetric, OS-owned partitioning. **No SATA anywhere.** |
| **6** | **UAC2** | B49 | C+ never. Studio: **complete circuit populated, firmware-dark** until the host fits the 160T and a board measures it. Pro and Pro II: enabled ("fitted and enabled, not yet measured"). |
| **7** | **Converters** | B49 | AKM AK4458/AK5720 primary; Cirrus CS4385/CS5368 is a **respin contingency**, not a drop-in. **Dual footprint where the packages allow**, so a supply swap is not a respin. |
| **8** | **68k legacy** | B49 | An open-core 68k block is **reserved on every model**, as the CPU half of a future legacy stack. Not built; **no Amiga compatibility is shipped or claimed**. |
| **9** | **3D and AI** | B49 | **Deferred on every model, never missing.** Later work; not in this revision. |
| **10** | **PCIe generations** | B49 | FPGA port **Gen2 ×4** on Studio/Pro (×1 on C+). **Gen4-capable switch and Gen4 PCB layout on Studio and above**, so a later 3D/Gen3/Gen4 part is a parts swap, not a respin. Gen4 *silicon* today is a different price class. |
| **11** | **Budget** | B49 | No corporate budget or oversight; hardware is deferred **by choice**, not funded. The design study is the deliverable until a board is justified. |

---

*Started 4 November 2026 · Rev. AW (B49) · append-only*
