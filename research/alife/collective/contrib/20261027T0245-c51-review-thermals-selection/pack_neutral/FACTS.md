# Evidence pack: reacting-thermals (seed 6)

- world: `../../20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 114s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/20261027T0245-c51-review-thermals-selection/pack_neutral --seeds 6 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.6906], min area 6 px

## Measurements
- components: final 27, mean 20.2, max 38; occupancy final 0.02
- tracks: 941; persistent (alive >= 50% of run): 0; longest 224 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 35, 27], H1 [0, 0, 0]
- motion: 356 long-lived tracks moved >= 1 body length; max speed 1.14/time; max body lengths 36.8
- replication (lineage window K = 20 frames = time 20, default): splits 186, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 7, merges 32, merge/split ratio 0.172, nucleations 510
- channel total drift (end/start - 1): [-0.8554, -0.3365, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 315 at frame 585: holes 0, rim-vs-core 0.24, rim-vs-outside 0.48, heterogeneity 0.08; core [0.969, 0.006, 1.0, 0.057] rim [0.779, 0.055, 0.861, 0.045]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.933, rim/outside 6.12 (aggregate of 85 individuals; 2/85 membrane-like individually; rim level 0.76)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9.5, rim/outside 0.571 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.174)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 4.83 (aggregate of 85 individuals; 2/85 membrane-like individually; rim level 0.638)
  - radial label b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.02 (aggregate of 85 individuals; 3/85 membrane-like individually; rim level 0.294)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #126 (t=363, R_eq 1.95): none; #259 (t=555, R_eq 2.11): none; #462 (t=817, R_eq 2.26): none; #315 (t=585, R_eq 2.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
