# Evidence pack: driven-condensate-prey-predator (seed 16)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1104s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0519-c51-review-hunting-controls/twin256_s16 --seeds 16 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.1181, 0.8754], min area 6 px

## Measurements
- components: final 78, mean 53.9, max 78; occupancy final 0.15
- tracks: 104; persistent (alive >= 50% of run): 52; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 45.17 (1 = constant size)
- enclosures: components with a hole mean 0.29, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [90, 80, 78], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00107/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 26, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 52
- channel total drift (end/start - 1): [-0.0, None, -0.5468, -0.5143]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.51, heterogeneity 0.08; core [0.916, 0.0, 0.022, 0.834] rim [0.704, 0.0, 0.096, 0.673]
  - track 3 at frame 62: holes 0, rim-vs-core 0.30, rim-vs-outside 0.56, heterogeneity 0.08; core [0.946, 0.0, 0.028, 0.889] rim [0.721, 0.0, 0.103, 0.701]
  - track 8 at frame 62: holes 0, rim-vs-core 0.31, rim-vs-outside 0.53, heterogeneity 0.08; core [0.938, 0.0, 0.025, 0.868] rim [0.706, 0.0, 0.105, 0.683]
  - track 84 at frame 111: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.09; core [0.93, 0.0, 0.073, 0.944] rim [0.647, 0.0, 0.147, 0.67]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 354 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 15.4 (aggregate of 354 individuals; 3/354 membrane-like individually; rim level 0.796)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 354 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.08, rim/outside 0.661 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.23)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 15.6 (aggregate of 354 individuals; 4/354 membrane-like individually; rim level 0.764)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 8.99): none; #3 (t=6200, R_eq 6.7): none; #8 (t=6200, R_eq 6.56): none; #84 (t=11100, R_eq 5.23): none
- species `prey` (channels ['prey a'], own threshold): components final 78, mean 54.5, max 78; tracks 106, persistent 52; splits 26, persistent splits 24 (K=5), max generation 2, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 354 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
