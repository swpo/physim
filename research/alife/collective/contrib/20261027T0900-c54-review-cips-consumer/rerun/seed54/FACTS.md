# Evidence pack: cips-consumer (seed 54)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 251s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0900-c54-review-cips-consumer/rerun/seed54 --seeds 54 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0381, 2.0009], min area 6 px

## Measurements
- components: final 34, mean 39.6, max 78; occupancy final 0.19
- tracks: 951; persistent (alive >= 50% of run): 0; longest 35 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.17, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 35, 32], H1 [0, 0, 0]
- motion: 143 long-lived tracks moved >= 1 body length; max speed 0.0204/time; max body lengths 4.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 424, persistent splits 93 (0 more failed only because the siblings re-merged within K), max generation 10, merges 16, merge/split ratio 0.038, nucleations 72
- channel total drift (end/start - 1): [0.0441, 0.0009, None, -0.591]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 140 at frame 26: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.28; core [0.719, 0.499, 0.451, 0.123] rim [0.487, 0.413, 0.206, 0.184]
  - track 427 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.35, heterogeneity 0.28; core [0.805, 0.458, 0.485, 0.111] rim [0.52, 0.393, 0.23, 0.186]
  - track 435 at frame 57: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.29; core [0.779, 0.554, 0.592, 0.128] rim [0.543, 0.392, 0.256, 0.193]
  - track 863 at frame 115: holes 0, rim-vs-core 0.06, rim-vs-outside 0.54, heterogeneity 0.03; core [0.87, 0.04, 0.005, 0.01] rim [0.845, 0.039, 0.004, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 10.4 (aggregate of 231 individuals; 14/231 membrane-like individually; rim level 0.664)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 9.33 (aggregate of 231 individuals; 27/231 membrane-like individually; rim level 0.369)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.675, rim/outside 12.9 (aggregate of 231 individuals; 17/231 membrane-like individually; rim level 0.297)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.54, rim/outside 0.765 (aggregate of 231 individuals; 0/231 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #140 (t=2600, R_eq 5.94): none; #427 (t=6100, R_eq 5.53): none; #435 (t=5700, R_eq 5.11): none; #863 (t=11500, R_eq 6.58): none
- species `prey` (channels ['prey a'], own threshold): components final 31, mean 37.5, max 63; tracks 984, persistent 0; splits 437, persistent splits 68 (K=5), max generation 9, merges 26, merge/split 0.059; moving tracks 118
- species `consumer` (channels ['consumer q'], own threshold): components final 28, mean 31.8, max 76; tracks 774, persistent 0; splits 245, persistent splits 28 (K=5), max generation 3, merges 13, merge/split 0.053; moving tracks 313

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
