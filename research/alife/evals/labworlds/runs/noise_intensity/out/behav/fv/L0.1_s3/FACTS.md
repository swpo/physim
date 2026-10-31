# Evidence pack: fed-vortices-noise (seed 3)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 77s; status ok
- command: `nsweep behav fv level 0.1`
- segmentation: matter > 0.25 of robust range [0.0006, 0.2374], min area 6 px

## Measurements
- components: final 59, mean 66.9, max 78; occupancy final 0.34
- tracks: 3038; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.48, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [81, 61, 34], H1 [6, 0, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.481/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 60, default): splits 767, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 748, merge/split ratio 0.975, nucleations 762
- channel total drift (end/start - 1): [0.1377, -0.1654, -1039.1158, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 121 at frame 26: holes 0, rim-vs-core 0.69, rim-vs-outside 0.25, heterogeneity 0.20; core [0.734, 0.263, 0.887, 0.577] rim [0.348, 0.487, 0.676, 0.094]
  - track 2330 at frame 131: holes 0, rim-vs-core 0.49, rim-vs-outside 0.27, heterogeneity 0.15; core [0.703, 0.084, 0.09, 0.361] rim [0.38, 0.282, 0.266, 0.097]
  - track 2073 at frame 116: holes 0, rim-vs-core 0.34, rim-vs-outside 0.23, heterogeneity 0.11; core [0.563, 0.492, 0.165, 0.387] rim [0.375, 0.567, 0.269, 0.13]
  - track 1751 at frame 100: holes 0, rim-vs-core 0.32, rim-vs-outside 0.22, heterogeneity 0.10; core [0.564, 0.323, 0.164, 0.318] rim [0.375, 0.42, 0.269, 0.11]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 361 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.705, rim/outside 2.65 (aggregate of 361 individuals; 9/361 membrane-like individually; rim level 0.47)
  - radial fuel Y: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.99, rim/outside 0.942 (aggregate of 361 individuals; 0/361 membrane-like individually; rim level 0.599)
  - radial vorticity (signed): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 0.992 (aggregate of 361 individuals; 0/361 membrane-like individually; rim level 0.479)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.531, rim/outside 4.62 (aggregate of 361 individuals; 24/361 membrane-like individually; rim level 0.259)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #121 (t=78, R_eq 4.26): none; #2330 (t=393, R_eq 5.05): none; #2073 (t=348, R_eq 4.03): none; #1751 (t=300, R_eq 4.79): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 361 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
