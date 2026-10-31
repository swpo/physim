# Evidence pack: fed-vortices-noise (seed 3)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 77s; status ok
- command: `nsweep behav fv level 0.03`
- segmentation: matter > 0.28 of robust range [0.0002, 0.2141], min area 6 px

## Measurements
- components: final 31, mean 35.5, max 45; occupancy final 0.13
- tracks: 136; persistent (alive >= 50% of run): 32; longest 151 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 15.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 33, 31], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 15.3
- replication (lineage window K = 20 frames = time 60, default): splits 32, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 23, merge/split ratio 0.719, nucleations 2
- channel total drift (end/start - 1): [-0.4904, 0.1694, 1580.9987, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.64, rim-vs-outside 0.48, heterogeneity 0.20; core [0.857, 0.109, 0.034, 0.78] rim [0.513, 0.268, 0.195, 0.285]
  - track 3 at frame 76: holes 0, rim-vs-core 0.66, rim-vs-outside 0.24, heterogeneity 0.18; core [0.755, 0.117, 0.069, 0.565] rim [0.372, 0.294, 0.271, 0.103]
  - track 11 at frame 76: holes 0, rim-vs-core 0.80, rim-vs-outside 0.34, heterogeneity 0.21; core [0.851, 0.128, 0.038, 0.786] rim [0.426, 0.343, 0.241, 0.174]
  - track 61 at frame 78: holes 0, rim-vs-core 0.70, rim-vs-outside 0.30, heterogeneity 0.19; core [0.785, 0.128, 0.904, 0.632] rim [0.393, 0.341, 0.691, 0.132]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 204 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.732, rim/outside 9.85 (aggregate of 204 individuals; 1/204 membrane-like individually; rim level 0.636)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.5, rim/outside 0.793 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.467)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 1.08 (aggregate of 204 individuals; 0/204 membrane-like individually; rim level 0.513)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.635, rim/outside 25.8 (aggregate of 204 individuals; 6/204 membrane-like individually; rim level 0.458)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=228, R_eq 3.83): none; #3 (t=228, R_eq 4.48): none; #11 (t=228, R_eq 4.26): none; #61 (t=234, R_eq 4.72): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 204 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
