# Evidence pack: condensate-food-chain (seed 21)

- world: `../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 125s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1555-c41-review-foodchain/twin_nopred --seeds 21 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0255, 1.1626], min area 6 px

## Measurements
- components: final 79, mean 78.3, max 81; occupancy final 0.30
- tracks: 173; persistent (alive >= 50% of run): 79; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [79, 79, 79], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 32, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.469, nucleations 10
- channel total drift (end/start - 1): [0.2122, None, -0.7073, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.09; core [0.893, 0.0, 0.035, 0.887] rim [0.514, 0.0, 0.094, 0.705]
  - track 17 at frame 61: holes 0, rim-vs-core 0.44, rim-vs-outside 0.32, heterogeneity 0.09; core [0.883, 0.0, 0.04, 0.866] rim [0.483, 0.0, 0.095, 0.7]
  - track 69 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.08; core [0.899, 0.0, 0.032, 0.897] rim [0.544, 0.0, 0.091, 0.714]
  - track 145 at frame 62: holes 0, rim-vs-core 0.40, rim-vs-outside 0.34, heterogeneity 0.08; core [0.896, 0.0, 0.038, 0.873] rim [0.535, 0.0, 0.091, 0.714]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 474 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 24 (aggregate of 474 individuals; 0/474 membrane-like individually; rim level 0.845)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 474 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.58, rim/outside 0.868 (aggregate of 474 individuals; 0/474 membrane-like individually; rim level 0.141)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 1.79 (aggregate of 474 individuals; 0/474 membrane-like individually; rim level 0.827)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=6100, R_eq 4.69): none; #17 (t=6100, R_eq 4.51): none; #69 (t=6100, R_eq 4.72): none; #145 (t=6200, R_eq 4.41): none
- species `prey` (channels ['prey a'], own threshold): components final 79, mean 78.3, max 81; tracks 173, persistent 79; splits 32, persistent splits 7 (K=5), max generation 1, merges 15, merge/split 0.469; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
