# Evidence pack: driven-condensate-prey-predator (seed 1)

- world: `../../world3_dthalf.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [128, 128]; wall 739s; status ok
- command: `python -m labkit.run collective/work_c46/world3_dthalf.py --out collective/work_c46/lk/dthalf_s1 --seeds 1 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.36 of robust range [0.1354, 1.1484], min area 6 px

## Measurements
- components: final 13, mean 13.5, max 21; occupancy final 0.10
- tracks: 49; persistent (alive >= 50% of run): 6; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 48.40 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 16, 11], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 9, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 31
- channel total drift (end/start - 1): [-0.1645, None, -0.4415, -0.6008]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 75: holes 0, rim-vs-core 0.10, rim-vs-outside 0.62, heterogeneity 0.07; core [0.817, 0.0, 0.002, 0.643] rim [0.762, 0.0, 0.07, 0.695]
  - track 15 at frame 81: holes 0, rim-vs-core 0.20, rim-vs-outside 0.51, heterogeneity 0.07; core [0.908, 0.0, 0.012, 0.778] rim [0.738, 0.0, 0.094, 0.704]
  - track 29 at frame 87: holes 0, rim-vs-core 0.16, rim-vs-outside 0.64, heterogeneity 0.07; core [0.949, 0.0, 0.017, 0.853] rim [0.822, 0.0, 0.07, 0.772]
  - track 13 at frame 44: holes 0, rim-vs-core 0.33, rim-vs-outside 0.29, heterogeneity 0.05; core [0.014, 0.939, 0.514, 0.014] rim [0.024, 0.614, 0.513, 0.021]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 7 (aggregate of 79 individuals; 7/79 membrane-like individually; rim level 0.565)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 7.35 (aggregate of 79 individuals; 4/79 membrane-like individually; rim level 0.262)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.83, rim/outside 0.834 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.339)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 7.99 (aggregate of 79 individuals; 8/79 membrane-like individually; rim level 0.552)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=7500, R_eq 10.34): ['product p']; #15 (t=8100, R_eq 8.21): none; #29 (t=8700, R_eq 7.27): none; #13 (t=4400, R_eq 2.52): none
- species `prey` (channels ['prey a'], own threshold): components final 7, mean 9.4, max 17; tracks 68, persistent 5; splits 19, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 11, mean 6.2, max 16; tracks 47, persistent 0; splits 9, persistent splits 6 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
