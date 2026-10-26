# Evidence pack: condensate-food-chain (seed 12)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [32, 32]; wall 18s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1646-c41-review-arena-size/L32_s12 --seeds 12 --size 32 32 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0266, 1.178], min area 6 px

## Measurements
- components: final 4, mean 3.8, max 5; occupancy final 0.31
- tracks: 14; persistent (alive >= 50% of run): 4; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.25, nucleations 1
- channel total drift (end/start - 1): [0.1721, -1.0, -0.7035, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 75: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.08; core [0.899, 0.0, 0.043, 0.927] rim [0.519, 0.0, 0.106, 0.824]
  - track 11 at frame 75: holes 0, rim-vs-core 0.29, rim-vs-outside 0.42, heterogeneity 0.07; core [0.915, 0.0, 0.038, 0.935] rim [0.642, 0.0, 0.088, 0.854]
  - track 12 at frame 76: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.08; core [0.906, 0.0, 0.042, 0.93] rim [0.511, 0.0, 0.107, 0.823]
  - track 13 at frame 76: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.08; core [0.896, 0.0, 0.044, 0.926] rim [0.502, 0.0, 0.108, 0.821]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 29 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.861)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 2.28 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.042)  MEMBRANE-LIKE
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.9, rim/outside 0.869 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.174)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 1.41 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.892)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): predator b (peak at rho=0.25, outside the peak band)
- membrane-like channels per top track at mid-life: #10 (t=7500, R_eq 5.01): none; #11 (t=7500, R_eq 4.98): none; #12 (t=7600, R_eq 5.05): none; #13 (t=7600, R_eq 5.05): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 3.7, max 5; tracks 12, persistent 4; splits 3, persistent splits 2 (K=5), max generation 1, merges 1, merge/split 0.333; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.2, max 2; tracks 4, persistent 0; splits 1, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
