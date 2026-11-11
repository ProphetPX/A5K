# A5K — informal market signals

**Status:** informal feedback, not market research and not a product claim. These
are signals worth remembering because they are specific, and because they point at
a product shape rather than a slogan. They do not prove demand.

---

## 10 November 2026 — HeatDeath, Commodore Discord

After the position was narrowed to a **deterministic A/V engine** rather than “the
next Amiga,” HeatDeath replied, in substance:

- the deterministic A/V stack is “very cool”;
- it is “probably very niche”;
- it belongs in the same general category as the **Ultimate II mainboard** before
  it was commercialized;
- a few dozen units per batch at semi-reasonable prices is plausible through
  **PCBWay or a similar small-batch manufacturer**.

**Interpretation.** This is the first realistic product-shape response: a niche,
small-batch, enthusiast/professional instrument — not a mass-market Apple
competitor. It is more useful than “I’d buy one” because it names a scale and a
manufacturing route.

**Caveat.** It is one person’s estimate, not a market study or a quote.

---

## 10 November 2026 — Dave Haynie

Dave Haynie was shown the repository and called it **“interesting.”** He also made
clear he had not reviewed it in detail.

**Interpretation.** A door, not an endorsement. It is worth recording because it is
from a relevant engineer, but it must not be quoted as approval. The honest form is:

> “Dave Haynie called it interesting; he has not reviewed it.”

**Caveat.** Do not turn “interesting” into “he likes it” or “he validated it.”

---

## 10 November 2026 — community reaction

An unnamed community member said:

> “I want your mad max amiga now”

The author replied: “haha me too.”

**Interpretation.** “Mad Max Amiga” is a memorable community nickname: scrappy,
open, built-from-parts, not nostalgic. It is a better reaction than “next Amiga”
because it describes the object, not a compatibility claim.

**Caveat.** Keep it as a nickname, not a product name or a silkscreen. The project’s
trademark rule stands: do not put “Amiga” on a box, store page, or product branding.
“Mad Max” alone is fine; “Amiga” stays descriptive.

---

## Positioning language (11 November 2026)

The audit in `A5K-Ethos-Audit.md` gives the long version. The short public
language is:

> **A5K is an open design study for a PCIe card that draws pictures and plays
> sound on a schedule you can predict — inspired by the Amiga’s custom chips, but
> not an Amiga and not a clone.**

What to say it keeps:

- the Amiga’s **engineering ethos** — chipset-first design, deterministic beam
  timing, fixed-function parallelism, separable compute, more-with-less, open
  documentation;
- the idea of a **schedule you can count**, so a change can happen on an exact
  line of the picture;
- a **CPU you can swap** — the host supplies the processor; the card keeps the
  chipset.

What **not** to say:

- “the true Amiga in every way”
- “the next Amiga”
- “an Amiga 5000”
- “Amiga-compatible”
- “mass-market”
- “a whole computer”

Those claims are false, and they invite exactly the arguments the project has
already lost. The accurate sentence is:

> A5K keeps the Amiga’s **engineering ethos** and deliberately does not claim its
> **platform ethos** of compatibility, mass-market affordability, or a
> whole-system product.

---

## What these signals do not mean

- They are **not** a market study.
- They are **not** preorders.
- They are **not** validation of the timing claims.
- They do **not** make A5K a mass-market product.
- They do **not** justify a “home supercomputer” claim.

## What they do suggest

- The **deterministic A/V card** is the understandable product.
- The plausible first scale is **a few dozen units per batch**, not a mass market.
- The **Ultimate II** small-batch model is a better reference than “next Amiga.”
- The **Mad Max** framing resonates; use it as a nickname, not a brand.
- A concrete next step is a **small-batch manufacturing note**: BOM, PCBWay-class
  process, test plan, and unit cost at 10/25/50 units.

## What to ask next

1. What would a few dozen units cost at PCBWay-class pricing?
2. What is the minimum test rig for a batch?
3. Which parts have a second source?
4. What does the Ultimate II case study teach about batch size, support, and
   customer expectations?
5. What is the smallest demonstrable unit: card + host driver + one A/V demo?
