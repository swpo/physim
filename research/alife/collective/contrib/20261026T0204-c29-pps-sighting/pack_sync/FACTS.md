# Evidence pack: pps (seed 0)

- world: `../world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 112s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0230-c29-pps-sighting/world.py --out collective/contrib/20261026T0230-c29-pps-sighting/pack_sync --seeds 0 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 8.5938], min area 6 px

## Measurements
- components: final 44, mean 30.9, max 83; occupancy final 0.18
- tracks: 1827; persistent (alive >= 50% of run): 2; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.24 (1 = constant size)
- enclosures: components with a hole mean 0.40, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [72, 62, 49], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00337/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 3000, default): splits 641, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 598, merge/split ratio 0.933, nucleations 1
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 639 at frame 139: holes 0, rim-vs-core 0.12, rim-vs-outside 0.03, heterogeneity 0.14; core [0.111, 0.0, 0.111] rim [0.028, 0.0, 0.028]
  - track 759 at frame 148: holes 0, rim-vs-core 0.47, rim-vs-outside 0.02, heterogeneity 0.24; core [0.343, 0.111, 0.306] rim [0.0, 0.0, 0.0]
  - track 861 at frame 148: holes 0, rim-vs-core 0.44, rim-vs-outside 0.01, heterogeneity 0.20; core [0.317, 0.0, 0.3] rim [0.0, 0.0, 0.0]
  - track 621 at frame 126: holes 0, rim-vs-core 0.41, rim-vs-outside 0.03, heterogeneity 0.24; core [0.293, 0.034, 0.282] rim [0.0, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 203 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.683, rim/outside 3.53 (aggregate of 203 individuals; 57/203 membrane-like individually; rim level 0.163)
  - radial cell N>35: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.184, rim/outside 1.66 (aggregate of 203 individuals; 40/203 membrane-like individually; rim level 0.01)
  - radial ring 15<N<=35: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 6.38 (aggregate of 203 individuals; 70/203 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #639 (t=20850, R_eq 2.59): none; #759 (t=22200, R_eq 3.39): none; #861 (t=22200, R_eq 2.71): none; #621 (t=18900, R_eq 3.95): ['particles', 'ring 15<N<=35']

## Warnings
- radial: 6 of 203 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
