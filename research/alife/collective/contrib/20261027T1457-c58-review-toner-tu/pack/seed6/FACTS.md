# Evidence pack: eating-flocks (seed 6)

- world: `../../../20261027T0210-c51-toner-tu-eaters-fronts/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T1457-c58-review-toner-tu/pack --seeds 5 6 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.8639], min area 6 px

## Measurements
- components: final 4, mean 5.8, max 24; occupancy final 0.26
- tracks: 488; persistent (alive >= 50% of run): 0; longest 8 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 6, 3], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 400, default): splits 12, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.167, nucleations 423
- channel total drift (end/start - 1): [0.9127, -0.5246, -0.2968, 4.7598]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 252 at frame 55: holes 0, rim-vs-core 0.18, rim-vs-outside 0.24, heterogeneity 0.11; core [0.596, 0.175, 0.827, 0.581] rim [0.477, 0.27, 0.741, 0.564]
  - track 102 at frame 16: holes 0, rim-vs-core 0.25, rim-vs-outside 0.75, heterogeneity 0.16; core [0.79, 0.007, 0.921, 0.873] rim [0.629, 0.149, 0.824, 0.779]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.663, rim/outside 1.52 (aggregate of 32 individuals; 5/32 membrane-like individually; rim level 0.308)
  - radial food c: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.86, rim/outside 0.979 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.438)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.714, rim/outside 1.55 (aggregate of 32 individuals; 5/32 membrane-like individually; rim level 0.435)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 1.06 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.513)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #252 (t=1100, R_eq 4.79): none; #479 (t=2940, R_eq 21.74, ring): none; #102 (t=320, R_eq 13.83, ring): none; #228 (t=960, R_eq 22.02, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
