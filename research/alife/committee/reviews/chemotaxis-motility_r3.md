# Review: chemotaxis-motility, sprint 3 (2026-10-24)

**Decision: STOP. The program ends, and this is the thread's final record** (promise 7/10).

This review supersedes the provisional r3 record of 20:42, which was written before the judges had seen REPORT_r3 and the ledger. Its "L6 Supported (low)" for evopursuit is withdrawn.

**Headline.** evopursuit closes as the lab's clearest eco-evolutionary interaction, at **L5[L2]+L4b with high confidence**.
- Across 18 matched fixed-allele arms, consuming predators are lethal to ancestral A prey (0.15-0.36x the prey-alone mass) and a net benefit to evasive B prey (2.4-3.5x).
- The predators themselves grow on B (1.75-1.88x) and collapse on A (0.20-0.32x).

The heredity side does not hold up as well as the report says.
- The ledger counts daughters, not events: there are 23 clean B fission events, not 46, against 28 A→B conversions.
- The tracker can credit near-contacts as fissions.
- Most of the ~90 B bodies gained come from births nobody classified.

**L6 and L7 in evopursuit stay Weak (near-Supported).**

## Final consensus (all sprints)

| world | final judged rung | conf. | key observation | pack | moved since earlier reviews |
|---|---|---|---|---|---|
| evopursuit (+ arms_\*, preytrack_\*, _neutral, _nopred, _dthalf, _cost\*) | **L5[L2]+L4b**; L6 Weak; L7 Weak (both near-Supported); L3 Contradicted | high (L5) | **Sheets.** `arms_B_pred_s0`: ~30-35 orange crescents, each cupping a magenta predator, from t=204 to 1500. A+pred thins to ~4-5 pairs.<br>**Prey mass, t1500/t150 (3/3 seeds each).** B+pred 1.28-1.32, B alone 0.36-0.54, A+pred 0.11-0.15, A alone 0.41-0.76.<br>**Skeptic, seed 11 at 96².** Reproduces the order: B+esc 2.19 > B+pred 1.55 > B alone 0.57. Clip mass ≤0.005.<br>**Ledger.** Net conversion +5 (28 A→B vs 23 B→A) against ~90 B bodies gained. 23 clean B fission events; strict generation 3/2/4. | threads/chemotaxis-motility/packs/evopursuit (+ packs/arms_B_pred_s0, packs/arms_summary.md, packs/preytrack_evopursuit_s*) | L5 confidence medium → high. L6 and L7 unchanged (Weak) since r2, now traced by a flawed ledger. |
| swimfission | **L6[L2]+L4b**; L4c Weak | medium | Waist pinch into two equal ovals that swim apart. Strict rule: 10/10/15 clean fissions and generation 3/3/3. dt/2 reaches generation 3, with the first five fission times identical. Reticulate: merges 56/56/45 > splits 45/39/31. The "strict" strips are byte-identical to the r2 founder strips (md5). | threads/chemotaxis-motility/packs/swimfission | Rung unchanged since r2. Credited depth is 3 (4/3/5 is not credited). dt/2 passed. |
| kstrail | **L4b[L2]**; L3 Weak | high | Noise → spot → ring → crescent. chi_h=0 gives static spots. Passes dt/2 and 2x resolution. Coarsens by t=1800. | threads/chemotaxis-motility/packs/kstrail | unchanged since r1 |
| pursuit | **L4b[L2]**; L5 Weak | high | Chaser-in-rear composites; the 2x2 ablation shows that pursuit binds. Species are conserved. | threads/chemotaxis-motility/packs/pursuit | unchanged since r1 |
| toxforage | **L4b[L2]**; L4c Weak (near-Supported); L4a Weak | medium | Toxic self-trail sets body size and keeps 9-14 swimmers with turnover. The n=0 fork was run on 1 seed only. | threads/chemotaxis-motility/packs/toxforage | unchanged since r1 |
| ecology | **L4b[L2]**; L5 Weak | medium | Prey-predator composites. The matched decomposition that L5 was provisional on ran in evopursuit, not here. | threads/chemotaxis-motility/packs/ecology | L5[L2] low (r1, provisional) → L4b[L2] |
| swimevo | **L6[L2]**; L7 Weak | low | Growth-rate allele with ~10 bodies per run. Superseded. | threads/chemotaxis-motility/packs/swimevo | unchanged since r2 |

**evopursuit modifiers.** Spontaneity 3, robustness 2, numerics 2, novelty 2, mechanism 2, beyond-diffusion 1, PhySim 3.

**Showcase.** `movies/showcase.mp4` at t≈1450 shows A0/B45 prey, and every orange crescent carries a magenta rider. The mass strip shows predators dipping, then rising with B. It reads without explanation.

## Judges

**Biologist (promise 7)** saw real motile individuals with a consistent prey-rider plan and a matched genotype-by-environment reversal: B ≤ A alone in 3/3 seeds, B ≫ A with predators. Checks on the saved evidence:
- Recomputed the 18 arms from metrics.json. The prey-alone arms are still declining at t=1500, so the chase ratios depend on run length.
- Showed that the "strict" swimfission strips are the r2 strips.
- Judged about 5 of 10 B-birth strips to be clean, and noted that a neighbour touches at division in s2 rows 2-3.

**Skeptic (promise 7)** reran, on seed 11 at 96² to t=600:
- **Arm ordering.** Reproduced B+esc > B+pred > B alone, with 12.2 / 13.5 / 5.7 bodies.
- **dt/2 of B+esc.** Agrees to t=204 (995.8 vs 995.0).
- **Clipping log at 64².** Clipping creates 0.002-0.005 of mass against prey totals of 198-542, which rules out a positivity artifact.
- **Colour.** The white and cyan in the B arms is preyA at ~1e-5, stretched by a per-channel colour scale.
- **Code.** In preytrack.py, a body linked to two parents is still added to `children_of[P]`, so it can pass as a fission daughter.

