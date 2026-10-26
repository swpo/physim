# Evidence pack: condensate-food-chain (seed 3)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 415s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0426-c32-review-foodchain/world.py --out collective/contrib/20261026T0426-c32-review-foodchain/pack --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2469], min area 6 px

## Measurements
- components: final 181, mean 168.5, max 207; occupancy final 0.32
- tracks: 703; persistent (alive >= 50% of run): 172; longest 101 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 17.38 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [181, 181, 181], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0015/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 168, persistent splits 55 (0 more failed only because the siblings re-merged within K), max generation 3, merges 67, merge/split ratio 0.399, nucleations 19
- channel total drift (end/start - 1): [0.2833, -0.9997, -0.7337, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.52, heterogeneity 0.07; core [0.952, 0.0, 0.024, 0.958] rim [0.656, 0.0, 0.076, 0.873]
  - track 39 at frame 50: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.07; core [0.899, 0.0, 0.04, 0.93] rim [0.502, 0.0, 0.087, 0.855]
  - track 49 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.898, 0.0, 0.041, 0.926] rim [0.506, 0.0, 0.087, 0.852]
  - track 691 at frame 76: holes 0, rim-vs-core 0.34, rim-vs-outside 0.51, heterogeneity 0.07; core [0.954, 0.0, 0.026, 0.954] rim [0.626, 0.0, 0.078, 0.871]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1007 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 16.9 (aggregate of 1007 individuals; 5/1007 membrane-like individually; rim level 0.877)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.03 (aggregate of 1007 individuals; 3/1007 membrane-like individually; rim level 0.0048)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.87, rim/outside 0.877 (aggregate of 1007 individuals; 0/1007 membrane-like individually; rim level 0.131)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 1.24 (aggregate of 1007 individuals; 0/1007 membrane-like individually; rim level 0.914)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=5000, R_eq 6.28): none; #39 (t=5000, R_eq 5.89): none; #49 (t=5000, R_eq 5.86): none; #691 (t=7600, R_eq 6.13): none
- species `prey` (channels ['prey a'], own threshold): components final 181, mean 164.6, max 199; tracks 577, persistent 172; splits 134, persistent splits 55 (K=20), max generation 3, merges 49, merge/split 0.366; moving tracks 5
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 7.7, max 73; tracks 160, persistent 0; splits 31, persistent splits 0 (K=20), max generation 0, merges 11, merge/split 0.355; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 1007 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
