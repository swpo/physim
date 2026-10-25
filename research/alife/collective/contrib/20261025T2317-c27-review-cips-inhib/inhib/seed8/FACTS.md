# Evidence pack: cips-inhib (seed 8)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27k/world.py --out collective/contrib/wip-c27k/inhib --seeds 7 8 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0014, 0.9891], min area 6 px

## Measurements
- components: final 31, mean 30.5, max 44; occupancy final 0.13
- tracks: 54; persistent (alive >= 50% of run): 31; longest 535 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 10, merge/split ratio n/a, nucleations 44
- channel total drift (end/start - 1): [0.0, -0.5798, 0.3994, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 333: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.10; core [0.95, 0.874, 0.189, 0.851] rim [0.801, 0.76, 0.278, 0.767]
  - track 1 at frame 333: holes 0, rim-vs-core 0.39, rim-vs-outside 0.40, heterogeneity 0.10; core [0.946, 0.874, 0.197, 0.842] rim [0.685, 0.675, 0.346, 0.703]
  - track 2 at frame 333: holes 0, rim-vs-core 0.37, rim-vs-outside 0.40, heterogeneity 0.10; core [0.953, 0.89, 0.179, 0.856] rim [0.713, 0.695, 0.329, 0.715]
  - track 3 at frame 338: holes 0, rim-vs-core 0.36, rim-vs-outside 0.40, heterogeneity 0.10; core [0.951, 0.879, 0.193, 0.846] rim [0.718, 0.692, 0.334, 0.714]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 210 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 28.7 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.914)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 4.58 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.823)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.89, rim/outside 0.701 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.512)
  - radial I: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 2.34 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.824)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3330, R_eq 4.37): none; #1 (t=3330, R_eq 4.48): none; #2 (t=3330, R_eq 4.55): none; #3 (t=3380, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
