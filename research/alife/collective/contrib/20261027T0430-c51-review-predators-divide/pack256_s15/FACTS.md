# Evidence pack: driven-condensate-prey-predator (seed 15)

- world: `../../20261026T2024-c46-hunting-predators-divide-256/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1560s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2024-c46-hunting-predators-divide-256/world.py --out collective/contrib/20261027T0430-c51-review-predators-divide/pack256_s15 --seeds 15 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1438, 1.1976], min area 6 px

## Measurements
- components: final 74, mean 77.5, max 133; occupancy final 0.06
- tracks: 301; persistent (alive >= 50% of run): 31; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.19 (1 = constant size)
- enclosures: components with a hole mean 0.43, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [87, 74, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 47, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 205
- channel total drift (end/start - 1): [-0.1147, None, -0.4843, -0.579]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 67: holes 1, rim-vs-core 0.22, rim-vs-outside 0.58, heterogeneity 0.07; core [0.934, 0.0, 0.0, 0.771] rim [0.763, 0.0, 0.032, 0.638]
  - track 9 at frame 46: holes 0, rim-vs-core 0.31, rim-vs-outside 0.29, heterogeneity 0.05; core [0.018, 0.91, 0.498, 0.015] rim [0.03, 0.597, 0.495, 0.024]
  - track 18 at frame 46: holes 0, rim-vs-core 0.34, rim-vs-outside 0.29, heterogeneity 0.05; core [0.014, 0.913, 0.514, 0.015] rim [0.029, 0.569, 0.511, 0.026]
  - track 170 at frame 97: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.05; core [0.031, 0.812, 0.465, 0.024] rim [0.042, 0.5, 0.463, 0.032]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 447 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 3.94 (aggregate of 447 individuals; 18/447 membrane-like individually; rim level 0.35)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 9.46 (aggregate of 447 individuals; 4/447 membrane-like individually; rim level 0.474)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.927 (aggregate of 447 individuals; 0/447 membrane-like individually; rim level 0.398)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 4.45 (aggregate of 447 individuals; 19/447 membrane-like individually; rim level 0.346)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #58 (t=6700, R_eq 11.03, ring): ['prey a', 'product p']; #9 (t=4600, R_eq 2.71): none; #18 (t=4600, R_eq 2.99): none; #170 (t=9700, R_eq 2.59): none
- species `prey` (channels ['prey a'], own threshold): components final 26, mean 33.0, max 64; tracks 347, persistent 4; splits 63, persistent splits 2 (K=5), max generation 1, merges 1, merge/split 0.016; moving tracks 31
- species `predator` (channels ['predator b'], own threshold): components final 57, mean 53.9, max 87; tracks 291, persistent 5; splits 40, persistent splits 14 (K=5), max generation 2, merges 7, merge/split 0.175; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 447 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
