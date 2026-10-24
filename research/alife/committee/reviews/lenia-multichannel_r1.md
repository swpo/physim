# Review: lenia-multichannel, sprint 1 (2026-10-24)

**Decision: CONTINUE, redirected from cycle refinement to heredity** (promise 6/10). **Headline:** Chan's MIRd+ replicators were given a build-from-food metabolism with a maintenance cost. The result is a solid **L6[L2] + L4c + L5** (medium confidence). However, the headline "sustained consumer-resource cycle" is really intermittent food-driven boom-bust near the dormant-lattice boundary, and every L4+ result uses planted Chan creatures. The spontaneous r-two56 cells are a static but numerically sound **L3**, and they are better converged than the researcher reported. Next sprint: an L7 attempt on the fed line, with a metabolic trait, a neutral arm and an audit of horizontal transfer.

## Consensus

| world | judged rung | conf. | key observation | pack |
|---|---|---|---|---|
| mcfd-MIRd | **L6[L2] + L4c + L5**; L3 Weak | medium | Pack lineage reads gen 0, which is a tracker failure. The biologist's dense re-simulation of seed 2 (`judge-scratch/lenia-multichannel-r1-biologist/viz/mcfd_seed2_divisions.png`, which I examined) shows two binary fissions during regrowth after a trough (t=548-560, t=569-579). Both daughters re-form the white/cyan core, orange cap and dots. Population goes 4→17 in ~100 t. Seed 2 shows 4 booms with food in antiphase. Every judge seed persists (seed 11: t=1400-2200; seed 12: t=1600). In seed 11 the population sat ~650 t as a static fed lattice, and its troughs reach 2 cells. | threads/lenia-multichannel/packs/mcfd-MIRd |
| mcf-MIRd | **L6[L2] + L4c**; L5 Weak; L3 Weak | high | 6 persistent splits and gen 3 in seeds 0 and 2. Without food the same creature reaches gen 4 (mc-MIRd). Norefill goes extinct in 3/3 seeds by t≈230-310, against 11-16 survivors with refill. Only one boom and decline occurs in 400 t. | threads/lenia-multichannel/packs/mcf-MIRd (+ mcf-MIRd-norefill) |
| mcf-fastcell | **L4b[L3] + L4c** | medium | 3-4 cyan-shelled gliders travel 8-15 BL in 3 seeds (seed 11: 5.3 BL). Radial profile (biologist): A2 nucleus, A1 ring at r≈6-7, A0 shell at r 14-22, with A0=0 inside r<8. Norefill leaves 0/0/1 survivors against 3/4/3. The glider is planted, there is baseline attrition without food, and no dt/R test was run. | threads/lenia-multichannel/packs/mcf-fastcell |
| r-two56 | **L3** (spontaneous, static); L4a Contradicted | high | Cog cells (white centre, cyan core, orange shell) form from noise in 3 pack seeds plus 3 judge seeds. They stay unchanged to t=400-500. At dt/2 from noise, 6 cells remain. Formed cells survive at R=15/288² and R=20/384² with the same ~10 teeth (`judge-scratch/lenia-multichannel-r1-physicist/res_compare.png`, examined). The parameter island is narrow (1/5 jitter draws). There is no turnover, division or core repair. | threads/lenia-multichannel/packs/r-two56 |
| r-two-s1-60 | **L4b[L2]**; L5 Weak | medium | C-gliders peel off a jammed crowd of ~45 bodies and travel 3.0-3.8 BL. The second channel is dead by t≈2-6, and the constant-k5 ablation keeps the glider, so this is the known single-channel class. The bricks are grid-aligned. | threads/lenia-multichannel/packs/r-two-s1-60 |
| eco-MIRd-Rplus | L6[L2] (inherited); L5 Weak; L4c Not tested | low | Both species persist in 3/3 seeds to t=300. The long run has 1 seed, the starts are unequal, the exclusion term is imposed, and there are no per-species counts. | threads/lenia-multichannel/packs/eco-MIRd-Rplus |

## Judges

**Biologist (promise 7).** Did the decisive L6 work. Re-simulating densely shows real fissions deep in the lineage, and re-tracking with K=20 frames recovers gen 2 where labkit (K = 10% of the run) reads 0. Radial profiles over hundreds of cell-frames separate a real membrane (the fast-cell A0 shell, 0 inside, peak at r 14-22) from texture: the MIRd+ "dotted halo" is single-pixel saturated dots at R=15, and the cap is an open crescent. For that reason MIRd+ is qualified as [L2], not [L3]. I accept both points; the biologist's heredity design is the basis of the main experiment.

**Skeptic (promise 6).** Did the decisive numerics. (1) On a new seed (11), mcfd persists, but it holds a near-static lattice from t≈190 to 870, crashes to 2-3 cells, and regrows. Peak spacing across pack seeds is 530/290/260. The lag-0 matter/food anticorrelation (−0.84) is built in by fixed-yield accounting. (2) r-two56 converges: from noise at dt/2 it keeps 6 cells, and in a continuation at 1.5x and 2x resolution the formed cells keep their morphology and tooth count. **Disagreements.** The skeptic rated mcfd L5 Weak and the other two rated it Supported. I examined seed 2's timeseries (4 clean booms) and the skeptic's seed-11 timeseries (plateau, then crash). **Ruling:** L5 is Supported because competition for a shared resource sets the population dynamics, repeatably. Without food the colony fills the grid, with norefill it dies, and decay 0 / 0.01 / 0.03 gives dormant / fed static / boom-bust. Each regime appears across 3 pack seeds and 4 judge runs. The researcher's specific claim of a "sustained regular cycle that abolishes dormancy" is **not supported**. It should be restated as intermittent boom-bust near a bifurcation. On r-two56 numerics I side with the skeptic against the biologist's "lattice effect": the tooth count scales with R, not with pixels. Formation from noise at R≥15 is still untested.

