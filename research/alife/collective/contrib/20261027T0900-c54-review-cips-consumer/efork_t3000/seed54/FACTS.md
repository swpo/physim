# Evidence pack: cips-consumer (seed 54)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 51 frames x 400 steps x dt 0.25 = time 5000; grid [128, 128]; wall 110s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0900-c54-review-cips-consumer/efork_t3000/seed54 --seeds 54 --frames 50 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0406, 1.9742], min area 6 px

## Measurements
- components: final 0, mean 25.5, max 78; occupancy final 0.00
- tracks: 304; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.0205/time; max body lengths 3.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 113, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.053, nucleations 61
- channel total drift (end/start - 1): [-1.0, 0.0009, None, 0.0334]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 12: holes 0, rim-vs-core 0.37, rim-vs-outside 0.35, heterogeneity 0.27; core [0.777, 0.487, 0.529, 0.107] rim [0.538, 0.388, 0.267, 0.16]
  - track 69 at frame 13: holes 0, rim-vs-core 0.41, rim-vs-outside 0.36, heterogeneity 0.29; core [0.784, 0.507, 0.564, 0.105] rim [0.544, 0.391, 0.257, 0.168]
  - track 138 at frame 20: holes 0, rim-vs-core 0.39, rim-vs-outside 0.35, heterogeneity 0.28; core [0.795, 0.461, 0.491, 0.091] rim [0.543, 0.351, 0.227, 0.158]
  - track 190 at frame 22: holes 0, rim-vs-core 0.08, rim-vs-outside 0.46, heterogeneity 0.03; core [0.85, 0.034, 0.004, 0.011] rim [0.805, 0.031, 0.003, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [8, 17, 25]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 8.89 (aggregate of 122 individuals; 7/122 membrane-like individually; rim level 0.694)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.721, rim/outside 10.7 (aggregate of 122 individuals; 9/122 membrane-like individually; rim level 0.355)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.651, rim/outside 15.3 (aggregate of 122 individuals; 6/122 membrane-like individually; rim level 0.327)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.54, rim/outside 0.768 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.22)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=1200, R_eq 5.26): none; #69 (t=1300, R_eq 5.35): none; #138 (t=2000, R_eq 5.5): none; #190 (t=2200, R_eq 6.26): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 24.1, max 64; tracks 319, persistent 0; splits 110, persistent splits 13 (K=5), max generation 2, merges 15, merge/split 0.136; moving tracks 27
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 21.9, max 76; tracks 244, persistent 0; splits 59, persistent splits 8 (K=5), max generation 2, merges 2, merge/split 0.034; moving tracks 83

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
