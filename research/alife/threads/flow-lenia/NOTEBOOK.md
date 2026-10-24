# flow-lenia notebook

Sprint 1 started 2026-10-24 14:28 UTC.

## E1. Reference Flow-Lenia re-implementation (`worlds/fl_base`)
numpy port of Plantec et al. 2023 (priors from erwanplantec/FlowLenia): k=10 kernels, kernel radius
(R+15)r, Sobel gradients, alpha=clip((A_c/C)^2), reintegration tracking with sigma=0.65, dd=5, dt=0.2,
periodic. Scatter implementation: every source cell spreads its mass over the 3x3 cells its 1.3-wide
square can touch (np.bincount). 128^2, C=1: 400 steps in 3.5 s.
- **Mass conservation: drift 2-4e-12 after 600 steps for every rule tried** (24 rules, C=1 and C=3).
- C=1, 16 random rules, one 40x40 noise patch (screens/base_r*.png): every rule gives ONE bounded
  body; 14/16 are static, radially symmetric "cells": ring + core (r5, r15), nested rings (r13), ring
  with a dotted interior lattice (r0, r11), rim + internal "organelles" (r2). r8: asymmetric body that
  slowly drifts/reshapes; r12: breaks into ~10 small blobs (debris-sized). No gliders.
- C=3, 12 random rules (screens/c3_r*.png): bounded bodies with **channel layering**: e.g. r0 =
  cyan interior with a dot lattice, orange rim ring, magenta dotted outer halo; r9 = concentric
  magenta/cyan/orange shells; r1 magenta membrane around a cyan core. Again mostly static. r2, r7
  begin to rotate / break symmetry late (t>400).
- Reading: mass conservation + the alpha term (pressure when crowded) gives sharp bounded bodies
  for almost any rule: boundedness is cheap in Flow-Lenia; motion is not (a centred symmetric patch
  gives a symmetric body).

## E2. Many bodies: smaller kernels (R_scale 0.4), 6 noise patches (screens/pop_r*.png)
C=3, 128^2, 1000 steps. Each patch condenses into its own layered body; overlapping patches give
elongated bodies. Mostly static. r7: an elongated body splits into 2-3 round bodies by t~600 (one
split event, mass is fixed so it cannot repeat). r8: blobs crumble into ~50 small membrane-bound
cells (cyan rim, pink core). r3/r6: bodies plus a shed cloud of dots.
- Reading: with mass conserved, a body above a preferred mass splits; below it, nothing can grow.
  Division can therefore happen at most once per unit of initial mass -> need a matter source.

## E3. Metabolism with a conserved total (`worlds/fl_food`)
New operator: food phi (diffuses, does not flow). eat = k_eat*phi*q/(1+q), q=(A_sum/K)^n, distributed
over channels in proportion to A_c; every channel decays to food at k_dec=0.002. sum(A)+sum(phi)
conserved to 8e-12 (checked over 1500 steps).
- n=1 (linear uptake), food0=0.3 (screens/food_r*.png, packs/scr_food_r0): matter x4.6.
  r0: the 3 founding cells grow, **divide** (t~140-190 in pack time) and turn into ~12 motile
  "comet" cells with food-depletion wakes. BUT the faint halo the cells shed becomes a
  space-filling lattice of matter dots that also eats ("grey goo"): a sea of matter in the
  background (channel A0 x6.6). r6: labyrinth (L1). r8: blobs crumble to motile particles with
  wakes, number decays as food is used up.
- n=3, K=0.3 (Hill uptake: only dense matter eats) (screens/foodH_r*.png, foodH3_*): the r8 sea is
  gone. r8 becomes a population of **worm-like chains with a cyan sheath around a bead core** that
  grow, break and merge; they stay where food is depleted and leave food-rich patches. r0 still
  makes the background dot lattice (its shed dots are dense enough to pass the Hill gate): negative.
