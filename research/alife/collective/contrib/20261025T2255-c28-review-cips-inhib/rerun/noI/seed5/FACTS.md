# Evidence pack: cips-inhib (seed 5)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 601 frames x 100 steps x dt 0.1 = time 6000; grid [128, 128]; wall 125s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out /tmp/claude-0/c28ci/noI --seeds 5 6 --frames 600 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0001, 0.9994], min area 6 px

## Measurements
- components: final 35, mean 45.9, max 73; occupancy final 0.14
- tracks: 116; persistent (alive >= 50% of run): 44; longest 583 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 35, 35], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0012/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 40, merge/split ratio n/a, nucleations 76
- channel total drift (end/start - 1): [0.0, -0.2577, 0.1773, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 313: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.07; core [0.971, 0.828, 0.239, 0.0] rim [0.729, 0.65, 0.362, 0.0]
  - track 9 at frame 313: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.07; core [0.977, 0.849, 0.221, 0.0] rim [0.775, 0.681, 0.339, 0.0]
  - track 10 at frame 313: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.07; core [0.97, 0.818, 0.242, 0.0] rim [0.742, 0.654, 0.354, 0.0]
  - track 14 at frame 313: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.08; core [0.98, 0.862, 0.183, 0.0] rim [0.78, 0.692, 0.305, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 275 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 56 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.956)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 4.29 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.819)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.67, rim/outside 0.696 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.465)
  - radial I: flat profile (no radial structure; level 0; aggregate of 275 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3130, R_eq 3.43): none; #9 (t=3130, R_eq 3.43): none; #10 (t=3130, R_eq 3.29): none; #14 (t=3130, R_eq 3.57): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
