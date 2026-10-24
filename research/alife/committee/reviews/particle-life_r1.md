# Review: particle-life, sprint 1 (2026-10-24)

**Decision: CONTINUE, opening the closed box** (promise 6/10). **Headline:** `sporecell` is a spontaneous, reproducible **L2** world. Ringed founders form from about 20 random catalyst particles, shed single-particle spores that grow into parent-size cells, and every lineage link comes from matter identity. This is the lab's only propagule mode of reproduction. Everything above L2 is **Weak**, and the closed food pool explains every failure:
- The M ring is a food-contact label, and every cell loses it when food runs out.
- Reproduction is one burst (generation 2: 8/1/1) followed by a frozen lattice.
- The repair test turns the erased half into food at the wound.

`sporecell-gene` shows real selection among particles against a neutral control, but kinds do not breed true (**L7 Contradicted**).

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| sporecell | **L2**. L3, L4c and L6[L2] Weak; L5 Weak (not claimed) | high (L2) | `seed{0,1,2}/particles.png`: one-particle orange M rings around cyan cores at t≈52-146 in all seeds. Every ring is gone by t≈157, and the same ~40 cells persist without rings to t=240 (38-41 per seed; the skeptic's seed 11 gave 39). The biologist's movie strip (t=80-124) shows the founder staying intact while 8-10 daughters appear around it. Generation 1 has 40/34/36 daughters at parent size; generation 2 has 8/1/1, born after depletion and without rings. `screens/L_nomem_clans.png`: with the membrane off, cells form by t≈14 and reach the same lattice by t≈44. L4c: `abl_starve.png` covers one seed of the R2=1 variant, and the decline 488→226 equals the imposed decay. | threads/particle-life/packs/sporecell |
| sporecell (repair) | L4a **Weak** | medium | `screens/D_sporecell.png`: the half-cut cell re-rounds with a full ring by +6, then loses the ring by +36, as the control does. The cut puts a pile of food against the wound. In labkit's own disk cut (`packs/sporecell_damage/particles.png`, t=97→104) the cell is replaced by small separate clusters, and the report does not mention this. | threads/particle-life/packs/sporecell_damage |
| sporecell-gene | **L2**; L6[L2] Weak; **L7 Contradicted** | medium | Two-sector "Janus" cells from t≈180 (`screens/G_mu01_s1_types.png`). At t=400 the looser mutant makes up 7/10, 11/11 and 6/11 cells, against 3/9, 0/9 and 1/10 for the neutral control, but purity is 0.55-0.88 and parent-child agreement 0.58-0.93. The "gen 9" in `N_mu01_lineage.png` is a staircase of individuals that live 10-60 t. The evidence is at mu=0.01, while the pack runs at mu=0.002. | threads/particle-life/packs/sporecell-gene |
| plife-m2 | **L3** (known Mohr/Ventrella cells; calibration) | medium | Concentric type-sorted shells (white on a green core, pink on cyan) form from random types by t≈3.5 and persist to t=80 in 3 seeds. One matrix, a short run, no dt check. labkit flags movers at 8.9-13.2 BL that nobody has examined. | threads/particle-life/packs/plife-m2 |

## Judges and arbitration

**Biologist (promise 6).** Under this lens, every life-like property is conditional or thin. The best new evidence is the movie strip `judge-scratch/particle-life-r1-biologist/movie_s0_topleft.png`: the founder stays whole while daughters appear, so this is true spore shedding and not breakup. The biologist also found that labkit's damage pack contradicts the repair claim, and that the closed box is the root cause.

**Skeptic (promise 6).** Re-ran sporecell on seed 11, and the whole arc reproduced: a ringed founder at t≈42, spores at t≈77, about 35 ringed cells by t≈125, rings lost at t≈146, and 39 cells at t=160. A dt probe found a maximum step displacement of 0.158 at dt=0.02 against 0.038 at dt=0.01, about half the hard-core radius, so spore ejection may be under-resolved. The gene world's catalyst lookup has no kind bias. The starvation ablation used R2=1 (NOTEBOOK l.99), not the promoted world.

**Curator (promise 6).** Alone gave L3 Supported "while fed". Novelty is modest: PPS spores, Cabaret vesicles, and LITERATURE §2.3.5 idea 3 prescribes this recipe. The curator named three assets: propagule reproduction, exact matter provenance, and two-level selection, which is stochastic-corrector territory. The curator also found the ratchet in lineage.py: births follow the majority label and the largest fragment continues the parent. And every claim above L3 rests on custom screens rather than packs.

**Arbitration.**
1. *L3 (2 Weak, 1 Supported).* I examined `packs/sporecell/seed0/particles.png`. The rings are crisp on every fed cell, and between t=146 and t=157 they vanish from every cell at once while the cells live on. `L_nomem_clans.png` shows that individuality and reproduction do not need the ring; it only delays the burst. A layer the environment switches on and off for the whole population, with no work shown, does not "persist with the individual". Verdict: **Weak**. It becomes Supported if, under steady feeding, the ring lasts through each cell's life and the k_diff=0 arm differs in growth, spore release or death (the fisim r1 rule for readout membranes).
2. *L4a.* I examined `D_sporecell.png` and `sporecell_damage/particles.png`. The re-ring is real but follows by definition, and the labkit cut cell did not recover. It was mid-shedding, so that test is not clean either, but it should have been reported.
3. *Generation depth.* `N_mu01_lineage.png` confirms the ratchet: short-lived steps, and a cluster count that jumps between 6 and 14 from one sample to the next. The headline "gen 3-9" is withdrawn.

## Next sprint

**Main experiment: turnover with deaths in sporecell (B on). Does the spore life cycle repeat, and does the ring stay with the cell?**
- **(a) Screen** (T=300, seed 0). Compare two routes to turnover:
  - whole-cell dilution: remove a random cell at rate δ and return its particles as uniform food, at 2 values of δ;
  - a costlier dormancy: k_dec ∈ {0.02, 0.03, 0.05}. lenia-multichannel found μ=0.01 gives a static fed lattice and μ=0.03 gives cycles.

  Pick the setting that keeps food above the induction threshold, with births and deaths ongoing.
- **(b) Main runs.** The chosen setting and its k_diff=0 twin, 3 seeds each, at least 600 t.
- **(c) Merge-aware lineage.** A birth counts only if the daughter:
  - starts from ≤3 particles shed by the parent;
  - reaches ≥15 particles;
  - stays separate for ≥20 samples;
  - never re-merges.

  Log merges separately, and show strips of 5 random births at generation ≥3.

Report per seed:
- cell count over time;
- births and deaths per 100 t;
- maximum generation;
- the fraction of each cell's life spent with a complete ring;
- growth, spore and death rates, ring vs no-ring.

**Pass, in 3/3 seeds:**
- a stationary population;
- ≥5 merge-aware generations;
- a ring for ≥80% of each cell's life;
- the ring arm differs from k_diff=0.

That gives L6[L3] and L3 Supported. If the ring persists but changes nothing, L3 stays Weak, and giving M a job becomes the sprint-3 target: gated food crossing (lab convergence 1).

**Secondary goals**
1. **Repair in the fed steady state.** Cut mature, non-shedding cells by 30-50%, with both half-plane and disk cuts. Relocate the removed particles as uniform background food, compare against matched branched twins, and use 3 seeds.
2. **Numerics.** Rerun one main seed at dt=0.01 and run ±10% k_cat/k_dec on one seed.
3. **Heredity, only if the main experiment passes.** Use the spore as a bottleneck: μ ≤ 0.002, looser vs neutral arms, 3 seeds. Each cell grows from one spore, so it should be clonal.

All claims ship as labkit packs with the lineage JSON saved inside.

**Defer:** new membrane rules, closed-box gene runs, L4b screens, and the plife-m2 movers.

## Cross-pollination

- **Out:**
  - **autopoiesis and active-droplets:** neutral provenance labels. Split a kind into identical-dynamics labelled copies, or have new matter copy its catalyst's label as `sporecell` does (`lineage.py`). This measures directly how much of a cell's matter came from its parent versus its neighbours, which is the horizontal channel both threads must close.
  - **flow-lenia:** sporecell's single-particle propagules can be compared with the ring spores in fl_cells_food. Body repulsion (the B shell) stops merges that cut lineages, but without deaths it freezes the population.
- **In:**
  - lenia-multichannel's maintenance threshold (REPORT_r1 §4, `packs/mcfd-MIRd`);
  - active-droplets' within-droplet cross-inhibition β and neutral arm (REPORT_r1 Mechanism 4, `packs/ad5-evolve` vs `ad5n-neutral`);
  - autopoiesis's audit of conversions of intact cells per mutation, and phase_membrane's chi=0 test of whether the ring is load-bearing.

## Rubric issues

1. **L3, conditional layers.** A boundary type set by a local environment rule, which the whole population loses at once when the environment changes, is "conditional L3" and scores Weak. To be Supported it must persist through most of each individual's life, or an ablation must show that it does work.
2. **L6, propagules and matter-identity lineage.** Majority-label lineage with "largest continues" ratchets generations through split and re-merge cycles. Require a merge-aware persistence filter and strips of random births at the deepest generation claimed.
3. **L4a.** "Erased" matter must leave the individual's reach (deleted, or relocated as background), not be turned into its resource at the wound. The target must be mature and not reproducing.
4. **labkit, particle worlds.** The 128² raster (1.5 px smoothing) cannot see one-particle rings or single-particle spores: 0 splits, 0 holes, and M in the core about equal to M in the rim. labkit needs:
   - per-type radial profiles computed from `particles()`;
   - matter-identity lineage (port `lineage.py` with the merge filter);
   - a particle damage hook that removes particles.
