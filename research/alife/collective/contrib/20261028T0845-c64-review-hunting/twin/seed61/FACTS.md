# Evidence pack: driven-condensate-prey-predator (seed 61)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1475s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261028T0845-c64-review-hunting/twin/seed61 --seeds 61 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1173, 0.8757], min area 6 px

## Measurements
- components: final 78, mean 55.7, max 78; occupancy final 0.15
- tracks: 103; persistent (alive >= 50% of run): 53; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 35.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [89, 81, 78], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 25, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 53
- channel total drift (end/start - 1): [0.0, None, -0.5493, -0.515]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 62: holes 0, rim-vs-core 0.30, rim-vs-outside 0.53, heterogeneity 0.08; core [0.937, 0.0, 0.029, 0.877] rim [0.713, 0.0, 0.107, 0.698]
  - track 12 at frame 63: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.08; core [0.92, 0.0, 0.024, 0.846] rim [0.706, 0.0, 0.091, 0.668]
  - track 16 at frame 63: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.07; core [0.92, 0.0, 0.017, 0.82] rim [0.712, 0.0, 0.101, 0.683]
  - track 53 at frame 98: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.08; core [0.931, 0.0, 0.064, 0.94] rim [0.653, 0.0, 0.146, 0.675]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 364 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 15.9 (aggregate of 364 individuals; 0/364 membrane-like individually; rim level 0.799)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 364 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.33, rim/outside 0.661 (aggregate of 364 individuals; 0/364 membrane-like individually; rim level 0.232)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 16.3 (aggregate of 364 individuals; 0/364 membrane-like individually; rim level 0.77)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=6200, R_eq 6.58): none; #12 (t=6300, R_eq 8.85): none; #16 (t=6300, R_eq 7.25): none; #53 (t=9800, R_eq 5.61): none
- species `prey` (channels ['prey a'], own threshold): components final 78, mean 56.2, max 78; tracks 103, persistent 53; splits 25, persistent splits 25 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
