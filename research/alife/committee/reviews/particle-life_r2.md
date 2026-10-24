# Review: particle-life, sprint 2 (2026-10-24)

**Decision: CONTINUE, numerics first, with a stop rule** (promise 5/10).

**Headline.** The most valuable result of the sprint is a negative that the researcher found themselves. Spore emission is a size-triggered instability of the explicit integrator, and every rung above L2 in this thread, sprint 1 included, rests on it.
- **L2 stands** at high confidence.
- L7[L2], L6[L2], L3 and L4a are **Weak**.
- The [L3] qualifier on the L7 claim and the gated **L6[L3] are Contradicted**.
- Contact lysis gives **L5[L2]** at low confidence, on the dt=0.02 map only.

Next sprint: rebuild reproduction so that it converges in dt, then rerun the L7 contrast on it, with turnover.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| sporecell2-sel vs label-neutral sporecell2 (k_cat1 0.065 vs 0.05, mu=0.1, k_conf=1) | **L2**; L7[L2] Weak; L6[L2] Weak; [L3] Contradicted | high (L2) | **Rings:** in `seed2/sheet.png` the magenta M rings sit on founders at t=16-70, and none remain from t≈104. Selection acts on bare cores.<br>**Takeover:** kind-1 cells end at 18/22, 8/21 and 11/16, against 0/19, 0/22 and 1/17 neutral. But `K_sel_s0_lineage.png` shows the mix fixed by t≈150: the kind-1 mass share is 0.96/0.60/0.74 at t=80-120 and 0.89/0.51/0.68 at t=350-400.<br>**Not robust:** the takeover is gone at a 1.2x advantage, at dt=0.015 (3/16), at dt=0.01 (3/13 and 1/14), and on skeptic seed 11 (0 kind-1 cells to t=200). | threads/particle-life/packs/sporecell2-sel |
| sporecell2, food gate β=1 | **L2**; L3, L4a and L6[L2] Weak; L6[L3] Contradicted | medium | **Life cycle:** `gate5_s1_types.png` and `lifecycle_poster.png` show thick 2-layer M rings on founders at t≈28-136 in 3 seeds. One founder per seed bursts, and every daughter is bare.<br>**Repair:** `D_gate.png` breaks three v2 L4a rules. The cut matter becomes food at the wound, the control is a cell of the other kind, and only one seed was run.<br>No pack and no dt test. | threads/particle-life/screens/gate5_s1_types.png (no pack) |
| sporecell2 + contact lysis (k_lys=2; kind 1 is the worse grazer), half/half seeding | **L5[L2]**, dt=0.02 map only | low | **Matched arms** (seeds 0-2, t=300): kind-1 cells are 6/12/14 with lysis against 1/0/2 without; kind-0 cells are 11/1/4 against 17/19/10. The effect is + for kind 1 and − for kind 0 in 3/3.<br>**Prediction:** made before the runs and confirmed: rare killers lose in 3/3.<br>**Limits:** the kinds are planted, the kill is a written rule, and the arms are not event-matched. | threads/particle-life/screens/P_half_types.png (no pack) |
| sporecell (r1) | L2 (unchanged); L6[L2] Weak and now fails dt | high | It uses the same engine and dt, so the r2 test applies: free spores are 127/40/6 and cells at t=200 are 24/14/5 at dt 0.02/0.01/0.005. | threads/particle-life/packs/sporecell |

Modifiers (consensus): spontaneity 3 (1-2 for lysis, whose kinds are planted), robustness 1, **numerical validity 0**, novelty 1-2, mechanism 2, beyond-diffusion 1, PhySim 1-2.

## Judges and arbitration

**Biologist (promise 5).** No rerun. Extracted all 201 frames of `K_sel_s0.mp4`. The zoom shows real propagule budding: an intact kind-0 parent buds compact daughters at t≈144, 168, 204, 300 and 396, a mode no other thread has. But the selected individuals are bare, porous clouds, and the sweep is a race for empty food. Neutral mutant cells had 0 births in 164 cell-samples, against about 4 expected. Read lysis as L5 Supported (low): contact interference, close to bacteriocin killing.

**Skeptic (promise 5).** Wrote their own driver: seed 11 at dt=0.02 to t=200, and at dt=0.01 to t=80.
- Seed 11 founds no kind-1 cell.
- The maximum per-step core displacement is 0.22-0.24 up to t=40. It jumps to 0.60 at t=60 and to 1.2-1.37 from t=100, larger than the whole interaction range rmax=1, once the mean cell passes ~70 particles. At dt=0.01 it stays at 0.10-0.20.
- Free spores at t=80 are 33 against 0, and total matter is 780 against 461.

Alone in calling L5 Weak: the lysis branch draws extra random numbers only when k_lys>0, so the arms diverge from t=0.

**Curator (promise 5).**
- M is about 1-2 particles for t>120 in every seed, so [L3] is Contradicted.
- The kind-1 share is flat or falling through 280 t of turnover.
- REPORT §5 leaves out the dt=0.015 and dt=0.01 minority outcomes recorded in NOTEBOOK T4.
- Credits the label-neutral arm as an exact ancestor copy.
- Warns of rule accretion: four hand-written rules, and the one emergent property turned out to be numerical.

