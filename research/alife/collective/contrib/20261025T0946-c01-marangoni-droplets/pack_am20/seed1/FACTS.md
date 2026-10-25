# Evidence pack: marangoni-droplets (seed 1)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 263s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T0946-c01-marangoni-droplets/pack_am20 --seeds 0 1 --no-movie`
- segmentation: matter > 0.46 of robust range [-1.05, 1.2544], min area 6 px

## Measurements
- components: final 8, mean 5.0, max 8; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 2; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.24 (1 = constant size)
- enclosures: components with a hole mean 0.36, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 8], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00164/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1162, -0.5295, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 141: holes 0, rim-vs-core 0.19, rim-vs-outside 0.52, heterogeneity 0.11; core [0.89, 0.029, 0.289] rim [0.736, 0.117, 0.214]
  - track 5 at frame 141: holes 0, rim-vs-core 0.19, rim-vs-outside 0.52, heterogeneity 0.11; core [0.886, 0.029, 0.293] rim [0.732, 0.118, 0.218]
  - track 6 at frame 155: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.10; core [0.94, 0.025, 0.234] rim [0.734, 0.109, 0.178]
  - track 10 at frame 158: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.10; core [0.962, 0.023, 0.354] rim [0.744, 0.104, 0.231]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 24.6 (aggregate of 32 individuals; 8/32 membrane-like individually; rim level 0.795)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.7, rim/outside 0.617 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.203)
  - radial |v| (flow speed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.829, rim/outside 3.17 (aggregate of 32 individuals; 2/32 membrane-like individually; rim level 0.271)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=14100, R_eq 8.79): none; #5 (t=14100, R_eq 8.83): none; #6 (t=15500, R_eq 8.2): none; #10 (t=15800, R_eq 7.76): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
