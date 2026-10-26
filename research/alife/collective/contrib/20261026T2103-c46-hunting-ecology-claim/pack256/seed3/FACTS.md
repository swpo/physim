# Evidence pack: driven-condensate-prey-predator (seed 3)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1572s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/c256_s3 --seeds 3 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1445, 1.1736], min area 6 px

## Measurements
- components: final 49, mean 64.5, max 120; occupancy final 0.07
- tracks: 246; persistent (alive >= 50% of run): 20; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 69.25 (1 = constant size)
- enclosures: components with a hole mean 1.06, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [66, 52, 36], H1 [2, 2, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 38, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 169
- channel total drift (end/start - 1): [-0.0467, None, -0.5134, -0.5528]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 73: holes 1, rim-vs-core 0.18, rim-vs-outside 0.58, heterogeneity 0.07; core [0.909, 0.0, 0.001, 0.739] rim [0.764, 0.0, 0.041, 0.64]
  - track 62 at frame 75: holes 1, rim-vs-core 0.19, rim-vs-outside 0.60, heterogeneity 0.07; core [0.916, 0.0, 0.002, 0.755] rim [0.767, 0.0, 0.04, 0.646]
  - track 72 at frame 80: holes 0, rim-vs-core 0.15, rim-vs-outside 0.59, heterogeneity 0.07; core [0.9, 0.0, 0.001, 0.701] rim [0.764, 0.0, 0.05, 0.657]
  - track 178 at frame 94: holes 0, rim-vs-core 0.17, rim-vs-outside 0.19, heterogeneity 0.03; core [0.021, 0.696, 0.552, 0.019] rim [0.027, 0.526, 0.549, 0.024]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 361 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 4.6 (aggregate of 361 individuals; 21/361 membrane-like individually; rim level 0.404)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 8.92 (aggregate of 361 individuals; 4/361 membrane-like individually; rim level 0.427)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.899 (aggregate of 361 individuals; 0/361 membrane-like individually; rim level 0.383)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 5.22 (aggregate of 361 individuals; 23/361 membrane-like individually; rim level 0.396)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=7300, R_eq 10.87, ring): ['prey a', 'product p']; #62 (t=7500, R_eq 11.31, ring): ['prey a', 'product p']; #72 (t=8000, R_eq 10.03): none; #178 (t=9400, R_eq 2.46): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 30.9, max 65; tracks 329, persistent 5; splits 76, persistent splits 2 (K=5), max generation 1, merges 1, merge/split 0.013; moving tracks 15
- species `predator` (channels ['predator b'], own threshold): components final 27, mean 42.1, max 68; tracks 234, persistent 0; splits 36, persistent splits 19 (K=5), max generation 3, merges 6, merge/split 0.167; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 361 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
