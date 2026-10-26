# Evidence pack: driven-condensate-prey-predator (seed 2)

- world: `../../world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1186s; status ok
- command: `python -m labkit.run collective/work_c46/world3.py --out collective/work_c46/lk/np256_s2 --seeds 2 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.50 of robust range [0.12, 0.8758], min area 6 px

## Measurements
- components: final 77, mean 56.6, max 77; occupancy final 0.15
- tracks: 97; persistent (alive >= 50% of run): 57; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [90, 82, 76], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000962/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 20, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 57
- channel total drift (end/start - 1): [0.0, None, -0.5456, -0.5157]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.32, rim-vs-outside 0.54, heterogeneity 0.08; core [0.955, 0.0, 0.025, 0.895] rim [0.714, 0.0, 0.104, 0.693]
  - track 2 at frame 62: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.07; core [0.916, 0.0, 0.016, 0.811] rim [0.712, 0.0, 0.1, 0.684]
  - track 0 at frame 61: holes 0, rim-vs-core 0.20, rim-vs-outside 0.56, heterogeneity 0.08; core [0.899, 0.0, 0.015, 0.789] rim [0.738, 0.0, 0.085, 0.698]
  - track 57 at frame 101: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.926, 0.0, 0.057, 0.918] rim [0.641, 0.0, 0.138, 0.651]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 369 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 17.5 (aggregate of 369 individuals; 2/369 membrane-like individually; rim level 0.812)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 369 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.16, rim/outside 0.663 (aggregate of 369 individuals; 0/369 membrane-like individually; rim level 0.23)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 17.2 (aggregate of 369 individuals; 3/369 membrane-like individually; rim level 0.784)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 6.1): none; #2 (t=6200, R_eq 7.36): none; #0 (t=6100, R_eq 8.08): none; #57 (t=10100, R_eq 5.73): none
- species `prey` (channels ['prey a'], own threshold): components final 75, mean 57.5, max 75; tracks 94, persistent 57; splits 18, persistent splits 13 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 369 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
