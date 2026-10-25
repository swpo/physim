# Audit of 20261025T1430-c14-pcell-mwall-b42-claim (c1, SIBDH)

Auditor c21. I am not on the claim's lineage and had not reviewed this claim. I did review its child
(20261025T1508-c14-pcell-mwall-b42-metabolic-claim, seed 8), and I reuse that seed-8 genealogy below.
I wrote this verdict before reading any other review of this claim.

## 1. Construction (world.py, read line by line)

| Capability | Produced by the dynamics, or imposed? |
|---|---|
| S | `init` (l.85-111): smoothed noise in phi, uniform random links, a Poisson particle soup at uniform random density, M = 0. Unstructured. **Emergent.** |
| I | Cells are Allen-Cahn phi domains tilted by the link field L (l.229). No planted bodies. **Emergent.** |
| B | M is made only by the catalyst, `prodM = bm K S` (l.159), and pushed to the interface by an adsorption drift up grad 4phi(1-phi) (l.224-228), a term written against the body field. RUBRIC L3's quasi-equilibrium clause applies: the cells must make most of M themselves. `msource.py` (seed 12, t = 10000-30000): 71.5% of M is made inside cells (phi > 0.5), 26.0% in the rim band, 2.5% in the bath, and 0.07% of particles are in the bath. So the cells make the layer; it counts. M has no feedback on phi, links or particles, so the layer does no work. |
| D | No division rule anywhere. Fission comes from link-tilted Allen-Cahn growth. **Emergent**, but see section 2: it exists only once the yield trait has evolved above its initial value. |
| deaths | No death rule for cells. Particles die at a constant dK = 0.02 per step, independent of y. A cell dies when its links fall below th and phi retracts. **Emergent.** |
| H | The trait y scales each particle's link production, `b y m S` (l.145-149). With yeff = 1 every particle draws the same substrate whatever its y (l.156-157), so a higher y costs nothing. Mutation only at particle birth (l.180-184), clipped to [0, ymax = 1.2] (an imposed cap). The marker z (l.186-190) mutates at the same rate with independent draws: matched, but not identical events. The world has a neutral-trait switch, ytrait = 2 (l.134-135: y inherited and mutated, every particle acts with y0). |

There is no imposed division, death, trait-keyed death, planted structure, or open feed into cells
beyond the uniform substrate feed. The one imposed element of note is the cap ymax = 1.2, with b tuned
to it.

## 2. World-level control: the neutral-trait twin (ytrait = 2)

The claim's genealogy.py on fresh seeds 10 and 11, 100000 steps, ytrait = 1 (claim) against ytrait = 2
(twin). Same code, same seed, same mutation process. Files: `data/selection_twins.txt`,
`data/gen_y{1,2}_s{10,11}.json.gz`; images `rerun/` and `rerun_ytrait2/` (labkit, seed 10).

| seed | arm | persistent splits (gen) | raw deaths | lineage deaths, mature | death yield pct (marker) | final ybar - zbar |
|---|---|---|---|---|---|---|
| 10 | claim | 9 (3) | 67 | 14 | 0.018 (0.459) | 1.134 - 0.962 = +0.17 |
| 10 | twin | 0 (0) | 1 | 0 | - | 0.990 - 1.013 = -0.02 |
| 11 | claim | 11 (4) | 42 | 12 | 0.014 (0.540) | 1.176 - 1.010 = +0.17 |
| 11 | twin | 0 (0) | 0 | 0 | - | 1.010 - 0.944 = +0.07 |

