# Evidence pack: driven-condensate-prey-predator (seed 9)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 238s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c49rev4/fed128 --seeds 9 --frames 70 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1377, 1.2401], min area 6 px

## Measurements
- components: final 27, mean 22.3, max 39; occupancy final 0.07
- tracks: 42; persistent (alive >= 50% of run): 18; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 28, 24], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 42
- channel total drift (end/start - 1): [-0.1852, None, -0.438, -0.6108]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 37: holes 0, rim-vs-core 0.29, rim-vs-outside 0.24, heterogeneity 0.05; core [0.006, 0.808, 0.485, 0.003] rim [0.02, 0.516, 0.478, 0.013]
  - track 1 at frame 37: holes 0, rim-vs-core 0.32, rim-vs-outside 0.28, heterogeneity 0.05; core [0.003, 0.896, 0.508, 0.003] rim [0.017, 0.574, 0.503, 0.014]
  - track 7 at frame 38: holes 0, rim-vs-core 0.32, rim-vs-outside 0.24, heterogeneity 0.05; core [0.009, 0.839, 0.449, 0.004] rim [0.024, 0.524, 0.444, 0.014]
  - track 8 at frame 38: holes 0, rim-vs-core 0.24, rim-vs-outside 0.19, heterogeneity 0.04; core [0.005, 0.754, 0.491, 0.002] rim [0.02, 0.516, 0.484, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 2.89 (aggregate of 140 individuals; 11/140 membrane-like individually; rim level 0.269)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 13.8 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.549)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.954 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.391)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 3.33 (aggregate of 140 individuals; 12/140 membrane-like individually; rim level 0.28)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3700, R_eq 3.78): none; #1 (t=3700, R_eq 3.43): none; #7 (t=3800, R_eq 3.34): none; #8 (t=3800, R_eq 3.66): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 9.6, max 19; tracks 61, persistent 0; splits 7, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 23, mean 15.5, max 32; tracks 41, persistent 15; splits 0, persistent splits 0 (K=5), max generation 0, merges 1, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
