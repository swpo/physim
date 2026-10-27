# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 133s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/20261027T0222-c49-thermals-selection-claim/pack_neutral --seeds 0 1 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.41 of robust range [0.0, 0.6122], min area 6 px

## Measurements
- components: final 24, mean 19.5, max 47; occupancy final 0.02
- tracks: 1037; persistent (alive >= 50% of run): 0; longest 244 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 25], H1 [0, 0, 0]
- motion: 372 long-lived tracks moved >= 1 body length; max speed 1.5/time; max body lengths 46.7
- replication (lineage window K = 20 frames = time 20, default): splits 185, persistent splits 42 (0 more failed only because the siblings re-merged within K), max generation 5, merges 31, merge/split ratio 0.168, nucleations 612
- channel total drift (end/start - 1): [-0.8202, -0.3231, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 759 at frame 968: holes 0, rim-vs-core 0.11, rim-vs-outside 0.51, heterogeneity 0.07; core [0.867, 0.0, 0.942, 0.296] rim [0.789, 0.032, 0.876, 0.269]
  - track 127 at frame 192: holes 0, rim-vs-core 0.17, rim-vs-outside 0.49, heterogeneity 0.05; core [1.0, 0.001, 0.0, 0.0] rim [0.838, 0.054, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 87 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 5.61 (aggregate of 87 individuals; 1/87 membrane-like individually; rim level 0.713)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.82, rim/outside 0.565 (aggregate of 87 individuals; 0/87 membrane-like individually; rim level 0.173)
  - radial label a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 4.48 (aggregate of 87 individuals; 2/87 membrane-like individually; rim level 0.601)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 4.48 (aggregate of 87 individuals; 1/87 membrane-like individually; rim level 0.395)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #832 (t=1049, R_eq 2.03): none; #759 (t=968, R_eq 2.99, ring): ['heat T', 'label b']; #127 (t=192, R_eq 3.39): none; #530 (t=706, R_eq 1.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 87 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
