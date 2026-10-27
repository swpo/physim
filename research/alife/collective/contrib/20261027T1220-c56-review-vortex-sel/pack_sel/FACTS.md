# Evidence pack: fed-vortices (seed 4)

- world: `../../../collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 907s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0845-c53-fed-vortex-selection-claim/world.py --out c56work/vs/pack_sel --seeds 4 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2114], min area 6 px

## Measurements
- components: final 32, mean 33.5, max 43; occupancy final 0.20
- tracks: 1361; persistent (alive >= 50% of run): 0; longest 517 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 40, 33], H1 [0, 0, 0]
- motion: 488 long-lived tracks moved >= 1 body length; max speed 0.706/time; max body lengths 30.6
- replication (lineage window K = 20 frames = time 60, default): splits 458, persistent splits 118 (0 more failed only because the siblings re-merged within K), max generation 23, merges 418, merge/split ratio 0.913, nucleations 0
- channel total drift (end/start - 1): [-0.3737, -0.002, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 252: holes 0, rim-vs-core 0.73, rim-vs-outside 0.38, heterogeneity 0.17; core [0.823, 0.141, 0.91, 0.005] rim [0.399, 0.388, 0.368, 0.002]
  - track 69 at frame 252: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.16; core [0.786, 0.133, 0.915, 0.006] rim [0.399, 0.39, 0.376, 0.003]
  - track 1 at frame 202: holes 0, rim-vs-core 0.62, rim-vs-outside 0.39, heterogeneity 0.14; core [0.741, 0.124, 0.927, 0.005] rim [0.427, 0.359, 0.445, 0.003]
  - track 1316 at frame 1462: holes 0, rim-vs-core 0.54, rim-vs-outside 0.53, heterogeneity 0.18; core [0.836, 0.081, 0.448, 0.755] rim [0.509, 0.259, 0.252, 0.425]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 192 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.735, rim/outside 9.32 (aggregate of 192 individuals; 6/192 membrane-like individually; rim level 0.592)
  - radial fuel Y: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.98, rim/outside 0.795 (aggregate of 192 individuals; 0/192 membrane-like individually; rim level 0.461)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.739, rim/outside 10 (aggregate of 192 individuals; 7/192 membrane-like individually; rim level 0.36)
  - radial label b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.729, rim/outside 9.66 (aggregate of 192 individuals; 6/192 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=756, R_eq 4.82): none; #69 (t=756, R_eq 5.44): none; #1 (t=606, R_eq 5.75): none; #1316 (t=4386, R_eq 4.98): none

## Warnings
- radial: 7 of 192 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
