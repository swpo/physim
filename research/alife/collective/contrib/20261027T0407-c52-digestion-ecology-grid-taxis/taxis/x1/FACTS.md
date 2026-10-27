# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 215s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/lks/x1 --seeds 0 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1508, 1.7454], min area 6 px

## Measurements
- components: final 28, mean 33.3, max 41; occupancy final 0.23
- tracks: 81; persistent (alive >= 50% of run): 27; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 43.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 27, 15], H1 [0, 0, 0]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.00686/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 2000, default): splits 18, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.167, nucleations 42
- channel total drift (end/start - 1): [-0.0216, None, -0.6154, -0.6048, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 42: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.16; core [0.799, 0.166, 0.109, 0.812, 0.135] rim [0.499, 0.104, 0.16, 0.514, 0.034]
  - track 28 at frame 43: holes 0, rim-vs-core 0.32, rim-vs-outside 0.43, heterogeneity 0.06; core [0.854, 0.074, 0.015, 0.68, 0.026] rim [0.585, 0.063, 0.096, 0.517, 0.012]
  - track 33 at frame 45: holes 0, rim-vs-core 0.37, rim-vs-outside 0.44, heterogeneity 0.07; core [0.874, 0.084, 0.017, 0.713, 0.035] rim [0.581, 0.074, 0.092, 0.507, 0.016]
  - track 41 at frame 61: holes 0, rim-vs-core 0.49, rim-vs-outside 0.17, heterogeneity 0.24; core [0.362, 0.573, 0.289, 0.446, 0.399] rim [0.29, 0.207, 0.303, 0.354, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 207 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 6.97 (aggregate of 207 individuals; 30/207 membrane-like individually; rim level 0.549)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.454, rim/outside 2.83 (aggregate of 207 individuals; 4/207 membrane-like individually; rim level 0.202)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.78, rim/outside 0.845 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.239)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 6.58 (aggregate of 207 individuals; 22/207 membrane-like individually; rim level 0.544)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.394, rim/outside 10.2 (aggregate of 207 individuals; 7/207 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=4200, R_eq 5.05): none; #28 (t=4300, R_eq 8.7): none; #33 (t=4500, R_eq 7.94): none; #41 (t=6100, R_eq 4.15): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 32.5, max 40; tracks 91, persistent 18; splits 22, persistent splits 10 (K=20), max generation 2, merges 1, merge/split 0.045; moving tracks 29
- species `predator` (channels ['predator b'], own threshold): components final 16, mean 17.4, max 34; tracks 67, persistent 1; splits 9, persistent splits 5 (K=20), max generation 1, merges 0, merge/split 0; moving tracks 30

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 207 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
