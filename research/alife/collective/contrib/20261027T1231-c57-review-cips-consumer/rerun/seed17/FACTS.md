# Evidence pack: cips-consumer (seed 17)

- world: `../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 226s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/c57-w2/rerun --seeds 17 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0385, 1.9948], min area 6 px

## Measurements
- components: final 43, mean 39.0, max 87; occupancy final 0.19
- tracks: 873; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 43, 39], H1 [0, 0, 0]
- motion: 122 long-lived tracks moved >= 1 body length; max speed 0.0232/time; max body lengths 4.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 375, persistent splits 83 (0 more failed only because the siblings re-merged within K), max generation 9, merges 22, merge/split ratio 0.059, nucleations 75
- channel total drift (end/start - 1): [-0.0243, 0.0409, None, -0.5816]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 405 at frame 66: holes 0, rim-vs-core 0.37, rim-vs-outside 0.55, heterogeneity 0.28; core [0.794, 0.502, 0.554, 0.094] rim [0.559, 0.448, 0.283, 0.157]
  - track 474 at frame 78: holes 0, rim-vs-core 0.31, rim-vs-outside 0.57, heterogeneity 0.28; core [0.848, 0.382, 0.44, 0.079] rim [0.599, 0.405, 0.278, 0.158]
  - track 396 at frame 62: holes 0, rim-vs-core 0.49, rim-vs-outside 0.38, heterogeneity 0.30; core [0.752, 0.609, 0.626, 0.135] rim [0.51, 0.408, 0.255, 0.211]
  - track 820 at frame 117: holes 0, rim-vs-core 0.54, rim-vs-outside 0.44, heterogeneity 0.26; core [0.794, 0.691, 0.761, 0.177] rim [0.566, 0.422, 0.359, 0.227]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 10.6 (aggregate of 227 individuals; 8/227 membrane-like individually; rim level 0.68)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 8.83 (aggregate of 227 individuals; 21/227 membrane-like individually; rim level 0.333)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.692, rim/outside 13.1 (aggregate of 227 individuals; 15/227 membrane-like individually; rim level 0.279)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.6, rim/outside 0.77 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.236)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #405 (t=6600, R_eq 6.15): none; #474 (t=7800, R_eq 6.6): none; #396 (t=6200, R_eq 5.2): none; #820 (t=11700, R_eq 3.83): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 36.8, max 77; tracks 888, persistent 0; splits 377, persistent splits 76 (K=5), max generation 7, merges 30, merge/split 0.08; moving tracks 95
- species `consumer` (channels ['consumer q'], own threshold): components final 36, mean 28.7, max 62; tracks 695, persistent 0; splits 205, persistent splits 22 (K=5), max generation 2, merges 24, merge/split 0.117; moving tracks 267

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 227 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
