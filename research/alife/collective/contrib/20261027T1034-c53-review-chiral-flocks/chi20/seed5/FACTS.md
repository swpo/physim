# Evidence pack: chiral-eating-flocks (seed 5)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c53-rev-ch/chi20 --seeds 5 6 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5294], min area 6 px

## Measurements
- components: final 63, mean 51.1, max 63; occupancy final 0.42
- tracks: 377; persistent (alive >= 50% of run): 46; longest 292 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.07 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 63, 63], H1 [37, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 127, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 2, merges 80, merge/split ratio 0.63, nucleations 2
- channel total drift (end/start - 1): [0.516, -0.4987, -0.2459, 5.5236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 78 at frame 156: holes 0, rim-vs-core 0.45, rim-vs-outside 0.58, heterogeneity 0.14; core [0.822, 0.081, 0.903, 0.056] rim [0.577, 0.271, 0.626, 0.217]
  - track 88 at frame 156: holes 0, rim-vs-core 0.45, rim-vs-outside 0.31, heterogeneity 0.13; core [0.801, 0.119, 0.855, 0.69] rim [0.517, 0.294, 0.563, 0.644]
  - track 131 at frame 161: holes 0, rim-vs-core 0.43, rim-vs-outside 0.59, heterogeneity 0.13; core [0.84, 0.078, 0.912, 0.019] rim [0.592, 0.255, 0.644, 0.17]
  - track 172 at frame 174: holes 0, rim-vs-core 0.40, rim-vs-outside 0.57, heterogeneity 0.13; core [0.824, 0.08, 0.905, 0.741] rim [0.598, 0.257, 0.65, 0.626]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 327 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 3.01 (aggregate of 327 individuals; 2/327 membrane-like individually; rim level 0.75)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 9.47, rim/outside 1.04 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.463)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 3.25 (aggregate of 327 individuals; 1/327 membrane-like individually; rim level 0.807)
  - radial p_x: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.01 (aggregate of 327 individuals; 0/327 membrane-like individually; rim level 0.488)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #78 (t=1560, R_eq 6.56): none; #88 (t=1560, R_eq 5.64): none; #131 (t=1610, R_eq 6.02): none; #172 (t=1740, R_eq 6.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 327 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
