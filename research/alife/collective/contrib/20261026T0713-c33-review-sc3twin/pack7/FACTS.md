# Evidence pack: sporecell3-det (seed 7)

- world: `../../../../threads/particle-life/worlds/sporecell3-det/world.py`, family `particle`
- parent: sporecell3; mutation: promoted gate settings: surface detachment k_det=0.05 for particles with < 60 matter neighbours (dt-converged release route)
- run: 201 frames x 50 steps x dt 0.02 = time 200; grid [128, 128]; wall 853s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell3-det/world.py --out collective/contrib/wip-c33-s3/pack7 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 9.0525], min area 6 px

## Measurements
- components: final 9, mean 4.8, max 9; occupancy final 0.01
- tracks: 12; persistent (alive >= 50% of run): 6; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 11, 7], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0807/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 12
- channel total drift (end/start - 1): [-0.9082, 227.1818, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 123: holes 0, rim-vs-core 0.04, rim-vs-outside 0.44, heterogeneity 0.02; core [0.055, 1.0, 0.0, 0.0] rim [0.022, 0.974, 0.0, 0.0]
  - track 1 at frame 129: holes 0, rim-vs-core 0.03, rim-vs-outside 0.16, heterogeneity 0.01; core [0.054, 0.0, 0.0, 1.0] rim [0.027, 0.0, 0.0, 1.0]
  - track 3 at frame 141: holes 0, rim-vs-core 0.00, rim-vs-outside 0.24, heterogeneity 0.00; core [0.0, 1.0, 0.0, 0.008] rim [0.0, 0.998, 0.0, 0.007]
  - track 4 at frame 143: holes 0, rim-vs-core 0.00, rim-vs-outside 0.06, heterogeneity 0.00; core [0.001, 0.0, 0.0, 1.0] rim [0.005, 0.0, 0.0, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.555 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.0279)
  - radial C0 core kind 0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.959, rim/outside 6.75 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.614)
  - radial M membrane: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 4.1 (aggregate of 31 individuals; 2/31 membrane-like individually; rim level 0.0472)  MEMBRANE-LIKE
  - radial C1 core kind 1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 4.95 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.417)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M membrane
- membrane-like channels per top track at mid-life: #0 (t=123, R_eq 4.37): none; #1 (t=129, R_eq 4.22): none; #3 (t=141, R_eq 3.09): none; #4 (t=143, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
