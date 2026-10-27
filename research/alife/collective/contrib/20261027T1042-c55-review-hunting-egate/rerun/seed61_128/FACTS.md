# Evidence pack: driven-condensate-prey-predator (seed 61)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 470s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/hunt/pack128 --seeds 61 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.39 of robust range [0.1334, 1.0766], min area 6 px

## Measurements
- components: final 13, mean 12.7, max 19; occupancy final 0.15
- tracks: 34; persistent (alive >= 50% of run): 8; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 36.44 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 15, 13], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 5, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 24
- channel total drift (end/start - 1): [0.0066, None, -0.5364, -0.533]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 67: holes 0, rim-vs-core 0.21, rim-vs-outside 0.48, heterogeneity 0.07; core [0.878, 0.0, 0.015, 0.736] rim [0.704, 0.0, 0.101, 0.662]
  - track 3 at frame 40: holes 0, rim-vs-core 0.18, rim-vs-outside 0.44, heterogeneity 0.06; core [0.85, 0.0, 0.011, 0.675] rim [0.694, 0.0, 0.09, 0.629]
  - track 16 at frame 85: holes 0, rim-vs-core 0.28, rim-vs-outside 0.53, heterogeneity 0.07; core [0.956, 0.0, 0.023, 0.869] rim [0.739, 0.0, 0.099, 0.705]
  - track 24 at frame 99: holes 0, rim-vs-core 0.28, rim-vs-outside 0.48, heterogeneity 0.08; core [0.918, 0.0, 0.031, 0.835] rim [0.712, 0.0, 0.089, 0.66]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 8.32 (aggregate of 75 individuals; 3/75 membrane-like individually; rim level 0.654)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 5.53 (aggregate of 75 individuals; 1/75 membrane-like individually; rim level 0.156)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.82, rim/outside 0.765 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.284)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 9.74 (aggregate of 75 individuals; 3/75 membrane-like individually; rim level 0.621)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=6700, R_eq 9.24): none; #3 (t=4000, R_eq 9.52): none; #16 (t=8500, R_eq 6.68): none; #24 (t=9900, R_eq 9.39): none
- species `prey` (channels ['prey a'], own threshold): components final 12, mean 10.0, max 15; tracks 44, persistent 8; splits 10, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 4, mean 3.9, max 9; tracks 22, persistent 0; splits 3, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
