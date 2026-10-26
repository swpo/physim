# Evidence pack: condensate-food-chain (seed 7)

- world: `../../world_claim.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 160s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/seed7 --seeds 7 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0355, 1.3373], min area 6 px

## Measurements
- components: final 29, mean 33.6, max 69; occupancy final 0.23
- tracks: 440; persistent (alive >= 50% of run): 0; longest 34 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.22, final 5; holes at thresholds 0.2/0.35/0.5 final [4, 5, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 28, 16], H1 [5, 5, 2]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00915/time; max body lengths 1.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 135, persistent splits 63 (0 more failed only because the siblings re-merged within K), max generation 5, merges 42, merge/split ratio 0.311, nucleations 54
- channel total drift (end/start - 1): [-0.3579, 2.7874, -0.4115, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 19: holes 0, rim-vs-core 0.37, rim-vs-outside 0.33, heterogeneity 0.07; core [0.926, 0.0, 0.051, 0.789] rim [0.577, 0.0, 0.139, 0.707]
  - track 44 at frame 17: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.005, 0.834, 0.698, 0.192] rim [0.016, 0.575, 0.697, 0.191]
  - track 78 at frame 18: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.07; core [0.921, 0.001, 0.048, 0.822] rim [0.581, 0.002, 0.139, 0.733]
  - track 387 at frame 109: holes 0, rim-vs-core 0.17, rim-vs-outside 0.45, heterogeneity 0.04; core [0.002, 0.871, 0.677, 0.09] rim [0.009, 0.705, 0.675, 0.086]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 172 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 3.21 (aggregate of 172 individuals; 26/172 membrane-like individually; rim level 0.238)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 4.93 (aggregate of 172 individuals; 17/172 membrane-like individually; rim level 0.491)
  - radial fuel u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.941 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.495)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 1.27 (aggregate of 172 individuals; 0/172 membrane-like individually; rim level 0.438)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=1900, R_eq 5.59): none; #44 (t=1700, R_eq 5.73): none; #78 (t=1800, R_eq 5.86): none; #387 (t=10900, R_eq 6.79): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 13.2, max 61; tracks 301, persistent 0; splits 90, persistent splits 15 (K=5), max generation 4, merges 12, merge/split 0.133; moving tracks 7
- species `predator` (channels ['predator b'], own threshold): components final 21, mean 23.9, max 34; tracks 299, persistent 0; splits 74, persistent splits 30 (K=5), max generation 3, merges 19, merge/split 0.257; moving tracks 23

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 172 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
