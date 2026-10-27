# Evidence pack: digestion-driven-predators (seed 5)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 237s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/20261027T0545-c51-review-digestion/dfork128_s5 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0176, 1.7642], min area 6 px

## Measurements
- components: final 0, mean 33.2, max 52; occupancy final 0.00
- tracks: 106; persistent (alive >= 50% of run): 23; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 12, 3], H1 [10, 1, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.00796/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 2000, default): splits 10, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 19, merge/split ratio 1.9, nucleations 67
- channel total drift (end/start - 1): [-0.9999, None, 0.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 33: holes 0, rim-vs-core 0.33, rim-vs-outside 0.13, heterogeneity 0.15; core [0.639, 0.23, 0.096, 0.62, 0.091] rim [0.432, 0.175, 0.134, 0.378, 0.031]
  - track 4 at frame 33: holes 0, rim-vs-core 0.45, rim-vs-outside 0.13, heterogeneity 0.25; core [0.557, 0.453, 0.122, 0.541, 0.362] rim [0.469, 0.15, 0.151, 0.426, 0.06]
  - track 0 at frame 31: holes 0, rim-vs-core 0.44, rim-vs-outside 0.12, heterogeneity 0.25; core [0.539, 0.456, 0.124, 0.514, 0.35] rim [0.457, 0.155, 0.15, 0.407, 0.065]
  - track 58 at frame 49: holes 0, rim-vs-core 0.52, rim-vs-outside 0.17, heterogeneity 0.23; core [0.545, 0.528, 0.168, 0.558, 0.454] rim [0.463, 0.172, 0.188, 0.445, 0.099]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 184 components >= 12 px at frames [13, 27, 40, 53]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 1.98 (aggregate of 184 individuals; 3/184 membrane-like individually; rim level 0.569)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.4, rim/outside 8.15 (aggregate of 184 individuals; 3/184 membrane-like individually; rim level 0.254)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.854 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.17)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 2.55 (aggregate of 184 individuals; 9/184 membrane-like individually; rim level 0.535)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.335, rim/outside 13.1 (aggregate of 184 individuals; 2/184 membrane-like individually; rim level 0.149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=3300, R_eq 5.01): none; #4 (t=3300, R_eq 5.32): none; #0 (t=3100, R_eq 5.41): none; #58 (t=4900, R_eq 4.18): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 33.1, max 53; tracks 240, persistent 7; splits 76, persistent splits 3 (K=20), max generation 1, merges 48, merge/split 0.632; moving tracks 32
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 22.7, max 50; tracks 90, persistent 12; splits 5, persistent splits 3 (K=20), max generation 1, merges 3, merge/split 0.6; moving tracks 40

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
