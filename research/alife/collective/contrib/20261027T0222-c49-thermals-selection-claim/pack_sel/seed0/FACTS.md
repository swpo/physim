# Evidence pack: reacting-thermals (seed 0)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 131s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/20261027T0222-c49-thermals-selection-claim/pack_sel --seeds 0 1 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7543], min area 6 px

## Measurements
- components: final 29, mean 18.8, max 43; occupancy final 0.02
- tracks: 813; persistent (alive >= 50% of run): 0; longest 214 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 38, 29], H1 [0, 0, 0]
- motion: 359 long-lived tracks moved >= 1 body length; max speed 1.01/time; max body lengths 30.9
- replication (lineage window K = 20 frames = time 20, default): splits 182, persistent splits 69 (0 more failed only because the siblings re-merged within K), max generation 8, merges 19, merge/split ratio 0.104, nucleations 399
- channel total drift (end/start - 1): [-0.8476, -0.367, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 249 at frame 575: holes 0, rim-vs-core 0.11, rim-vs-outside 0.43, heterogeneity 0.08; core [0.855, 0.0, 0.055, 0.967] rim [0.758, 0.036, 0.057, 0.94]
  - track 260 at frame 585: holes 0, rim-vs-core 0.22, rim-vs-outside 0.61, heterogeneity 0.10; core [0.922, 0.05, 0.981, 0.286] rim [0.745, 0.121, 0.879, 0.226]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 6.02 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.725)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.26, rim/outside 0.579 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.181)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 3.86 (aggregate of 84 individuals; 1/84 membrane-like individually; rim level 0.361)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 5.22 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.629)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #249 (t=575, R_eq 2.39): ['label a']; #490 (t=887, R_eq 1.95): none; #260 (t=585, R_eq 2.52): none; #359 (t=666, R_eq 1.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
