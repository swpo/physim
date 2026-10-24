# particle-life: sprint 2 report

## 0. Response to the committee's r1 review (it arrived at 17:37, 60 min into the sprint)

Sections 1–6 below were done on my own plan before the review arrived. In the remaining
~40 minutes I re-planned around the review's decision.

**Corrections accepted.**
- L3 for `sporecell` is Weak: the ring is a reversible food-contact label.
- Reproduction is L6[L2] Weak: generation 2 is 8/1/1 and the daughters are ringless.
- I withdraw "gen 3–9". `lineage.py`'s rule (the majority label is the parent and the largest fragment continues it) ratchets through split/re-merge, so sprint-2 generation counts are also upper bounds.
- L4a is Weak. My cut returns the removed particles as food at the wound. labkit's disk damage shattered its cell (t=97→104), which I omitted.
- L4c is Weak (one seed, R2=1).
- L7 for `sporecell-gene` is Contradicted.

**The dt concern is confirmed, and it is the key fact for the main experiment.** I ran the committee's requested dt check on the sprint-2 world (same engine, dt and rep as sporecell). Spore emission does not converge: mean free spores are 127 / 40 / 6 at dt = 0.02 / 0.01 / 0.005, and core noise or a softer core does not fix it (§5). The turnover experiment below therefore measures the dt=0.02 map. Making spore release dt-converged has to come before any L6[L3] or L7 claim can be Supported.

**Main experiment, step (a), done this sprint.** `worlds/sporecell-turnover`: sporecell with B on, plus whole-cell dilution (each cell is removed at rate δ and its particles return as uniform food). Screened at seed 0, T=300: k_dec ∈ {0.02, 0.03, 0.05} and δ ∈ {0.005, 0.02}. Results are in §0.1. Steps (b) and (c) (3+3 seeds at ≥600 t, merge-aware lineage with birth strips) were not done.

### 0.1 Turnover screen (main experiment step a; sporecell-turnover, seed 0, T=300, dt=0.02)

| setting | late free food (t≥150) | cells (t=50/100/200/300) | ringed-cell fraction (t≥150) | births / max gen |
|---|---|---|---|---|
| k_dec 0.02 | 1364 | 4/2/35/39 | 0.24 | 42 / 2 |
| k_dec 0.03 | 2954 | 6/3/4/40 | 0.81 (mostly before the burst) | 39 / 2 |
| k_dec 0.05 | 3923 | 5/2/1/1 | 1.00 (one cell) | 0 / 0 |
| δ 0.005 (k_dec 0.01) | 814 | 6/14/38/39 | 0.05 | 69 / 3 |
| δ 0.02 (k_dec 0.01) | 3978 | 3/0/0/0 (extinct) | – | 0 / 0 |

Ringed cell = more than 20% of its particles are M. Generation counts come from the old, ratcheting lineage rule.

**Reading.** No setting passes. Rings need free food above the induction threshold, and that requires a high maintenance cost or high dilution. But high cost or dilution keeps the population small or kills it.
- k_dec 0.03 holds rings while there are only 2–4 cells, then bursts to 40 cells at t≈250–300, which will deplete the food and strip the rings.
- Dilution δ=0.005 gives real deaths and the most births, but only 5% of cells are ringed.

There may be a narrow window around k_dec 0.025 or δ≈0.01. Finding it and running step (b) (3+3 seeds, ≥600 t, k_diff=0 twin) is the first task for sprint 3. Step (c) needs a merge-aware lineage, and the dt problem should be fixed first.


## 1. Headline

**Cell-level heredity from a single-particle spore bottleneck. It meets the lab's L7 bar at dt=0.02, but a dt-convergence check shows the spore emission behind it is mostly a numerical artifact.**

In `sporecell2`, core particles adopt the kind of their local majority, as in the brief's "types change by majority vote of neighbours". That erases mutants inside a cell, so a cell's kind is fixed when its spore germinates.

