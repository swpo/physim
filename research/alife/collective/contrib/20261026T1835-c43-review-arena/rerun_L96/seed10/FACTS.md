# Evidence pack: condensate-food-chain (seed 10)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [96, 96]; wall 123s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1835-c43-review-arena/world.py --out collective/contrib/20261026T1835-c43-review-arena/rerun_L96/seed10 --seeds 10 --size 96 96 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.035, 1.3527], min area 6 px

## Measurements
- components: final 17, mean 19.1, max 41; occupancy final 0.18
- tracks: 249; persistent (alive >= 50% of run): 0; longest 35 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.76, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 17, 10], H1 [2, 2, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00409/time; max body lengths 1.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 79, persistent splits 37 (0 more failed only because the siblings re-merged within K), max generation 8, merges 23, merge/split ratio 0.291, nucleations 31
- channel total drift (end/start - 1): [-0.3839, 2.1187, -0.3436, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 18: holes 0, rim-vs-core 0.24, rim-vs-outside 0.27, heterogeneity 0.04; core [0.005, 0.857, 0.731, 0.11] rim [0.016, 0.62, 0.723, 0.115]
  - track 25 at frame 17: holes 0, rim-vs-core 0.25, rim-vs-outside 0.40, heterogeneity 0.08; core [0.895, 0.017, 0.037, 0.845] rim [0.671, 0.025, 0.118, 0.753]
  - track 55 at frame 18: holes 0, rim-vs-core 0.12, rim-vs-outside 0.47, heterogeneity 0.05; core [0.002, 0.85, 0.66, 0.197] rim [0.008, 0.731, 0.643, 0.208]
  - track 222 at frame 112: holes 0, rim-vs-core 0.18, rim-vs-outside 0.27, heterogeneity 0.05; core [0.004, 0.829, 0.552, 0.238] rim [0.01, 0.648, 0.552, 0.236]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 3.4 (aggregate of 95 individuals; 9/95 membrane-like individually; rim level 0.26)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.02 (aggregate of 95 individuals; 10/95 membrane-like individually; rim level 0.467)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.944 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.512)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 1.3 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.422)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=1800, R_eq 5.29): none; #25 (t=1700, R_eq 5.97): none; #55 (t=1800, R_eq 6.15): none; #222 (t=11200, R_eq 3.61): none
- species `prey` (channels ['prey a'], own threshold): components final 3, mean 7.8, max 35; tracks 161, persistent 0; splits 47, persistent splits 12 (K=5), max generation 7, merges 4, merge/split 0.085; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 13, mean 13.1, max 21; tracks 174, persistent 0; splits 42, persistent splits 12 (K=5), max generation 1, merges 12, merge/split 0.286; moving tracks 12

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 14 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
