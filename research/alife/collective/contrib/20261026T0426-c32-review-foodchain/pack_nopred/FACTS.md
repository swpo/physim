# Evidence pack: condensate-food-chain (seed 3)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 415s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0426-c32-review-foodchain/world.py --out collective/contrib/20261026T0426-c32-review-foodchain/pack_nopred --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0092, 1.2169], min area 6 px

## Measurements
- components: final 223, mean 220.8, max 227; occupancy final 0.32
- tracks: 505; persistent (alive >= 50% of run): 223; longest 101 frames; alive start-to-end: 12
- size of persistent tracks: max/min area ratio 23.50 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [223, 223, 223], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 86, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 46, merge/split ratio 0.535, nucleations 29
- channel total drift (end/start - 1): [0.2713, None, -0.738, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.07; core [0.885, 0.0, 0.037, 0.899] rim [0.677, 0.0, 0.057, 0.842]
  - track 15 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.07; core [0.895, 0.0, 0.035, 0.904] rim [0.517, 0.0, 0.076, 0.789]
  - track 18 at frame 50: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.07; core [0.892, 0.0, 0.041, 0.882] rim [0.517, 0.0, 0.077, 0.784]
  - track 489 at frame 56: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.07; core [0.896, 0.0, 0.034, 0.907] rim [0.509, 0.0, 0.077, 0.783]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1335 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 18 (aggregate of 1335 individuals; 0/1335 membrane-like individually; rim level 0.878)
  - radial predator b: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.243 (aggregate of 1335 individuals; 0/1335 membrane-like individually; rim level 0.0014)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.98, rim/outside 0.889 (aggregate of 1335 individuals; 0/1335 membrane-like individually; rim level 0.112)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 1.41 (aggregate of 1335 individuals; 0/1335 membrane-like individually; rim level 0.876)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=5000, R_eq 5.5): none; #15 (t=5000, R_eq 5.41): none; #18 (t=5000, R_eq 4.98): none; #489 (t=5600, R_eq 5.59): none
- species `prey` (channels ['prey a'], own threshold): components final 223, mean 220.8, max 227; tracks 505, persistent 223; splits 86, persistent splits 8 (K=20), max generation 1, merges 46, merge/split 0.535; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 4.7, max 161; tracks 302, persistent 0; splits 70, persistent splits 0 (K=20), max generation 0, merges 5, merge/split 0.071; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
