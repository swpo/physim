# Evidence pack: condensate-food-chain (seed 5)

- world: `../../20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 567s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out collective/contrib/wip-c33-fc/rerun --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0091, 1.2652], min area 6 px

## Measurements
- components: final 175, mean 161.8, max 228; occupancy final 0.31
- tracks: 754; persistent (alive >= 50% of run): 146; longest 101 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 13.60 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [176, 175, 175], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00471/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 186, persistent splits 60 (0 more failed only because the siblings re-merged within K), max generation 3, merges 80, merge/split ratio 0.43, nucleations 16
- channel total drift (end/start - 1): [0.2934, -0.9996, -0.7329, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 71 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.51, heterogeneity 0.07; core [0.95, 0.0, 0.026, 0.96] rim [0.643, 0.0, 0.078, 0.886]
  - track 138 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.95, 0.0, 0.025, 0.964] rim [0.648, 0.0, 0.079, 0.886]
  - track 192 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.51, heterogeneity 0.07; core [0.948, 0.0, 0.024, 0.963] rim [0.65, 0.0, 0.079, 0.885]
  - track 678 at frame 68: holes 0, rim-vs-core 0.31, rim-vs-outside 0.52, heterogeneity 0.07; core [0.954, 0.0, 0.026, 0.961] rim [0.653, 0.0, 0.077, 0.888]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 949 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 17.1 (aggregate of 949 individuals; 5/949 membrane-like individually; rim level 0.863)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 1.28 (aggregate of 949 individuals; 4/949 membrane-like individually; rim level 0.0111)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.36, rim/outside 0.874 (aggregate of 949 individuals; 0/949 membrane-like individually; rim level 0.136)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 1.21 (aggregate of 949 individuals; 0/949 membrane-like individually; rim level 0.92)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #71 (t=5000, R_eq 6.28): none; #138 (t=5000, R_eq 6.43): none; #192 (t=5000, R_eq 6.46): none; #678 (t=6800, R_eq 6.15): none
- species `prey` (channels ['prey a'], own threshold): components final 175, mean 156.3, max 197; tracks 583, persistent 146; splits 130, persistent splits 61 (K=20), max generation 3, merges 43, merge/split 0.331; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 10.0, max 88; tracks 189, persistent 0; splits 34, persistent splits 0 (K=20), max generation 0, merges 13, merge/split 0.382; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 949 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
