# Evidence pack: digestion-food-chain-3 (seed 5)

- world: `../../20261027T0407-c52-third-level-negative/world3.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 101 frames x 500 steps x dt 0.2 = time 10000; grid [128, 128]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0407-c52-third-level-negative/world3.py --out collective/contrib/20261027T1650-c58-review-third-level/w2 --seeds 5 --size 128 128 --frames 100 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1514, 1.8022], min area 6 px

## Measurements
- components: final 48, mean 44.3, max 52; occupancy final 0.20
- tracks: 194; persistent (alive >= 50% of run): 27; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [51, 48, 43], H1 [0, 0, 0]
- motion: 61 long-lived tracks moved >= 1 body length; max speed 0.00794/time; max body lengths 6.8
- replication (lineage window K = 20 frames = time 2000, default): splits 34, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 43, merge/split ratio 1.26, nucleations 84
- channel total drift (end/start - 1): [-0.0546, None, -0.6201, -0.6074, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 52: holes 0, rim-vs-core 0.34, rim-vs-outside 0.13, heterogeneity 0.10; core [0.606, 0.09, 0.108, 0.642, 0.012, 0.0, 0.0] rim [0.376, 0.127, 0.141, 0.392, 0.014, 0.0, 0.0]
  - track 23 at frame 52: holes 0, rim-vs-core 0.34, rim-vs-outside 0.13, heterogeneity 0.15; core [0.422, 0.417, 0.127, 0.444, 0.213, 0.0, 0.0] rim [0.335, 0.156, 0.146, 0.344, 0.048, 0.0, 0.0]
  - track 37 at frame 55: holes 0, rim-vs-core 0.48, rim-vs-outside 0.14, heterogeneity 0.18; core [0.412, 0.5, 0.153, 0.465, 0.377, 0.0, 0.0] rim [0.33, 0.156, 0.176, 0.361, 0.071, 0.0, 0.0]
  - track 67 at frame 69: holes 0, rim-vs-core 0.49, rim-vs-outside 0.16, heterogeneity 0.19; core [0.512, 0.444, 0.123, 0.563, 0.392, 0.0, 0.0] rim [0.362, 0.138, 0.156, 0.388, 0.08, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 275 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 3.83 (aggregate of 275 individuals; 31/275 membrane-like individually; rim level 0.466)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.346, rim/outside 5.04 (aggregate of 275 individuals; 7/275 membrane-like individually; rim level 0.211)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.853 (aggregate of 275 individuals; 0/275 membrane-like individually; rim level 0.169)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 3.91 (aggregate of 275 individuals; 23/275 membrane-like individually; rim level 0.483)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.291, rim/outside 11.2 (aggregate of 275 individuals; 9/275 membrane-like individually; rim level 0.135)
  - radial top c: flat profile (no radial structure; level 0; aggregate of 275 individuals)
  - radial top product s2: flat profile (no radial structure; level 0; aggregate of 275 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=5200, R_eq 3.91): none; #23 (t=5200, R_eq 4.92): none; #37 (t=5500, R_eq 4.69): none; #67 (t=6900, R_eq 4.69): none
- species `prey` (channels ['prey a'], own threshold): components final 48, mean 44.0, max 51; tracks 177, persistent 25; splits 36, persistent splits 13 (K=20), max generation 4, merges 12, merge/split 0.333; moving tracks 71
- species `predator` (channels ['predator b'], own threshold): components final 47, mean 34.5, max 50; tracks 141, persistent 18; splits 17, persistent splits 9 (K=20), max generation 2, merges 4, merge/split 0.235; moving tracks 65
- species `top` (channels ['top c'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 275 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
