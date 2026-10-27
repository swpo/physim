# Evidence pack: reacting-thermals (seed 21)

- world: `../../../20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 125s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out collective/contrib/c53-rev-sel/pack_neutral --seeds 21 22 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.742], min area 6 px

## Measurements
- components: final 22, mean 20.0, max 42; occupancy final 0.02
- tracks: 944; persistent (alive >= 50% of run): 0; longest 278 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 29, 25], H1 [0, 0, 0]
- motion: 381 long-lived tracks moved >= 1 body length; max speed 1.24/time; max body lengths 33.4
- replication (lineage window K = 20 frames = time 20, default): splits 164, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 6, merges 31, merge/split ratio 0.189, nucleations 553
- channel total drift (end/start - 1): [-0.8608, -0.3373, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 652 at frame 1029: holes 0, rim-vs-core 0.31, rim-vs-outside 0.55, heterogeneity 0.11; core [0.973, 0.039, 0.353, 0.917] rim [0.763, 0.113, 0.278, 0.721]
  - track 574 at frame 958: holes 0, rim-vs-core 0.16, rim-vs-outside 0.56, heterogeneity 0.10; core [0.95, 0.0, 0.111, 0.989] rim [0.817, 0.058, 0.101, 0.912]
  - track 195 at frame 454: holes 0, rim-vs-core 0.27, rim-vs-outside 0.63, heterogeneity 0.10; core [1.0, 0.025, 0.313, 0.994] rim [0.837, 0.084, 0.271, 0.79]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 5.67 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.713)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.74, rim/outside 0.585 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.178)
  - radial label a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 4.53 (aggregate of 84 individuals; 1/84 membrane-like individually; rim level 0.464)
  - radial label b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 4.22 (aggregate of 84 individuals; 3/84 membrane-like individually; rim level 0.431)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #577 (t=988, R_eq 2.11): none; #652 (t=1029, R_eq 2.19): none; #574 (t=958, R_eq 2.46): none; #195 (t=454, R_eq 2.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
