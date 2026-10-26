# Evidence pack: cips-layered-flow (seed 4)

- world: `../../../20261026T1729-c44-cips-flow-reactor-budding-niche/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [128, 128]; wall 1029s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1729-c44-cips-flow-reactor-budding-niche/world.py --out collective/contrib/20261026T2207-c47-review-cips-flow/rerun/seed4 --seeds 4 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0176, 0.9829], min area 6 px

## Measurements
- components: final 16, mean 15.4, max 19; occupancy final 0.15
- tracks: 189; persistent (alive >= 50% of run): 0; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 16, 16], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.0219/time; max body lengths 10.2
- replication (lineage window K = 20 frames = time 2000, default): splits 66, persistent splits 59 (0 more failed only because the siblings re-merged within K), max generation 17, merges 49, merge/split ratio 0.742, nucleations 6
- channel total drift (end/start - 1): [0.4739, -0.3425, 0.3582, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 55: holes 0, rim-vs-core 0.67, rim-vs-outside 0.40, heterogeneity 0.16; core [0.959, 0.895, 0.275, 0.113] rim [0.701, 0.641, 0.407, 0.661]
  - track 25 at frame 81: holes 0, rim-vs-core 0.54, rim-vs-outside 0.64, heterogeneity 0.17; core [0.987, 0.946, 0.216, 0.073] rim [0.782, 0.698, 0.357, 0.488]
  - track 7 at frame 43: holes 0, rim-vs-core 0.53, rim-vs-outside 0.63, heterogeneity 0.16; core [0.984, 0.938, 0.16, 0.082] rim [0.787, 0.695, 0.322, 0.481]
  - track 166 at frame 285: holes 0, rim-vs-core 0.73, rim-vs-outside 0.38, heterogeneity 0.17; core [0.957, 0.896, 0.275, 0.122] rim [0.681, 0.634, 0.413, 0.725]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 22.3 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.891)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 7.73 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.783)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.14, rim/outside 0.76 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.492)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.41, rim/outside 17.8 (aggregate of 100 individuals; 92/100 membrane-like individually; rim level 0.594)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #11 (t=5500, R_eq 5.61): ['s']; #25 (t=8100, R_eq 6.08): ['s']; #7 (t=4300, R_eq 7.07): ['s']; #166 (t=28500, R_eq 5.81): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
