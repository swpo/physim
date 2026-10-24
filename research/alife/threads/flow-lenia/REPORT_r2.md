# flow-lenia: sprint 2 report

## 1. Headline

**I forked the heritable-allele protocol of active-droplets and autopoiesis into the Flow-Lenia
foragers, and it shows selection that a neutral control does not.** Every parcel of matter
carries an uptake gene that travels with it through transport and division and mutates during
the run. With the gene active, the matter-weighted mean log g rises in 5/6 runs (to +0.34…+0.73).
With the gene as a neutral marker (same mutation process, no effect), it wanders around 0
(−0.24…+0.11). Mann-Whitney U = 31/36, one-sided p≈0.008, over 6+6 runs. What wins is not a
better glider: fast eaters overgrow into large, slow multi-ring cells.

**Second result: a predator-prey ecology of gliders** (`fl_predator`). Predator gliders chase
prey gliders and absorb their mass; prey gliders flee and eat food. All 3 seeds coexist for the
whole run with 2-3 boom-and-crash prey cycles. Ablating the chase or the flee term ends in
extinction (of the predators, or of both species). This is the thread's movie:
`packs/fl_predator/seed0/movie.mp4`.

## 2. Claims

| world | claimed rung | strongest evidence (pack, time) | known weaknesses |
|---|---|---|---|
| `fl_forager_gene` | **L7[L2]** (heritable variation arising in-run, neutral control, ≥3 seeds) | `evo2/gene_all.png`: 6 selection runs vs 6 neutral runs, final mean log g as above. Trajectories rise steadily under selection and wander around 0 in the controls. `packs/fl_forager_gene/seed3` sheet: ancestral (white) matter is replaced by orange high-g lineages from t≈600; low-g (cyan) gliders vanish by t≈1100. | One selection seed fell (−0.17) after a bottleneck to 3-7 bodies. The variants are a continuous trait in one gene, mutated by an imposed rule (forked protocol). Winners lose motility (gigantism), so the "kind" that wins differs in morphology but has no new organization. |
| `fl_predator` | **L5[L2]** (predation with population cycles), L4b, L4c | `packs/fl_predator/seed{0,1,2}` sheet and movie: orange predators run down cyan gliders and absorb them. `populations.png`: prey peaks at t≈400-500 and 1900; predator peaks lag them, and both persist to t=2400 in 3/3 seeds (minimum predator matter 25-57). Ablations: `screens/abl_pred_nochase.png` (predators starve by t≈2700), `screens/abl_pred_noflee.png` (prey exterminated, then the predators; total extinction). | Predators are blobby, less coherent gliders than the prey. Chase and flee are imposed nonlocal sensing terms (a blurred field of the other species). Only one parameter point coexists among the 9 tried (knife edge). 128² holds only ~10-20 prey bodies. |
| `fl_predator_gene` (heritable prey flee gene) | L7 **not supported** | `evo2/pgene.png`: 3 selection vs 3 neutral runs (8000 steps). All 6 end with mean log f between +0.16 and +0.29, and coexistence holds in all 6. | No difference between selection and control. Both drift upward for a reason I have not found. |

## 3. Mechanisms learned

- **The forked allele protocol works in Flow-Lenia because transport by stochastic sampling
  keeps genes discrete inside bodies.** A body carries an exact copy of its parent's gene
  through division. Sprint 1's (m,s,h) variants were near-neutral (40 runs, no consistent
  winner). An uptake gene acts directly on the birth-death balance and is selected.
- **Selection on uptake trades motility for size.** High g grows bodies past the glider's
  preferred mass, so the winners are big multi-ring cells that sit in place. To keep motile
  winners, the next step is a maintenance cost that scales with body mass or with g.
- **Predator-prey coexistence needs pursuit and evasion.** Chase only: the predators find and
  exterminate the prey, then starve. Flee only: the predators starve. Coexistence comes from
  spatial refuges that the prey make by fleeing, plus predator decay (a maintenance cost).

## 4. Negative and open results

- Predator-prey: 8 of the 9 parameter points went extinct (`screens/pred_a`…`pred_i`).
- **Heritable prey flee gene** (`fl_predator_gene`): no selection signal. Selection gave +0.19, +0.16, +0.23; neutral gave +0.24, +0.25, +0.29. All runs drift upward, including the controls. That bias is unexplained: mutations are symmetric N(0, 0.3), and the same code centres on 0 in the uptake-gene controls. I need to find it before trusting any result from this world.
- **Maintenance-cost prediction failed.** With decay ∝ g^1.5, high g has a worse break-even food level (R*), so I predicted that mean log g would fall. It ended at +0.14, −0.23 and +0.32 (`evo2/gene_cost.log`), much like the runs without a cost. Selection on g is therefore not R*-driven; growth and division during the colonization phase are the likelier channel. Untested.

## 5. Next sprint

1. Find out what is actually selected in `fl_forager_gene`: per-lineage growth vs division vs survival, early vs late (the cost test says it is not R*). Then pick a cost that keeps motile winners.
2. Co-evolution: put a heritable chase gene in the predators as well as the flee gene in the
   prey, and look for arms-race signatures against neutral controls.
3. Replace the imposed blurred-field sensing with a field the bodies emit (a secreted signal
   that diffuses), so that chase and flee become chemotaxis in a world-made field.
4. Movie: a 256² predator-prey run (~4x the compute; ~18 min per seed).
