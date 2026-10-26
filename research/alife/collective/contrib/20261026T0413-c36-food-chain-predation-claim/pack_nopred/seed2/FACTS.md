# Evidence pack: condensate-food-chain (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 686s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packC/s2 --seeds 2 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2167], min area 6 px

## Measurements
- components: final 216, mean 215.5, max 227; occupancy final 0.31
- tracks: 486; persistent (alive >= 50% of run): 216; longest 101 frames; alive start-to-end: 15
- size of persistent tracks: max/min area ratio 22.43 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [216, 216, 216], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00122/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 76, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 39, merge/split ratio 0.513, nucleations 48
- channel total drift (end/start - 1): [0.2974, None, -0.7372, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 50: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.08; core [0.897, 0.0, 0.032, 0.914] rim [0.493, 0.0, 0.08, 0.776]
  - track 41 at frame 50: holes 0, rim-vs-core 0.36, rim-vs-outside 0.52, heterogeneity 0.08; core [0.953, 0.0, 0.019, 0.952] rim [0.628, 0.0, 0.07, 0.807]
  - track 44 at frame 50: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.07; core [0.898, 0.0, 0.037, 0.897] rim [0.508, 0.0, 0.078, 0.785]
  - track 472 at frame 54: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.891, 0.0, 0.04, 0.885] rim [0.503, 0.0, 0.078, 0.782]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1300 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 18.9 (aggregate of 1300 individuals; 0/1300 membrane-like individually; rim level 0.883)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.231 (aggregate of 1300 individuals; 0/1300 membrane-like individually; rim level 0.0008)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 6.16, rim/outside 0.885 (aggregate of 1300 individuals; 0/1300 membrane-like individually; rim level 0.114)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 1.42 (aggregate of 1300 individuals; 0/1300 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=5000, R_eq 5.97): none; #41 (t=5000, R_eq 6.05): none; #44 (t=5000, R_eq 5.35): none; #472 (t=5400, R_eq 5.17): none
- species `prey` (channels ['prey a'], own threshold): components final 216, mean 215.5, max 227; tracks 485, persistent 216; splits 76, persistent splits 7 (K=20), max generation 1, merges 39, merge/split 0.513; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.2, max 151; tracks 289, persistent 0; splits 68, persistent splits 0 (K=20), max generation 0, merges 2, merge/split 0.029; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
