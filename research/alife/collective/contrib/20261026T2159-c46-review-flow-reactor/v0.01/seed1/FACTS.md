# Evidence pack: cips-layered-flow (seed 1)

- world: `../../../20261026T1729-c44-cips-flow-reactor-budding-niche/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [128, 128]; wall 793s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1729-c44-cips-flow-reactor-budding-niche/world.py --out collective/contrib/20261026T2159-c46-review-flow-reactor/v0.01/seed1 --seeds 1 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.018, 0.982], min area 6 px

## Measurements
- components: final 17, mean 15.2, max 19; occupancy final 0.15
- tracks: 87; persistent (alive >= 50% of run): 1; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.0114/time; max body lengths 8.5
- replication (lineage window K = 20 frames = time 2000, default): splits 30, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 6, merges 20, merge/split ratio 0.667, nucleations 7
- channel total drift (end/start - 1): [0.4863, -0.3524, 0.3679, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 86: holes 0, rim-vs-core 0.38, rim-vs-outside 0.56, heterogeneity 0.13; core [0.975, 0.848, 0.139, 0.044] rim [0.762, 0.622, 0.254, 0.234]
  - track 15 at frame 106: holes 0, rim-vs-core 0.74, rim-vs-outside 0.37, heterogeneity 0.17; core [0.955, 0.883, 0.252, 0.122] rim [0.669, 0.618, 0.389, 0.736]
  - track 0 at frame 58: holes 0, rim-vs-core 0.29, rim-vs-outside 0.66, heterogeneity 0.14; core [0.973, 0.842, 0.114, 0.049] rim [0.813, 0.688, 0.197, 0.208]
  - track 59 at frame 257: holes 0, rim-vs-core 0.50, rim-vs-outside 0.54, heterogeneity 0.15; core [0.964, 0.814, 0.059, 0.077] rim [0.752, 0.604, 0.198, 0.454]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 22.7 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.922)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 7.96 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.79)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.2, rim/outside 0.75 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.457)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 7.31, rim/outside 19.2 (aggregate of 100 individuals; 99/100 membrane-like individually; rim level 0.576)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #6 (t=8600, R_eq 6.23): ['s']; #15 (t=10600, R_eq 5.81): ['s']; #0 (t=5800, R_eq 7.23): ['s']; #59 (t=25700, R_eq 7.94): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