**Curator (promise 5).** Rated mcfd L6 Weak on the strength of labkit's 0 splits. I overrule this using the dense division strip above. eco-MIRd-Rplus was rated L2, which I raise to L6[L2] at low confidence, since both replicators divide (gen 2 in 2 seeds); the world's own claim (L5) remains Weak. I accept the curator's main points. Build-from-food plus decay has the structure of a Gray-Scott chemostat, so the cycle is generic consumer-resource ecology, and the nonlocal kernel only supplies the individuals; beyond-diffusion leverage is modest. This thread's distinct assets are (a) the "free dormancy" mechanism (turnover-charged metabolism makes jammed bodies free) and (b) the cross-kernel distance-set-point membrane of r-two56. Its own item 1 (period and amplitude vs rho, μ, D) is refinement and is not funded.

## Next sprint

**Main experiment: heredity and selection on mcfd-MIRd (L7 attempt).** Use 192², decay 0.03 and rho 0.02 (20-28 cells with continuous turnover).
1. Add a discrete allele field a(x) carried by A-matter. Newly built matter takes the *kernel-weighted majority* allele of the matter that built it. Do not average: flow-lenia and Michel et al. found that averaging erases evolutionary activity.
2. Make allele 1 metabolic, not a kernel parameter: yield Y×1.15 or maintenance μ×0.85, whichever leaves morphology unchanged in a T=300 monoculture check.
3. Mutation is a rare event that flips one whole cell (a connected A0 component), so that within-cell majority cannot erase it. Use ~5-10% of cells per 1000 t, with nothing planted.
4. Run two arms, 3 seeds each, t≥2000 (3000 if affordable): **S** (allele 1 has its effect) and **N** (label only, same mutation rate).
5. Readouts:
   - allele as a sheet colour;
   - mass-weighted allele fraction vs time;
   - per-division inheritance from dense frames with fixed K≈20 frames;
   - allele changes of living cells without division, against mutation events (the autopoiesis contagion audit).

**Pass:** allele 1 arises during the run, ≥90% of divisions breed true, conversions ≤ mutations, and allele 1 rises in 3/3 S seeds beyond the spread of N. **Equally decisive fail:** alleles leak across touching halos (conversions ≫ mutations). Report that as a law and try confining the allele with an r-two56-style shell.

**Secondary goals**
1. **Is the cycle real?** Reuse the N arm's matter series, and add 2 seeds at 256² and one dt/2 run at 192². Report the minimum count, extinction times, and the spectral peak and relative amplitude vs grid area. If the amplitude falls like 1/√area, call it demographic noise.
2. **Put r-two56 on the metabolism.** Use build-from-food plus decay μ∈{0.01, 0.03}. Shelled cells that form from noise and must eat would be a spontaneous L4c[L3], and the thread's most distinctive possible result. Watch for core-starvation fission. Retest formation at R=15 with noise smoothed on the kernel scale.

**Stop:** cycle parameter sweeps, random-graph screens, and the r-two-s1-* worlds. **Pause:** eco-MIRd-Rplus until the S/N arms exist.

## Cross-pollination

- **Out:**
  - particle-life, active-droplets and autopoiesis: populations frozen into lattices need a *maintenance decay* rebuilt from food. Expect a sharp threshold (0.025 static vs 0.03 boom-bust).
  - flow-lenia and fisim-beyond-laplacian: the r-two56 ring-kernel set-point membrane (k4 places the shell where ring-sensed core density ≈0.23; k5 feeds the core; k0 caps size; `threads/lenia-multichannel/screens/r-two56_ablations.png`).
- **In:**
  - active-droplets: cell-scale mutation, neutral arm and argmax alleles (`threads/active-droplets/packs/ad5-evolve`, `ad5n-neutral`);
  - autopoiesis: horizontal-transfer audit (`threads/autopoiesis/packs/phase_kinds`; `committee/reviews/autopoiesis_r1.md`);
  - flow-lenia: the negotiation rule, and why (m,s,h) competition was near-neutral (`threads/flow-lenia/REPORT_r1.md` §4);
  - fisim-beyond-laplacian: per-division kinds accounting (`threads/fisim-beyond-laplacian/packs/xcell-her/seed0/kinds.json`).

## Rubric issues

1. **labkit lineage.** `lineage_stats` uses K = 10% of n_frames, so long runs with turnover read 0 persistent splits despite visible fission (mcfd: K = 140 t). Use an absolute K tied to division time, and do not end a lineage at a brief merge.
2. **labkit rim metrics.** These follow only the `matter` channel, so the claimed membrane channel (fast-cell A0 shell, MIRd+ halo) is outside the mask. FACTS should report per-channel radial profiles per tracked cell (as in the biologist's `viz/radial.py`).
3. **L3 in kernel worlds.** Boundary features of 1-2 px, well below the kernel scale, should not count unless they survive a 1.5x resolution continuation.
4. **L4c ablations.** These must be run on the world claimed: the mcfd evidence came from the parent world without decay.
5. **L5 oscillation claims.** These need peak spacing reported across ≥3 seeds and a grid-size check before being called a cycle.
