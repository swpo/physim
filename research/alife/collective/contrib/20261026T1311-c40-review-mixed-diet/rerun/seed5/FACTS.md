# Evidence pack: condensate-food-chain (seed 5)

- world: `../../../20261026T1200-c42-mixed-diet-predators/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 149s; status ok
- command: `python -m labkit.run ../20261026T1200-c42-mixed-diet-predators/world.py --out rerun/seed5 --seeds 5 --frames 120 --size 128 128 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0341, 1.5378], min area 6 px

## Measurements
- components: final 24, mean 26.0, max 47; occupancy final 0.19
- tracks: 485; persistent (alive >= 50% of run): 0; longest 26 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.02, final 3; holes at thresholds 0.2/0.35/0.5 final [5, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 22, 5], H1 [6, 3, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 153, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 47, merge/split ratio 0.307, nucleations 87
- channel total drift (end/start - 1): [-0.6644, 4.6351, -0.2801, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 273 at frame 75: holes 0, rim-vs-core 0.15, rim-vs-outside 0.21, heterogeneity 0.02; core [0.005, 0.769, 0.7, 0.036] rim [0.012, 0.616, 0.698, 0.036]
  - track 94 at frame 19: holes 0, rim-vs-core 0.13, rim-vs-outside 0.20, heterogeneity 0.03; core [0.006, 0.747, 0.722, 0.054] rim [0.012, 0.613, 0.72, 0.054]
  - track 51 at frame 14: holes 0, rim-vs-core 0.16, rim-vs-outside 0.24, heterogeneity 0.03; core [0.004, 0.822, 0.703, 0.028] rim [0.012, 0.657, 0.702, 0.028]
  - track 309 at frame 76: holes 1, rim-vs-core 0.11, rim-vs-outside 0.35, heterogeneity 0.02; core [0.004, 0.779, 0.71, 0.022] rim [0.009, 0.669, 0.709, 0.022]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 0.648 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.0382)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 4.8 (aggregate of 141 individuals; 21/141 membrane-like individually; rim level 0.587)
  - radial fuel u: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.702)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 1.01 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.0778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #273 (t=7500, R_eq 5.53): none; #94 (t=1900, R_eq 5.44): none; #51 (t=1400, R_eq 3.19): none; #309 (t=7600, R_eq 6.21, ring): ['predator b']
- species `prey` (channels ['prey a'], own threshold): components final 1, mean 7.4, max 46; tracks 224, persistent 0; splits 42, persistent splits 0 (K=20), max generation 0, merges 11, merge/split 0.262; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 21, mean 21.8, max 33; tracks 418, persistent 0; splits 136, persistent splits 0 (K=20), max generation 0, merges 29, merge/split 0.213; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
