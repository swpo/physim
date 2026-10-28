# Evidence pack: digestion-predators-half-taxis (seed 31)

- world: `../../20261027T2013-c60-halftaxis-ecology/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1739s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2013-c60-halftaxis-ecology/world.py --seeds 31 --size 256 256 --frames 120 --no-movie --lineage-k 20 --out collective/contrib/20261027T2330-c61-review-halftaxis/rerun`
- segmentation: matter > 0.21 of robust range [0.1582, 1.8147], min area 6 px

## Measurements
- components: final 172, mean 161.8, max 187; occupancy final 0.21
- tracks: 758; persistent (alive >= 50% of run): 57; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [181, 167, 143], H1 [0, 0, 0]
- motion: 272 long-lived tracks moved >= 1 body length; max speed 0.00786/time; max body lengths 7.6
- replication (lineage window K = 20 frames = time 2000, --lineage-k): splits 199, persistent splits 82 (0 more failed only because the siblings re-merged within K), max generation 4, merges 111, merge/split ratio 0.558, nucleations 255
- channel total drift (end/start - 1): [-0.0465, None, -0.6121, -0.5998, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.14, heterogeneity 0.24; core [0.361, 0.513, 0.209, 0.417, 0.313] rim [0.295, 0.177, 0.226, 0.332, 0.072]
  - track 104 at frame 64: holes 0, rim-vs-core 0.51, rim-vs-outside 0.21, heterogeneity 0.26; core [0.568, 0.419, 0.136, 0.617, 0.431] rim [0.408, 0.12, 0.164, 0.435, 0.099]
  - track 15 at frame 57: holes 0, rim-vs-core 0.55, rim-vs-outside 0.18, heterogeneity 0.25; core [0.568, 0.421, 0.115, 0.594, 0.447] rim [0.391, 0.111, 0.149, 0.397, 0.083]
  - track 589 at frame 106: holes 0, rim-vs-core 0.48, rim-vs-outside 0.23, heterogeneity 0.25; core [0.379, 0.534, 0.193, 0.43, 0.36] rim [0.38, 0.149, 0.198, 0.42, 0.073]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1023 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 4.67 (aggregate of 1023 individuals; 174/1023 membrane-like individually; rim level 0.466)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.352, rim/outside 4.78 (aggregate of 1023 individuals; 16/1023 membrane-like individually; rim level 0.219)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.857 (aggregate of 1023 individuals; 0/1023 membrane-like individually; rim level 0.2)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 4.66 (aggregate of 1023 individuals; 130/1023 membrane-like individually; rim level 0.476)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.302, rim/outside 10.8 (aggregate of 1023 individuals; 28/1023 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=6200, R_eq 4.58): none; #104 (t=6400, R_eq 4.37): none; #15 (t=5700, R_eq 4.58): none; #589 (t=10600, R_eq 4.69): none
- species `prey` (channels ['prey a'], own threshold): components final 165, mean 160.9, max 182; tracks 761, persistent 61; splits 213, persistent splits 92 (K=20), max generation 5, merges 55, merge/split 0.258; moving tracks 289
- species `predator` (channels ['predator b'], own threshold): components final 162, mean 132.1, max 178; tracks 606, persistent 44; splits 124, persistent splits 77 (K=20), max generation 5, merges 12, merge/split 0.097; moving tracks 295

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 1023 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
