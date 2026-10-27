# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 441s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c53-rev-hd/base --seeds 4 6 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1427, 1.2218], min area 6 px

## Measurements
- components: final 28, mean 21.6, max 34; occupancy final 0.07
- tracks: 84; persistent (alive >= 50% of run): 4; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.17 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 18], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 9, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 65
- channel total drift (end/start - 1): [-0.1756, None, -0.4581, -0.6067]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 41: holes 0, rim-vs-core 0.33, rim-vs-outside 0.24, heterogeneity 0.05; core [0.016, 0.852, 0.475, 0.013] rim [0.03, 0.52, 0.471, 0.023]
  - track 0 at frame 32: holes 0, rim-vs-core 0.31, rim-vs-outside 0.22, heterogeneity 0.05; core [0.001, 0.825, 0.545, 0.001] rim [0.012, 0.519, 0.538, 0.01]
  - track 36 at frame 77: holes 0, rim-vs-core 0.33, rim-vs-outside 0.27, heterogeneity 0.05; core [0.007, 0.888, 0.492, 0.005] rim [0.02, 0.558, 0.488, 0.014]
  - track 43 at frame 86: holes 0, rim-vs-core 0.27, rim-vs-outside 0.30, heterogeneity 0.04; core [0.027, 0.875, 0.481, 0.024] rim [0.035, 0.605, 0.479, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 3.45 (aggregate of 128 individuals; 5/128 membrane-like individually; rim level 0.32)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 10.2 (aggregate of 128 individuals; 1/128 membrane-like individually; rim level 0.479)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.939 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.378)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 3.97 (aggregate of 128 individuals; 6/128 membrane-like individually; rim level 0.328)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=4100, R_eq 2.99): none; #0 (t=3200, R_eq 4.44): none; #36 (t=7700, R_eq 3.04): none; #43 (t=8600, R_eq 2.26): none
- species `prey` (channels ['prey a'], own threshold): components final 6, mean 8.3, max 19; tracks 101, persistent 0; splits 17, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 15.6, max 25; tracks 82, persistent 0; splits 9, persistent splits 3 (K=5), max generation 1, merges 1, merge/split 0.111; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
