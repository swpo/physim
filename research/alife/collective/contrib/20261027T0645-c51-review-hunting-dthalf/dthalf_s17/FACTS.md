# Evidence pack: driven-condensate-prey-predator (seed 17)

- world: `../../20261026T2119-c46-hunting-ecology-dthalf/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [128, 128]; wall 783s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out collective/contrib/20261027T0645-c51-review-hunting-dthalf/dthalf_s17 --seeds 17 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.138, 1.1736], min area 6 px

## Measurements
- components: final 8, mean 15.8, max 33; occupancy final 0.04
- tracks: 61; persistent (alive >= 50% of run): 5; longest 72 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 31.79 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 11, 7], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 12, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.083, nucleations 35
- channel total drift (end/start - 1): [-0.1289, None, -0.4776, -0.5812]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 82: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.07; core [0.926, 0.002, 0.012, 0.795] rim [0.714, 0.0, 0.092, 0.667]
  - track 15 at frame 68: holes 0, rim-vs-core 0.25, rim-vs-outside 0.50, heterogeneity 0.07; core [0.934, 0.0, 0.011, 0.805] rim [0.734, 0.0, 0.08, 0.675]
  - track 16 at frame 69: holes 0, rim-vs-core 0.29, rim-vs-outside 0.50, heterogeneity 0.07; core [0.952, 0.0, 0.011, 0.831] rim [0.727, 0.0, 0.086, 0.672]
  - track 50 at frame 112: holes 0, rim-vs-core 0.14, rim-vs-outside 0.19, heterogeneity 0.03; core [0.009, 0.695, 0.575, 0.009] rim [0.014, 0.556, 0.571, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 5.55 (aggregate of 85 individuals; 6/85 membrane-like individually; rim level 0.449)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 8.12 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.373)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.57, rim/outside 0.874 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.369)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 6.41 (aggregate of 85 individuals; 6/85 membrane-like individually; rim level 0.438)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=8200, R_eq 7.96): none; #15 (t=6800, R_eq 8.31): none; #16 (t=6900, R_eq 7): none; #50 (t=11200, R_eq 3.14): none
- species `prey` (channels ['prey a'], own threshold): components final 3, mean 8.7, max 19; tracks 80, persistent 3; splits 21, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 9, mean 9.4, max 16; tracks 55, persistent 0; splits 8, persistent splits 6 (K=5), max generation 2, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
