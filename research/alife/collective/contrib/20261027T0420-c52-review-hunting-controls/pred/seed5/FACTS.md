# Evidence pack: driven-condensate-prey-predator (seed 5)

- world: `../../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 417s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0420-c52-review-hunting-controls/pred/seed5 --seeds 5 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1447, 1.2337], min area 6 px

## Measurements
- components: final 30, mean 23.8, max 35; occupancy final 0.06
- tracks: 102; persistent (alive >= 50% of run): 6; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.57 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 24], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 16, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 70
- channel total drift (end/start - 1): [-0.2174, None, -0.4369, -0.6267]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 34: holes 0, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.05; core [0.003, 0.843, 0.536, 0.003] rim [0.015, 0.518, 0.53, 0.013]
  - track 3 at frame 37: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.05; core [0.006, 0.887, 0.495, 0.004] rim [0.021, 0.561, 0.489, 0.016]
  - track 37 at frame 78: holes 0, rim-vs-core 0.35, rim-vs-outside 0.24, heterogeneity 0.05; core [0.025, 0.839, 0.474, 0.021] rim [0.039, 0.487, 0.471, 0.032]
  - track 49 at frame 79: holes 0, rim-vs-core 0.22, rim-vs-outside 0.31, heterogeneity 0.04; core [0.022, 0.838, 0.51, 0.02] rim [0.03, 0.62, 0.504, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 2.87 (aggregate of 138 individuals; 7/138 membrane-like individually; rim level 0.256)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 11.7 (aggregate of 138 individuals; 1/138 membrane-like individually; rim level 0.558)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.953 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.402)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.21 (aggregate of 138 individuals; 7/138 membrane-like individually; rim level 0.255)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3400, R_eq 4.07): none; #3 (t=3700, R_eq 3.24): none; #37 (t=7800, R_eq 2.88): none; #49 (t=7900, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 8.6, max 21; tracks 112, persistent 0; splits 20, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 28, mean 17.5, max 28; tracks 106, persistent 0; splits 16, persistent splits 5 (K=5), max generation 2, merges 3, merge/split 0.188; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 138 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
