# Evidence pack: cips-consumer (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 257s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/efork_t3000/seed1 --seeds 1 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0451, 1.938], min area 6 px

## Measurements
- components: final 0, mean 15.0, max 86; occupancy final 0.00
- tracks: 283; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.019/time; max body lengths 2.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 100, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 0.06, nucleations 63
- channel total drift (end/start - 1): [-1.0, 0.0362, None, 0.0401]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 102 at frame 13: holes 0, rim-vs-core 0.31, rim-vs-outside 0.67, heterogeneity 0.28; core [0.81, 0.544, 0.663, 0.09] rim [0.613, 0.474, 0.435, 0.144]
  - track 46 at frame 10: holes 0, rim-vs-core 0.16, rim-vs-outside 0.28, heterogeneity 0.03; core [0.91, 0.047, 0.008, 0.021] rim [0.758, 0.041, 0.005, 0.081]
  - track 155 at frame 20: holes 0, rim-vs-core 0.11, rim-vs-outside 0.51, heterogeneity 0.04; core [0.935, 0.071, 0.017, 0.013] rim [0.829, 0.065, 0.014, 0.043]
  - track 203 at frame 24: holes 0, rim-vs-core 0.12, rim-vs-outside 0.50, heterogeneity 0.03; core [0.921, 0.05, 0.009, 0.007] rim [0.821, 0.046, 0.007, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 7.14 (aggregate of 71 individuals; 6/71 membrane-like individually; rim level 0.673)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 7.46 (aggregate of 71 individuals; 10/71 membrane-like individually; rim level 0.306)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.692, rim/outside 10.9 (aggregate of 71 individuals; 8/71 membrane-like individually; rim level 0.284)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.65, rim/outside 0.749 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.207)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #102 (t=1300, R_eq 6.1): none; #46 (t=1000, R_eq 5.67): none; #155 (t=2000, R_eq 6.28): none; #203 (t=2400, R_eq 6.08): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 14.1, max 64; tracks 296, persistent 0; splits 96, persistent splits 9 (K=5), max generation 2, merges 14, merge/split 0.146; moving tracks 21
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 11.7, max 67; tracks 225, persistent 0; splits 47, persistent splits 5 (K=5), max generation 2, merges 5, merge/split 0.106; moving tracks 71

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 71 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
