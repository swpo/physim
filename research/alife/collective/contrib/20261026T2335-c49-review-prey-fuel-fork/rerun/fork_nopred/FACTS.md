# Evidence pack: driven-condensate-prey-predator (seed 7)

- world: `../../../20261026T1851-c46-driven-prey-fuel-fork/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 166s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1851-c46-driven-prey-fuel-fork/world.py --out collective/contrib/20261026T2335-c49-review-prey-fuel-fork/rerun/fork_nopred --seeds 7 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.125, 0.8714], min area 6 px

## Measurements
- components: final 0, mean 11.6, max 15; occupancy final 0.00
- tracks: 15; persistent (alive >= 50% of run): 15; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 1, 1], H1 [2, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 15
- channel total drift (end/start - 1): [0.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 32: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.06; core [0.918, 0.0, 0.195, 0.827] rim [0.71, 0.0, 0.273, 0.713]
  - track 1 at frame 33: holes 0, rim-vs-core 0.24, rim-vs-outside 0.50, heterogeneity 0.06; core [0.917, 0.0, 0.195, 0.826] rim [0.72, 0.0, 0.272, 0.722]
  - track 2 at frame 33: holes 0, rim-vs-core 0.29, rim-vs-outside 0.55, heterogeneity 0.07; core [0.961, 0.0, 0.208, 0.913] rim [0.736, 0.0, 0.275, 0.748]
  - track 3 at frame 33: holes 0, rim-vs-core 0.29, rim-vs-outside 0.53, heterogeneity 0.07; core [0.954, 0.0, 0.204, 0.894] rim [0.721, 0.0, 0.276, 0.731]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [12, 23, 35, 47, 58]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 20.8 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.875)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 71 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.94, rim/outside 0.793 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.382)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 7.84 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.87)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3200, R_eq 7.61): none; #1 (t=3300, R_eq 7.59): none; #2 (t=3300, R_eq 6.58): none; #3 (t=3300, R_eq 6.68): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 12.3, max 15; tracks 15, persistent 15; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
