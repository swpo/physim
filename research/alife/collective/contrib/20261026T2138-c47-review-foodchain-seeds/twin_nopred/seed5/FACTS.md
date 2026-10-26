# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 109s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T2138-c47-review-foodchain-seeds/twin_nopred/seed5 --seeds 5 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0254, 1.1627], min area 6 px

## Measurements
- components: final 77, mean 75.6, max 77; occupancy final 0.30
- tracks: 162; persistent (alive >= 50% of run): 77; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 6.30 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 77, 77], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 34, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 1, merges 13, merge/split ratio 0.382, nucleations 4
- channel total drift (end/start - 1): [0.1834, None, -0.7069, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.08; core [0.9, 0.0, 0.035, 0.895] rim [0.546, 0.0, 0.092, 0.729]
  - track 25 at frame 61: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.09; core [0.88, 0.0, 0.039, 0.883] rim [0.486, 0.0, 0.098, 0.712]
  - track 32 at frame 61: holes 0, rim-vs-core 0.46, rim-vs-outside 0.29, heterogeneity 0.09; core [0.873, 0.0, 0.04, 0.877] rim [0.45, 0.0, 0.101, 0.702]
  - track 138 at frame 63: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.09; core [0.893, 0.0, 0.034, 0.9] rim [0.513, 0.0, 0.097, 0.714]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 461 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 21.9 (aggregate of 461 individuals; 0/461 membrane-like individually; rim level 0.848)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 461 individuals)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.95, rim/outside 0.87 (aggregate of 461 individuals; 0/461 membrane-like individually; rim level 0.144)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 1.71 (aggregate of 461 individuals; 0/461 membrane-like individually; rim level 0.836)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=6100, R_eq 4.65): none; #25 (t=6100, R_eq 4.79): none; #32 (t=6100, R_eq 4.82): none; #138 (t=6300, R_eq 4.95): none
- species `prey` (channels ['prey a'], own threshold): components final 77, mean 75.6, max 77; tracks 162, persistent 77; splits 34, persistent splits 12 (K=5), max generation 1, merges 13, merge/split 0.382; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
