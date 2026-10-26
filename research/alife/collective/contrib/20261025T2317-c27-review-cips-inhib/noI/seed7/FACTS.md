# Evidence pack: cips-inhib (seed 7)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 123s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27k/world.py --out collective/contrib/wip-c27k/noI --seeds 7 8 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9994], min area 6 px

## Measurements
- components: final 39, mean 45.8, max 79; occupancy final 0.14
- tracks: 119; persistent (alive >= 50% of run): 44; longest 582 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 36, merge/split ratio n/a, nucleations 83
- channel total drift (end/start - 1): [-0.0, -0.244, 0.1684, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 313: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.08; core [0.978, 0.863, 0.182, 0.0] rim [0.777, 0.688, 0.314, 0.0]
  - track 2 at frame 313: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.06; core [0.975, 0.817, 0.227, 0.0] rim [0.794, 0.671, 0.33, 0.0]
  - track 6 at frame 313: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.07; core [0.975, 0.815, 0.242, 0.0] rim [0.79, 0.672, 0.344, 0.0]
  - track 7 at frame 313: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.07; core [0.975, 0.836, 0.254, 0.0] rim [0.765, 0.67, 0.374, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 271 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 58.3 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.954)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.44 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.819)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.11, rim/outside 0.689 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.473)
  - radial I: flat profile (no radial structure; level 0; aggregate of 271 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3130, R_eq 3.66): none; #2 (t=3130, R_eq 3.09): none; #6 (t=3130, R_eq 3.04): none; #7 (t=3130, R_eq 3.29): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
