# Evidence pack: cips-layered-flow (seed 3)

- world: `../../../20261026T1729-c44-cips-flow-reactor-budding-niche/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [128, 128]; wall 1029s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1729-c44-cips-flow-reactor-budding-niche/world.py --out collective/contrib/20261026T2207-c47-review-cips-flow/rerun/seed3 --seeds 3 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0177, 0.9831], min area 6 px

## Measurements
- components: final 16, mean 15.8, max 19; occupancy final 0.15
- tracks: 207; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 16], H1 [0, 0, 0]
- motion: 65 long-lived tracks moved >= 1 body length; max speed 0.0227/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 2000, default): splits 71, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 16, merges 58, merge/split ratio 0.817, nucleations 7
- channel total drift (end/start - 1): [0.4961, -0.3381, 0.3533, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 48: holes 0, rim-vs-core 0.69, rim-vs-outside 0.38, heterogeneity 0.16; core [0.959, 0.892, 0.26, 0.116] rim [0.695, 0.635, 0.397, 0.688]
  - track 9 at frame 45: holes 0, rim-vs-core 0.53, rim-vs-outside 0.64, heterogeneity 0.16; core [0.987, 0.945, 0.212, 0.073] rim [0.787, 0.7, 0.353, 0.474]
  - track 59 at frame 113: holes 0, rim-vs-core 0.59, rim-vs-outside 0.49, heterogeneity 0.17; core [0.963, 0.906, 0.266, 0.11] rim [0.741, 0.677, 0.388, 0.586]
  - track 193 at frame 290: holes 0, rim-vs-core 0.70, rim-vs-outside 0.39, heterogeneity 0.16; core [0.959, 0.897, 0.275, 0.117] rim [0.696, 0.641, 0.41, 0.693]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 98 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 23.1 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.887)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.854, rim/outside 8.11 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.781)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.27, rim/outside 0.757 (aggregate of 98 individuals; 0/98 membrane-like individually; rim level 0.496)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 6.43, rim/outside 18.2 (aggregate of 98 individuals; 93/98 membrane-like individually; rim level 0.58)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #15 (t=4800, R_eq 5.84): ['s']; #9 (t=4500, R_eq 6.13): ['s']; #59 (t=11300, R_eq 5.78): ['s']; #193 (t=29000, R_eq 5.73): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
