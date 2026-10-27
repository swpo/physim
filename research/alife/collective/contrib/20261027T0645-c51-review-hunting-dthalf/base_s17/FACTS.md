# Evidence pack: driven-condensate-prey-predator (seed 17)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 394s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0645-c51-review-hunting-dthalf/base_s17 --seeds 17 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.138, 1.1785], min area 6 px

## Measurements
- components: final 8, mean 15.8, max 33; occupancy final 0.04
- tracks: 60; persistent (alive >= 50% of run): 5; longest 72 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 44.30 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 11, 7], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 12, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.083, nucleations 35
- channel total drift (end/start - 1): [-0.1281, None, -0.4783, -0.5807]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 82: holes 0, rim-vs-core 0.26, rim-vs-outside 0.48, heterogeneity 0.07; core [0.926, 0.002, 0.012, 0.796] rim [0.714, 0.0, 0.092, 0.666]
  - track 15 at frame 68: holes 0, rim-vs-core 0.24, rim-vs-outside 0.51, heterogeneity 0.07; core [0.935, 0.0, 0.01, 0.805] rim [0.738, 0.0, 0.079, 0.679]
  - track 16 at frame 69: holes 0, rim-vs-core 0.27, rim-vs-outside 0.50, heterogeneity 0.07; core [0.955, 0.0, 0.011, 0.833] rim [0.738, 0.0, 0.084, 0.682]
  - track 52 at frame 115: holes 0, rim-vs-core 0.30, rim-vs-outside 0.27, heterogeneity 0.05; core [0.001, 0.924, 0.57, 0.001] rim [0.007, 0.622, 0.565, 0.006]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 5.53 (aggregate of 86 individuals; 7/86 membrane-like individually; rim level 0.445)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 8.08 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.379)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.59, rim/outside 0.876 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.37)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 6.41 (aggregate of 86 individuals; 7/86 membrane-like individually; rim level 0.435)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=8200, R_eq 7.94): none; #15 (t=6800, R_eq 8.27): none; #16 (t=6900, R_eq 6.93): none; #52 (t=11500, R_eq 3.34): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 8.6, max 19; tracks 76, persistent 3; splits 19, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 6
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 9.4, max 16; tracks 55, persistent 0; splits 8, persistent splits 6 (K=5), max generation 2, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
