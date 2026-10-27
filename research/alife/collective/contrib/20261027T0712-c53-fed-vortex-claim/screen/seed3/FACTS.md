# Evidence pack: fed-vortices (seed 3)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2085], min area 6 px

## Measurements
- components: final 34, mean 35.2, max 45; occupancy final 0.14
- tracks: 96; persistent (alive >= 50% of run): 31; longest 151 frames; alive start-to-end: 13
- size of persistent tracks: max/min area ratio 3.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 36, 35], H1 [0, 0, 0]
- motion: 47 long-lived tracks moved >= 1 body length; max speed 0.351/time; max body lengths 12.7
- replication (lineage window K = 20 frames = time 60, default): splits 20, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.55, nucleations 0
- channel total drift (end/start - 1): [-0.5587, 0.1558, 1121.0721, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.76, rim-vs-outside 0.34, heterogeneity 0.20; core [0.85, 0.094, 0.041, 0.753] rim [0.436, 0.295, 0.244, 0.178]
  - track 5 at frame 76: holes 0, rim-vs-core 0.74, rim-vs-outside 0.27, heterogeneity 0.19; core [0.787, 0.142, 0.904, 0.681] rim [0.385, 0.267, 0.69, 0.113]
  - track 11 at frame 76: holes 0, rim-vs-core 0.44, rim-vs-outside 0.43, heterogeneity 0.17; core [0.746, 0.102, 0.078, 0.545] rim [0.49, 0.248, 0.215, 0.254]
  - track 54 at frame 81: holes 0, rim-vs-core 0.36, rim-vs-outside 0.62, heterogeneity 0.20; core [0.788, 0.132, 0.063, 0.667] rim [0.588, 0.217, 0.173, 0.396]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 206 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.736, rim/outside 16.1 (aggregate of 206 individuals; 2/206 membrane-like individually; rim level 0.649)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.12, rim/outside 0.781 (aggregate of 206 individuals; 0/206 membrane-like individually; rim level 0.443)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 1.07 (aggregate of 206 individuals; 0/206 membrane-like individually; rim level 0.519)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.634, rim/outside 27.9 (aggregate of 206 individuals; 6/206 membrane-like individually; rim level 0.479)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=228, R_eq 4.22): none; #5 (t=228, R_eq 3.34): none; #11 (t=228, R_eq 4.95): none; #54 (t=243, R_eq 4.22): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 206 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
