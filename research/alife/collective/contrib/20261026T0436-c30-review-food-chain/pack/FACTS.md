# Evidence pack: condensate-food-chain (seed 4)

- world: `../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 564s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/20261026T0436-c30-review-food-chain/pack --seeds 4 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2653], min area 6 px

## Measurements
- components: final 177, mean 161.6, max 200; occupancy final 0.31
- tracks: 810; persistent (alive >= 50% of run): 156; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.56 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [178, 178, 177], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00624/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 209, persistent splits 78 (0 more failed only because the siblings re-merged within K), max generation 5, merges 83, merge/split ratio 0.397, nucleations 31
- channel total drift (end/start - 1): [0.298, -0.9997, -0.7333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 205 at frame 51: holes 0, rim-vs-core 0.27, rim-vs-outside 0.59, heterogeneity 0.07; core [0.959, 0.0, 0.024, 0.962] rim [0.701, 0.0, 0.068, 0.902]
  - track 221 at frame 51: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.07; core [0.944, 0.0, 0.025, 0.966] rim [0.644, 0.0, 0.08, 0.889]
  - track 254 at frame 51: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.95, 0.0, 0.024, 0.965] rim [0.647, 0.0, 0.079, 0.887]
  - track 779 at frame 75: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.955, 0.0, 0.026, 0.961] rim [0.65, 0.0, 0.077, 0.891]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 960 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 16.7 (aggregate of 960 individuals; 4/960 membrane-like individually; rim level 0.868)
  - radial predator b: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 1.23 (aggregate of 960 individuals; 5/960 membrane-like individually; rim level 0.0099)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.36, rim/outside 0.875 (aggregate of 960 individuals; 0/960 membrane-like individually; rim level 0.136)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 1.21 (aggregate of 960 individuals; 0/960 membrane-like individually; rim level 0.922)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #205 (t=5100, R_eq 6.15): none; #221 (t=5100, R_eq 6.53): none; #254 (t=5100, R_eq 6.48): none; #779 (t=7500, R_eq 6.1): none
- species `prey` (channels ['prey a'], own threshold): components final 177, mean 156.7, max 202; tracks 653, persistent 156; splits 156, persistent splits 79 (K=20), max generation 5, merges 47, merge/split 0.301; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 10.7, max 87; tracks 230, persistent 0; splits 49, persistent splits 0 (K=20), max generation 0, merges 22, merge/split 0.449; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 960 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
