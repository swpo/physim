# Evidence pack: driven-condensate-prey-predator (seed 7)

- world: `../../../20261026T1851-c46-driven-prey-fuel-fork/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 224s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1851-c46-driven-prey-fuel-fork/world.py --out collective/contrib/20261026T2335-c49-review-prey-fuel-fork/rerun/fed --seeds 7 --frames 70 --no-movie`
- segmentation: matter > 0.46 of robust range [0.0713, 1.0123], min area 6 px

## Measurements
- components: final 38, mean 27.8, max 42; occupancy final 0.17
- tracks: 55; persistent (alive >= 50% of run): 35; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 38, 38], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00232/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 31
- channel total drift (end/start - 1): [-0.1033, None, -0.492, -0.559]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 38: holes 0, rim-vs-core 0.23, rim-vs-outside 0.31, heterogeneity 0.04; core [0.001, 0.897, 0.635, 0.0] rim [0.008, 0.666, 0.628, 0.002]
  - track 8 at frame 41: holes 0, rim-vs-core 0.22, rim-vs-outside 0.29, heterogeneity 0.04; core [0.0, 0.943, 0.666, 0.0] rim [0.005, 0.718, 0.66, 0.001]
  - track 9 at frame 41: holes 0, rim-vs-core 0.10, rim-vs-outside 0.45, heterogeneity 0.06; core [0.858, 0.0, 0.008, 0.628] rim [0.77, 0.0, 0.052, 0.592]
  - track 26 at frame 50: holes 0, rim-vs-core 0.23, rim-vs-outside 0.34, heterogeneity 0.04; core [0.001, 0.978, 0.572, 0.0] rim [0.008, 0.748, 0.57, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 179 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.776, rim/outside 4.2 (aggregate of 179 individuals; 4/179 membrane-like individually; rim level 0.445)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 9.4 (aggregate of 179 individuals; 1/179 membrane-like individually; rim level 0.427)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.61, rim/outside 0.895 (aggregate of 179 individuals; 0/179 membrane-like individually; rim level 0.438)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 6.4 (aggregate of 179 individuals; 4/179 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=3800, R_eq 3.66): none; #8 (t=4100, R_eq 3.39): none; #9 (t=4100, R_eq 9.39): none; #26 (t=5000, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 18, mean 16.1, max 30; tracks 55, persistent 16; splits 4, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 0.5; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 20, mean 14.5, max 24; tracks 31, persistent 15; splits 7, persistent splits 6 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
