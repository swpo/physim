# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 212s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/fork_seed4 --seeds 4 --frames 70 --no-movie`
- segmentation: matter > 0.44 of robust range [0.0715, 1.0559], min area 6 px

## Measurements
- components: final 22, mean 27.0, max 42; occupancy final 0.08
- tracks: 55; persistent (alive >= 50% of run): 20; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 23, 22], H1 [1, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00272/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.091, nucleations 31
- channel total drift (end/start - 1): [-0.3491, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 37: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.04; core [0.001, 0.883, 0.728, 0.004] rim [0.009, 0.649, 0.725, 0.007]
  - track 4 at frame 37: holes 0, rim-vs-core 0.26, rim-vs-outside 0.32, heterogeneity 0.04; core [0.001, 0.903, 0.81, 0.005] rim [0.01, 0.64, 0.808, 0.008]
  - track 5 at frame 38: holes 0, rim-vs-core 0.22, rim-vs-outside 0.31, heterogeneity 0.04; core [0.001, 0.9, 0.76, 0.004] rim [0.008, 0.685, 0.755, 0.007]
  - track 48 at frame 55: holes 0, rim-vs-core 0.23, rim-vs-outside 0.32, heterogeneity 0.04; core [0.005, 0.927, 0.682, 0.005] rim [0.013, 0.695, 0.676, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 173 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 3.69 (aggregate of 173 individuals; 4/173 membrane-like individually; rim level 0.435)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 12.1 (aggregate of 173 individuals; 1/173 membrane-like individually; rim level 0.429)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.93 (aggregate of 173 individuals; 0/173 membrane-like individually; rim level 0.458)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 5.87 (aggregate of 173 individuals; 6/173 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3700, R_eq 3.7): none; #4 (t=3700, R_eq 3.87): none; #5 (t=3800, R_eq 3.57): none; #48 (t=5500, R_eq 2.11): none
- species `prey` (channels ['prey a'], own threshold): components final 1, mean 17.0, max 37; tracks 64, persistent 10; splits 2, persistent splits 1 (K=20), max generation 1, merges 12, merge/split 6; moving tracks 8
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 13.7, max 22; tracks 27, persistent 13; splits 5, persistent splits 3 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
