# Evidence pack: driven-condensate-prey-predator (seed 7)

- world: `../../../20261026T1851-c46-driven-prey-fuel-fork/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 226s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1851-c46-driven-prey-fuel-fork/world.py --out collective/contrib/20261026T2335-c49-review-prey-fuel-fork/rerun/fork --seeds 7 --frames 70 --no-movie`
- segmentation: matter > 0.44 of robust range [0.0718, 1.0556], min area 6 px

## Measurements
- components: final 22, mean 26.0, max 42; occupancy final 0.08
- tracks: 55; persistent (alive >= 50% of run): 25; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 24, 22], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00274/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 31
- channel total drift (end/start - 1): [-0.3475, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 38: holes 0, rim-vs-core 0.22, rim-vs-outside 0.30, heterogeneity 0.04; core [0.002, 0.865, 0.704, 0.004] rim [0.009, 0.64, 0.698, 0.006]
  - track 8 at frame 41: holes 0, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.03; core [0.001, 0.909, 0.728, 0.003] rim [0.007, 0.691, 0.724, 0.006]
  - track 10 at frame 41: holes 0, rim-vs-core 0.25, rim-vs-outside 0.33, heterogeneity 0.04; core [0.001, 0.951, 0.656, 0.004] rim [0.009, 0.696, 0.652, 0.006]
  - track 26 at frame 50: holes 0, rim-vs-core 0.24, rim-vs-outside 0.32, heterogeneity 0.04; core [0.003, 0.954, 0.652, 0.005] rim [0.01, 0.719, 0.65, 0.006]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 3.45 (aggregate of 165 individuals; 4/165 membrane-like individually; rim level 0.381)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 12.4 (aggregate of 165 individuals; 1/165 membrane-like individually; rim level 0.495)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.931 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.475)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 5.57 (aggregate of 165 individuals; 4/165 membrane-like individually; rim level 0.362)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=3800, R_eq 3.66): none; #8 (t=4100, R_eq 3.39): none; #10 (t=4100, R_eq 3.14): none; #26 (t=5000, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 2, mean 14.6, max 30; tracks 55, persistent 8; splits 3, persistent splits 0 (K=20), max generation 0, merges 5, merge/split 1.67; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 14.6, max 24; tracks 31, persistent 16; splits 7, persistent splits 6 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
