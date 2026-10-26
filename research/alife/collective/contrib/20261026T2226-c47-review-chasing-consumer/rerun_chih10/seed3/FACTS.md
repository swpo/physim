# Evidence pack: cips-consumer (seed 3)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 31 frames x 1000 steps x dt 0.1 (--dt; world META dt 0.25) = time 3000; grid [128, 128]; wall 197s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2226-c47-review-chasing-consumer/world.py --out collective/contrib/20261026T2226-c47-review-chasing-consumer/rerun_chih10/seed3 --seeds 3 --spf 1000 --dt 0.1 --frames 30 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0462, 2.0722], min area 6 px

## Measurements
- components: final 24, mean 27.2, max 79; occupancy final 0.11
- tracks: 368; persistent (alive >= 50% of run): 1; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.10 (1 = constant size)
- enclosures: components with a hole mean 1.03, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 30, 21], H1 [2, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 127, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 44, merge/split ratio 0.346, nucleations 85
- channel total drift (end/start - 1): [-0.2249, -0.0183, None, -0.4293]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 114 at frame 17: holes 0, rim-vs-core 0.68, rim-vs-outside 0.73, heterogeneity 0.17; core [0.786, 0.997, 0.93, 0.313] rim [0.29, 0.836, 0.505, 0.393]
  - track 248 at frame 24: holes 0, rim-vs-core 0.28, rim-vs-outside 0.92, heterogeneity 0.18; core [0.621, 0.997, 0.872, 0.343] rim [0.477, 0.889, 0.656, 0.383]
  - track 255 at frame 24: holes 0, rim-vs-core 0.67, rim-vs-outside 0.72, heterogeneity 0.19; core [0.884, 0.993, 0.968, 0.238] rim [0.477, 0.66, 0.556, 0.329]
  - track 247 at frame 23: holes 0, rim-vs-core 0.74, rim-vs-outside 0.54, heterogeneity 0.23; core [0.814, 0.729, 0.69, 0.049] rim [0.849, 0.176, 0.205, 0.081]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 134 components >= 12 px at frames [5, 10, 15, 20, 25, 30]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 8.11 (aggregate of 134 individuals; 4/134 membrane-like individually; rim level 0.688)
  - radial consumer q: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 15.4 (aggregate of 134 individuals; 46/134 membrane-like individually; rim level 0.508)
  - radial product r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 16.9 (aggregate of 134 individuals; 41/134 membrane-like individually; rim level 0.453)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.65, rim/outside 0.726 (aggregate of 134 individuals; 0/134 membrane-like individually; rim level 0.29)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #114 (t=1700, R_eq 3.83): none; #248 (t=2400, R_eq 4.55): none; #255 (t=2400, R_eq 4.07): none; #247 (t=2300, R_eq 6.31): none
- species `prey` (channels ['prey a'], own threshold): components final 21, mean 21.3, max 47; tracks 171, persistent 7; splits 48, persistent splits 2 (K=5), max generation 1, merges 13, merge/split 0.271; moving tracks 1
- species `consumer` (channels ['consumer q'], own threshold): components final 35, mean 36.5, max 86; tracks 475, persistent 1; splits 87, persistent splits 0 (K=5), max generation 0, merges 43, merge/split 0.494; moving tracks 21

## Warnings
- --dt 0.1 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 10 of 134 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
