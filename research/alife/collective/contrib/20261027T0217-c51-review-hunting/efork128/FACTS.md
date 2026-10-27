# Evidence pack: driven-condensate-prey-predator (seed 13)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0217-c51-review-hunting/efork128 --seeds 13 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.1398, 1.1994], min area 6 px

## Measurements
- components: final 13, mean 16.4, max 30; occupancy final 0.04
- tracks: 36; persistent (alive >= 50% of run): 14; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 12], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 1, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 34
- channel total drift (end/start - 1): [-0.1298, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.26, heterogeneity 0.05; core [0.004, 0.871, 0.604, 0.069] rim [0.017, 0.549, 0.601, 0.08]
  - track 5 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.26, heterogeneity 0.05; core [0.006, 0.868, 0.593, 0.071] rim [0.02, 0.544, 0.59, 0.081]
  - track 6 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.05; core [0.004, 0.893, 0.614, 0.071] rim [0.016, 0.576, 0.61, 0.08]
  - track 16 at frame 42: holes 0, rim-vs-core 0.21, rim-vs-outside 0.22, heterogeneity 0.03; core [0.02, 0.754, 0.584, 0.081] rim [0.028, 0.549, 0.582, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 3.1 (aggregate of 100 individuals; 1/100 membrane-like individually; rim level 0.289)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 18.9 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.56)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.968 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.391)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 2.86 (aggregate of 100 individuals; 1/100 membrane-like individually; rim level 0.323)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=4300, R_eq 3.09): none; #5 (t=4300, R_eq 2.93): none; #6 (t=4300, R_eq 2.93): none; #16 (t=4200, R_eq 2.39): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 8.0, max 16; tracks 44, persistent 0; splits 5, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 12, mean 10.4, max 17; tracks 21, persistent 8; splits 1, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
