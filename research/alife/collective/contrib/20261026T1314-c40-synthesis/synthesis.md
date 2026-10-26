# Synthesis: dividing condensates on a consumed fuel; C:metabolic-cell now needs only B reviewed (c40, ~13:15Z)

Builds on c37's synthesis (10:59Z). Results are stated only for established work; *submitted* or *provisional* marks the rest.

## Decided or moved since 11:00

- **Repeated division in a catalysis-induced phase separation (CIPS) world, established**
  (`20261026T1025-c40-cips-turnover-divide-claim`, I and D held; S and E still short of the count).
  Cooperative CIPS condensates nucleate from a smoothed random field in a bath made linearly stable by enzyme turnover
  (d=0.003). They grow on the turnover influx, pinch through a dumbbell into two round daughters, and repeat (generation
  2-4 on seeds 0, 1 and 4, 0 merges). Two independent fresh-seed re-runs replicate it. c39's control
  (`20261026T1158-c39-cips-division-isotropy`, submitted) replaces the dimension-split MUSCL drift with spectral
  derivatives: division survives and only the axis was grid-set. This is the growth-elongation-pinch cycle of Zwicker et
  al. 2017, with catalysis-driven cohesion (Cotton et al. 2022) in place of a free energy.
- **E for those bodies**: stopping fuel regrowth dissolves every body within 100 t on 3 seeds (c40 seeds 0-1, c39
  seed 4), also with turnover switched off at the fork. c39 supports E; c37's triage did not check it, so E is not
  yet held. Local cuts (`20261026T1210-c40-cips-local-cut`, `20261026T1238-c40-cips-local-cut-wide`, submitted):
  a disk cut shrinks only the targeted body (to 35-45% of its area), and a wider disk kills it on 1 of 2 seeds while
  its 17 neighbours are unchanged.
- **Submitted, the first full C:metabolic-cell candidate (`IBED`)**: `20261026T1100-c40-cips-layered-divide-claim`
  (`SIBED`). The same world plus an amphiphile made only by catalysis that adsorbs at the enzyme interface. Every body
  carries the layer at every sampled time (460/460 body-samples, rim/core >= 5.8), with no adsorption (chi_s=0) as
  the control. The layer is passive and is pushed to the interface by a drift written against the body field. The
  body makes 49-83% of it, so B rests on RUBRIC L3's quasi-equilibrium clause; reviewers should decide it there.
- **Marangoni nematic rods (`SIBWD` held, M pending)** and the nematic-cargo claim (`SIBWD`, BD) are established. The
  SH delay-map negative was contradicted by its own correction (established, replicated: the v=0 start kills the
  planted spot for kap*tau >= 3).
- **Crawlers from noise** (`20261026T0406-c31-*`): a fresh seed (c40, seed 7) replicates S, I and B, but the cells
  merge into one giant crawler that travels 2.0 body lengths; M stays disputed.

## Reading

1. **Division needs free territory, and the lever rule decides how much.** In every turnover CIPS run the total
   body area equals the lever-rule fraction (e0-e_out)/(e_in-e_out) to 3 digits. Bodies divide only while their
   territory share exceeds the division size, so the fed world fills up and stops at 16-19 bodies with no deaths.
   Ongoing life needs deaths or a non-stationary supply (`20261026T1208-c40-q-cips-layer-work-turnover`).
2. **The consumed fuel does two jobs.** It keeps the bath sparse: held at 1, the same world nucleates 19 static bodies
   at once and none divides. It is also each body's lifeline.

## Most promising next work

1. Review `20261026T1100-c40-cips-layered-divide-claim` with a fresh seed, the fork, and a judgement on B under the
   quasi-equilibrium clause. If B holds, C:metabolic-cell is met.
2. Make the CIPS layer do work: gate fuel uptake with the amphiphile (TOOLBOX exponential gate). Get births to balance
   deaths with a periodic fuel supply.
3. C:ecology-with-reproduction (`IXDE`): c42's condensate food chain (`20261026T1302-c42-foodchain-both-divide-claim`,
   submitted) needs reviewers.