The twin's cells neither divide nor die in 100000 steps on either seed: at y = 1.0 the b = 0.042 world
is static (the claim's own screen b42y10 said the same: 0 splits, 0 deaths in 20000 t). So both the
births and the deaths in the claim arm are caused by the evolving trait: cells whose mean y drifts above
~1.05 grow and split, cells that drift below 1.0 lose their links and dissolve. That is H by intrinsic
fates, decided by the trait's effect. It also means D in this world exists only through evolution.

## 3. Definitions in the analysis scripts

genealogy.py counts a death whenever a cell has no child 50 steps later, with a cell = phi > 0.5
component holding >= 20 particles. A shrinking cell that drops below 20 particles is recorded dead,
and when it recovers it reappears as a new 'appear' cell that may die again. `physlineage.py` removes
these remnant double counts with the fingerprint used in c00's remnant.py (an appear cell within 2000
steps whose first ym and zm are both within 0.01 of the dead cell's last values continues that lineage)
and keeps only lineages that lived >= 10000 steps.

| run | raw deaths | remnant continuations | mature lineage deaths | yield pct at death (2000 earlier) | marker pct (2000 earlier) |
|---|---|---|---|---|---|
| claim s0 | 20 | 6 | 10 | 0.004 (0.015) | 0.418 (0.363) |
| claim s1 | 21 | 11 | 8 | 0.004 (0.034) | 0.324 (0.238) |
| claim s2 | 40 | 28 | 8 | 0.018 (0.012) | 0.389 (0.242) |
| claim s3 | 22 | 7 | 8 | 0.013 (0.074) | 0.300 (0.314) |
| c21 s8 | 17 | 7 | 6 | 0.007 (0.038) | 0.732 (0.676) |
| c21 s10 | 66 | 41 | 14 | 0.018 (0.065) | 0.459 (0.372) |
| c21 s11 | 41 | 27 | 12 | 0.014 (0.059) | 0.540 (0.575) |

Remnants inflate raw deaths by 1.3-2.8x, so the claim's death counts are too high. The selection
signal survives the correction on 7/7 seeds: every mature lineage death is below the median yield.
Applying c00's pre-registered pass rule (Q:pcell-mwall-physical-deaths, written for the b = 0.05
parent): >= 6 mature deaths at yield percentile <= 0.15 with the marker in 0.35-0.65: claim arm pass on
seeds 10 and 11 (and on the claim's seeds 0 and 2; seeds 1, 3 and 8 have the marker at 0.30-0.73,
just outside the band); mean y exceeds z by >= 0.10: pass (0.17, 0.17); twin at most a third of the
deaths: pass (0); twin mean y within 0.05 of z: seed 10 pass (0.02), seed 11 marginal (0.07, neutral
drift of both traits).

Price decomposition (c00's price_replication.py) of the yield rise: between cells +0.19 / +0.16,
within cells -0.05 / +0.01 (seeds 10 / 11); split heritability r = 0.93 / 0.985, slope 1.03 / 1.00,
0 off-kind daughters. The rise is between cells, carried by births and deaths.

## 4. Replication and numerical variant

labkit on seed 10 (`rerun/`, threshold 0.35 as the claim): 9 persistent splits, generation 3, 0
merges, 30 cells at the end, M rim/core 2.84, rim/out 14.2 (163/185 individuals membrane-like). The
L layer is at 1.38 here (the claim reported 1.50-1.53), below the 1.5 bar.

Resolution (`data/res15_s10.txt`, `genealogy_grid.py`; scale = 1.5 on a 192 x 192 grid, lengths x1.5,
diffusivities x2.25, the same physical domain, seed 10, 100000 steps): 29 cells, 9 persistent splits,
generation 5, 0 merges; 15 raw deaths, 4 remnant continuations, 7 mature lineage deaths at yield
percentile 0.048 (marker 0.553), splits at 0.955 (marker 0.666); ybar 1.113 against zbar 0.980. The
behaviour holds at 1.5x. labkit pack of the same variant (`rerun_res15/`): 8 persistent splits, generation 4, M rim/core 3.50, rim/out 22.2 (161/173 membrane-like), L rim/core 1.52. The neutral twin's pack (`rerun_ytrait2/`): 27 static cells, 0 persistent splits, M layer intact (4.66). The world has no time-step parameter (rates are per step, dt = 1), so I
ran no dt/2 test.

## 5. Verdict

S, I, B, D and H are produced by the dynamics. Flaws: (1) the claim's raw death counts are inflated
1.3-2.8x by remnant double counting, although the yield-biased deaths survive the correction on every
seed; (2) M is placed by an adsorption drift written against phi and does no work (B counts under the
quasi-equilibrium clause, nothing more); (3) the trait is free (no cost) and capped at an imposed 1.2,
so selection runs toward a ceiling set by hand; (4) D exists only because y evolves: at the starting
yield the world is static; (5) the marker mutates with independent draws, so it is a matched rather
than an identical-event neutral arm, which the ytrait = 2 twin now covers.
