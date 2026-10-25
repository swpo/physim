# Synthesis 6: heredity by intrinsic deaths is established in one class, but what it selects is a within-life decline; the heredity line now needs B, not more H (c06, ~5 h in)

Score at writing (STATE.md, 11:22Z): P = 62, P_BD = 12, Q = 12, K = 8, C = 40 (synthesis 5 at 11:05Z: K = 6, C = 36).
Only established results are stated as results; *submitted* marks work still under review.

## Established since synthesis 5

- **Active-nematic rod colony (`SIMD`, c11, 1014).** My fresh-seed review agrees (seed 5: 26 persistent
  splits, generation 4; zeta = 0 gives 10 static drops, 0 splits), but motility is marginal (best track
  3.3 body lengths, speed not dt-converged).
- **pcell `SIDH` (c06, 0820) and its containment version (0857).** Walled Allen-Cahn cells whose catalyst
  is ~8000 identity-carrying particles; a heritable link yield arises by mutation, and the cells that die
  without any imposed death are the low-yield ones (3rd-5th yield percentile; inert marker 0.29-0.55).
  It is the first established claim with H driven only by intrinsic deaths.
- **What that H actually is (established negatives and audits).** Dying cells are born near-average and
  decline during life (c09, 0952; c06, 0923): rank at birth 0.30-0.59, at death 0.02-0.07. The decline
  is absolute, not relative to an improving population, and it happens even with no explicit replication
  cost, because link making draws on the substrate that each particle's own replication uses
  (c06, 1012, *submitted*). The selected unit is therefore partly the cell lineage and partly the
  particle inside it: cells age by within-cell erosion of a public good.
- **Containment without a gate (c01's law, established).** Cargo with no barrier is held at
  contrast - 1 ~ Dc^-0.93. In pcell the gate matters less for contrast than for individuality: the
  lowered-D no-gate twin still holds particles 4-37x but its cells fuse into one body (0857).

## What changed in the reading

1. **Heredity needs kinds fixed between births, and the cost that makes deaths also erodes kinds.** With
   a cost, cells turn over but decline during life. Without one (yield as pure efficiency,
   c06 1037 *submitted*), cells keep their yield for life and the mean responds against an inert marker
   (1.13 vs 1.04 at t ~30000), but the response runs away into giant cells. A capped trait
   (c06 1108, *submitted*, 4 seeds) keeps 11-15 bounded cells. There, dying cells are below the median
   already at birth (rank 0.25-0.40; marker 0.42-0.63) and lose only 0.03-0.08 during life, though
   low- vs high-born death rates differ on only 2 of 4 seeds.
2. **Turnover remains the bottleneck everywhere else.** Particle-fed FCH micelles (c06 1013) and
   metabolic FCH micelles (c03 1000) both freeze at a carrying capacity with no deaths. Starving FCH
   bodies shrink to a stable size instead of dying, so FCH lines will not give H until something
   destabilizes small bodies.
3. **Rings and motion still trade off.** In pcell with c05's label-free slip, the link ring passes
   (rim/core 1.62) only below the swimming transition. Above it cells swim 40-90 body lengths but lose
   ring and division (c06 0914, as c05 0724 found for the field version).

## Most promising next steps

- **`C:autonomous-heredity` now lacks B, not H.** pcell's L ring sits at rim/core 1.4-1.5. Two cheap
  leads to test on the capped-efficiency world: the slip drive at mu ~2.2, which raised the ring to 1.62
  without making cells swim far (one seed), and a stronger chi with a lower tilt to keep cells alive.
- **Make kinds discrete at birth.** For example, mutate only at division (one particle reseeds a
  daughter), so the L7 rule "kinds change only at mutation or birth" holds by design; then run a powered
  identical-event neutral arm.
- **Reviews should keep asking for the life-course readout** (rank at birth vs at death,
  `birthfate.py`) on every H claim. It separated "selected kinds" from "aging cells" in one reading.
