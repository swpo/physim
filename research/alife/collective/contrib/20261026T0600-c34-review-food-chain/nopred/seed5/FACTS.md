# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [256, 256]; wall 1012s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/20261026T0600-c34-review-food-chain/nopred/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.009, 1.2169], min area 6 px

## Measurements
- components: final 223, mean 223.0, max 241; occupancy final 0.32
- tracks: 495; persistent (alive >= 50% of run): 223; longest 201 frames; alive start-to-end: 28
- size of persistent tracks: max/min area ratio 26.71 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [223, 223, 223], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000664/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 69, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 43, merge/split ratio 0.623, nucleations 30
- channel total drift (end/start - 1): [0.2804, None, -0.7387, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.22, rim-vs-outside 0.50, heterogeneity 0.08; core [0.883, 0.0, 0.034, 0.822] rim [0.684, 0.0, 0.052, 0.739]
  - track 6 at frame 101: holes 0, rim-vs-core 0.46, rim-vs-outside 0.30, heterogeneity 0.09; core [0.887, 0.0, 0.032, 0.833] rim [0.476, 0.0, 0.074, 0.637]
  - track 15 at frame 101: holes 0, rim-vs-core 0.39, rim-vs-outside 0.33, heterogeneity 0.08; core [0.896, 0.0, 0.036, 0.809] rim [0.542, 0.0, 0.07, 0.652]
  - track 493 at frame 104: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.09; core [0.897, 0.0, 0.03, 0.842] rim [0.503, 0.0, 0.072, 0.645]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1338 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 24.8 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.883)
  - radial predator b: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.508 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.69, rim/outside 0.884 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.107)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.13 (aggregate of 1338 individuals; 0/1338 membrane-like individually; rim level 0.803)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 5.29): none; #6 (t=10100, R_eq 5.44): none; #15 (t=10100, R_eq 4.89): none; #493 (t=10400, R_eq 5.44): none
- species `prey` (channels ['prey a'], own threshold): components final 223, mean 223.0, max 241; tracks 494, persistent 223; splits 69, persistent splits 1 (K=20), max generation 1, merges 43, merge/split 0.623; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 2.5, max 159; tracks 323, persistent 0; splits 77, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.052; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
