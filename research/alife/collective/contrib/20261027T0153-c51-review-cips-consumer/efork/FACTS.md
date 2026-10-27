# Evidence pack: cips-consumer (seed 7)

- world: `../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 135s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0153-c51-review-cips-consumer/efork --seeds 7 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0449, 1.9311], min area 6 px

## Measurements
- components: final 0, mean 16.2, max 82; occupancy final 0.00
- tracks: 317; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.0215/time; max body lengths 3.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 114, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.07, nucleations 68
- channel total drift (end/start - 1): [-1.0, 0.0191, None, 0.0387]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 125 at frame 16: holes 0, rim-vs-core 0.39, rim-vs-outside 0.38, heterogeneity 0.28; core [0.74, 0.535, 0.563, 0.125] rim [0.508, 0.375, 0.3, 0.186]
  - track 109 at frame 13: holes 0, rim-vs-core 0.35, rim-vs-outside 0.48, heterogeneity 0.29; core [0.703, 0.581, 0.621, 0.127] rim [0.586, 0.41, 0.345, 0.153]
  - track 53 at frame 11: holes 0, rim-vs-core 0.35, rim-vs-outside 0.58, heterogeneity 0.29; core [0.828, 0.442, 0.556, 0.079] rim [0.576, 0.433, 0.329, 0.145]
  - track 272 at frame 28: holes 0, rim-vs-core 0.57, rim-vs-outside 0.39, heterogeneity 0.27; core [0.729, 0.661, 0.733, 0.144] rim [0.486, 0.385, 0.296, 0.194]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 8.05 (aggregate of 80 individuals; 2/80 membrane-like individually; rim level 0.7)
  - radial consumer q: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 9.72 (aggregate of 80 individuals; 11/80 membrane-like individually; rim level 0.336)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.69, rim/outside 12.7 (aggregate of 80 individuals; 9/80 membrane-like individually; rim level 0.341)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.67, rim/outside 0.763 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.208)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #125 (t=1600, R_eq 5.89): none; #109 (t=1300, R_eq 5.5): none; #53 (t=1100, R_eq 6.21): none; #272 (t=2800, R_eq 4.44): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 15.2, max 70; tracks 325, persistent 0; splits 108, persistent splits 15 (K=5), max generation 2, merges 15, merge/split 0.139; moving tracks 20
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 12.8, max 66; tracks 250, persistent 0; splits 60, persistent splits 5 (K=5), max generation 1, merges 3, merge/split 0.05; moving tracks 75

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
