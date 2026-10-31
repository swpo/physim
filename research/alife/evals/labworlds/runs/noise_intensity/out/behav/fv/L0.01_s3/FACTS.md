# Evidence pack: fed-vortices-noise (seed 3)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 71s; status ok
- command: `nsweep behav fv level 0.01`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2084], min area 6 px

## Measurements
- components: final 31, mean 34.6, max 45; occupancy final 0.13
- tracks: 81; persistent (alive >= 50% of run): 33; longest 151 frames; alive start-to-end: 15
- size of persistent tracks: max/min area ratio 13.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 33, 32], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.28/time; max body lengths 14.5
- replication (lineage window K = 20 frames = time 60, default): splits 15, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.333, nucleations 0
- channel total drift (end/start - 1): [-0.5432, 0.1632, 1056.0376, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.71, rim-vs-outside 0.31, heterogeneity 0.19; core [0.807, 0.118, 0.914, 0.67] rim [0.415, 0.333, 0.704, 0.154]
  - track 3 at frame 76: holes 0, rim-vs-core 0.77, rim-vs-outside 0.30, heterogeneity 0.20; core [0.823, 0.117, 0.053, 0.724] rim [0.404, 0.29, 0.26, 0.133]
  - track 11 at frame 76: holes 0, rim-vs-core 0.41, rim-vs-outside 0.47, heterogeneity 0.17; core [0.746, 0.11, 0.078, 0.554] rim [0.509, 0.247, 0.204, 0.278]
  - track 77 at frame 118: holes 0, rim-vs-core 0.68, rim-vs-outside 0.31, heterogeneity 0.18; core [0.792, 0.106, 0.056, 0.615] rim [0.404, 0.337, 0.26, 0.143]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 202 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 14.7 (aggregate of 202 individuals; 1/202 membrane-like individually; rim level 0.667)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9.83, rim/outside 0.782 (aggregate of 202 individuals; 0/202 membrane-like individually; rim level 0.462)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.05 (aggregate of 202 individuals; 0/202 membrane-like individually; rim level 0.508)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.653, rim/outside 29.1 (aggregate of 202 individuals; 2/202 membrane-like individually; rim level 0.501)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.69): none; #3 (t=228, R_eq 3.87): none; #11 (t=228, R_eq 5.08): none; #77 (t=354, R_eq 5.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 202 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
