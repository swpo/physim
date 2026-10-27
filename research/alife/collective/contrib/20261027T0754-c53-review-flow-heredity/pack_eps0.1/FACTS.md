# Evidence pack: reacting-thermals (seed 21)

- world: `../../20261027T0209-c49-thermals-flow-heredity/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 801 frames x 25 steps x dt 0.04 = time 800; grid [128, 128]; wall 95s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0209-c49-thermals-flow-heredity/world.py --out collective/contrib/c53-rev-fh/pack_eps0.1 --seeds 21 --frames 800 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.742], min area 6 px

## Measurements
- components: final 32, mean 18.9, max 42; occupancy final 0.03
- tracks: 615; persistent (alive >= 50% of run): 0; longest 186 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 44, 35], H1 [0, 0, 0]
- motion: 243 long-lived tracks moved >= 1 body length; max speed 1.16/time; max body lengths 22.3
- replication (lineage window K = 20 frames = time 20, default): splits 131, persistent splits 47 (0 more failed only because the siblings re-merged within K), max generation 8, merges 17, merge/split ratio 0.13, nucleations 298
- channel total drift (end/start - 1): [-0.8266, -0.3957, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 379 at frame 632: holes 0, rim-vs-core 0.28, rim-vs-outside 0.59, heterogeneity 0.09; core [0.993, 0.058, 0.986, 0.297] rim [0.775, 0.103, 0.832, 0.234]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 5.84 (aggregate of 85 individuals; 1/85 membrane-like individually; rim level 0.691)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.54, rim/outside 0.625 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.198)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 5.06 (aggregate of 85 individuals; 3/85 membrane-like individually; rim level 0.655)
  - radial label b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 3.55 (aggregate of 85 individuals; 5/85 membrane-like individually; rim level 0.207)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #247 (t=565, R_eq 1.95): none; #442 (t=713, R_eq 1.78): none; #185 (t=457, R_eq 1.87): none; #379 (t=632, R_eq 2.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
