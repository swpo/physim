# Evidence pack: eating-flocks (seed 6)

- world: `../../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/c53-rev-tt/pack_v0 --seeds 5 6 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.6446], min area 6 px

## Measurements
- components: final 162, mean 142.9, max 162; occupancy final 0.37
- tracks: 371; persistent (alive >= 50% of run): 150; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.40 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [162, 162, 162], H1 [53, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 400, default): splits 139, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 3, merges 30, merge/split ratio 0.216, nucleations 5
- channel total drift (end/start - 1): [1.1559, -0.5901, -0.1917, 0.4183]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 77: holes 0, rim-vs-core 0.44, rim-vs-outside 0.40, heterogeneity 0.17; core [0.825, 0.073, 0.845, 0.262] rim [0.474, 0.216, 0.644, 0.363]
  - track 68 at frame 77: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.18; core [0.843, 0.066, 0.801, 0.503] rim [0.572, 0.176, 0.719, 0.497]
  - track 69 at frame 77: holes 0, rim-vs-core 0.36, rim-vs-outside 0.52, heterogeneity 0.15; core [0.853, 0.063, 0.855, 0.064] rim [0.581, 0.173, 0.706, 0.212]
  - track 361 at frame 118: holes 0, rim-vs-core 0.42, rim-vs-outside 0.36, heterogeneity 0.14; core [0.842, 0.07, 0.879, 0.813] rim [0.506, 0.197, 0.689, 0.703]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 921 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 4.53 (aggregate of 921 individuals; 2/921 membrane-like individually; rim level 0.693)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.94 (aggregate of 921 individuals; 0/921 membrane-like individually; rim level 0.337)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 3.67 (aggregate of 921 individuals; 24/921 membrane-like individually; rim level 0.786)
  - radial p_x: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 1.06 (aggregate of 921 individuals; 11/921 membrane-like individually; rim level 0.523)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #67 (t=1540, R_eq 3.66): none; #68 (t=1540, R_eq 3.52): none; #69 (t=1540, R_eq 3.48): none; #361 (t=2360, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 921 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
