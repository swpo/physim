# Evidence pack: driven-condensate-prey-predator (seed 16)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1415s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0519-c51-review-hunting-controls/pack256_s16 --seeds 16 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1437, 1.1716], min area 6 px

## Measurements
- components: final 54, mean 65.2, max 103; occupancy final 0.07
- tracks: 258; persistent (alive >= 50% of run): 12; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.25 (1 = constant size)
- enclosures: components with a hole mean 0.31, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 56, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 43, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.023, nucleations 171
- channel total drift (end/start - 1): [-0.058, None, -0.5042, -0.5521]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 85: holes 0, rim-vs-core 0.23, rim-vs-outside 0.49, heterogeneity 0.06; core [0.922, 0.001, 0.002, 0.767] rim [0.731, 0.001, 0.048, 0.656]
  - track 20 at frame 39: holes 0, rim-vs-core 0.36, rim-vs-outside 0.28, heterogeneity 0.06; core [0.003, 0.922, 0.479, 0.001] rim [0.019, 0.567, 0.473, 0.012]
  - track 135 at frame 89: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.07; core [0.972, 0.0, 0.004, 0.889] rim [0.74, 0.0, 0.061, 0.69]
  - track 166 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.26, heterogeneity 0.04; core [0.023, 0.836, 0.532, 0.024] rim [0.03, 0.566, 0.53, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 365 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 4.9 (aggregate of 365 individuals; 10/365 membrane-like individually; rim level 0.427)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 9.47 (aggregate of 365 individuals; 5/365 membrane-like individually; rim level 0.411)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.893 (aggregate of 365 individuals; 0/365 membrane-like individually; rim level 0.362)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.853, rim/outside 5.62 (aggregate of 365 individuals; 9/365 membrane-like individually; rim level 0.423)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #109 (t=8500, R_eq 8.08): none; #20 (t=3900, R_eq 3.48): none; #135 (t=8900, R_eq 6.02): none; #166 (t=8800, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 24, mean 33.0, max 55; tracks 301, persistent 3; splits 62, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 24
- species `predator` (channels ['predator b'], own threshold): components final 35, mean 40.5, max 65; tracks 231, persistent 0; splits 34, persistent splits 19 (K=5), max generation 2, merges 2, merge/split 0.059; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 365 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
