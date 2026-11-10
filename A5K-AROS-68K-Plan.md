# A5K — AROS, 68k, and compatibility plan

**Status:** decision document, not a design claim. No hardware, no RTL, no
measurements. This file separates three paths that are often mixed together:

1. **Native AROS on the host** — no 68k core.
2. **Host-emulated 68k** — the host runs UAE/Amiberry; A5K is a display/audio
   device at most.
3. **On-card 68k soft core + chipset compatibility** — A5K becomes a compatible
   Amiga-like system, not just a card.

The card stays a PCIe add-in card in all three. The question is what runs where.

---

## 1. Definitions

| Term | Meaning |
|---|---|
| **Native AROS** | AROS compiled for the host CPU (x86-64, ARM, etc.). Apps are host binaries. No 68k core is needed. |
| **AROS 68k** | AROS built for the 68k. It needs a 68k CPU or a 68k emulator. |
| **Classic Amiga software** | 68k binaries that expect Amiga chipset registers, timing, and often Kickstart. Needs 68k plus chipset equivalents. |
| **Soft core** | A CPU implemented in FPGA logic (RTL). Flexible, uses FPGA resources, runs at FPGA speed. |
| **Hard core** | A CPU fixed in silicon (e.g., an ARM core in a SoC, or a physical 68060). Faster and more efficient, but not changeable. |
| **Compatibility mode** | A mode in which A5K exposes Amiga-compatible registers/timing instead of only its native A5K interface. |

A5K’s own slot table is **not** the same contract as Amiga chipset timing. A5K
timing is largely settled for A5K’s display/audio engine; Amiga-compatible timing
is not settled and would need its own verification.

---

## 2. Path A — Native AROS on the host

**What it is:** the host CPU runs AROS natively. A5K is a PCIe display/audio
device with an AROS driver/HIDD.

**Requirements**

- PCIe enumeration and BAR mapping (BAR0 registers, BAR2 Chip RAM aperture).
- AROS graphics HIDD for A5K: modeset, framebuffer/plane mapping, vblank,
  beam-synchronous fence.
- AROS audio driver (AHI) for the card’s audio path.
- Interrupt handling (MSI-X or legacy), DMA setup, buffer management.
- A host GPU or firmware display for early boot; A5K is not a boot display.

**What it gives**

- Native AROS apps run at host speed.
- No 68k core, no chipset emulation, no Kickstart.
- The card does what it is good at: deterministic display/audio.

**What it does not give**

- Classic Amiga 68k binaries.
- Amiga chipset register compatibility.
- A standalone machine.

**Effort:** driver + HIDD + audio driver + validation. Months, not years. This is
the natural first integration.

---

## 3. Path B — Host-emulated 68k

**What it is:** the host runs UAE, Amiberry, or another Amiga emulator. The
emulator provides the 68k CPU and chipset. A5K may be used as a display sink, but
the emulator is doing the compatibility work.

**Requirements**

- A host emulator with a path to A5K output, or ordinary host output.
- Kickstart or AROS ROM for the emulated machine (Kickstart is proprietary; do
  not ship it).
- No 68k core on the card.

**What it gives**

- The fastest route to running classic Amiga software.
- Compatibility is the emulator’s problem, not A5K’s.
- Good reference for what compatibility actually requires.

**What it does not give**

- A5K chipset compatibility.
- A hardware story; the card is a display device at most.
- Deterministic Amiga timing on the card.

**Effort:** low to moderate, mostly software integration. This is a stopgap and a
test bed, not the product.

---

## 4. Path C — On-card 68k soft core + chipset compatibility

**What it is:** A5K carries a 68k soft core and enough Amiga-compatible chipset
logic to run AROS 68k or classic software. It becomes a compatible system on a
card, not just a display/audio engine.

**Requirements**

- **68k soft core.** Reuse an existing open core (TG68K, fx68k, ao68000, or a
  Minimig/MiSTer-derived core) rather than writing one. Verify the licence before
  integrating.
- **Chipset equivalents:** Agnus-class DMA/beam, Denise-class planar scanout,
  Paula-class audio/interrupts, CIA-class timers, and the memory map.
- **Kickstart or AROS ROM.** AROS is open; Kickstart is proprietary and must not
  be shipped without a licence.
