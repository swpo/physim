# Evidence pack: condensate-food-chain (seed 47)

- world: `../../../20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 101s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out collective/contrib/20261026T1721-c45-review-foodchain/nopred/seed47 --seeds 47 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.026, 1.1619], min area 6 px

## Measurements
- components: final 73, mean 72.5, max 75; occupancy final 0.30
- tracks: 150; persistent (alive >= 50% of run): 73; longest 121 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 12.40 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [73, 73, 73], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 29, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.379, nucleations 9
- channel total drift (end/start - 1): [0.2383, None, -0.7042, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.09; core [0.897, 0.0, 0.036, 0.885] rim [0.529, 0.0, 0.099, 0.69]
  - track 17 at frame 61: holes 0, rim-vs-core 0.43, rim-vs-outside 0.33, heterogeneity 0.09; core [0.894, 0.0, 0.041, 0.866] rim [0.506, 0.0, 0.099, 0.69]
  - track 29 at frame 61: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.09; core [0.891, 0.0, 0.042, 0.861] rim [0.497, 0.0, 0.1, 0.688]
  - track 140 at frame 63: holes 0, rim-vs-core 0.23, rim-vs-outside 0.49, heterogeneity 0.09; core [0.859, 0.0, 0.054, 0.822] rim [0.644, 0.0, 0.076, 0.758]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 439 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 24.3 (aggregate of 439 individuals; 0/439 membrane-like individually; rim level 0.85)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 439 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.61, rim/outside 0.864 (aggregate of 439 individuals; 0/439 membrane-like individually; rim level 0.149)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 1.87 (aggregate of 439 individuals; 0/439 membrane-like individually; rim level 0.817)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=6100, R_eq 4.95): none; #17 (t=6100, R_eq 4.69): none; #29 (t=6100, R_eq 4.62): none; #140 (t=6300, R_eq 4.48): none
- species `prey` (channels ['prey a'], own threshold): components final 73, mean 72.5, max 75; tracks 150, persistent 73; splits 29, persistent splits 4 (K=5), max generation 1, merges 11, merge/split 0.379; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
