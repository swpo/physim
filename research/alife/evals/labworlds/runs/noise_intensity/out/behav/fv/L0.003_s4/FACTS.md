# Evidence pack: fed-vortices-noise (seed 4)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 73s; status ok
- command: `nsweep behav fv level 0.003`
- segmentation: matter > 0.29 of robust range [0.0, 0.2075], min area 6 px

## Measurements
- components: final 30, mean 31.1, max 38; occupancy final 0.14
- tracks: 94; persistent (alive >= 50% of run): 28; longest 151 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 5.56 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 30], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.245/time; max body lengths 12.9
- replication (lineage window K = 20 frames = time 60, default): splits 23, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.435, nucleations 0
- channel total drift (end/start - 1): [-0.549, 0.1674, 809.5358, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.75, rim-vs-outside 0.28, heterogeneity 0.19; core [0.81, 0.111, 0.915, 0.653] rim [0.39, 0.329, 0.691, 0.118]
  - track 1 at frame 76: holes 0, rim-vs-core 0.65, rim-vs-outside 0.31, heterogeneity 0.17; core [0.801, 0.097, 0.051, 0.619] rim [0.433, 0.307, 0.245, 0.16]
  - track 4 at frame 76: holes 0, rim-vs-core 0.72, rim-vs-outside 0.32, heterogeneity 0.19; core [0.825, 0.104, 0.923, 0.68] rim [0.429, 0.317, 0.712, 0.163]
  - track 84 at frame 125: holes 0, rim-vs-core 0.69, rim-vs-outside 0.29, heterogeneity 0.19; core [0.794, 0.112, 0.061, 0.633] rim [0.4, 0.308, 0.263, 0.135]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 15.4 (aggregate of 186 individuals; 2/186 membrane-like individually; rim level 0.665)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.82, rim/outside 0.784 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.481)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 1.07 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.515)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 26.8 (aggregate of 186 individuals; 4/186 membrane-like individually; rim level 0.502)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.79): none; #1 (t=228, R_eq 4.92): none; #4 (t=228, R_eq 4.58): none; #84 (t=375, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 186 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
