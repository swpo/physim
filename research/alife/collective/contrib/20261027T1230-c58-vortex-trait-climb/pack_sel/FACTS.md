# Evidence pack: fed-vortices (seed 1)

- world: `../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 2001 frames x 150 steps x dt 0.02 = time 6000; grid [128, 128]; wall 1089s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261027T1230-c58-vortex-trait-climb/world.py --out /home/user/physim/research/alife/collective/contrib/20261027T1230-c58-vortex-trait-climb/pack_sel --seeds 1 --frames 2000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2071], min area 6 px

## Measurements
- components: final 27, mean 29.1, max 49; occupancy final 0.40
- tracks: 4916; persistent (alive >= 50% of run): 0; longest 596 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.37, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [73, 53, 30], H1 [2, 0, 0]
- motion: 593 long-lived tracks moved >= 1 body length; max speed 1.05/time; max body lengths 78.3
- replication (lineage window K = 20 frames = time 60, default): splits 1702, persistent splits 67 (0 more failed only because the siblings re-merged within K), max generation 17, merges 1625, merge/split ratio 0.955, nucleations 6
- channel total drift (end/start - 1): [0.151, -0.2918, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 73 at frame 319: holes 0, rim-vs-core 0.66, rim-vs-outside 0.35, heterogeneity 0.15; core [0.785, 0.172, 0.859, 0.012] rim [0.406, 0.395, 0.36, 0.012]
  - track 32 at frame 286: holes 0, rim-vs-core 0.38, rim-vs-outside 0.64, heterogeneity 0.16; core [0.805, 0.194, 0.849, 0.012] rim [0.574, 0.303, 0.572, 0.012]
  - track 18 at frame 235: holes 0, rim-vs-core 0.64, rim-vs-outside 0.39, heterogeneity 0.15; core [0.833, 0.298, 0.865, 0.0] rim [0.427, 0.472, 0.399, 0.0]
  - track 4006 at frame 1782: holes 0, rim-vs-core 0.72, rim-vs-outside 0.35, heterogeneity 0.20; core [0.788, 0.087, 0.831, 0.628] rim [0.391, 0.203, 0.354, 0.274]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 3.56 (aggregate of 165 individuals; 7/165 membrane-like individually; rim level 0.528)
  - radial fuel Y: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.13, rim/outside 0.867 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.384)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.732, rim/outside 3.91 (aggregate of 165 individuals; 11/165 membrane-like individually; rim level 0.535)
  - radial trait theta*c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 2.3 (aggregate of 165 individuals; 9/165 membrane-like individually; rim level 0.226)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #73 (t=957, R_eq 5.41): none; #32 (t=858, R_eq 4.62): none; #18 (t=705, R_eq 3.48): none; #4006 (t=5346, R_eq 3.91): none

## Warnings
- radial: 18 of 165 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
