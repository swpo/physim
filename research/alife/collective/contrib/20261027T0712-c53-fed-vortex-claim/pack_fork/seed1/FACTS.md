# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 751 frames x 150 steps x dt 0.02 = time 2250; grid [128, 128]; wall 238s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack_fork --seeds 0 1 --frames 750 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2065], min area 6 px

## Measurements
- components: final 0, mean 30.2, max 49; occupancy final 0.00
- tracks: 232; persistent (alive >= 50% of run): 13; longest 684 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 6, 2], H1 [0, 0, 0]
- motion: 116 long-lived tracks moved >= 1 body length; max speed 0.365/time; max body lengths 33.9
- replication (lineage window K = 20 frames = time 60, default): splits 64, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 56, merge/split ratio 0.875, nucleations 0
- channel total drift (end/start - 1): [-1.0, 0.0255, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 40 at frame 340: holes 0, rim-vs-core 0.77, rim-vs-outside 0.29, heterogeneity 0.20; core [0.815, 0.112, 0.921, 0.68] rim [0.387, 0.321, 0.695, 0.119]
  - track 17 at frame 340: holes 0, rim-vs-core 0.84, rim-vs-outside 0.30, heterogeneity 0.21; core [0.838, 0.14, 0.054, 0.772] rim [0.39, 0.333, 0.276, 0.128]
  - track 5 at frame 340: holes 0, rim-vs-core 0.80, rim-vs-outside 0.32, heterogeneity 0.20; core [0.852, 0.107, 0.047, 0.769] rim [0.426, 0.316, 0.257, 0.157]
  - track 211 at frame 624: holes 0, rim-vs-core 0.77, rim-vs-outside 0.29, heterogeneity 0.20; core [0.816, 0.141, 0.919, 0.731] rim [0.404, 0.318, 0.705, 0.139]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 164 components >= 12 px at frames [126, 252, 378, 498, 624]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 15.5 (aggregate of 164 individuals; 1/164 membrane-like individually; rim level 0.685)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.777 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.465)
  - radial vorticity (signed): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.996 (aggregate of 164 individuals; 0/164 membrane-like individually; rim level 0.485)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 26.8 (aggregate of 164 individuals; 3/164 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #40 (t=1020, R_eq 4.62): none; #17 (t=1020, R_eq 3.99): none; #5 (t=1020, R_eq 4.26): none; #211 (t=1872, R_eq 4.18): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 164 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
