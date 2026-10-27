# Evidence pack: driven-condensate-prey-predator (seed 61)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 346s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/hunt/twin128 --seeds 61 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.51 of robust range [0.1226, 0.8691], min area 6 px

## Measurements
- components: final 21, mean 12.1, max 21; occupancy final 0.15
- tracks: 31; persistent (alive >= 50% of run): 11; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 40.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 21, 21], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 10, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 11
- channel total drift (end/start - 1): [0.0, None, -0.5477, -0.523]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 56: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.07; core [0.907, 0.0, 0.019, 0.807] rim [0.703, 0.0, 0.104, 0.683]
  - track 1 at frame 54: holes 0, rim-vs-core 0.22, rim-vs-outside 0.50, heterogeneity 0.07; core [0.882, 0.0, 0.015, 0.761] rim [0.701, 0.0, 0.098, 0.67]
  - track 9 at frame 62: holes 0, rim-vs-core 0.29, rim-vs-outside 0.54, heterogeneity 0.08; core [0.928, 0.0, 0.025, 0.858] rim [0.707, 0.0, 0.105, 0.693]
  - track 11 at frame 106: holes 0, rim-vs-core 0.27, rim-vs-outside 0.64, heterogeneity 0.08; core [0.971, 0.0, 0.034, 0.949] rim [0.774, 0.0, 0.099, 0.771]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 15.5 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.786)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 81 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.91, rim/outside 0.658 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.232)
  - radial product p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 14.9 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.757)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=5600, R_eq 7.9): none; #1 (t=5400, R_eq 8.63): none; #9 (t=6200, R_eq 7.76): none; #11 (t=10600, R_eq 6.21): none
- species `prey` (channels ['prey a'], own threshold): components final 21, mean 12.1, max 21; tracks 31, persistent 11; splits 10, persistent splits 10 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
