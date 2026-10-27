# Evidence pack: reacting-thermals (seed 42)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.7097], min area 6 px

## Measurements
- components: final 15, mean 11.0, max 43; occupancy final 0.02
- tracks: 154; persistent (alive >= 50% of run): 2; longest 107 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.38 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 17, 16], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.929/time; max body lengths 18.7
- replication (lineage window K = 20 frames = time 20, default): splits 50, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.18, nucleations 13
- channel total drift (end/start - 1): [-0.8577, -0.234, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 119 at frame 148: holes 0, rim-vs-core 0.17, rim-vs-outside 0.52, heterogeneity 0.15; core [0.741, 0.193, 0.453, 0.828] rim [0.614, 0.235, 0.469, 0.72]
  - track 121 at frame 148: holes 0, rim-vs-core 0.17, rim-vs-outside 0.40, heterogeneity 0.10; core [0.665, 0.194, 0.447, 0.738] rim [0.549, 0.233, 0.485, 0.628]
  - track 136 at frame 166: holes 0, rim-vs-core 0.28, rim-vs-outside 0.52, heterogeneity 0.17; core [0.844, 0.197, 0.319, 0.943] rim [0.648, 0.246, 0.406, 0.772]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.954, rim/outside 5.24 (aggregate of 48 individuals; 3/48 membrane-like individually; rim level 0.527)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.77, rim/outside 0.742 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.339)
  - radial vorticity: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.03 (aggregate of 48 individuals; 8/48 membrane-like individually; rim level 0.475)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.32 (aggregate of 48 individuals; 6/48 membrane-like individually; rim level 0.583)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #119 (t=148, R_eq 3.57, ring): ['heat T', 'burn r']; #121 (t=148, R_eq 2.39): none; #126 (t=153, R_eq 1.87): none; #136 (t=166, R_eq 2.03): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
