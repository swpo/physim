# Evidence pack: fed-vortices (seed 11)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T1401-c58-vortex-trait3d/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 1263s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1401-c58-vortex-trait3d/world.py --out /tmp/claude-0/-home-user-physim/2d575f79-4c3f-55f6-aa7f-4e952f913959/scratchpad/lmpack --seeds 11 12 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2095], min area 6 px

## Measurements
- components: final 30, mean 34.3, max 45; occupancy final 0.31
- tracks: 2497; persistent (alive >= 50% of run): 0; longest 337 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 48, 29], H1 [1, 0, 0]
- motion: 479 long-lived tracks moved >= 1 body length; max speed 1.17/time; max body lengths 81.7
- replication (lineage window K = 20 frames = time 60, default): splits 858, persistent splits 48 (0 more failed only because the siblings re-merged within K), max generation 13, merges 789, merge/split ratio 0.92, nucleations 3
- channel total drift (end/start - 1): [-0.0529, -0.1784, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 62 at frame 185: holes 0, rim-vs-core 0.69, rim-vs-outside 0.37, heterogeneity 0.16; core [0.82, 0.117, 0.86, 0.714] rim [0.416, 0.351, 0.355, 0.714]
  - track 260 at frame 218: holes 0, rim-vs-core 0.69, rim-vs-outside 0.38, heterogeneity 0.16; core [0.843, 0.126, 0.877, 0.714] rim [0.418, 0.35, 0.379, 0.714]
  - track 209 at frame 202: holes 0, rim-vs-core 0.70, rim-vs-outside 0.40, heterogeneity 0.16; core [0.871, 0.132, 0.89, 0.714] rim [0.439, 0.363, 0.384, 0.714]
  - track 2393 at frame 992: holes 0, rim-vs-core 0.60, rim-vs-outside 0.62, heterogeneity 0.21; core [0.836, 0.082, 0.908, 0.404] rim [0.5, 0.267, 0.492, 0.591]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 203 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 4.07 (aggregate of 203 individuals; 7/203 membrane-like individually; rim level 0.511)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.58, rim/outside 0.853 (aggregate of 203 individuals; 0/203 membrane-like individually; rim level 0.465)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.681, rim/outside 4.44 (aggregate of 203 individuals; 9/203 membrane-like individually; rim level 0.516)
  - radial trait z_1: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.27, rim/outside 0.993 (aggregate of 203 individuals; 0/203 membrane-like individually; rim level 0.679)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #62 (t=555, R_eq 4.89): none; #260 (t=654, R_eq 4.33): none; #209 (t=606, R_eq 3.99): none; #2393 (t=2976, R_eq 6.18): none

## Warnings
- radial: 15 of 203 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
