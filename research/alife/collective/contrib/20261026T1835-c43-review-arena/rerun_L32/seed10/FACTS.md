# Evidence pack: condensate-food-chain (seed 10)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [32, 32]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1835-c43-review-arena/world.py --out collective/contrib/20261026T1835-c43-review-arena/rerun_L32/seed10 --seeds 10 --size 32 32 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0275, 1.1711], min area 6 px

## Measurements
- components: final 4, mean 3.3, max 4; occupancy final 0.28
- tracks: 14; persistent (alive >= 50% of run): 4; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.25 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 5, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.2, nucleations 1
- channel total drift (end/start - 1): [0.534, -1.0, -0.698, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 80: holes 0, rim-vs-core 0.34, rim-vs-outside 0.37, heterogeneity 0.07; core [0.905, 0.0, 0.036, 0.972] rim [0.574, 0.0, 0.092, 0.931]
  - track 11 at frame 82: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.07; core [0.893, 0.0, 0.039, 0.969] rim [0.513, 0.0, 0.1, 0.924]
  - track 12 at frame 83: holes 0, rim-vs-core 0.23, rim-vs-outside 0.46, heterogeneity 0.07; core [0.895, 0.0, 0.038, 0.97] rim [0.673, 0.0, 0.075, 0.943]
  - track 13 at frame 83: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.06; core [0.904, 0.0, 0.037, 0.971] rim [0.55, 0.0, 0.097, 0.927]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 15.5 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.764)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 4.94 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.079)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 4.11, rim/outside 0.877 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.209)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.13 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.874)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=8000, R_eq 4.82): none; #11 (t=8200, R_eq 4.79): none; #12 (t=8300, R_eq 4.75): none; #13 (t=8300, R_eq 4.69): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 2.9, max 4; tracks 12, persistent 4; splits 3, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.5, max 3; tracks 3, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
