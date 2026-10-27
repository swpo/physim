# Evidence pack: digestion-predators-half-taxis (seed 7)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1923s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2013-c60-halftaxis-ecology/world.py --out collective/contrib/20261027T2013-c60-halftaxis-ecology/pack/seed7 --seeds 7 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1564, 1.815], min area 6 px

## Measurements
- components: final 174, mean 168.9, max 195; occupancy final 0.21
- tracks: 712; persistent (alive >= 50% of run): 69; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [185, 174, 146], H1 [0, 0, 0]
- motion: 283 long-lived tracks moved >= 1 body length; max speed 0.00796/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 2000, default): splits 165, persistent splits 77 (0 more failed only because the siblings re-merged within K), max generation 5, merges 124, merge/split ratio 0.752, nucleations 260
- channel total drift (end/start - 1): [-0.0503, None, -0.6137, -0.6, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 59 at frame 63: holes 0, rim-vs-core 0.49, rim-vs-outside 0.17, heterogeneity 0.26; core [0.394, 0.545, 0.19, 0.454, 0.385] rim [0.319, 0.172, 0.208, 0.358, 0.088]
  - track 86 at frame 63: holes 0, rim-vs-core 0.50, rim-vs-outside 0.18, heterogeneity 0.26; core [0.493, 0.454, 0.156, 0.555, 0.39] rim [0.345, 0.144, 0.185, 0.381, 0.079]
  - track 111 at frame 64: holes 0, rim-vs-core 0.46, rim-vs-outside 0.16, heterogeneity 0.26; core [0.442, 0.47, 0.182, 0.509, 0.352] rim [0.316, 0.17, 0.211, 0.359, 0.069]
  - track 555 at frame 107: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.26; core [0.436, 0.483, 0.171, 0.492, 0.366] rim [0.322, 0.182, 0.195, 0.356, 0.083]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1071 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 4.57 (aggregate of 1071 individuals; 158/1071 membrane-like individually; rim level 0.468)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.344, rim/outside 4.91 (aggregate of 1071 individuals; 11/1071 membrane-like individually; rim level 0.218)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.85 (aggregate of 1071 individuals; 0/1071 membrane-like individually; rim level 0.187)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 4.61 (aggregate of 1071 individuals; 113/1071 membrane-like individually; rim level 0.481)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.288, rim/outside 11.2 (aggregate of 1071 individuals; 28/1071 membrane-like individually; rim level 0.137)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #59 (t=6300, R_eq 4.48): none; #86 (t=6300, R_eq 4.55): none; #111 (t=6400, R_eq 4.58): none; #555 (t=10700, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 169, mean 169.4, max 190; tracks 749, persistent 70; splits 191, persistent splits 94 (K=20), max generation 5, merges 59, merge/split 0.309; moving tracks 324
- species `predator` (channels ['predator b'], own threshold): components final 170, mean 138.2, max 183; tracks 601, persistent 56; splits 102, persistent splits 69 (K=20), max generation 5, merges 19, merge/split 0.186; moving tracks 315

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 1071 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
