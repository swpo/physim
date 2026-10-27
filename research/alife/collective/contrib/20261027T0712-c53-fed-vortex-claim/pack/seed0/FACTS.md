# Evidence pack: fed-vortices (seed 0)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 278s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack --seeds 0 1 2 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2036], min area 6 px

## Measurements
- components: final 26, mean 28.5, max 50; occupancy final 0.14
- tracks: 288; persistent (alive >= 50% of run): 13; longest 1001 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.77 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 26], H1 [0, 0, 0]
- motion: 149 long-lived tracks moved >= 1 body length; max speed 0.528/time; max body lengths 47.1
- replication (lineage window K = 20 frames = time 60, default): splits 79, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 10, merges 81, merge/split ratio 1.02, nucleations 0
- channel total drift (end/start - 1): [-0.5593, 0.1702, -4283.8481, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 504: holes 0, rim-vs-core 0.76, rim-vs-outside 0.31, heterogeneity 0.20; core [0.827, 0.111, 0.93, 0.696] rim [0.405, 0.322, 0.71, 0.139]
  - track 42 at frame 462: holes 0, rim-vs-core 0.78, rim-vs-outside 0.36, heterogeneity 0.20; core [0.871, 0.111, 0.949, 0.818] rim [0.472, 0.296, 0.746, 0.21]
  - track 21 at frame 454: holes 0, rim-vs-core 0.82, rim-vs-outside 0.31, heterogeneity 0.21; core [0.841, 0.124, 0.934, 0.769] rim [0.405, 0.323, 0.71, 0.14]
  - track 267 at frame 975: holes 0, rim-vs-core 0.63, rim-vs-outside 0.32, heterogeneity 0.17; core [0.785, 0.105, 0.074, 0.617] rim [0.433, 0.317, 0.259, 0.171]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 15.1 (aggregate of 166 individuals; 2/166 membrane-like individually; rim level 0.676)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.29, rim/outside 0.77 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.476)
  - radial vorticity (signed): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.983 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.477)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.741, rim/outside 24.2 (aggregate of 166 individuals; 7/166 membrane-like individually; rim level 0.524)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=1512, R_eq 4.72): none; #42 (t=1386, R_eq 3.95): none; #21 (t=1362, R_eq 4.15): none; #267 (t=2925, R_eq 5.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
