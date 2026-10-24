# Review: flow-lenia, sprint 3 (2026-10-24)

**Decision: STOP. The program ends; this is the thread's final record** (promise 5/10).

**Headline.** The researcher ran the level-of-selection audit as commissioned (identical-event twins on their own RNG stream, an exact Price identity, a per-kind ledger) and withdrew their own L7. **L7 is Contradicted for the uptake gene** (unanimous). The report misreads its own split in two places, though:
- **"Fusion spreads the gene" is a bookkeeping artefact.** Fused mass is credited to the main parent in the between term and corrected in the fusion term, so the two terms anti-correlate (r = −0.90 over 15 runs). Taken together, the body-level term's paired S−N excess is small: +0.09/0.00/+0.41/+0.25/+0.08, mean +0.17. The within-body term carries most of the shift: +0.44/+0.44/−0.38/+1.07/+0.25, mean +0.36.
- **"Births < conversions" compares gross flicker with persistent births.** Net conversions into high g are within ±3 in 13/15 runs, and −13 in S_s0 (51 in, 64 out). So the gene does not spread by contagion between individuals. It spreads by turnover inside mosaic bodies, and no body dies (0 deaths in 13/15 runs).

No thread-level rung moved. The line ends at **fl_forager L6[L2]+L4b** (r1). fl_predator stays at L4b[L2] with L5 Weak, and its r2 qualifier "near-Supported" is withdrawn.

## Final consensus (all sprints)

| world | final rung | conf. | key observation | pack | moved? |
|---|---|---|---|---|---|
| fl_forager | **L6[L2]+L4b**; L4c, L5, L3 Weak | medium | One noise patch becomes 8-14 motile crescents with food wakes. 0 nucleations in 4 seeds, 2-generation chains in 3 seeds, and propulsion is emergent. Merges ≈80% of splits. At 2x resolution the gliders and division hold, but crescents become ring-in-halo bodies. The r3 gene2 S seed-0 sheet (t=104-944) shows the same gliders. | threads/flow-lenia/packs/fl_forager | unchanged since r1 |
| fl_forager_gene2 (S vs identical-event N) | **L4b[L2]**; L7 Contradicted; L6, L5, L3 Weak | medium (rung) | Paired S−N +0.54/+0.43/+0.03/+1.32/+0.33. The within-body term dominates (above), and there are no high-g deaths in any of the 15 runs. labkit: 0 persistent splits at K=t160, merge/split 0.90. S_s1 and S_s3 end as 1-2 static giants. Neutral N_s3 fuses an orange and a cyan cell, and cyan takes the giant over from inside (`evo3/sheet_N_s3.png`, t≈1148-2400). | threads/flow-lenia/packs/fl_forager_gene2_S | L7 Weak, low (r2, as fl_forager_gene) → Contradicted |
| fl_forager_gene2 S_body (g_eff, σ=5 px) | **L2** (sheets only); L7 Contradicted; L4b, L5 Weak | low | S_body−N +0.57/+0.25/+0.16/−0.17/+0.35. 2 final bodies in 3/5 seeds, with mosaic giants in `sheet_Sb_s1` from t≥1880. σ=5 px is smaller than the 30-60 px giants, so the hypothesis went untested exactly where takeover happens. | threads/flow-lenia/evo3/sheet_Sb_s1.png | new in r3 |
| fl_forager_gene (r2, rate-matched N) | L4b[L2]; L7 Contradicted (superseded by the gene2 audit) | medium | p=0.021. Seed 3: an undivided cell is taken over after a mutation patch (t≈780-940). | threads/flow-lenia/packs/fl_forager_gene | L7 Weak → Contradicted |
| fl_predator | **L4b[L2]** (prey only); L5 Weak; L4c Weak | medium | Engulfment repeats: seed 0 #355/#395/#497; skeptic seed 12 at t=304/536/800. Coexistence survives the early crash in 4/5 seeds (0, 1, 2, 12), but seed 12 is truncated at t=880 and seed 11 loses its predators at t≈704. Matched arms exist only on seed 11, where the prey-only arm is not mass-matched: the +274 prey gap ≈ 277 units of predator mass, so the predators' effect on prey is ≈0 or positive there. Sensing is imposed σ-12 blur, and only 1 of 9 parameter points coexists. | threads/flow-lenia/packs/fl_predator (arms: packs/fl_predator_{noflee,nochase,preyonly}/seed11; movies/showcase.mp4) | L5 "Weak (near-Supported)" → Weak |
| fl_predator_gene | as fl_predator; L7 Contradicted | low | All arms drift upward (+0.16..+0.29). | threads/flow-lenia/evo2/pgene.png | unchanged since r2 |
| fl_cells (+damage) | **L4a[L3]** | medium | A 1.5-px A1 ring that is 0 inside and out, converged at 2x resolution. 38-44% cuts re-form against twins on 3 seeds, leaving a smaller cell with a hollow core. Static. | threads/flow-lenia/packs/fl_cells_damage | unchanged since r1 |
| fl_cells_food | L2; L6[L3] Contradicted | medium | A "morula", then the A1 dots tile the domain; 257 nucleations. | threads/flow-lenia/packs/fl_cells_food | unchanged since r1 |
| fl_morph257 | L2; L5, L4b, L6 Weak | low | Ring and crescent sorting with cupped pairs. One seed. | threads/flow-lenia/packs/fl_morph257 | unchanged since r1 |
| fl_forager_mut / fl_forager_evo | L2; L7 Weak / Contradicted | low / medium | Turnover matches the neutral twin, and the 40-run tournament is a coin flip. | threads/flow-lenia/packs/fl_forager_mut, packs/fl_forager_evo | unchanged since r1 |