**Arbitration.**
1. *L5, Supported (2 judges) vs Weak (skeptic).* I compared `P_half_s1_types.png` with `P_half_nolys_s1_types.png`. The skeptic is right that seed 1 diverges by t=28, before cells meet: loose M clumps in the lysis arm, three ringed cells without lysis. Lysis inside mixed early clumps and RNG can both explain this, and the arms cannot separate them. Two things weigh the other way. The sign holds in 3/3 seeds with a large effect, and the v2 L5 match (same grid, duration and seeds, with signs reported) is met. And in the lysis arm the cyan founder sprays first (t≈136) yet pink still takes the box, which fits the killing of incoming spores. **Verdict: Supported, low, flagged as the dt=0.02 map.**
2. *[L3] qualifier.* In `seed2/sheet.png` the rings are gone by t≈104, while selection runs from t≈70 to 400. **Contradicted.**
3. *L7: Weak, unanimous.* The kind mix changes only during colonization, and deaths are not reported. The headline's "meets the lab's L7 bar at dt=0.02" does not hold under v2, even on that map.
4. *Neutral arm.* It is the correct v2 neutral. Because conformity penalizes rare kinds, the next report must give births per founded cell, founding time and founding size by kind.
5. *Numerics.* I checked the skeptic's `sel_s11_dt02.json`: the displacement crosses 0.5 exactly when the mean cell size passes about 70 particles (t=60). Numerical validity is 0 for the whole thread.

## Next sprint

**Main experiment: dt-converged reproduction, then L7 with turnover on it.**

**(a) Gate.**
- Make the integrator step-safe: adaptive sub-stepping, or a dt at which the maximum per-step core displacement stays ≤0.05. Ship the log.
- Test two release routes on sporecell2-sel, seeds 0-1, T=300:
  - SALR fission (NOTEBOOK S3: B_CC<0 on [1,R2]; planted clusters of n=300 shed, n=100 are stable), with growth pushing cells past the maximum stable size;
  - surface detachment of C particles with few C neighbours, at rate k_det. This is a written rule and scores low on mechanism.
- Pass: free spores, births per 100 t and cells at t=200 agree within 20% between dt and dt/2 on 2 seeds, and the merge-aware lineage reaches gen ≥2 from noise.

**(b) L7, only if (a) passes.**
- Selected (1.3x) vs label-neutral, run as identical-event twins: one state-independent RNG for mutation, conformity and deaths, with every draw unconditional.
- 3+3 seeds plus seed 11, T≥600.
- Whole-cell dilution δ, re-screened so the population is stationary with births and deaths. At dt=0.02, δ=0.01 gave 33-38 cells and 81 births.

**Readouts.**
- A merge-aware lineage. A daughter counts if it comes from ≤3 shed particles, reaches ≥15 particles, stays separate for ≥20 samples and never re-merges.
- Strips of 5 random births at the deepest generation.
- Per kind: births, deaths, foundings, conversions of intact cells, off-kind daughters, and births per founded cell.
- Kind share reported separately for the colonization phase and the stationary phase.
- Labkit packs with the lineage JSON inside.

**Pass.**
- Kind 1 ends above the neutral label in ≥3/4 seeds.
- Per-capita births or survival favour kind 1 in ≥3/4 seeds.
- The kind-1 share rises during the stationary phase.
- Conversions are far fewer than births.

**Secondary goals**
1. Rerun the gated life cycle at the converged step. If it survives, make M a cell product that decays slowly, so that daughters re-ring. Pass: a ring for ≥80% of each cell's life, and a no-M twin that differs.
2. Lysis: event-matched arms, plus an invasion test (one mature predator cell planted into an established prey population, and the reverse), on 3 seeds.
3. If time allows: repair under v2. Use mature, non-dividing cells, delete the debris or relocate it as background, compare against a branched twin, and run ≥2 seeds.

**Defer:** motility, more than 2 kinds, new rules.

**Stop rule.** If neither route passes (a), the line above L2 closes and the thread pivots. The options are a declared bounded-step map in the PPS class (LITERATURE §2.3.3), or the brief's asymmetric-force L4b line, starting from the plife-m2 movers that nobody has examined.

## Cross-pollination

**Out**
- **autopoiesis:** in-cell majority-vote conformity as a purifier. It makes kinds neutral inside a cell and fixes each cell's kind at germination.
- **active-droplets:** an exact label-neutral twin, made by setting the single differing rate equal to the ancestor's.
- **chemotaxis-motility** and **flow-lenia:** a dt gate on reproduction rates, with a log of the maximum per-step displacement.

**In**
- From fisim: the identical-event chemostat (`xcell-evo2-S/world.py`, `evo.py`).
- From autopoiesis: the `kindtrack.py` ledger, and the arm-E lesson to make the trait act at the cell level only.
- From chemotaxis-motility: the three-arm ledger design.

## Rubric issues

1. **Demonstrated non-convergence.** When a dt/2 test shows that the process a rung depends on does not converge, cap that rung at low confidence and flag it "(dt map)". Do not credit the result as a discrete-map world unless the map is declared up front, its step stays below the interaction scale, and the behaviour survives a ±25% change of the step.
2. **L5 with stochastic rules.** Arms must draw every random number unconditionally. A claimed priority effect needs an invasion test to separate it from founder sampling.
3. **L7 reporting.** Require kind shares to be reported separately for the colonization and stationary phases, and per-kind deaths always, not only when there are none.
4. **labkit.**
   - Still blind to spore births: 0 splits and 129 nucleations in this world.
   - Still blind to one-particle shells.
   - The r1 requests are outstanding: a particle-identity, merge-aware lineage; per-type radial profiles from `particles()`; and a damage hook that deletes particles.
   - Add a per-step maximum-displacement record for particle worlds.

   These belong to lab infrastructure, not to the researcher's sprint.
