# Evidence pack: reacting-thermals (seed 41)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7527], min area 6 px

## Measurements
- components: final 10, mean 9.4, max 42; occupancy final 0.02
- tracks: 153; persistent (alive >= 50% of run): 0; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 12], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 1.12/time; max body lengths 18.5
- replication (lineage window K = 20 frames = time 20, default): splits 39, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.256, nucleations 27
- channel total drift (end/start - 1): [-0.9154, -0.1962, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 81: holes 0, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.16; core [0.787, 0.236, 0.65, 0.934] rim [0.568, 0.292, 0.59, 0.747]
  - track 111 at frame 126: holes 0, rim-vs-core 0.14, rim-vs-outside 0.47, heterogeneity 0.16; core [0.652, 0.201, 0.395, 0.732] rim [0.558, 0.256, 0.477, 0.683]
  - track 130 at frame 166: holes 0, rim-vs-core 0.23, rim-vs-outside 0.41, heterogeneity 0.14; core [0.689, 0.227, 0.543, 0.828] rim [0.551, 0.243, 0.498, 0.656]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.797, rim/outside 5 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.463)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.65, rim/outside 0.781 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.377)
  - radial vorticity: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.09 (aggregate of 42 individuals; 7/42 membrane-like individually; rim level 0.483)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 5.97 (aggregate of 42 individuals; 2/42 membrane-like individually; rim level 0.551)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=81, R_eq 2.19): ['vorticity']; #100 (t=77, R_eq 1.69): ['vorticity']; #111 (t=126, R_eq 3.09): ['burn r']; #130 (t=166, R_eq 2.82): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 42 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
