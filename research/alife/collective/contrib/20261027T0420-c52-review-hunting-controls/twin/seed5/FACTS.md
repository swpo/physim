# Evidence pack: driven-condensate-prey-predator (seed 5)

- world: `../../../../collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 308s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0420-c52-review-hunting-controls/twin/seed5 --seeds 5 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1194, 0.8795], min area 6 px

## Measurements
- components: final 23, mean 18.2, max 23; occupancy final 0.15
- tracks: 28; persistent (alive >= 50% of run): 18; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 32.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 23, 23], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 18
- channel total drift (end/start - 1): [-0.0, None, -0.5629, -0.5187]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.54, heterogeneity 0.08; core [0.954, 0.0, 0.027, 0.906] rim [0.707, 0.0, 0.108, 0.693]
  - track 3 at frame 63: holes 0, rim-vs-core 0.30, rim-vs-outside 0.54, heterogeneity 0.08; core [0.939, 0.0, 0.025, 0.884] rim [0.713, 0.0, 0.106, 0.701]
  - track 4 at frame 63: holes 0, rim-vs-core 0.19, rim-vs-outside 0.61, heterogeneity 0.08; core [0.93, 0.0, 0.022, 0.863] rim [0.779, 0.0, 0.083, 0.756]
  - track 18 at frame 95: holes 0, rim-vs-core 0.41, rim-vs-outside 0.33, heterogeneity 0.09; core [0.923, 0.0, 0.06, 0.927] rim [0.637, 0.0, 0.139, 0.65]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 20.9 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.845)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 118 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.8, rim/outside 0.665 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.224)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 20.7 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.822)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 6.02): none; #3 (t=6300, R_eq 6.43): none; #4 (t=6300, R_eq 6.86): none; #18 (t=9500, R_eq 5.5): none
- species `prey` (channels ['prey a'], own threshold): components final 23, mean 18.5, max 23; tracks 28, persistent 18; splits 5, persistent splits 5 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
