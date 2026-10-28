# Evidence pack: fed-vortices (seed 12)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T1401-c58-vortex-trait3d/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 1235s; status ok
- command: `python -m labkit.run collective/contrib/20261027T1401-c58-vortex-trait3d/world.py --out /tmp/claude-0/-home-user-physim/2d575f79-4c3f-55f6-aa7f-4e952f913959/scratchpad/lmpack --seeds 11 12 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2088], min area 6 px

## Measurements
- components: final 27, mean 36.4, max 47; occupancy final 0.34
- tracks: 2517; persistent (alive >= 50% of run): 0; longest 221 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 48, 31], H1 [4, 0, 0]
- motion: 527 long-lived tracks moved >= 1 body length; max speed 1.17/time; max body lengths 43.7
- replication (lineage window K = 20 frames = time 60, default): splits 859, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 12, merges 802, merge/split ratio 0.934, nucleations 1
- channel total drift (end/start - 1): [0.012, -0.2123, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 147 at frame 168: holes 0, rim-vs-core 0.66, rim-vs-outside 0.37, heterogeneity 0.16; core [0.815, 0.131, 0.868, 0.648] rim [0.415, 0.342, 0.389, 0.648]
  - track 73 at frame 118: holes 0, rim-vs-core 0.59, rim-vs-outside 0.38, heterogeneity 0.14; core [0.823, 0.154, 0.868, 0.648] rim [0.441, 0.315, 0.444, 0.648]
  - track 1215 at frame 597: holes 0, rim-vs-core 0.67, rim-vs-outside 0.36, heterogeneity 0.16; core [0.805, 0.127, 0.856, 0.777] rim [0.395, 0.317, 0.365, 0.701]
  - track 2246 at frame 950: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.18; core [0.835, 0.195, 0.864, 0.389] rim [0.404, 0.389, 0.363, 0.541]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 209 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 3.8 (aggregate of 209 individuals; 9/209 membrane-like individually; rim level 0.506)
  - radial fuel Y: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.23, rim/outside 0.867 (aggregate of 209 individuals; 0/209 membrane-like individually; rim level 0.473)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.684, rim/outside 4.16 (aggregate of 209 individuals; 10/209 membrane-like individually; rim level 0.514)
  - radial trait z_1: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.984 (aggregate of 209 individuals; 0/209 membrane-like individually; rim level 0.608)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #147 (t=504, R_eq 4.44): none; #73 (t=354, R_eq 3.66): none; #1215 (t=1791, R_eq 4.48): none; #2246 (t=2850, R_eq 3.61): none

## Warnings
- radial: 14 of 209 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
