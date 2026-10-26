# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 159s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T2138-c47-review-foodchain-seeds/rerun/seed5 --seeds 5 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0403, 1.3566], min area 6 px

## Measurements
- components: final 32, mean 35.8, max 60; occupancy final 0.19
- tracks: 467; persistent (alive >= 50% of run): 0; longest 35 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.02, final 1; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 33, 25], H1 [3, 1, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00352/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 133, persistent splits 66 (0 more failed only because the siblings re-merged within K), max generation 4, merges 51, merge/split ratio 0.383, nucleations 87
- channel total drift (end/start - 1): [-0.5855, 3.7238, -0.2943, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 19: holes 0, rim-vs-core 0.24, rim-vs-outside 0.36, heterogeneity 0.28; core [0.507, 0.486, 0.192, 0.553] rim [0.353, 0.352, 0.286, 0.466]
  - track 56 at frame 16: holes 0, rim-vs-core 0.22, rim-vs-outside 0.25, heterogeneity 0.08; core [0.004, 0.82, 0.631, 0.219] rim [0.012, 0.597, 0.609, 0.237]
  - track 86 at frame 17: holes 0, rim-vs-core 0.37, rim-vs-outside 0.31, heterogeneity 0.07; core [0.92, 0.0, 0.053, 0.672] rim [0.566, 0.0, 0.126, 0.608]
  - track 277 at frame 64: holes 0, rim-vs-core 0.25, rim-vs-outside 0.27, heterogeneity 0.04; core [0.005, 0.862, 0.679, 0.191] rim [0.017, 0.609, 0.674, 0.192]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 190 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 2.14 (aggregate of 190 individuals; 16/190 membrane-like individually; rim level 0.16)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 5.58 (aggregate of 190 individuals; 20/190 membrane-like individually; rim level 0.574)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.975 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.591)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 1.25 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.279)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #90 (t=1900, R_eq 8.41): none; #56 (t=1600, R_eq 5.53): none; #86 (t=1700, R_eq 4.89): none; #277 (t=6400, R_eq 3.48): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 10.4, max 54; tracks 312, persistent 0; splits 74, persistent splits 3 (K=5), max generation 1, merges 14, merge/split 0.189; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 29, mean 28.9, max 41; tracks 360, persistent 0; splits 84, persistent splits 36 (K=5), max generation 3, merges 38, merge/split 0.452; moving tracks 14

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 190 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
