# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 134s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/20261027T0222-c49-thermals-selection-claim/pack_sel --seeds 0 1 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.40 of robust range [0.0, 0.6182], min area 6 px

## Measurements
- components: final 24, mean 21.4, max 47; occupancy final 0.03
- tracks: 997; persistent (alive >= 50% of run): 0; longest 275 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 28, 25], H1 [0, 0, 0]
- motion: 403 long-lived tracks moved >= 1 body length; max speed 1.27/time; max body lengths 34.7
- replication (lineage window K = 20 frames = time 20, default): splits 206, persistent splits 59 (0 more failed only because the siblings re-merged within K), max generation 9, merges 29, merge/split ratio 0.141, nucleations 533
- channel total drift (end/start - 1): [-0.822, -0.3446, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 443 at frame 716: holes 0, rim-vs-core 0.26, rim-vs-outside 0.57, heterogeneity 0.10; core [0.95, 0.0, 0.171, 0.966] rim [0.747, 0.049, 0.173, 0.808]
  - track 267 at frame 524: holes 0, rim-vs-core 0.17, rim-vs-outside 0.57, heterogeneity 0.08; core [0.929, 0.001, 0.065, 1.0] rim [0.782, 0.036, 0.053, 0.923]
  - track 728 at frame 958: holes 0, rim-vs-core 0.27, rim-vs-outside 0.57, heterogeneity 0.09; core [0.965, 0.006, 0.185, 0.949] rim [0.768, 0.07, 0.147, 0.787]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 90 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 5.33 (aggregate of 90 individuals; 2/90 membrane-like individually; rim level 0.686)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.68, rim/outside 0.554 (aggregate of 90 individuals; 0/90 membrane-like individually; rim level 0.164)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 3.41 (aggregate of 90 individuals; 2/90 membrane-like individually; rim level 0.272)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 4.5 (aggregate of 90 individuals; 2/90 membrane-like individually; rim level 0.608)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #419 (t=706, R_eq 1.87): none; #443 (t=716, R_eq 2.93): none; #267 (t=524, R_eq 2.26): none; #728 (t=958, R_eq 2.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 90 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
