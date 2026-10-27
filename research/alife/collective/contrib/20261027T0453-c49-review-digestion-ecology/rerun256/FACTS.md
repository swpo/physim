# Evidence pack: digestion-driven-predators (seed 4)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1950s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c49rev10/rerun256 --seeds 4 --size 256 256 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1577, 1.7931], min area 6 px

## Measurements
- components: final 195, mean 177.0, max 200; occupancy final 0.21
- tracks: 787; persistent (alive >= 50% of run): 85; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [203, 191, 166], H1 [0, 0, 0]
- motion: 321 long-lived tracks moved >= 1 body length; max speed 0.00813/time; max body lengths 9.1
- replication (lineage window K = 20 frames = time 2000, default): splits 142, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 3, merges 169, merge/split ratio 1.19, nucleations 337
- channel total drift (end/start - 1): [-0.0523, None, -0.6156, -0.6026, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.18, heterogeneity 0.25; core [0.426, 0.503, 0.148, 0.473, 0.346] rim [0.337, 0.189, 0.166, 0.365, 0.086]
  - track 37 at frame 62: holes 0, rim-vs-core 0.51, rim-vs-outside 0.16, heterogeneity 0.26; core [0.469, 0.495, 0.136, 0.519, 0.402] rim [0.356, 0.142, 0.162, 0.383, 0.081]
  - track 47 at frame 63: holes 0, rim-vs-core 0.48, rim-vs-outside 0.17, heterogeneity 0.26; core [0.551, 0.399, 0.105, 0.589, 0.37] rim [0.37, 0.141, 0.143, 0.387, 0.072]
  - track 541 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.12, heterogeneity 0.25; core [0.368, 0.525, 0.163, 0.414, 0.354] rim [0.332, 0.151, 0.176, 0.361, 0.073]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1129 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.976, rim/outside 3.89 (aggregate of 1129 individuals; 159/1129 membrane-like individually; rim level 0.455)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.351, rim/outside 5.96 (aggregate of 1129 individuals; 15/1129 membrane-like individually; rim level 0.233)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.853 (aggregate of 1129 individuals; 0/1129 membrane-like individually; rim level 0.171)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 3.95 (aggregate of 1129 individuals; 99/1129 membrane-like individually; rim level 0.47)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.294, rim/outside 11.9 (aggregate of 1129 individuals; 14/1129 membrane-like individually; rim level 0.142)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=6200, R_eq 4.48): none; #37 (t=6200, R_eq 4.55): none; #47 (t=6300, R_eq 4.82): none; #541 (t=10100, R_eq 4.82): none
- species `prey` (channels ['prey a'], own threshold): components final 191, mean 175.3, max 199; tracks 727, persistent 95; splits 135, persistent splits 62 (K=20), max generation 4, merges 65, merge/split 0.481; moving tracks 325
- species `predator` (channels ['predator b'], own threshold): components final 189, mean 146.8, max 196; tracks 591, persistent 87; splits 68, persistent splits 40 (K=20), max generation 3, merges 23, merge/split 0.338; moving tracks 304

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 1129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
