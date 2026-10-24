# Evidence pack: sporecell3-det (seed 0)

- world: `../../../worlds/sporecell3-det/world.py`, family `particle`
- parent: sporecell3; mutation: promoted gate settings: surface detachment k_det=0.05 for particles with < 60 matter neighbours (dt-converged release route)
- run: 101 frames x 100 steps x dt 0.02 = time 200; grid [128, 128]; wall 465s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell3-det/world.py --out threads/particle-life/packs/sporecell3-det --seeds 0 1 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.1386], min area 6 px

## Measurements
- components: final 12, mean 7.6, max 13; occupancy final 0.02
- tracks: 19; persistent (alive >= 50% of run): 9; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 16, 10], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0745/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 40, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 19
- channel total drift (end/start - 1): [-0.9089, 136.7333, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.05, rim-vs-outside 0.35, heterogeneity 0.02; core [0.121, 0.0, 0.0, 1.0] rim [0.075, 0.0, 0.0, 0.983]
  - track 1 at frame 61: holes 0, rim-vs-core 0.23, rim-vs-outside 0.33, heterogeneity 0.05; core [0.04, 0.994, 0.0, 0.004] rim [0.053, 0.761, 0.0, 0.005]
  - track 2 at frame 62: holes 0, rim-vs-core 0.23, rim-vs-outside 0.38, heterogeneity 0.04; core [0.004, 1.0, 0.0, 0.0] rim [0.018, 0.773, 0.0, 0.0]
  - track 3 at frame 62: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.03; core [0.0, 0.997, 0.0, 0.0] rim [0.0, 0.765, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [33, 50, 67, 83, 100]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.44 (aggregate of 47 individuals; 2/47 membrane-like individually; rim level 0.0197)
  - radial C0 core kind 0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 17.1 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.657)
  - radial M membrane: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.05 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.0014)
  - radial C1 core kind 1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 7.6 (aggregate of 47 individuals; 2/47 membrane-like individually; rim level 0.366)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=122, R_eq 3.95): none; #1 (t=122, R_eq 3.52): ['F food']; #2 (t=124, R_eq 4.07): none; #3 (t=124, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
