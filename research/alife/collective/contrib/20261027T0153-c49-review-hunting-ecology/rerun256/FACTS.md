# Evidence pack: driven-condensate-prey-predator (seed 9)

- world: `../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1988s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/c49rev4/rerun256 --seeds 9 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.34 of robust range [0.145, 1.2002], min area 6 px

## Measurements
- components: final 77, mean 75.0, max 127; occupancy final 0.06
- tracks: 294; persistent (alive >= 50% of run): 18; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 57.14 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [86, 77, 57], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00121/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 46, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 201
- channel total drift (end/start - 1): [-0.108, None, -0.4893, -0.5736]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 101 at frame 81: holes 0, rim-vs-core 0.26, rim-vs-outside 0.22, heterogeneity 0.04; core [0.0, 0.829, 0.506, 0.0] rim [0.002, 0.567, 0.5, 0.001]
  - track 102 at frame 80: holes 0, rim-vs-core 0.21, rim-vs-outside 0.19, heterogeneity 0.03; core [0.008, 0.754, 0.536, 0.008] rim [0.018, 0.542, 0.532, 0.015]
  - track 0 at frame 36: holes 0, rim-vs-core 0.17, rim-vs-outside 0.48, heterogeneity 0.06; core [0.894, 0.0, 0.001, 0.722] rim [0.737, 0.0, 0.053, 0.68]
  - track 225 at frame 110: holes 0, rim-vs-core 0.28, rim-vs-outside 0.26, heterogeneity 0.04; core [0.023, 0.845, 0.487, 0.02] rim [0.032, 0.569, 0.487, 0.027]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 441 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 3.97 (aggregate of 441 individuals; 11/441 membrane-like individually; rim level 0.353)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 9.33 (aggregate of 441 individuals; 3/441 membrane-like individually; rim level 0.464)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.922 (aggregate of 441 individuals; 0/441 membrane-like individually; rim level 0.381)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 4.51 (aggregate of 441 individuals; 11/441 membrane-like individually; rim level 0.352)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #101 (t=8100, R_eq 3.66): none; #102 (t=8000, R_eq 3.09): none; #0 (t=3600, R_eq 9.11): none; #225 (t=11000, R_eq 2.52): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 31.9, max 64; tracks 350, persistent 2; splits 72, persistent splits 1 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 24
- species `predator` (channels ['predator b'], own threshold): components final 55, mean 52.5, max 83; tracks 272, persistent 0; splits 41, persistent splits 21 (K=5), max generation 2, merges 3, merge/split 0.073; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 441 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
