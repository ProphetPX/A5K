# A5K — bus technology reference

**Purpose:** a plain reference for the buses that exist around A5K, so design
choices are made with the right category in mind. This is not a claim that A5K
needs any of them. Most of them are irrelevant to a display/audio card, and that
is the point.

**Status:** reference note, November 2026. Figures are from published standards
and vendor material; they are raw or nominal, not measured on A5K hardware.

---

## 1. There is no single “best” bus

“Better” depends on the job:

| Need | Best-fit class | Examples |
|---|---|---|
| General I/O expansion, drivers, hot-plug, cheap | **PCIe** | PCIe 4.0–7.0 |
| Coherent memory pooling, cache coherency | **CXL** | CXL 3.x, CXL 4.0 |
| GPU-to-GPU scale-up | **NVLink**, **UALink** | NVLink 6, UALink 200G |
| Die-to-die inside a package | **UCIe**, UltraFusion, Infinity Fabric | UCIe 3.0 |
| CPU-to-CPU / CPU-to-die coherency | **UPI**, Infinity Fabric | Intel UPI, AMD IF |
| Memory bandwidth | **HBM / DDR** | HBM3E, HBM4, DDR5 |
| External network | **Ethernet / InfiniBand** | 800G, 1.6T |

None of these is a drop-in replacement for PCIe. They differ in protocol,
topology, coherency, cost, and ecosystem.

---

## 2. PCIe generations

Raw bandwidth per direction. Usable bandwidth is lower because of encoding,
framing, and protocol overhead. A x16 link is 16 lanes.

| Generation | Transfer rate | Per lane | x4 | x8 | x16 |
|---|---:|---:|---:|---:|---:|
| PCIe 1.0 | 2.5 GT/s | ~250 MB/s | ~1 GB/s | ~2 GB/s | ~4 GB/s |
| PCIe 2.0 | 5 GT/s | ~500 MB/s | ~2 GB/s | ~4 GB/s | ~8 GB/s |
| PCIe 3.0 | 8 GT/s | ~985 MB/s | ~3.9 GB/s | ~7.9 GB/s | ~15.75 GB/s |
| PCIe 4.0 | 16 GT/s | ~1.97 GB/s | ~7.9 GB/s | ~15.75 GB/s | ~31.5 GB/s |
| PCIe 5.0 | 32 GT/s | ~3.94 GB/s | ~15.75 GB/s | ~31.5 GB/s | ~63 GB/s |
| PCIe 6.0 | 64 GT/s | ~8 GB/s | ~32 GB/s | ~64 GB/s | ~128 GB/s |
| PCIe 7.0 | 128 GT/s | ~16 GB/s | ~64 GB/s | ~128 GB/s | ~256 GB/s |

Notes:

- PCIe 6.0 and 7.0 use PAM4 signaling and FLIT-based framing; raw rates are not
  the same as usable payload.
- PCIe 7.0 was released in June 2025. Products are emerging; PCIe 6.0 products
  are shipping.
- PCIe is **not coherent**. It is an I/O bus. That is a feature for a card, not a
  defect.

---

## 3. The other interconnects

| Interconnect | Category | Nominal bandwidth | Coherent | Status / notes |
|---|---|---|---|---|
| **CXL 4.0** | Coherent memory fabric over PCIe 7 PHY | 128 GT/s; memory pooling, coherency, bundled ports | Yes | Spec November 2025; products emerging |
| **NVLink 6** | GPU scale-up | 3.6 TB/s bidirectional per GPU | Proprietary | Shipping with Vera Rubin, 2026 |
| **UALink 200G 1.0** | Open accelerator scale-up | 200 Gb/s per lane; 100 GB/s per 4-lane station per direction | Accelerator fabric | Spec April 2025; 2.0 April 2026; products emerging |
| **UCIe 3.0** | Die-to-die chiplet | 48/64 GT/s per lane; 64-lane UCIe-A ~4 Tb/s | Chiplet protocol | Spec August 2025 |
| **Apple UltraFusion** | Die-to-die | ~2.5 TB/s | Proprietary | Shipping in Ultra chips |
| **AMD Infinity Fabric** | CPU/GPU die interconnect | Hundreds of GB/s; varies | Yes | Proprietary, shipping |
| **Intel UPI** | CPU-to-CPU / die | Hundreds of GB/s; varies | Yes | Proprietary, shipping |
| **HBM3E / HBM4** | Memory interface | >1 TB/s per stack | N/A — memory bus | Shipping / emerging |
| **Ethernet / InfiniBand** | External network | 800G, 1.6T and beyond | No | Not an internal system bus |

