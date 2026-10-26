# Evidence pack: driven-condensate-prey-predator (seed 0)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 372s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/c_s0 --seeds 0 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1422, 1.2084], min area 6 px

## Measurements
- components: final 22, mean 20.0, max 35; occupancy final 0.09
- tracks: 77; persistent (alive >= 50% of run): 4; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 22, 20], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 9, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.111, nucleations 58
- channel total drift (end/start - 1): [-0.1062, None, -0.4911, -0.5728]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 35: holes 0, rim-vs-core 0.34, rim-vs-outside 0.24, heterogeneity 0.05; core [0.002, 0.869, 0.543, 0.002] rim [0.014, 0.531, 0.537, 0.013]
  - track 0 at frame 32: holes 0, rim-vs-core 0.34, rim-vs-outside 0.24, heterogeneity 0.05; core [0.001, 0.884, 0.538, 0.001] rim [0.013, 0.541, 0.531, 0.012]
  - track 5 at frame 34: holes 0, rim-vs-core 0.29, rim-vs-outside 0.26, heterogeneity 0.05; core [0.001, 0.867, 0.537, 0.001] rim [0.011, 0.579, 0.532, 0.009]
  - track 43 at frame 86: holes 0, rim-vs-core 0.26, rim-vs-outside 0.33, heterogeneity 0.05; core [0.012, 0.885, 0.51, 0.011] rim [0.023, 0.622, 0.501, 0.018]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 113 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 3.86 (aggregate of 113 individuals; 4/113 membrane-like individually; rim level 0.332)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 10.3 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.486)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 0.924 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.383)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 4.4 (aggregate of 113 individuals; 4/113 membrane-like individually; rim level 0.328)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=3500, R_eq 4.03): none; #0 (t=3200, R_eq 4.18): none; #5 (t=3400, R_eq 3.99): none; #43 (t=8600, R_eq 2.76): none
- species `prey` (channels ['prey a'], own threshold): components final 11, mean 8.4, max 17; tracks 95, persistent 0; splits 17, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 14, mean 13.9, max 26; tracks 67, persistent 0; splits 8, persistent splits 3 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
