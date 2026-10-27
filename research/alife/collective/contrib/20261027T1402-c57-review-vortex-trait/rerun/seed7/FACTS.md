# Evidence pack: fed-vortices (seed 7)

- world: `../../20261027T1230-c58-vortex-trait-climb/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 2001 frames x 150 steps x dt 0.02 = time 6000; grid [128, 128]; wall 1181s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1230-c58-vortex-trait-climb/world.py --out collective/contrib/c57-w6/rerun_sel --seeds 7 --frames 2000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2048], min area 6 px

## Measurements
- components: final 29, mean 30.9, max 44; occupancy final 0.39
- tracks: 4216; persistent (alive >= 50% of run): 0; longest 673 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [71, 56, 34], H1 [12, 0, 0]
- motion: 394 long-lived tracks moved >= 1 body length; max speed 0.702/time; max body lengths 34.4
- replication (lineage window K = 20 frames = time 60, default): splits 1433, persistent splits 48 (0 more failed only because the siblings re-merged within K), max generation 16, merges 1384, merge/split ratio 0.966, nucleations 0
- channel total drift (end/start - 1): [0.1563, -0.308, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2492 at frame 1664: holes 0, rim-vs-core 0.76, rim-vs-outside 0.38, heterogeneity 0.19; core [0.82, 0.087, 0.868, 0.553] rim [0.396, 0.249, 0.354, 0.23]
  - track 87 at frame 387: holes 0, rim-vs-core 0.66, rim-vs-outside 0.40, heterogeneity 0.16; core [0.865, 0.193, 0.887, 0.007] rim [0.452, 0.397, 0.41, 0.007]
  - track 60 at frame 286: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.15; core [0.769, 0.186, 0.833, 0.008] rim [0.392, 0.387, 0.341, 0.008]
  - track 4100 at frame 1983: holes 0, rim-vs-core 0.86, rim-vs-outside 0.48, heterogeneity 0.22; core [0.821, 0.061, 0.874, 0.943] rim [0.413, 0.216, 0.353, 0.409]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 177 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.736, rim/outside 3.29 (aggregate of 177 individuals; 9/177 membrane-like individually; rim level 0.509)
  - radial fuel Y: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 3.01, rim/outside 0.892 (aggregate of 177 individuals; 0/177 membrane-like individually; rim level 0.382)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.713, rim/outside 3.7 (aggregate of 177 individuals; 10/177 membrane-like individually; rim level 0.521)
  - radial trait theta*c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.704, rim/outside 2.69 (aggregate of 177 individuals; 9/177 membrane-like individually; rim level 0.258)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2492 (t=4992, R_eq 4.75): none; #87 (t=1161, R_eq 4.03): none; #60 (t=858, R_eq 5.35): none; #4100 (t=5949, R_eq 5.86): none

## Warnings
- radial: 15 of 177 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