## Judges and arbitration

**Biologist (promise 5)** ran no simulation and re-analysed `audit.json` instead.
- Combined between+fusion and found the body-level residual.
- Found that the audit's "persistent" window is t=40, 4x shorter than labkit's.
- Showed that origin walk-backs cannot separate 18 fusions from one inherited fusion.
- Showed that high g wins 92/139 inter-kind fusions in S_s0 against 27/78 in its twin.
- Reading: genes behave "like clones in a syncytium".

**Skeptic (promise 5)** reran fl_predator on a new seed 12 (128², t=880, 294 s).
- Mass is conserved to float16 precision.
- Predators fall 289→45 by t=144, then recover to 269 at t≈440 after a prey peak of 735 at t≈240. A second prey peak (729, t≈720) is followed by a predator rise (89→206).
- Independently found r(between, fusion) = −0.90 and the unmatched prey-only mass.

**Curator (promise 4)** said not to enter "infection" as an L5 result.
- Showed that conversions are as frequent in N as in S.
- Placed novelty against Plantec et al. 2025, autopoiesis' infection law and chemotaxis-motility evopursuit.
- Argued that the glider-versus-giant regime, not fusion itself, is the control variable.

**Arbitration.**
1. **Mechanism of the sweep.** I re-tabulated the 15-run ledger and examined the sheets. In `evo3/sheet_S_s0.png` the body count holds at ~15-20 small gliders. Orange first appears as patches on pale bodies, and at t=1984-2400 many orange bodies still carry pale lobes, so colour changes inside living bodies. `sheet_N_s3.png` shows fusion and a takeover from inside under pure drift.
   - **Ruling:** L7 is Contradicted on the grounds of within-body change plus no deaths, not on the grounds of fusion or contagion.
   - The curator's "+0.92 between-body excess" in seed 0 is the bookkeeping artefact; combined with fusion it is +0.09.
   - For gene2, L5 stays Weak and the label "infection" is rejected. The gene wins inside mosaic bodies and biases fusion outcomes, but fusion was never ablated.
