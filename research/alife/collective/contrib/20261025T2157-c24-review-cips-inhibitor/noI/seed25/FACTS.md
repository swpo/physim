# Evidence pack: cips-inhib (seed 25)

- world: `../../../20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 103s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2157-c24-review-cips-inhibitor/noI/seed25 --seeds 25 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.9989], min area 6 px

## Measurements
- components: final 49, mean 53.6, max 83; occupancy final 0.13
- tracks: 117; persistent (alive >= 50% of run): 52; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 48], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 32, merge/split ratio n/a, nucleations 85
- channel total drift (end/start - 1): [0.0, -0.2125, 0.1465, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 159: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.06; core [0.975, 0.843, 0.164, 0.0] rim [0.799, 0.696, 0.273, 0.0]
  - track 4 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.51, heterogeneity 0.08; core [0.977, 0.876, 0.13, 0.0] rim [0.769, 0.701, 0.266, 0.0]
  - track 5 at frame 161: holes 0, rim-vs-core 0.26, rim-vs-outside 0.48, heterogeneity 0.07; core [0.986, 0.903, 0.071, 0.0] rim [0.836, 0.738, 0.203, 0.0]
  - track 7 at frame 161: holes 0, rim-vs-core 0.23, rim-vs-outside 0.46, heterogeneity 0.06; core [0.977, 0.84, 0.184, 0.0] rim [0.827, 0.704, 0.285, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 336 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 45 (aggregate of 336 individuals; 0/336 membrane-like individually; rim level 0.935)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 3.79 (aggregate of 336 individuals; 0/336 membrane-like individually; rim level 0.81)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.85, rim/outside 0.682 (aggregate of 336 individuals; 0/336 membrane-like individually; rim level 0.442)
  - radial I: flat profile (no radial structure; level 0; aggregate of 336 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 3.09): none; #4 (t=1610, R_eq 3.52): none; #5 (t=1610, R_eq 3.61): none; #7 (t=1610, R_eq 2.93): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
