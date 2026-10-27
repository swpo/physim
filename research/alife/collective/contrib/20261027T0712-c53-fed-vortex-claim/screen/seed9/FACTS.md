# Evidence pack: fed-vortices (seed 9)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 47s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2103], min area 6 px

## Measurements
- components: final 36, mean 41.4, max 49; occupancy final 0.14
- tracks: 100; persistent (alive >= 50% of run): 39; longest 151 frames; alive start-to-end: 13
- size of persistent tracks: max/min area ratio 8.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 37], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.267/time; max body lengths 15.3
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 12, merge/split ratio 0.545, nucleations 0
- channel total drift (end/start - 1): [-0.5459, 0.1343, 470.4298, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 76: holes 0, rim-vs-core 0.77, rim-vs-outside 0.32, heterogeneity 0.20; core [0.832, 0.114, 0.923, 0.732] rim [0.423, 0.318, 0.707, 0.156]
  - track 4 at frame 76: holes 0, rim-vs-core 0.73, rim-vs-outside 0.32, heterogeneity 0.19; core [0.82, 0.108, 0.919, 0.678] rim [0.419, 0.338, 0.705, 0.154]
  - track 7 at frame 76: holes 0, rim-vs-core 0.76, rim-vs-outside 0.30, heterogeneity 0.20; core [0.805, 0.162, 0.908, 0.723] rim [0.406, 0.322, 0.698, 0.136]
  - track 52 at frame 78: holes 0, rim-vs-core 0.72, rim-vs-outside 0.29, heterogeneity 0.19; core [0.801, 0.116, 0.908, 0.661] rim [0.402, 0.327, 0.696, 0.138]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 242 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.717, rim/outside 15.8 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.652)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.49, rim/outside 0.789 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.485)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 1.11 (aggregate of 242 individuals; 0/242 membrane-like individually; rim level 0.535)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.598, rim/outside 29.8 (aggregate of 242 individuals; 4/242 membrane-like individually; rim level 0.483)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=228, R_eq 4.15): none; #4 (t=228, R_eq 4.58): none; #7 (t=228, R_eq 3.52): none; #52 (t=234, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 242 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