**Curator (promise 7)** factored B's advantage, and alone rated L6 Supported (low).
- Per seed, B+pred/A+pred = 8.7/11.2/11.5. That splits into a cost when alone (0.72-0.89), a larger chase gain (1.7-2.8) and better retention under consumption (5.8-6.2).
- Novelty 2: evasion evolving under predation, drift-bifurcation spots and chaser-fleer pairs all have precedents. The positive non-consumptive chase benefit in emergent dividing bodies does not.

**Arbitration.**
1. **L6 in evopursuit is Weak (2-1, and my own image check).** I viewed all 10 random deepest-generation strips.
   - Clean pinches: s0 row 1, s1 rows 1 and 3, s2 row 1. Plausible: s0 row 2, and s1 row 2 (an S-body that breaks into a crescent and a blob).
   - s1 row 4 and s2 rows 2-4 involve a second body that is present before the event or fuses at it.
   - The deepest chain (s2, generation 4) runs through those rows.
   - There is no merge/split ratio. labkit, species-separated, gives 58 merges vs 50 splits in `arms_B_pred_s0`.
   - My seed-11 ledger (128², t=1500) has 2 clean B fission events, all from generation-0 parents, while B rises from 0 to 22.
2. **L7 is Weak (unanimous).** The evidence cuts both ways.
   - *For:* the sweep is demographic, not contagion. Net conversion is +5 over 3 seeds (−2 on seed 11) against ~90 B bodies gained, and there were 0/3 sweeps neutral and 0/3 without predators.
   - *Against:* per event, clean fissions run 0.8x conversions (23 vs 28), not 1.6x. B deaths total 158 over 3 seeds, and the replacements are unclassified.
   - *Against:* the 49-px swap disc exceeds the median body it hits (35-47 px). It flips 0.55-0.76 bodies per event, and its rate is set per domain.
   - *Against:* there is no identical-event twin, and deaths are not split into eaten vs toxin.
3. **Framing: I side with the curator against the report's headline.** The report says B "does not win by escaping".
   - In fact, B beats A mainly by losing far less to consumption, and only secondarily by gaining more from the chase.
   - What stands, and is new, is the **sign flip**: with B the predator is a net benefactor, with A it is lethal.
   - Caveats: partner abundance is unmatched (escorts fixed at 1.0x, predators 0.2-1.9x). B+escort bodies are amoeboid and fuse (sheet), so individuality is weakest where the benefit is largest.
4. **swimfission L6 stands at medium.** Deepest-generation strips are still not shown, and the genealogy is reticulate.

## What a future lab should do next
1. **Close evopursuit's L7 with a correct, closed ledger and an identical-event twin.**
   - Flip whole bodies chosen by identity, from a state-independent RNG, and replay the same events at e=cost=0.
   - Fix preytrack: a merge product can never be a daughter, daughters need ≥25% of parent mass and must survive ≥200 t, and births are counted per event.
   - Classify every origin and every end; split deaths into eaten vs toxin.
   - Check that final + deaths = sources, and report per-capita birth − death per kind and per arm.
2. **Name the chase benefit.**
   - Arms: speed-matched lone prey (chi_h raised); a non-chasing escort (chi_y=0) at the predators' realized abundance; and a k→0 titration (the report's untested prediction).
   - Readouts: toxin and food under each body.
   - If speed alone reproduces the gain, the law is "motility is a self-toxin homeostat", and it transfers.
3. **Numerics and beyond-diffusion.**
   - Run evopursuit and swimfission at 1.5-2x resolution with lengths scaled.
   - Run the matched Laplacian-only slow-inhibitor twin of kstrail. It has been owed for 3 sprints, so beyond-diffusion stays at 1 for the whole thread.

## Cross-pollination
- **Out, to autopoiesis:** harmless chasers multiply prey (B 2.4-2.5x, A 1.2-1.6x, against 0.36-0.76x alone) and raise prey speed from 0.27 to 0.41 px/t. Test whether this is the motile_trait_tox law.
- **Out, to flow-lenia (fl_predator):** the fixed-kind × {consuming, non-consuming, none} decomposition, comparing kinds on each component. The sign flip appears only there.
- **Out, to particle-life:** add a non-lysing contact-partner arm to sporecell2-lysis.
- **Out, to active-droplets and lenia-multichannel:** compare the net conversion flux with the winner's final count, and count births per event.
- **Out, to fisim:** an allele carried by the body flux breeds true in motile dividers (1 off-kind daughter in 50).
- **In:**
  - autopoiesis membrane_evo identical-event twin plus `evotrack.py`;
  - the autopoiesis r3 skeptic's birth-cause classifier;
  - fisim's +10/+30 t daughter purity;
  - flow-lenia's Price split.

## Rubric issues
1. **L7 under symmetric whole-body mutation.** Require a per-event birth count, a closed demographic budget (final + deaths = sources) and net conversion flux against the winner's final count. "Births ≫ conversions" counted per daughter is mis-posed.
2. **L6 lineage.** A daughter must not be linked to ≥2 parents and must carry ≥25% of the parent's mass. Strips must be regenerated from the run claimed, not reused.
3. **L5 decompositions.** Compare kinds on each component and match partner abundance. Report time courses when a control arm is not at steady state.
4. **labkit.**
   - Per-channel colour scales turn ~1e-5 channels into visible bodies.
   - Motion and lineage fail in crowded multispecies worlds (0 persistent splits, 1300-1500 tracks).
   - Port the 2-t, species-aware tracker into labkit once the merge-daughter bug is fixed.
