# Evidence pack: fed-vortices (seed 31)

- world: `../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 614s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0835-c63-review-vortex-trait-climb/world.py --out collective/contrib/20261028T0835-c63-review-vortex-trait-climb/pack_sel --seeds 31 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2096], min area 6 px

## Measurements
- components: final 29, mean 31.5, max 48; occupancy final 0.35
- tracks: 1936; persistent (alive >= 50% of run): 0; longest 464 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.24, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 44, 29], H1 [4, 1, 0]
- motion: 317 long-lived tracks moved >= 1 body length; max speed 1/time; max body lengths 47.9
- replication (lineage window K = 20 frames = time 60, default): splits 676, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 10, merges 613, merge/split ratio 0.907, nucleations 1
- channel total drift (end/start - 1): [0.0403, -0.2388, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 235: holes 0, rim-vs-core 0.71, rim-vs-outside 0.33, heterogeneity 0.16; core [0.814, 0.183, 0.844, 0.013] rim [0.379, 0.381, 0.318, 0.013]
  - track 64 at frame 244: holes 0, rim-vs-core 0.66, rim-vs-outside 0.38, heterogeneity 0.15; core [0.847, 0.174, 0.879, 0.013] rim [0.431, 0.357, 0.393, 0.014]
  - track 61 at frame 244: holes 0, rim-vs-core 0.71, rim-vs-outside 0.35, heterogeneity 0.16; core [0.799, 0.153, 0.867, 0.013] rim [0.399, 0.401, 0.336, 0.013]
  - track 1813 at frame 983: holes 0, rim-vs-core 0.73, rim-vs-outside 0.40, heterogeneity 0.19; core [0.842, 0.156, 0.832, 0.547] rim [0.404, 0.272, 0.349, 0.23]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 177 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.749, rim/outside 4.46 (aggregate of 177 individuals; 5/177 membrane-like individually; rim level 0.545)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 3.52, rim/outside 0.851 (aggregate of 177 individuals; 0/177 membrane-like individually; rim level 0.41)
  - radial label c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.734, rim/outside 5.03 (aggregate of 177 individuals; 5/177 membrane-like individually; rim level 0.569)
  - radial trait theta*c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.679, rim/outside 2.77 (aggregate of 177 individuals; 6/177 membrane-like individually; rim level 0.212)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=705, R_eq 4.33): none; #64 (t=732, R_eq 3.83): none; #61 (t=732, R_eq 5.35): none; #1813 (t=2949, R_eq 3.24): none

## Warnings
- radial: 14 of 177 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
