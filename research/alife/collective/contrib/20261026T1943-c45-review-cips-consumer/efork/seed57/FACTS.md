# Evidence pack: cips-consumer (seed 57)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 41 frames x 400 steps x dt 0.25 = time 4000; grid [128, 128]; wall 80s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/cc/efork/seed57 --seeds 57 --frames 40 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0396, 1.9827], min area 6 px

## Measurements
- components: final 0, mean 32.7, max 85; occupancy final 0.00
- tracks: 365; persistent (alive >= 50% of run): 1; longest 25 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.71 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 0.0257/time; max body lengths 3.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 141, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.071, nucleations 61
- channel total drift (end/start - 1): [-1.0, -0.0292, None, 0.0489]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 14: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.27; core [0.744, 0.584, 0.605, 0.136] rim [0.546, 0.34, 0.256, 0.19]
  - track 194 at frame 20: holes 0, rim-vs-core 0.14, rim-vs-outside 0.27, heterogeneity 0.03; core [0.875, 0.041, 0.005, 0.025] rim [0.755, 0.037, 0.003, 0.091]
  - track 218 at frame 23: holes 0, rim-vs-core 0.44, rim-vs-outside 0.40, heterogeneity 0.28; core [0.738, 0.593, 0.612, 0.117] rim [0.584, 0.374, 0.266, 0.159]
  - track 220 at frame 19: holes 0, rim-vs-core 0.15, rim-vs-outside 0.49, heterogeneity 0.20; core [0.862, 0.159, 0.169, 0.024] rim [0.745, 0.181, 0.124, 0.106]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 169 components >= 12 px at frames [7, 13, 20, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 8.52 (aggregate of 169 individuals; 15/169 membrane-like individually; rim level 0.693)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 9.79 (aggregate of 169 individuals; 15/169 membrane-like individually; rim level 0.363)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 13.2 (aggregate of 169 individuals; 10/169 membrane-like individually; rim level 0.312)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.46, rim/outside 0.776 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.22)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=1400, R_eq 5.26): none; #194 (t=2000, R_eq 5.97): none; #218 (t=2300, R_eq 4.92): none; #220 (t=1900, R_eq 6.96): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 30.4, max 65; tracks 363, persistent 1; splits 124, persistent splits 12 (K=5), max generation 3, merges 18, merge/split 0.145; moving tracks 18
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 27.8, max 81; tracks 289, persistent 1; splits 71, persistent splits 7 (K=5), max generation 2, merges 11, merge/split 0.155; moving tracks 83

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 169 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
