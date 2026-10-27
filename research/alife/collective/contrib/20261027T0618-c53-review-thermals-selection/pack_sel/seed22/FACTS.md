# Evidence pack: reacting-thermals (seed 22)

- world: `../../../20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 129s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/c53-rev-sel/pack_sel --seeds 21 22 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7307], min area 6 px

## Measurements
- components: final 30, mean 20.4, max 45; occupancy final 0.03
- tracks: 1031; persistent (alive >= 50% of run): 0; longest 204 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 38, 29], H1 [0, 0, 0]
- motion: 401 long-lived tracks moved >= 1 body length; max speed 1.27/time; max body lengths 32.1
- replication (lineage window K = 20 frames = time 20, default): splits 197, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 7, merges 31, merge/split ratio 0.157, nucleations 578
- channel total drift (end/start - 1): [-0.8534, -0.3806, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 427 at frame 716: holes 0, rim-vs-core 0.20, rim-vs-outside 0.54, heterogeneity 0.10; core [0.945, 0.002, 0.18, 0.935] rim [0.781, 0.052, 0.151, 0.834]
  - track 661 at frame 918: holes 0, rim-vs-core 0.17, rim-vs-outside 0.58, heterogeneity 0.09; core [0.953, 0.0, 0.129, 0.963] rim [0.807, 0.049, 0.114, 0.882]
  - track 761 at frame 1018: holes 0, rim-vs-core 0.34, rim-vs-outside 0.47, heterogeneity 0.16; core [0.933, 0.031, 0.387, 0.895] rim [0.722, 0.082, 0.463, 0.642]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 5.72 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.69)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.34, rim/outside 0.573 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.175)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 3.39 (aggregate of 92 individuals; 1/92 membrane-like individually; rim level 0.31)
  - radial label b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 4.83 (aggregate of 92 individuals; 1/92 membrane-like individually; rim level 0.591)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #427 (t=716, R_eq 2.26): none; #661 (t=918, R_eq 2.52): none; #761 (t=1018, R_eq 2.19): none; #432 (t=676, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
