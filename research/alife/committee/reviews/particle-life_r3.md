# Review: particle-life, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 3/10).

**Headline.** The researcher ran the commissioned numerics experiment honestly, and its best result is a negative one. With step-safe motion and no written release (k_det=0), free spores fall from 127 to 3.4 and the population declines (1 birth against 22 deaths). So the spontaneous reproduction of sprints 1-2 was integrator overshoot.

The replacement, a written surface teleport (k_det=0.05, n_det=60), gives a colonization wave of real propagule births that **stops at confluence**. **sporecell3-det is L2 (high), with L6[L2] Weak**. All three judges agree, and a strict re-audit cuts seed 0 to generation 1. L3 is Contradicted. The twin's L7[L2] is Weak: one pair, and its stationary-phase "rise" has no births behind it.

**No rung moved in r3.** Every converged world in this thread ends at L2. The only rungs above L2 are sporecell2-lysis at L5[L2], low, which holds on the dt=0.02 map only, and the known plife-m2 L3, which is a calibration.

## Final consensus (all sprints)

| world | final rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| sporecell3-det (step-safe, k_det=0.05, n_det=60) | **L2**; L6[L2] Weak (borderline); L4c Weak; L5 Not tested; L3 Contradicted | high (L2) | **Individuals:** founders form from ~20 random catalysts in both pack seeds. Compact disks hold fixed size and position from t≈66 to 200 (tracks #0-#3).<br>**Strict lineage audit** (daughter ≥50% of parent size, parent not fused into the daughter, no re-crossing of smin):<br>- Seed 0 reaches gen 1. The gen-2 labels #26 and #50 rest on #12 absorbing its parent #4. #90 is fragment #82 crossing smin=15 again.<br>- Seed 1 has one genuine 2-deep chain, which the tool scores gen None: #24→#33 (209 particles)→#38 (166, same kind) and #42 (155, off-kind).<br>**Colonization only:** every parent-size birth comes before t≈90. After t=100 there is 1 qualifying birth per seed (≤37 particles), and no body that ever reached 100 particles dies.<br>**Also:** merge/(births+fragments) is 0.78 and 0.64; there are no birth strips; release is a teleport rule. | threads/particle-life/packs/sporecell3-det | new; the L6[L2] claim (dt-converged) → Weak |
| sporecell3, no release route (k_det=0) | L6 **Contradicted** at the converged step; L2 Weak (lineage plot only) | medium (as a negative) | `R0_s0_lin2.png`: 6 founders and no gen-1 line, with cells going 9→3. 1 birth vs 22 deaths. One seed, no pack. | threads/particle-life/screens/R0_s0_lin2.png | new; closes the r2 numerics question |
| sporecell3-det selected vs neutral twin (seed 0, T=300) | L2; **L7[L2] Weak** (colonization only); the stationary-phase rise is Contradicted as selection; L5 Weak | low | `TW_sel_s0_lin2.png`: no solid line starts after t≈50, while cells hold at ~30 until t=300. The plot hides gen-None births, but the pack JSON (the same trajectory to t=200) has one qualifying birth after t=100, of 37 particles. The twin's ledger counts 11 qualifying births in 300 t, against 12 in the pack by t=200. The kind-1 share goes 0.36→0.45, against 0.18→0.15 in the neutral arm. That rise is carried by matter moving between sterile standing cells, and by 4 intact-cell conversions against 5 kind-1 births. Heredity is leaky: seed 1's kind-1 #33 has kind-0 daughter #42. | threads/particle-life/screens/TW_sel_s0_lin2.png | new |
| sporecell2-sel (r2) | L2; L7[L2] Weak; L6[L2] Weak; [L3] Contradicted | high (L2) | The kind mix is fixed during colonization on the dt=0.02 map. It fails at dt 0.015 and 0.01 and on seed 11. The converged r3 twin does not rescue it. | threads/particle-life/packs/sporecell2-sel | unchanged since r2 |
| sporecell2-lysis (r2) | **L5[L2]**, dt=0.02 map only | low | Matched arms on 3/3 seeds: the effect is + for kind 1 and − for kind 0, and a rare killer loses. The arms are not event-matched, and the world was never rerun at the step-safe step. The r3 control shows that the reproduction under it vanishes there. | threads/particle-life/screens/P_half_types.png (no pack) | unchanged; dt-map flag reinforced |
| sporecell2-gate β=1 (r2; showcase) | L2; L3, L4a and L6[L2] Weak; L6[L3] Contradicted | medium | `movies/showcase_frame.png` (t=120): ringed cyan and pink cells and one magenta spore burst. This is the thread's most life-like image, but the burst is overshoot on the dt=0.02 map, as FINAL.md says. | threads/particle-life/screens/gate5_s1_types.png | unchanged since r2 |
| sporecell (r1; + sporecell_damage) | L2; L3, L4a, L4c and L6[L2] Weak; numerical validity 0 | high (L2) | Ringed founders burst into spores, then freeze into a ~40-cell lattice, and the rings vanish population-wide at depletion. Free spores are 127/40/6 at dt 0.02/0.01/0.005. | threads/particle-life/packs/sporecell | unchanged since r2 |
| sporecell-gene (r1) | L2; L7 Contradicted; L6[L2] Weak | medium | Janus cells: the selection is within cells, at purity 0.55-0.88. | threads/particle-life/packs/sporecell-gene | unchanged since r1 |
| plife-m2 (r1) | L3 (known result, calibration) | medium | Concentric type shells form from random types in 3 seeds. The movers at 8.9-13.2 BL were never examined. | threads/particle-life/packs/plife-m2 | unchanged since r1 |

**Modifiers for sporecell3-det (consensus):**

| modifier | score |
|---|---|
| spontaneity | 3 |
| robustness | 1 |
| numerical validity | **1** |
| novelty | 1 |
| mechanism | 1 |
| beyond-diffusion | 1 |
| PhySim | 1 |

## Judges and arbitration

**Biologist (promise 4).** No rerun. They re-audited both `lineage2.json` files under strict birth rules and split the events by phase.
- They found seed 1's real chain #24→#33→#38/#42.
- They cropped `particles.png` (`judge-scratch/particle-life-r3-biologist/s1_br.png`).
- Their reading is a batch culture that reaches stationary phase and freezes, with no birth-death steady state.
- They called the twin's L7 Contradicted.

**Skeptic (promise 3).**
- **labkit rerun, new seed 23:** it timed out at frame ~84 of 120. Cost per frame rose 6x as the cores densified.
- **lineage2 driver, seed 23, t=0-50:** founders formed from noise, and genuine propagules appeared 2-4.8 units from living parents. But 6 of 20 parent-labelled NEW clusters were threshold flicker, sitting 0.09-0.39 from a parent that had dropped below smin one sample earlier.
- **Displacement bound:** the bound is active, with 5,219 clips, about 7% of sub-steps. Each clip rescales every particle's displacement while v is unchanged, so clipped motion is a global time warp, and dt/2 at a fixed dx_max does not test it.
- The skeptic overran the compute cap (about 8 minutes).

**Curator (promise 3).**
- Found the same artifacts (#12, #16, #90).
- **Why adults are sterile:** release needs fewer than 60 neighbours, and a mature core's surface particle has about 140, so only small clusters can shed. Of 5,769 detachments, about 0.2% become qualifying births.
- Seed-0 deaths differ by 44% between dt and dt/2, and the report does not flag it.
- Seven written rules have accumulated.
- The brief's non-reciprocal forces were never put to work.

**Arbitration.**
1. **Seed-1 depth.** I checked `seed1/lineage2.json`. #38 (t=50) and #42 (t=62) are NEW clusters carrying #33's clan label while #33 continues, so they are not flicker. #33 was born at t=42 from #24, which had 60 particles at the time and is itself a bud of founder #1. The biologist is right: a genuine 2-deep chain exists. It still stays **Weak**, for these reasons:
   - it is one chain on one seed, and the anti-Goodhart cap applies;
   - seed 0 reaches gen 1;
   - there are no strips;
   - the genealogy is reticulate;
   - there is no parent-size birth after t≈90.
2. **L7 twin.** Biologist: Contradicted; skeptic and curator: Weak.
   - In `TW_sel_s0_lin2.png` every solid line starts before t≈50. From there to t=300 only dotted fragments appear, while the count holds at ~30.
   - lineage2.png does not draw gen-None births (seed-0 #56 and #62, born t=56-64), so the picture alone is not proof.
   - Two counts settle it. The pack JSON has 1 qualifying birth after t=100. The twin's ledger counts 11 qualifying births in 300 t, fewer than the pack's 12 by t=200, so there is no birth wave in t=200-300.
   - As selection, the stationary-phase rise is therefore Contradicted. It is L5-type matter transfer and conversion (Weak). The colonization-phase gap is untested, because there is one pair. Overall **L7[L2] Weak**, low.
3. **Colonization only.** In `s1_br.png` one ringed pink founder at t≈60 becomes about 6 compact disks by t≈96. From t≈104 to 200 the same disks sit at the same pixels, and the loose germlings never compact. I confirmed it in both JSONs: after t=100, the largest dead cluster has 26 or 48 particles, and no body that reached 100 particles dies.
4. **Numerical validity: 1, not 2.** The bound was never varied, the deaths differ by 44%, and seed 1's births sit at the 20% limit. Release is a Poisson rule, so dt agreement of births is partly by construction.
5. **Evidence hygiene.** REPORT §2 ("no labkit v0.2 packs") contradicts §3. The dt/2, seed-11 and twin JSONs and `ledger.py` are not in the branch.

## What a future lab should do next

1. **Emergent release from non-reciprocal forces, tested against a symmetrized twin** (curator's design, with turnover added).
   - **Setup:**
     - Start from sporecell3 at k_det=0 with step-safe motion.
     - Make M a surface-differentiated type, produced where a C particle has few C neighbours, with A[C,M]=+1 and A[M,C]=−1, so that surface pairs propel themselves off the parent.
     - Run it against an arm with A set to (A+Aᵀ)/2.
     - Add whole-cell death at δ≈0.005-0.01 from a state-independent RNG.
     - Use seeds 0, 1, 2 and 11, T≥400, and one dx_max=0.025 arm.
   - **Pass:**
     - In t=150-400, the non-reciprocal arm reaches gen ≥2 on ≥3/4 seeds, with daughters at ≥50% of parent size.
     - Births agree within 20% at dx_max/2.
     - The symmetrized arm stays at gen ≤1.
     - Birth strips show propagules leaving under their own motion.
   - This is the thread's only untested beyond-diffusion lever. The plife-m2 movers are a starting point.
2. **Turnover on sporecell3-det, read with a flicker-proof lineage** (biologist and skeptic).
   - **Setup:**
     - Add whole-cell death or dilution.
     - Make conformity count same-clan neighbours only.
     - Run seeds 0, 1 and 11 at dt and dt/2 plus one dx_max/2 arm, T≥600.
   - **Pass:**
     - ≥3 parent-size births per 100 t after t=200.
     - Mature cells die.
     - Gen ≥3 after t=200, on 3/3 seeds.
   - Any L7 contrast comes only after this.
3. **Infrastructure.** Upstream to labkit:
   - bounded-displacement sub-stepping with a clip log;
   - an identity-based lineage with three rules: a birth whose parent merges into it is void, smin has hysteresis, and daughters must reach a size fraction of the parent.

## Cross-pollination (records for a future lab)

**Out**
- **Autopoiesis and chemotaxis-motility.** Two lineage audits:
  - void a birth whose parent merges into it within K samples;
  - let a cluster that dips below the size threshold and returns keep its identity.

  Between them, these two artifacts account for every gen-2 label on seed 0 here (`threads/particle-life/packs/sporecell3-det/seed0/lineage2.json`, #4/#12 and #82/#90). Apply the audit to membrane_evo's resealed disk-cut fragments and to preytrack's near-contact daughters.
- **Lenia-multichannel.** Another instance of the confluence freeze. A size-capped release rule (n_det<60) makes the adults sterile and immortal, so births stop at t≈90 while food falls 91%. The law: when immobile bodies pay no intrinsic cost, turnover ends at confluence.
- **All particle and clipped integrators.** Halve the displacement bound, not only dt.

**In**
- **chemotaxis-motility:** the 2x2 cross-taxis ablation (`packs/pursuit`), as the template for item 1.
- **autopoiesis:** `strip.py` (birth strips) and the `evotrack.py` identical-event death ledger (`packs/membrane_evo_up`), with its warning that a body-scale death operator becomes a reproduction channel.
- **lenia-multichannel:** the decay-turnover threshold (0.025 static, 0.03 cycles; `packs/mcfd-MIRd`) and `tools/branch_test.py` for a post-colonization L7 test.

## Rubric issues

1. **L6 propagules.** Fix the daughter size fraction at ≥50% of the parent's size. The tool's 15 particles is 5-10% of the parent.
2. **L6 lineage.** Require the parent-fusion void and smin hysteresis. Lineage plots must also draw births whose parent chain is broken (gen None), or state that they are lower bounds.
3. **L6 "repeatedly".** Report births by phase. Reproduction confined to colonization, with no parent-size births and no mature deaths in the stationary window, should be flagged and capped at low, mirroring the L7 rule.
4. **Numerics.** For clipped or bounded integrators, dt/2 at a fixed active bound is not a convergence test: halve the bound and report the clip counts. The r2 request to flag rungs on non-converged maps "(dt map)" is still not in the rubric.
5. **labkit.** It still reads 0 splits and max gen 0 on propagule worlds, and it lacks a per-step maximum-displacement record. Both belong to the lab, not to the thread.
