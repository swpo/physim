# Evidence pack: condensate-food-chain (seed 21)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 81 frames x 200 steps x dt 0.5 = time 8000; grid [128, 128]; wall 116s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1555-c41-review-foodchain/efork_cut --seeds 21 --size 128 128 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0004, 1.2914], min area 6 px

## Measurements
- components: final 0, mean 29.5, max 67; occupancy final 0.00
- tracks: 327; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.30, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 1], H1 [2, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00501/time; max body lengths 1.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 80, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 2, merges 40, merge/split ratio 0.5, nucleations 37
- channel total drift (end/start - 1): [-1.0, -0.9892, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 20: holes 0, rim-vs-core 0.20, rim-vs-outside 0.42, heterogeneity 0.04; core [0.009, 0.85, 0.764, 0.443] rim [0.019, 0.649, 0.758, 0.444]
  - track 143 at frame 20: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.08; core [0.857, 0.056, 0.202, 0.902] rim [0.625, 0.04, 0.29, 0.831]
  - track 98 at frame 19: holes 0, rim-vs-core 0.29, rim-vs-outside 0.24, heterogeneity 0.05; core [0.01, 0.842, 0.715, 0.479] rim [0.023, 0.551, 0.71, 0.479]
  - track 240 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.26, heterogeneity 0.05; core [0.014, 0.863, 0.796, 0.451] rim [0.029, 0.559, 0.794, 0.451]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 136 components >= 12 px at frames [13, 27, 40, 53]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 2.87 (aggregate of 136 individuals; 10/136 membrane-like individually; rim level 0.237)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.86 (aggregate of 136 individuals; 16/136 membrane-like individually; rim level 0.529)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.976 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.614)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 1.08 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.609)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #95 (t=2000, R_eq 6.6): none; #143 (t=2000, R_eq 7.4): none; #98 (t=1900, R_eq 5.53): none; #240 (t=4300, R_eq 3.61): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 10.5, max 55; tracks 208, persistent 0; splits 37, persistent splits 3 (K=5), max generation 1, merges 16, merge/split 0.432; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 22.4, max 36; tracks 219, persistent 0; splits 50, persistent splits 14 (K=5), max generation 2, merges 20, merge/split 0.4; moving tracks 12

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 136 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
