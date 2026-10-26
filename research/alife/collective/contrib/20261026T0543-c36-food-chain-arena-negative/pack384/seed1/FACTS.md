# Evidence pack: condensate-food-chain (seed 1)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [384, 384]; wall 1569s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0413-c36-food-chain-predation-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/big/s1 --seeds 1 --frames 100 --size 384 384 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2392], min area 7 px

## Measurements
- components: final 406, mean 387.7, max 469; occupancy final 0.31
- tracks: 1522; persistent (alive >= 50% of run): 394; longest 101 frames; alive start-to-end: 20
- size of persistent tracks: max/min area ratio 13.45 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [406, 406, 406], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00673/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 335, persistent splits 112 (0 more failed only because the siblings re-merged within K), max generation 3, merges 145, merge/split ratio 0.433, nucleations 64
- channel total drift (end/start - 1): [0.312, -0.9997, -0.7333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 50: holes 0, rim-vs-core 0.32, rim-vs-outside 0.52, heterogeneity 0.07; core [0.943, 0.0, 0.025, 0.958] rim [0.642, 0.0, 0.077, 0.872]
  - track 61 at frame 50: holes 0, rim-vs-core 0.42, rim-vs-outside 0.30, heterogeneity 0.07; core [0.897, 0.0, 0.039, 0.93] rim [0.491, 0.0, 0.088, 0.852]
  - track 106 at frame 50: holes 0, rim-vs-core 0.33, rim-vs-outside 0.52, heterogeneity 0.07; core [0.952, 0.0, 0.025, 0.954] rim [0.639, 0.0, 0.076, 0.87]
  - track 1470 at frame 69: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.07; core [0.877, 0.0, 0.045, 0.922] rim [0.662, 0.0, 0.065, 0.89]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2302 components >= 14 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 18 (aggregate of 2302 individuals; 5/2302 membrane-like individually; rim level 0.881)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.99 (aggregate of 2302 individuals; 1/2302 membrane-like individually; rim level 0.0041)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.17, rim/outside 0.875 (aggregate of 2302 individuals; 0/2302 membrane-like individually; rim level 0.13)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 1.24 (aggregate of 2302 individuals; 0/2302 membrane-like individually; rim level 0.916)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=5000, R_eq 6.38): none; #61 (t=5000, R_eq 6): none; #106 (t=5000, R_eq 6.18): none; #1470 (t=6900, R_eq 5.78): none
- species `prey` (channels ['prey a'], own threshold): components final 406, mean 379.7, max 461; tracks 1223, persistent 394; splits 253, persistent splits 112 (K=20), max generation 3, merges 86, merge/split 0.34; moving tracks 16
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 16.6, max 170; tracks 335, persistent 0; splits 56, persistent splits 0 (K=20), max generation 0, merges 24, merge/split 0.429; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 2302 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
