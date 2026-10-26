# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1240-c42-slowfuel-standing-ecology/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 151s; status ok
- command: `python -m labkit.run ../20261026T1240-c42-slowfuel-standing-ecology/world.py --out rerun/seed5 --seeds 5 --frames 120 --size 128 128 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0531, 1.1666], min area 6 px

## Measurements
- components: final 42, mean 55.2, max 95; occupancy final 0.26
- tracks: 500; persistent (alive >= 50% of run): 20; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.38 (1 = constant size)
- enclosures: components with a hole mean 0.87, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 3, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 46, 39], H1 [7, 4, 1]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.00506/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 2000, default): splits 122, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 105, merge/split ratio 0.861, nucleations 57
- channel total drift (end/start - 1): [-0.3675, 2.0911, -0.3915, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 82 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.33, heterogeneity 0.06; core [0.921, 0.0, 0.043, 0.495] rim [0.62, 0.0, 0.145, 0.453]
  - track 97 at frame 62: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.07; core [0.9, 0.0, 0.061, 0.464] rim [0.552, 0.0, 0.161, 0.425]
  - track 98 at frame 62: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.07; core [0.901, 0.0, 0.059, 0.477] rim [0.563, 0.0, 0.156, 0.439]
  - track 363 at frame 95: holes 0, rim-vs-core 0.18, rim-vs-outside 0.44, heterogeneity 0.07; core [0.888, 0.0, 0.059, 0.514] rim [0.714, 0.0, 0.111, 0.492]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 308 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 7.34 (aggregate of 308 individuals; 2/308 membrane-like individually; rim level 0.559)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 3.89 (aggregate of 308 individuals; 4/308 membrane-like individually; rim level 0.231)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.847 (aggregate of 308 individuals; 0/308 membrane-like individually; rim level 0.42)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 1.28 (aggregate of 308 individuals; 0/308 membrane-like individually; rim level 0.409)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #82 (t=6200, R_eq 3.66): none; #97 (t=6200, R_eq 3.52): none; #98 (t=6200, R_eq 3.52): none; #363 (t=9500, R_eq 3.83): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 40.1, max 78; tracks 370, persistent 18; splits 89, persistent splits 8 (K=20), max generation 2, merges 10, merge/split 0.112; moving tracks 32
- species `predator` (channels ['predator b'], own threshold): components final 8, mean 17.8, max 34; tracks 217, persistent 0; splits 29, persistent splits 0 (K=20), max generation 0, merges 49, merge/split 1.69; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 308 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
