# Evidence pack: driven-condensate-prey-predator (seed 81)

- world: `../../claim_world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 438s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0930-c63-review-hunting-ecology/claim_world.py --out collective/contrib/20261028T0930-c63-review-hunting-ecology/rerun/seed81 --seeds 81 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1442, 1.1807], min area 6 px

## Measurements
- components: final 14, mean 16.2, max 32; occupancy final 0.05
- tracks: 67; persistent (alive >= 50% of run): 2; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.33 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 13], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 11, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 45
- channel total drift (end/start - 1): [0.0056, None, -0.5337, -0.5153]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 33: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.05; core [0.001, 0.868, 0.525, 0.001] rim [0.01, 0.554, 0.517, 0.009]
  - track 31 at frame 90: holes 0, rim-vs-core 0.33, rim-vs-outside 0.30, heterogeneity 0.05; core [0.0, 0.938, 0.518, 0.0] rim [0.004, 0.612, 0.511, 0.004]
  - track 1 at frame 33: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.05; core [0.001, 0.9, 0.506, 0.0] rim [0.01, 0.578, 0.5, 0.007]
  - track 35 at frame 83: holes 0, rim-vs-core 0.20, rim-vs-outside 0.24, heterogeneity 0.04; core [0.004, 0.776, 0.527, 0.003] rim [0.01, 0.572, 0.525, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 96 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 4.95 (aggregate of 96 individuals; 3/96 membrane-like individually; rim level 0.436)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 8.35 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.397)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.894 (aggregate of 96 individuals; 0/96 membrane-like individually; rim level 0.334)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 5.89 (aggregate of 96 individuals; 4/96 membrane-like individually; rim level 0.442)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3300, R_eq 4.33): none; #31 (t=9000, R_eq 3.7): none; #1 (t=3300, R_eq 3.91): none; #35 (t=8300, R_eq 3.09): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 7.6, max 17; tracks 78, persistent 0; splits 14, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 7, mean 10.6, max 19; tracks 61, persistent 0; splits 10, persistent splits 5 (K=5), max generation 1, merges 1, merge/split 0.1; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
