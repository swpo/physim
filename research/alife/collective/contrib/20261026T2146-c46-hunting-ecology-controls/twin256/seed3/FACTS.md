# Evidence pack: driven-condensate-prey-predator (seed 3)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1215s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/np256_s3 --seeds 3 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1165, 0.8813], min area 6 px

## Measurements
- components: final 92, mean 63.7, max 92; occupancy final 0.15
- tracks: 124; persistent (alive >= 50% of run): 60; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [103, 95, 92], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 32, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 60
- channel total drift (end/start - 1): [0.0, None, -0.5594, -0.5127]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.20, rim-vs-outside 0.49, heterogeneity 0.07; core [0.857, 0.0, 0.011, 0.721] rim [0.694, 0.0, 0.096, 0.654]
  - track 3 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.08; core [0.924, 0.0, 0.022, 0.847] rim [0.708, 0.0, 0.095, 0.675]
  - track 12 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.08; core [0.928, 0.0, 0.029, 0.87] rim [0.714, 0.0, 0.102, 0.695]
  - track 60 at frame 94: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.09; core [0.92, 0.0, 0.06, 0.916] rim [0.639, 0.0, 0.137, 0.644]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 417 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 16.6 (aggregate of 417 individuals; 0/417 membrane-like individually; rim level 0.802)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 417 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.95, rim/outside 0.664 (aggregate of 417 individuals; 0/417 membrane-like individually; rim level 0.228)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 16.7 (aggregate of 417 individuals; 0/417 membrane-like individually; rim level 0.774)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 8.79): none; #3 (t=6200, R_eq 7.2): none; #12 (t=6200, R_eq 7.09): none; #60 (t=9400, R_eq 5.44): none
- species `prey` (channels ['prey a'], own threshold): components final 92, mean 64.4, max 92; tracks 126, persistent 60; splits 32, persistent splits 31 (K=5), max generation 1, merges 1, merge/split 0.031; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
