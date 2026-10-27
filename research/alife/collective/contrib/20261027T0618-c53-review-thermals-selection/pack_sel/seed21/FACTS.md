# Evidence pack: reacting-thermals (seed 21)

- world: `../../../20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 126s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/c53-rev-sel/pack_sel --seeds 21 22 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7426], min area 6 px

## Measurements
- components: final 25, mean 19.0, max 42; occupancy final 0.02
- tracks: 987; persistent (alive >= 50% of run): 0; longest 243 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 33, 29], H1 [0, 0, 0]
- motion: 373 long-lived tracks moved >= 1 body length; max speed 1.33/time; max body lengths 32.5
- replication (lineage window K = 20 frames = time 20, default): splits 192, persistent splits 53 (0 more failed only because the siblings re-merged within K), max generation 6, merges 35, merge/split ratio 0.182, nucleations 538
- channel total drift (end/start - 1): [-0.8668, -0.3484, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 569 at frame 897: holes 0, rim-vs-core 0.21, rim-vs-outside 0.47, heterogeneity 0.09; core [0.901, 0.008, 0.289, 0.984] rim [0.755, 0.043, 0.247, 0.845]
  - track 633 at frame 948: holes 0, rim-vs-core 0.30, rim-vs-outside 0.54, heterogeneity 0.11; core [0.979, 0.019, 0.305, 0.98] rim [0.759, 0.071, 0.235, 0.798]
  - track 342 at frame 645: holes 0, rim-vs-core 0.16, rim-vs-outside 0.41, heterogeneity 0.07; core [0.912, 0.052, 1.0, 0.244] rim [0.764, 0.101, 0.973, 0.224]
  - track 350 at frame 605: holes 0, rim-vs-core 0.30, rim-vs-outside 0.58, heterogeneity 0.09; core [0.977, 0.012, 0.282, 0.995] rim [0.762, 0.076, 0.214, 0.802]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 6.07 (aggregate of 86 individuals; 3/86 membrane-like individually; rim level 0.699)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.01, rim/outside 0.62 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.194)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 3.84 (aggregate of 86 individuals; 2/86 membrane-like individually; rim level 0.317)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 5.03 (aggregate of 86 individuals; 3/86 membrane-like individually; rim level 0.612)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #569 (t=897, R_eq 2.11): none; #633 (t=948, R_eq 2.19): none; #342 (t=645, R_eq 2.19): none; #350 (t=605, R_eq 2.93): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
