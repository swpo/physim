# Evidence pack: driven-condensate-prey-predator (seed 13)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0217-c51-review-hunting/fed128 --seeds 13 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1378, 1.1928], min area 6 px

## Measurements
- components: final 18, mean 18.0, max 30; occupancy final 0.08
- tracks: 39; persistent (alive >= 50% of run): 16; longest 69 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 18, 14], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 3, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 33
- channel total drift (end/start - 1): [-0.1374, None, -0.4648, -0.5926]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 40: holes 0, rim-vs-core 0.36, rim-vs-outside 0.27, heterogeneity 0.05; core [0.004, 0.894, 0.539, 0.004] rim [0.017, 0.537, 0.535, 0.015]
  - track 8 at frame 38: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.05; core [0.001, 0.875, 0.526, 0.0] rim [0.012, 0.563, 0.52, 0.009]
  - track 6 at frame 36: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.05; core [0.002, 0.898, 0.537, 0.002] rim [0.015, 0.549, 0.531, 0.012]
  - track 16 at frame 42: holes 0, rim-vs-core 0.21, rim-vs-outside 0.23, heterogeneity 0.03; core [0.026, 0.782, 0.47, 0.018] rim [0.033, 0.569, 0.467, 0.023]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 3.89 (aggregate of 110 individuals; 4/110 membrane-like individually; rim level 0.359)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 11.8 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.458)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.924 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.385)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 4.4 (aggregate of 110 individuals; 4/110 membrane-like individually; rim level 0.359)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=4000, R_eq 3.29): none; #8 (t=3800, R_eq 3.83): none; #6 (t=3600, R_eq 3.57): none; #16 (t=4200, R_eq 2.39): none
- species `prey` (channels ['prey a'], own threshold): components final 5, mean 9.7, max 16; tracks 63, persistent 1; splits 14, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 14, mean 10.7, max 17; tracks 35, persistent 6; splits 3, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
