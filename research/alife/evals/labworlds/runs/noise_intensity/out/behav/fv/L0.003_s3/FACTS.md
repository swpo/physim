# Evidence pack: fed-vortices-noise (seed 3)

- world: `../../../../scripts/noisy_world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 72s; status ok
- command: `nsweep behav fv level 0.003`
- segmentation: matter > 0.29 of robust range [0.0, 0.2092], min area 6 px

## Measurements
- components: final 34, mean 35.2, max 45; occupancy final 0.14
- tracks: 95; persistent (alive >= 50% of run): 31; longest 151 frames; alive start-to-end: 14
- size of persistent tracks: max/min area ratio 5.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 34], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.339/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 60, default): splits 20, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [-0.5533, 0.1477, 1412.0643, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 76: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.19; core [0.832, 0.11, 0.048, 0.735] rim [0.436, 0.275, 0.242, 0.164]
  - track 5 at frame 76: holes 0, rim-vs-core 0.70, rim-vs-outside 0.28, heterogeneity 0.18; core [0.781, 0.141, 0.899, 0.661] rim [0.401, 0.259, 0.697, 0.126]
  - track 11 at frame 76: holes 0, rim-vs-core 0.51, rim-vs-outside 0.40, heterogeneity 0.16; core [0.769, 0.091, 0.065, 0.574] rim [0.478, 0.257, 0.22, 0.228]
  - track 87 at frame 136: holes 0, rim-vs-core 0.72, rim-vs-outside 0.31, heterogeneity 0.19; core [0.821, 0.097, 0.049, 0.669] rim [0.415, 0.306, 0.254, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 208 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.731, rim/outside 14.9 (aggregate of 208 individuals; 0/208 membrane-like individually; rim level 0.652)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.49, rim/outside 0.783 (aggregate of 208 individuals; 0/208 membrane-like individually; rim level 0.449)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.07 (aggregate of 208 individuals; 0/208 membrane-like individually; rim level 0.516)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.626, rim/outside 26.6 (aggregate of 208 individuals; 3/208 membrane-like individually; rim level 0.48)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=228, R_eq 3.78): none; #5 (t=228, R_eq 3.29): none; #11 (t=228, R_eq 4.95): none; #87 (t=408, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 208 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