### CXL

CXL is the most relevant “more sophisticated than PCIe” protocol: it runs over
the PCIe physical layer but adds **cache coherency**, **memory pooling**, and
**memory sharing**. It is not faster than PCIe at the same lane rate; it is more
capable for memory-centric systems.

A5K does not need CXL. It has no shared coherent memory with the host; it has a
BAR aperture and DMA. CXL would add complexity without solving an A5K problem.

### NVLink and UALink

NVLink is NVIDIA’s proprietary GPU-to-GPU fabric. UALink is the open,
accelerator-oriented alternative. Both are for **scale-up clusters**, not for a
display/audio card.

A5K does not need them. Its host link carries Copper lists, registers, and
occasional frame readback — not multi-terabyte-per-second GPU traffic.

### UCIe and die-to-die

UCIe is for **chiplets inside a package**. Apple UltraFusion and AMD Infinity
Fabric are proprietary die-to-die links. They are faster and lower-latency than
PCIe, but they are not expansion buses.

A5K does not need them unless it becomes a chiplet or a multi-die package, which
is a much later question.

### HBM

HBM is a **memory interface**, not a system bus. It offers >1 TB/s per stack, but
it is expensive, package-integrated, and not a host expansion interface.

A5K uses DDR3L because it is cheap, available, and sufficient for the line-buffer
model.

---

## 4. What A5K actually needs

A5K’s internal fabric is the limit, not PCIe.

| Model | PCIe link | Internal fabric | What PCIe carries |
|---|---:|---:|---|
| **A5K (C+)** | Gen2 ×1 (~0.5 GB/s) | 64-bit slots: ~1.19 GB/s | Copper lists, registers, occasional readback |
| **Studio** | Gen2 ×2 | 256-bit slots: ~4.75 GB/s | Control, capture, readback |
| **Studio Pro** | Gen2 ×4 (~2.0 GB/s) | 256-bit slots: ~4.75 GB/s | Control, capture, readback |

PCIe is **not** the display bandwidth path. The display is fetched from the
card’s own DDR3L into line buffers. PCIe carries control and host traffic.

That means:

- **PCIe 4.0 ×4 (~7.9 GB/s)** is already more than the card needs.
- **PCIe 5.0, 6.0, or 7.0** would add cost, power, signal-integrity work, and
  connector complexity for no display benefit.
- If future capture needs more host bandwidth, move to **Gen3/Gen4 ×4**, not
  PCIe 6/7.
- Do not use CXL, NVLink, UALink, or UCIe unless the product changes category.

The design rule is: **spend on the internal fabric, DDR, and thermals, not on a
faster host link that the card cannot use.**

---

## 5. Glossary

| Term | Meaning |
|---|---|
| **Lane** | One PCIe serial channel; a link is made of 1, 2, 4, 8, or 16 lanes |
| **GT/s** | Gigatransfers per second; not the same as Gb/s or GB/s |
| **Raw bandwidth** | Signaling rate before encoding/protocol overhead |
| **Usable bandwidth** | What the protocol delivers after overhead |
| **Coherent** | Hardware maintains a consistent view of shared memory across devices |
| **FLIT** | Flow control unit; PCIe 6/7 framing |
| **PAM4** | Four-level signaling used by PCIe 6/7 |
| **CXL** | Compute Express Link; coherency/memory protocol over PCIe PHY |
| **UALink** | Ultra Accelerator Link; open accelerator scale-up fabric |
| **UCIe** | Universal Chiplet Interconnect Express; die-to-die standard |
| **HBM** | High Bandwidth Memory; package-integrated memory |

---

## 6. Sources

- PCI-SIG, PCIe 7.0 specification announcement (June 2025)
- PCI-SIG, PCIe 6.0 specification
- CXL Consortium, CXL 4.0 specification (November 2025)
- UALink Consortium, UALink 200G 1.0 (April 2025) and 2.0 (April 2026)
- UCIe Consortium, UCIe 3.0 (August 2025)
- NVIDIA, NVLink 6 / Vera Rubin material (2026)
- Apple, UltraFusion material
- AMD, Infinity Fabric material
- Intel, UPI material

These are standards and vendor figures. No figure here is measured on A5K
hardware, because no A5K hardware exists.
