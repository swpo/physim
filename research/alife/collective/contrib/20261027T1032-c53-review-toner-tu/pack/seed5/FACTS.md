# Evidence pack: eating-flocks (seed 5)

- world: `../../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/c53-rev-tt/pack --seeds 5 6 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.8741], min area 6 px

## Measurements
- components: final 3, mean 6.5, max 30; occupancy final 0.25
- tracks: 495; persistent (alive >= 50% of run): 0; longest 17 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 6, 3], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.3
- replication (lineage window K = 20 frames = time 400, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.2, nucleations 431
- channel total drift (end/start - 1): [0.5751, -0.5154, -0.3093, -12.6019]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 458 at frame 135: holes 0, rim-vs-core 0.24, rim-vs-outside 0.78, heterogeneity 0.12; core [0.812, 0.027, 0.919, 0.05] rim [0.629, 0.146, 0.833, 0.11]
  - track 195 at frame 40: holes 0, rim-vs-core 0.33, rim-vs-outside 0.77, heterogeneity 0.17; core [0.86, 0.0, 0.924, 0.352] rim [0.63, 0.151, 0.828, 0.507]
  - track 188 at frame 38: holes 0, rim-vs-core 0.47, rim-vs-outside 0.78, heterogeneity 0.19; core [0.967, 0.005, 0.943, 0.636] rim [0.64, 0.127, 0.818, 0.349]
  - track 462 at frame 132: holes 0, rim-vs-core 0.23, rim-vs-outside 0.86, heterogeneity 0.13; core [0.827, 0.0, 0.914, 0.174] rim [0.65, 0.13, 0.842, 0.145]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 1.39 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.283)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.982 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.438)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.68, rim/outside 1.39 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.396)
  - radial p_x: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.21, rim/outside 0.995 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.467)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #458 (t=2700, R_eq 13.33): none; #195 (t=800, R_eq 16.06): none; #188 (t=760, R_eq 16.64): none; #462 (t=2640, R_eq 17.36, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