- **Storage and boot path:** floppy/IDE/SD image, or a host-provided image.
- **Compatibility mode:** registers, interrupts, DMA timing, Copper/Blitter
  behaviour, and enough timing accuracy for the target software.
- **Verification:** a test suite of Amiga software and hardware-level checks.

**What it gives**

- A card that can run AROS 68k and, eventually, classic software.
- A genuine compatibility path without building a full computer.

**What it does not give**

- A guarantee of cycle-exact OCS/ECS/AGA compatibility. That is a separate,
  much harder target.
- A cheap or quick project. This is a system-level effort.

**Effort:** years, not months. The 68k core is the easy part; the chipset and
timing are the hard part.

---

## 5. Comparison

| | **A. Native AROS** | **B. Host-emulated 68k** | **C. On-card 68k + chipset** |
|---|---|---|---|
| 68k core | No | No (emulated on host) | Yes, soft core |
| Chipset compatibility | No | Emulator provides it | Must be built/ported |
| Runs native AROS apps | Yes | Yes (host) | Yes (host or card) |
| Runs AROS 68k apps | No | Yes, via emulator | Yes, on card |
| Runs classic Amiga software | No | Yes, via emulator | Eventually, with verification |
| Kickstart needed | No | Yes, for classic emulation | Yes, or AROS ROM |
| A5K role | Display/audio device | Display sink at most | Display/audio + CPU + chipset |
| Effort | Months | Low–moderate | Years |
| Risk | Driver/timing integration | Emulator integration | Chipset/timing/legal |
| Fits PCIe card power/heat | Yes | Yes | Yes, but needs budget |

---

## 6. Power, heat, and the PCIe card shape

Keeping A5K as an add-in card is the right constraint:

- Power comes from the PCIe slot; no custom PSU, case, or cooling design.
- Heat is bounded by the card envelope and host airflow.
- The host provides the CPU, RAM, storage, keyboard, and monitor.
- Upgrading means a new card, not a new computer.

Things to watch:

- **Slot power budget.** Check the PCIe slot’s power limit for the chosen
  connector and card size. Do not assume a x16 slot’s full budget on a smaller
  slot.
- **68k soft core cost.** A 68k core adds FPGA logic and clock load. The exact
  LUT/FF/BRAM cost and power must come from synthesis; no number is claimed here.
- **Chipset cost.** A compatibility mode adds Agnus/Denise/Paula/CIA logic and
  verification effort, not just a CPU.
- **Boot display.** A5K is not a boot display; the host needs its own GPU or
  firmware display until AROS and the A5K driver are running.

---

## 7. Recommendation

**Do Path A first.** It is the shortest path to a useful A5K:

1. PCIe driver and BAR mapping.
2. AROS graphics HIDD.
3. AROS audio driver.
4. Beam-synchronous fence and vblank integration.
5. Validate with native AROS apps.

**Use Path B as a reference and stopgap.** Host emulation tells you what
compatibility actually requires, without committing the card to a 68k core.

**Treat Path C as a separate project.** Do not start it until:

- the Copper simulator and RTL exist,
- the card’s native display/audio path works,
- you have chosen a compatibility target (AROS 68k only, or classic software),
- and the FPGA resource/power budget is known from synthesis.

The 68k core is not the scary part. The chipset and timing are.

---

## 8. What would change the decision

- If the goal is **“run classic Amiga software soon”** → Path B, or buy an
  existing compatible FPGA Amiga.
- If the goal is **“AROS on modern hardware with A5K display/audio”** → Path A.
- If the goal is **“a card that is itself an Amiga-compatible system”** → Path C,
  with a multi-year scope.
- If the goal is **“future Amiga-like hardware, not compatibility”** → Path A,
  and leave 68k out of the critical path.

---

## 9. Open questions

1. Which AROS port is the target: x86-64, ARM, RISC-V, or 68k?
2. Is the compatibility target AROS 68k only, or classic Amiga software?
3. Is a 68k soft core acceptable on the card, or must the host emulate it?
4. What is the PCIe slot power/heat budget for the chosen card size?
5. What is the minimum compatibility test set: AROS boot, a few apps, or games?
6. Which existing 68k/chipset cores are licence-compatible with A5K?