A faster-catalysing kind arises by mutation *during* the run, breeds true, and takes over in 3/3 seeds. A neutral mutant with the same mutation rate is founded about as often but never reproduces (3/3 seeds).

Forking the lab's gated-mobility operator into the food gives persistent thick membrane rings and a striking grow-then-burst spore life cycle (`screens/lifecycle.mp4`). Contact predation between kinds reverses competition, and works only from abundance (a priority effect).

## 2. Claims

Images first. Particle images use cyan for kind-0 core, magenta for kind-1 core, orange for membrane and grey/white for food. Labkit's `sheet.png` uses its own palette: kind-0 core orange, kind-1 core green, membrane magenta.

| world | claim | strongest evidence | known weaknesses |
|---|---|---|---|
| `sporecell2-sel` (selected) vs `sporecell2` (neutral, k_cat1=0.05) | **L7[L3]**, but numerics fail (§5) | **Takeover:** final kind-1/all cells at t=400 were 18/22, 8/21, 11/16 (selected) against 0/19, 0/22, 1/17 (neutral) on seeds 0/1/2. Neutral mutant cells were founded 2, 0, 1 times and had 0 births. **Per-capita births** per 100 cell-samples (k0 vs k1, selected): 0.8 vs 2.6, 1.9 vs 2.2, 1.0 vs 2.4. **Breeding true:** median cell purity 0.99–1.00; 64/66, 22/28 and 45/50 children of kind-1 parents are kind 1. **Images:** `packs/sporecell2-sel/seed{0,1,2}/sheet.png` (green cells take over from t≈100); `screens/K_sel_s*_types.png`, `screens/K_*_lineage.png`; movie `screens/K_sel_s0.mp4` | Only two kinds. Mutation per copy is high (mu=0.1); conformity hides it inside cells. A faster catalyst also wins its spore's founding majority more often, so selection acts at germination as well as on cell reproduction. Labkit cannot see spore births (0 splits); lineage comes from `lineage.py`, which tracks particle identity. Not robust to a 1.2× advantage. Spore emission does not converge in dt (§5). |
| `sporecell2`, gate β=1 | **L3** persistent membrane, **L4a** repair, **L6[L3]** | **Rings:** thick 2-layer M rings (membrane fraction 0.6–0.78) hold for more than 54 time units (`screens/D_gate.png`). **Repair:** a cut removing 50% of a cell's particles reseals within 6 time units, next to an undamaged control. **Life cycle:** ring cells grow, then burst into spore clouds (t≈110–175) that found bare daughters; gen 3/6/6 on seeds 0/1/2. `screens/gate5*_types.png`, movie `screens/lifecycle.mp4` | After the burst, free food falls below the induction level and daughters are bare, so the ring stage is still tied to food density. Many early cells die. Any higher maintenance cost (k_dec ≥ 0.015) kills everything. |
| `sporecell2` + contact lysis | **L5** predation between heritable kinds | Half/half seeds, final kind-1/all cells: with lysis 6/17, 12/13, 14/18; without lysis 1/18, 0/19, 2/12 (3/3 seeds). Territories with a killing front: `screens/P_half_types.png` | Predation is a written-in rule. Rare predators lose (0/17, 0/17, 2/15 at 15% seeding) and a mutant predator never invades, so the interaction is not reached by evolution. |

## 3. Mechanisms learned (with ablations)

1. **A genetic bottleneck needs in-cell conformity.**
   - Without the majority vote (sprint 1), mutant genes spread *inside* cells: purity was 0.55–0.75 and kinds did not breed true.
   - With the vote (k_conf=1): purity is 1.00, but mutants are erased before they leave, so at mu ≤ 0.05 no mutant cell is ever founded.
   - At mu=0.1, a kind-1 cell is founded when mutant copies win the majority in a germinating spore of a few particles. That happens about 1–8 times in about 65 births.
   - Weaker conformity (k_conf 0.03–0.1) leaks mutants but still founds almost no mutant cells.
