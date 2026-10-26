# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 210s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/fed_seed4 --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.45 of robust range [0.0706, 1.0154], min area 6 px

## Measurements
- components: final 39, mean 28.9, max 42; occupancy final 0.18
- tracks: 59; persistent (alive >= 50% of run): 32; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 40, 39], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00232/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.25, nucleations 31
- channel total drift (end/start - 1): [-0.1201, None, -0.4912, -0.578]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 37: holes 0, rim-vs-core 0.24, rim-vs-outside 0.29, heterogeneity 0.04; core [0.001, 0.92, 0.668, 0.0] rim [0.008, 0.678, 0.664, 0.002]
  - track 4 at frame 37: holes 0, rim-vs-core 0.27, rim-vs-outside 0.33, heterogeneity 0.04; core [0.001, 0.939, 0.769, 0.001] rim [0.008, 0.669, 0.766, 0.003]
  - track 5 at frame 38: holes 0, rim-vs-core 0.22, rim-vs-outside 0.32, heterogeneity 0.04; core [0.0, 0.939, 0.708, 0.0] rim [0.007, 0.715, 0.701, 0.002]
  - track 48 at frame 55: holes 0, rim-vs-core 0.24, rim-vs-outside 0.34, heterogeneity 0.04; core [0.004, 0.968, 0.612, 0.001] rim [0.011, 0.725, 0.605, 0.002]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 190 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 4.26 (aggregate of 190 individuals; 4/190 membrane-like individually; rim level 0.482)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 8.92 (aggregate of 190 individuals; 1/190 membrane-like individually; rim level 0.377)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.6, rim/outside 0.894 (aggregate of 190 individuals; 0/190 membrane-like individually; rim level 0.421)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 6.4 (aggregate of 190 individuals; 6/190 membrane-like individually; rim level 0.45)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3700, R_eq 3.7): none; #4 (t=3700, R_eq 3.87): none; #5 (t=3800, R_eq 3.57): none; #48 (t=5500, R_eq 2.11): none
- species `prey` (channels ['prey a'], own threshold): components final 18, mean 18.8, max 33; tracks 51, persistent 19; splits 2, persistent splits 1 (K=20), max generation 1, merges 2, merge/split 1; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 13.7, max 22; tracks 27, persistent 13; splits 5, persistent splits 3 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