2. **Residual for the record.** In S_body the paired within-body excess shrinks to a mean of +0.05 (from +0.36 in S). The body-level excess is largest in the two seeds that stayed many-bodied (Sb_s2 +0.48, Sb_s4 +0.33), against +0.09/−0.06 in the giant seeds s0/s1. This is suggestive only: 5 seeds, births not normalised by body-time, and an N_s2 outlier. It agrees with the curator's view of the regime.
3. **fl_predator sign.** The judges' readings agree: a positive subsidy (biologist, curator) and ≈0 once mass-matched (skeptic) both mean the reference predator is not harmful to prey on the only matched seed. That is a sign flip against flee=0, so L5 stays Weak.
   - Showcase sheet: ~30 cyan prey on dark eaten food by t≈656-872. Orange predators are glowing blobs with comet tails, with rings closing on prey at t≈1960. They look pulled along a field, not self-propelled.

## What a future lab should do next

1. **Branch-point assay in the glider regime** (curator's design, built on lenia-multichannel r3's `tools/branch_test.py`).
   - From neutral seed-0-like states at 5 times between t=800 and 1600, flip 3 random whole gliders (coverage 1.0, plus contact founders) and run S/N for 500 t.
   - Use a per-component mean-g phenotype and a t≥160 persistence window.
   - Record per-kind births and deaths per body-time, gross and net conversions, a coalescent check, and between+fusion booked together.
   - Pass if S>N in ≥8/10 informative pairs, high-g births exceed net conversions, and the within-body term stays ≈0.
2. **Anti-fusion plus a death channel.** Add cross-body pressure from blurred other-label matter, and make starvation dissolution visible and counted.
   - Gate on the gene-off world: merge/split <0.5 and labkit persistent gen ≥2 on 3 seeds.
   - The behaviour must survive a 1.5-2x resolution continuation with kernels and flow scaled, which has been owed since r1.
   - Beware particle-life's frozen territory lattice.
3. **fl_predator done properly.**
   - 4 arms × ≥6 seeds, with a mass-matched prey-only arm (return the predators' mass as food).
   - Sensing made by the world: a secreted signal instead of imposed blur.
   - A domain of ≥256², peak spacing, and per-species segmentation.

## Cross-pollination

- **Out** (all records for a future lab):
  - *To all L7 threads, via labkit:* book fusion neutrally in any Price split, either by summing between+fusion or by treating fused partners as deaths and the product as a birth.
  - *lenia-multichannel:* confirmation of your gross-vs-net conversion rule. Here gross conversions run to 70 per run while net stays at ±3.
  - *chemotaxis-motility:* removal controls in mass-conserving worlds must return the removed mass, because a dying predator fertilises.
  - *particle-life:* use the identical-event twin plus the within/between split on sporecell-gene's within-cell spread.
- **In (record):**
  - lenia-multichannel r3: the branch assay;
  - autopoiesis r3: membrane_evo whole-cell flips with `evotrack.py`;
  - chemotaxis-motility r3: the fixed-allele decomposition (`packs/arms_summary.md`) for fl_predator;
  - active-droplets r3: exposure-normalised per-kind births and a power estimate.

## Rubric issues

1. **Price split with fusion.** "between > within+fusion" is ill-posed when fused mass goes to the main parent. Require between+fusion together, or a bookkeeping-neutral booking.
2. **L7 conversions.** Report gross and net conversions. Body-mean thresholds on mosaic bodies make conversions flicker in both directions.
3. **Persistence.** Persistence windows for births and generations must be stated in t and be at least labkit's K (t=160). The t=40 window gave pgen 3-7 where labkit gives gen 0.
4. **L5 controls.** In conserved-mass worlds, removal controls must be mass-matched.
5. **Somatic takeover.** Takeover inside one mosaic body is neither L7 nor L5 evidence on its own.
6. **labkit.** Flag render channels that split one material (the gene2 "membrane-like" radial flags are artefacts of the split), and add a per-body gene readout.
