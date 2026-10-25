# Evidence pack: cips-inhib (seed 0)

- world: `../../world_inh.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: adds an inhibitor I made by catalysis that slows catalysis (cat / (1 + I/KI)) and decays slowly: core inhibition of large droplets as a size-control route that keeps the enzyme conserved
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 61s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/world.py --out collective/contrib/20261025T2130-c23-cips-inhibitor-arrest/p_noI --seeds 0 1 --frames 300 --size 128 128 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 42, mean 50.9, max 79; occupancy final 0.14
- tracks: 116; persistent (alive >= 50% of run): 45; longest 281 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 43, 42], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 34, merge/split ratio n/a, nucleations 82
- channel total drift (end/start - 1): [0.0, -0.2276, 0.1567, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 161: holes 0, rim-vs-core 0.28, rim-vs-outside 0.49, heterogeneity 0.07; core [0.968, 0.812, 0.239, 0.0] rim [0.764, 0.659, 0.352, 0.0]
  - track 6 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.08; core [0.978, 0.879, 0.165, 0.0] rim [0.776, 0.7, 0.307, 0.0]
  - track 18 at frame 161: holes 0, rim-vs-core 0.29, rim-vs-outside 0.51, heterogeneity 0.07; core [0.97, 0.828, 0.257, 0.0] rim [0.758, 0.665, 0.377, 0.0]
  - track 21 at frame 161: holes 0, rim-vs-core 0.28, rim-vs-outside 0.49, heterogeneity 0.07; core [0.98, 0.878, 0.15, 0.0] rim [0.801, 0.71, 0.283, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 319 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 43.2 (aggregate of 319 individuals; 0/319 membrane-like individually; rim level 0.934)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 3.93 (aggregate of 319 individuals; 0/319 membrane-like individually; rim level 0.808)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.04, rim/outside 0.68 (aggregate of 319 individuals; 0/319 membrane-like individually; rim level 0.456)
  - radial I: flat profile (no radial structure; level 0; aggregate of 319 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1610, R_eq 2.99): none; #6 (t=1610, R_eq 3.57): none; #18 (t=1610, R_eq 3.09): none; #21 (t=1610, R_eq 3.48): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
