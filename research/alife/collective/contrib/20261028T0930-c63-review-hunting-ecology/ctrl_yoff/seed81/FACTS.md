# Evidence pack: driven-condensate-prey-predator (seed 81)

- world: `../../ctrl_world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0930-c63-review-hunting-ecology/ctrl_world.py --out collective/contrib/20261028T0930-c63-review-hunting-ecology/ctrl_yoff/seed81 --seeds 81 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.40 of robust range [0.0, 1.2457], min area 6 px

## Measurements
- components: final 11, mean 16.6, max 38; occupancy final 0.28
- tracks: 64; persistent (alive >= 50% of run): 3; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 57.14 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 11, 11], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 1.5, nucleations 50
- channel total drift (end/start - 1): [0.2399, None, 0.0, 0.8363]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 90: holes 0, rim-vs-core 0.33, rim-vs-outside 0.78, heterogeneity 0.08; core [0.989, 0.0, 1.0, 0.984] rim [0.763, 0.0, 1.0, 0.748]
  - track 25 at frame 84: holes 0, rim-vs-core 0.21, rim-vs-outside 0.89, heterogeneity 0.07; core [0.985, 0.0, 1.0, 0.981] rim [0.834, 0.0, 1.0, 0.828]
  - track 0 at frame 32: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.05; core [0.085, 0.859, 0.488, 0.018] rim [0.097, 0.55, 0.48, 0.023]
  - track 34 at frame 91: holes 0, rim-vs-core 0.41, rim-vs-outside 0.45, heterogeneity 0.07; core [0.953, 0.0, 1.0, 0.94] rim [0.66, 0.0, 1.0, 0.647]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 6.03 (aggregate of 101 individuals; 2/101 membrane-like individually; rim level 0.703)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 6.9 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.176)
  - radial fuel F: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.979 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.794)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 7.33 (aggregate of 101 individuals; 2/101 membrane-like individually; rim level 0.625)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=9000, R_eq 6.63): none; #25 (t=8400, R_eq 8.99): none; #0 (t=3200, R_eq 4.55): none; #34 (t=9100, R_eq 5.75): none
- species `prey` (channels ['prey a'], own threshold): components final 11, mean 12.1, max 29; tracks 67, persistent 2; splits 6, persistent splits 0 (K=5), max generation 0, merges 5, merge/split 0.833; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 5.9, max 18; tracks 34, persistent 0; splits 3, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
