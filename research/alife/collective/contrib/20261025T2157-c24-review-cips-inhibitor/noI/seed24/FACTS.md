# Evidence pack: cips-inhib (seed 24)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2157-c24-review-cips-inhibitor/noI/seed24 --seeds 24 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9991], min area 6 px

## Measurements
- components: final 44, mean 50.2, max 74; occupancy final 0.14
- tracks: 104; persistent (alive >= 50% of run): 47; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio n/a, nucleations 75
- channel total drift (end/start - 1): [0.0, -0.2264, 0.156, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.08; core [0.976, 0.855, 0.179, 0.0] rim [0.77, 0.685, 0.309, 0.0]
  - track 1 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.07; core [0.981, 0.879, 0.16, 0.0] rim [0.797, 0.704, 0.298, 0.0]
  - track 2 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.08; core [0.977, 0.856, 0.142, 0.0] rim [0.772, 0.689, 0.271, 0.0]
  - track 3 at frame 161: holes 0, rim-vs-core 0.21, rim-vs-outside 0.61, heterogeneity 0.07; core [0.977, 0.837, 0.22, 0.0] rim [0.827, 0.72, 0.306, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 316 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 49 (aggregate of 316 individuals; 0/316 membrane-like individually; rim level 0.939)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 4.01 (aggregate of 316 individuals; 0/316 membrane-like individually; rim level 0.811)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.06, rim/outside 0.682 (aggregate of 316 individuals; 0/316 membrane-like individually; rim level 0.461)
  - radial I: flat profile (no radial structure; level 0; aggregate of 316 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 3.39): none; #1 (t=1610, R_eq 3.52): none; #2 (t=1610, R_eq 3.43): none; #3 (t=1610, R_eq 3.14): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
