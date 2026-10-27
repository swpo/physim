# Evidence pack: driven-condensate-prey-predator (seed 4)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 2010s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0027-c48-review-hunting/rerun/seed4 --seeds 4 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1448, 1.2113], min area 6 px

## Measurements
- components: final 91, mean 81.3, max 130; occupancy final 0.07
- tracks: 322; persistent (alive >= 50% of run): 29; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 73.43 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [108, 95, 66], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 47, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 227
- channel total drift (end/start - 1): [-0.1399, None, -0.4712, -0.5874]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 65: holes 0, rim-vs-core 0.13, rim-vs-outside 0.45, heterogeneity 0.06; core [0.843, 0.0, 0.001, 0.657] rim [0.723, 0.0, 0.045, 0.64]
  - track 41 at frame 48: holes 0, rim-vs-core 0.34, rim-vs-outside 0.29, heterogeneity 0.05; core [0.012, 0.908, 0.506, 0.011] rim [0.026, 0.565, 0.502, 0.023]
  - track 28 at frame 44: holes 0, rim-vs-core 0.24, rim-vs-outside 0.23, heterogeneity 0.04; core [0.012, 0.813, 0.493, 0.009] rim [0.024, 0.574, 0.488, 0.018]
  - track 221 at frame 97: holes 0, rim-vs-core 0.21, rim-vs-outside 0.25, heterogeneity 0.04; core [0.015, 0.819, 0.541, 0.015] rim [0.021, 0.61, 0.54, 0.019]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 470 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 3.44 (aggregate of 470 individuals; 14/470 membrane-like individually; rim level 0.302)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 10 (aggregate of 470 individuals; 3/470 membrane-like individually; rim level 0.515)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.935 (aggregate of 470 individuals; 0/470 membrane-like individually; rim level 0.404)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.83 (aggregate of 470 individuals; 14/470 membrane-like individually; rim level 0.298)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=6500, R_eq 9.93): none; #41 (t=4800, R_eq 2.99): none; #28 (t=4400, R_eq 3.19): none; #221 (t=9700, R_eq 2.33): none
- species `prey` (channels ['prey a'], own threshold): components final 28, mean 33.4, max 66; tracks 390, persistent 4; splits 76, persistent splits 4 (K=5), max generation 1, merges 1, merge/split 0.013; moving tracks 22
- species `predator` (channels ['predator b'], own threshold): components final 72, mean 57.1, max 83; tracks 298, persistent 1; splits 39, persistent splits 21 (K=5), max generation 2, merges 3, merge/split 0.077; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 470 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
