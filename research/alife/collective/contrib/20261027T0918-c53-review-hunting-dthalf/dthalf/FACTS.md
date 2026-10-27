# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../20261026T2119-c46-hunting-ecology-dthalf/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [128, 128]; wall 874s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out collective/contrib/c53-rev-hd/dthalf --seeds 4 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1426, 1.2176], min area 6 px

## Measurements
- components: final 28, mean 21.5, max 34; occupancy final 0.07
- tracks: 90; persistent (alive >= 50% of run): 4; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 28, 21], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 13, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 63
- channel total drift (end/start - 1): [-0.1571, None, -0.468, -0.5979]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 40: holes 0, rim-vs-core 0.33, rim-vs-outside 0.24, heterogeneity 0.05; core [0.014, 0.85, 0.479, 0.011] rim [0.028, 0.525, 0.476, 0.022]
  - track 36 at frame 79: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.05; core [0.011, 0.89, 0.495, 0.009] rim [0.023, 0.553, 0.491, 0.018]
  - track 40 at frame 91: holes 0, rim-vs-core 0.34, rim-vs-outside 0.28, heterogeneity 0.05; core [0.021, 0.872, 0.474, 0.018] rim [0.035, 0.528, 0.471, 0.029]
  - track 41 at frame 78: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.04; core [0.024, 0.847, 0.513, 0.023] rim [0.033, 0.579, 0.51, 0.03]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 125 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 3.45 (aggregate of 125 individuals; 7/125 membrane-like individually; rim level 0.308)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 10.4 (aggregate of 125 individuals; 1/125 membrane-like individually; rim level 0.5)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.94 (aggregate of 125 individuals; 0/125 membrane-like individually; rim level 0.383)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 3.97 (aggregate of 125 individuals; 6/125 membrane-like individually; rim level 0.31)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=4000, R_eq 3.04): none; #36 (t=7900, R_eq 2.88): none; #40 (t=9100, R_eq 2.88): none; #41 (t=7800, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 8.3, max 19; tracks 100, persistent 0; splits 17, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 4
- species `predator` (channels ['predator b'], own threshold): components final 22, mean 15.6, max 26; tracks 85, persistent 0; splits 11, persistent splits 3 (K=5), max generation 1, merges 1, merge/split 0.091; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 125 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