2. **The food gate maintains the membrane and starves the core.**
   - Slowing food near M (D_F e^{-β n_M}) piles food against the rim. Food contact is the rim's induction signal, so the ring persists.
   - But the gate also keeps food from the catalytic core, so growth is slow and ends in a burst.
   - The same gate makes cells intolerant of turnover: k_dec 0.015 or 0.03 → extinction.
   - This is the lab's gated-mobility convergence, applied to a resource rather than to the cell's own matter.
3. **Contact killing gives positive frequency dependence.**
   - The worse grazer wins only when it starts abundant. At 50% it holds a territory and kills at the front; at 15% it loses in 3/3 seeds.
   - This was predicted before the rare-seeding runs and confirmed. It explains why a predator arising by mutation never invades (0/3 seeds, same as the no-lysis control).
4. **No territory shell (R2=1) plus decay turnover** gives 4–9 generations per 400 time units in every heredity run, so selection has generations to act on.

Robustness and numerics: see §5 (jitter runs, dt/2).

## 4. Negative results

- Conformity with low mutation (mu=0.01–0.05): purity 1.0 but no variation ever established.
- Gated cells with maintenance cost k_dec ≥ 0.015: extinct (2 runs).
- Gate β=0.3: 12 cells → 2, with no reproduction within t=240.
- A predator kind arising by mutation: founded 1–3 times per seed, but never reproduces or invades (3/3 seeds).
- Kind conversion of whole cells by contact (kind 0 → kind 1 during a cell's life): only 1–2 events per selected run and none in neutral runs, too few to claim.

## 5. Robustness and numerics (important)

- **Seeds:** the L7 contrast holds on 3/3 seeds at a 1.3× catalysis advantage.
- **Jitter:** with a 1.2× advantage and mu=0.09, the sweep is not reliable: kind-1 cells end at 6/18, 0/17 and 3/17, and per-capita births favour kind 1 on 1 of 3 seeds.
- **dt convergence fails.** Over t=60–200, mean free spores (core particles outside cells) at dt = 0.02 / 0.01 / 0.005 are 127 / 40 / 6, and cells at t=200 are 24 / 14 / 5. Adding core Brownian noise does not restore convergence (D_C=0.05: 146 / 77 / 8). A softer core (rep=3) dies at every dt.
- **What this means.** Spore emission is mostly numerical heating: the stiff core (rep=10, ff=10) overshoots at dt=0.02. So the reproduction rate behind sprint 1's `sporecell` and every sprint-2 result belongs to the dt=0.02 discrete map, not to a continuum limit.
- **What survives at dt/2 (seed 0):** the selection direction (per-capita births 1.4 vs 0.5) and breeding true (6/7). Births are about 5× fewer, though, and seed 1 shows no kind-1 births.
- **Numerical-validity modifier:** I would score these worlds 0 until emission comes from a dt-converged mechanism.

## 6. Next sprint

0. **First, fix the numerics.** Make spore release a dt-converged process, then redo L7 with neutral controls at a converged dt. Two options:
   - an explicit surface detachment rate, or
   - a physical mid-range C–C repulsion that buds surface fragments, with a semi-implicit or smaller-step integrator and dt-halving as a gate.
1. **Membrane that is the cell's own product.**
   - Let C make M from food, rather than M being induced by contact, so rings survive starvation.
   - Combine with the food gate, so the membrane controls uptake as a material barrier.
2. **Motility.** Add non-reciprocal C↔M forces for swimming ring cells, so heritable kinds can move and pursue (a motile predator could build its own front and escape the priority effect).
3. **Heredity with more than two kinds:** a continuous trait (catalysis rate or adhesion) carried by conformity, to look for open-ended drift or an optimum.
4. Move particle-identity lineage into labkit, since image tracking misses spore reproduction.
