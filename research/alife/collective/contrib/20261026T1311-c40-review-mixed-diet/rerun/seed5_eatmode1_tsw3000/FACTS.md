# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1200-c42-mixed-diet-predators/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run ../20261026T1200-c42-mixed-diet-predators/world.py --out rerun/seed5_eatmode1_tsw3000 --seeds 5 --frames 120 --size 128 128 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0204, 1.4234], min area 6 px

## Measurements
- components: final 47, mean 37.0, max 47; occupancy final 0.29
- tracks: 308; persistent (alive >= 50% of run): 27; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.10 (1 = constant size)
- enclosures: components with a hole mean 0.55, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 47, 47], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 96, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 37, merge/split ratio 0.385, nucleations 21
- channel total drift (end/start - 1): [0.2393, -1.0, -0.7376, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 229 at frame 81: holes 0, rim-vs-core 0.25, rim-vs-outside 0.52, heterogeneity 0.06; core [0.937, 0.0, 0.021, 0.965] rim [0.696, 0.0, 0.07, 0.901]
  - track 235 at frame 81: holes 0, rim-vs-core 0.27, rim-vs-outside 0.51, heterogeneity 0.06; core [0.937, 0.0, 0.023, 0.962] rim [0.674, 0.0, 0.072, 0.899]
  - track 236 at frame 81: holes 0, rim-vs-core 0.31, rim-vs-outside 0.31, heterogeneity 0.05; core [0.898, 0.0, 0.036, 0.945] rim [0.594, 0.0, 0.078, 0.89]
  - track 300 at frame 96: holes 0, rim-vs-core 0.32, rim-vs-outside 0.32, heterogeneity 0.06; core [0.902, 0.0, 0.037, 0.944] rim [0.585, 0.0, 0.079, 0.89]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 218 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 14.4 (aggregate of 218 individuals; 4/218 membrane-like individually; rim level 0.747)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 3.71 (aggregate of 218 individuals; 5/218 membrane-like individually; rim level 0.1)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 2.13, rim/outside 0.91 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.2)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 1.19 (aggregate of 218 individuals; 0/218 membrane-like individually; rim level 0.824)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #229 (t=8100, R_eq 6.18): none; #235 (t=8100, R_eq 6.1): none; #236 (t=8100, R_eq 5.78): none; #300 (t=9600, R_eq 5.59): none
- species `prey` (channels ['prey a'], own threshold): components final 47, mean 30.2, max 47; tracks 202, persistent 25; splits 60, persistent splits 18 (K=20), max generation 3, merges 11, merge/split 0.183; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 9.4, max 33; tracks 148, persistent 0; splits 47, persistent splits 0 (K=20), max generation 0, merges 11, merge/split 0.234; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 218 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
