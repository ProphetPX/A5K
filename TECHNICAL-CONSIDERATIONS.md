# Technical considerations for builders

**Status: design study. No HDL, no bitstream, no firmware, no ROM, no OS image, no PCB. Nothing described here has been built, simulated end-to-end, or tested.**

This file exists so that anyone who downloads this repository knows exactly what they have, what they would have to build, and what "it runs AROS" does and does not mean today.

---

## 1. What is in this repository

| Item | What it is |
|---|---|
| `A5K-Design-Proposition.pdf` | The design study: architecture, chip-by-chip mapping, bus options, Copper specification, Migen sketch, bill of materials |
| `A5K-Comparative-Addendum.pdf` | Comparison against AAA, Hombre, the shipped Amiga eras and a 2026 workstation |
| `README.md` | Overview and citation |
| `LEGAL.md`, `LICENSE-*`, `NOTICE`, `TRADEMARKS.md` | Legal notice and licences |
| `build_*.py` | Typesetting scripts that produce the PDFs. Not machine software. |
| Appendix B of the main PDF | Two illustrative Migen listings — sketches, with the difficult parts explicitly omitted |

## 2. What is **not** in this repository

- No HDL source tree, no constraints file, no bitstream.
- No boot monitor, no firmware, no device tree.
- No operating-system image, no ROM, no Kickstart.
- No schematic, no PCB layout, no Gerbers.
- No test results, no measurements, no working prototype.

The BOM in Appendix C is a costing exercise, not a validated design.

## 3. How a machine like this boots

Four layers, in order. None of them exist yet.

```
power on
  └─ 1. FPGA bitstream        (loaded from configuration flash)
       └─ 2. Boot monitor     (DDR init, PCIe enumeration, payload loader)
            └─ 3. OS payload  (AROS kernel + userspace)
                 └─ 4. Applications
```

| Layer | Who writes it | Exists? |
|---|---|---|
| Bitstream | the builder, from the HDL that has not been written | no |
| Boot monitor | the builder; a few hundred lines | no |
| OS payload | the AROS project (separate, existing) | yes — but not for this hardware |
| Applications | AROS and third parties | yes |

Nothing in that chain requires a Commodore ROM.

## 4. AROS: what it is, and what a port actually costs

**AROS** is an independent, open-source reimplementation of the AmigaOS 3.x **API**. It is licensed under the AROS Public Licence (APL), it has ports for x86, ARM, 68k and PowerPC, and it can also run *hosted* on top of Linux or Windows.

Important distinctions:

- **API-compatible, not binary-compatible.** Source code that uses AmigaOS calls can be rebuilt; Amiga binaries need an emulator.
- **There is no mature RISC-V port today.** The main document frames RISC-V as work to be done, not as something that exists.
- **A port is a software project**, not a configuration flag. It needs:
  1. a **platform layer** — timers, interrupt controller, memory map, PCIe enumeration;
  2. a **graphics HIDD** — AROS's display-driver model — driving the Denise registers described in Appendix A;
  3. **input and storage drivers** for the boot device.

### The fastest route to proof

Bare-metal AROS is the last step, not the first. The quickest demonstration of the chipset is:

> **hosted AROS or Linux on the PC + a DRM/HIDD driver talking to the card over PCIe.**

That exercises the Copper, the blitter and the scanout in weeks rather than years, and it is the path §C.3 of the main document describes.

## 5. ROMs and the Kickstart question

Two different things are often conflated:

| Need | What it requires |
|---|---|
| Run **AROS** | Nothing from Commodore. AROS has its own kernel and boot path. |
| Run **original Amiga software** | A 68k emulator **and** a Kickstart ROM — or an open replacement |

- **Kickstart is Commodore's copyright** and remains protected. It must never be distributed with this design.
- **AROS needs no Kickstart** and ships its own binaries.
- For emulation there is an **AROS ROM replacement** for UAE, written from scratch, for people who want to run without Commodore's files.
- This design deliberately claims **no binary compatibility**. That is a design statement, not a defect to be fixed later.

## 6. How the claims could be proven

Each milestone is falsifiable, and each one is a real project:

| # | Milestone | What it proves | Rough effort |
|---|---|---|---|
| M0 | Copper and slot table in simulation (Verilator), frames dumped to PNG | the timing model is coherent | weeks |
| M1 | FPGA bring-up, one video mode, DVI/HDMI out | Denise and Agnus work in silicon | weeks–months |
| M2 | Linux DRM driver over PCIe | the register map and BAR apertures are usable | months |
| M3 | AROS graphics HIDD | AROS can drive the chipset | months |
| M4 | Bare-metal AROS boot | the whole chain works without a host OS | longer |

Until M1 exists, statements such as "runs AROS" are **targets**, not results.

## 7. What a builder would need

- **Hardware:** an ECP5-85 or Artix-7 200T class board with DDR3, plus a PCIe host and an HDMI/DVI output path.
- **Toolchain:** Yosys + nextpnr (open flow) or vendor tools for larger parts; Verilator for simulation.
- **Skills:** RTL design and timing closure, clock-domain crossing, DDR3 bring-up, Linux DRM, and enough AROS internals to write a HIDD.
- **Patience:** the arbitration schedule — the slot table — is the machine's timing contract and is the hardest single thing to get right.

## 8. Known gaps and open technical questions

These are unresolved in the design as published:

- **Slot-table arbitration policy** is described but not specified cycle-by-cycle.
- **Clock-domain crossing** between the 7.09 MHz chip domain, the AXI domain and the pixel clock is unproven.
- **BAR2 coherency** — host writes visible to the next scanline fetch without a flush — is asserted, not designed.
- **DDR3 timing at 4K** has not been budgeted against the fetch schedule.
- **HDMI PHY** compliance and EMC are unaddressed.
- **3D** is absent by design; it would be a second pipeline or an external GPU.
- **Audio clocking** and jitter relative to video are undesigned.
- **Thermal and power** budgets are estimates from datasheets.

## 9. Licensing, for anyone who builds on this

| Artefact | Licence | What it means for you |
|---|---|---|
| Hardware design and documentation | CERN-OHL-S v2 | You may build and sell; if you distribute a product, you must publish your complete source under the same licence and keep the notices |
| Documents | CC BY 4.0 | Reuse with credit, a link and an indication of changes |
| Build scripts | MIT | Do as you like |
| Names and logos | not licensed | See `TRADEMARKS.md` |

The licences grant copyright permissions. **No patent is held or licensed by the author**, and no warranty of non-infringement is given.

If you intend to contribute code, note that the project can only offer alternative licensing while the author remains the sole copyright holder — hence a contributor licence agreement or a developer certificate of origin would be required before any contribution is merged.

## 10. Safety and compliance

The design is **not** for safety-critical, medical, life-support, aviation, aerospace, automotive or nuclear use. It has not been tested, certified, or reviewed by an engineer of record.

If you build and sell hardware from it, EMC, radio, electrical-safety and product-liability obligations are **yours**, not the author's. Nothing in this repository transfers them.

## 11. Where to read more

| Topic | Section of the main document |
|---|---|
| Architecture and ethos | §§1–3 |
| Bus, form factor | §4 |
| CPU choice | §5 |
| Reference build and BOM | §6, Appendix C |
| Software and AROS | §7 |
| Why not just use a GPU | §9 |
| Copper instruction set and register map | Appendix A |
| Implementation sketch | Appendix B |

---

*Design study, 2026. Not legal advice. If you are unsure whether your use is permitted, read `LEGAL.md` and ask a lawyer.*
