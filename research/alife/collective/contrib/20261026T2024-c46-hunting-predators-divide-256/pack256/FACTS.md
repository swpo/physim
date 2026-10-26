# Evidence pack: driven-condensate-prey-predator (seed 2)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1765s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/c256_s2 --seeds 2 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1421, 1.1691], min area 6 px

## Measurements
- components: final 50, mean 63.1, max 104; occupancy final 0.05
- tracks: 253; persistent (alive >= 50% of run): 11; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 33.14 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 54, 40], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 51, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 151
- channel total drift (end/start - 1): [-0.1012, None, -0.4848, -0.5695]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 96 at frame 84: holes 0, rim-vs-core 0.20, rim-vs-outside 0.47, heterogeneity 0.06; core [0.919, 0.0, 0.002, 0.764] rim [0.743, 0.0, 0.059, 0.677]
  - track 111 at frame 83: holes 0, rim-vs-core 0.25, rim-vs-outside 0.51, heterogeneity 0.07; core [0.946, 0.0, 0.005, 0.827] rim [0.739, 0.0, 0.071, 0.693]
  - track 9 at frame 36: holes 0, rim-vs-core 0.33, rim-vs-outside 0.28, heterogeneity 0.05; core [0.003, 0.922, 0.535, 0.003] rim [0.015, 0.59, 0.532, 0.014]
  - track 200 at frame 108: holes 0, rim-vs-core 0.34, rim-vs-outside 0.27, heterogeneity 0.05; core [0.008, 0.909, 0.533, 0.009] rim [0.021, 0.569, 0.53, 0.019]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 360 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 5.06 (aggregate of 360 individuals; 16/360 membrane-like individually; rim level 0.422)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 8.82 (aggregate of 360 individuals; 3/360 membrane-like individually; rim level 0.411)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.889 (aggregate of 360 individuals; 0/360 membrane-like individually; rim level 0.37)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 5.84 (aggregate of 360 individuals; 16/360 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #96 (t=8400, R_eq 7.88): none; #111 (t=8300, R_eq 7.46): none; #9 (t=3600, R_eq 3.43): none; #200 (t=10800, R_eq 3.04): none
- species `prey` (channels ['prey a'], own threshold): components final 10, mean 33.3, max 61; tracks 308, persistent 4; splits 75, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 21
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 38.8, max 64; tracks 241, persistent 0; splits 44, persistent splits 19 (K=5), max generation 2, merges 2, merge/split 0.045; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 360 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
