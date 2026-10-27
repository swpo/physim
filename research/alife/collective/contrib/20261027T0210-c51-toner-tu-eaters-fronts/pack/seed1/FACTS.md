# Evidence pack: eating-flocks (seed 1)

- world: `../../world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/pack --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.8547], min area 6 px

## Measurements
- components: final 3, mean 5.4, max 27; occupancy final 0.26
- tracks: 431; persistent (alive >= 50% of run): 0; longest 6 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 5, 2], H1 [3, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 400, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 0.625, nucleations 372
- channel total drift (end/start - 1): [1.2391, -0.5252, -0.2907, -5.3492]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 13: holes 0, rim-vs-core 0.32, rim-vs-outside 0.80, heterogeneity 0.18; core [0.793, 0.016, 0.907, 0.4] rim [0.651, 0.163, 0.83, 0.64]
  - track 236 at frame 59: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.12; core [0.779, 0.049, 0.903, 0.192] rim [0.553, 0.177, 0.793, 0.258]
  - track 246 at frame 63: holes 0, rim-vs-core 0.34, rim-vs-outside 0.85, heterogeneity 0.17; core [0.878, 0.059, 0.593, 0.421] rim [0.643, 0.139, 0.827, 0.395]
  - track 36 at frame 5: holes 0, rim-vs-core 0.30, rim-vs-outside 0.36, heterogeneity 0.15; core [0.708, 0.143, 0.864, 0.279] rim [0.491, 0.293, 0.736, 0.345]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.649, rim/outside 1.3 (aggregate of 30 individuals; 3/30 membrane-like individually; rim level 0.281)
  - radial food c: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 1.04 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.441)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.697, rim/outside 1.35 (aggregate of 30 individuals; 2/30 membrane-like individually; rim level 0.397)
  - radial p_x: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 1.01 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.543)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=260, R_eq 11.14, ring): ['density rho']; #236 (t=1180, R_eq 9.87, ring): none; #246 (t=1260, R_eq 21.13): none; #36 (t=100, R_eq 5.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
