# Evidence pack: reacting-thermals (seed 0)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [192, 192]; wall 155s; status ok
- command: `python -m labkit.run collective/contrib/c49wip2/world.py --out collective/contrib/c49wip2/pack_res15 --seeds 0 1 --size 192 192 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7086], min area 6 px

## Measurements
- components: final 40, mean 21.9, max 48; occupancy final 0.04
- tracks: 391; persistent (alive >= 50% of run): 0; longest 263 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 40, 38], H1 [0, 0, 0]
- motion: 193 long-lived tracks moved >= 1 body length; max speed 1.49/time; max body lengths 33.7
- replication (lineage window K = 20 frames = time 20, default): splits 143, persistent splits 66 (0 more failed only because the siblings re-merged within K), max generation 11, merges 6, merge/split ratio 0.042, nucleations 49
- channel total drift (end/start - 1): [-0.8417, -0.3708, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 208 at frame 469: holes 0, rim-vs-core 0.28, rim-vs-outside 0.45, heterogeneity 0.16; core [0.868, 0.129, 0.478, 0.93] rim [0.667, 0.176, 0.448, 0.738]
  - track 187 at frame 413: holes 0, rim-vs-core 0.23, rim-vs-outside 0.45, heterogeneity 0.09; core [0.774, 0.191, 0.414, 0.931] rim [0.637, 0.216, 0.364, 0.75]
  - track 213 at frame 439: holes 0, rim-vs-core 0.29, rim-vs-outside 0.55, heterogeneity 0.14; core [0.942, 0.164, 0.409, 0.996] rim [0.706, 0.205, 0.433, 0.838]
  - track 368 at frame 585: holes 0, rim-vs-core 0.29, rim-vs-outside 0.48, heterogeneity 0.12; core [0.858, 0.181, 0.569, 0.987] rim [0.658, 0.215, 0.582, 0.783]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 5.88 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.636)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.18, rim/outside 0.728 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.273)
  - radial vorticity: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.02 (aggregate of 133 individuals; 12/133 membrane-like individually; rim level 0.465)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 7.75 (aggregate of 133 individuals; 3/133 membrane-like individually; rim level 0.67)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #208 (t=469, R_eq 3.19): ['vorticity']; #187 (t=413, R_eq 2.46): none; #213 (t=439, R_eq 2.65): ['vorticity']; #368 (t=585, R_eq 2.71): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
