# Evidence pack: driven-condensate-prey-predator (seed 10)

- world: `../../20261026T2024-c46-hunting-predators-divide-256/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1932s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2024-c46-hunting-predators-divide-256/world.py --out collective/contrib/c49rev9/rerun256 --seeds 10 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1431, 1.1636], min area 6 px

## Measurements
- components: final 51, mean 64.3, max 107; occupancy final 0.07
- tracks: 220; persistent (alive >= 50% of run): 19; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 38.12 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 54, 28], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 35, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 150
- channel total drift (end/start - 1): [-0.0654, None, -0.499, -0.5549]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 81: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.06; core [0.921, 0.0, 0.006, 0.776] rim [0.736, 0.0, 0.073, 0.678]
  - track 26 at frame 45: holes 0, rim-vs-core 0.18, rim-vs-outside 0.46, heterogeneity 0.06; core [0.872, 0.0, 0.005, 0.703] rim [0.717, 0.001, 0.075, 0.658]
  - track 27 at frame 44: holes 0, rim-vs-core 0.37, rim-vs-outside 0.27, heterogeneity 0.06; core [0.017, 0.893, 0.467, 0.012] rim [0.033, 0.519, 0.463, 0.024]
  - track 180 at frame 110: holes 0, rim-vs-core 0.31, rim-vs-outside 0.27, heterogeneity 0.05; core [0.023, 0.884, 0.533, 0.024] rim [0.031, 0.579, 0.53, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 369 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 5.04 (aggregate of 369 individuals; 14/369 membrane-like individually; rim level 0.435)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 8.65 (aggregate of 369 individuals; 4/369 membrane-like individually; rim level 0.397)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.895 (aggregate of 369 individuals; 0/369 membrane-like individually; rim level 0.373)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 5.75 (aggregate of 369 individuals; 15/369 membrane-like individually; rim level 0.429)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #65 (t=8100, R_eq 8.12): none; #26 (t=4500, R_eq 9.39): none; #27 (t=4400, R_eq 3.09): none; #180 (t=11000, R_eq 2.39): none
- species `prey` (channels ['prey a'], own threshold): components final 19, mean 33.1, max 53; tracks 293, persistent 9; splits 68, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 17
- species `predator` (channels ['predator b'], own threshold): components final 39, mean 39.3, max 67; tracks 207, persistent 2; splits 30, persistent splits 12 (K=5), max generation 1, merges 3, merge/split 0.1; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 369 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
