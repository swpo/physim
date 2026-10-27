# Evidence pack: digestion-driven-predators (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [192, 192]; wall 974s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/grid192/seed0 --seeds 0 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1597, 1.8002], min area 6 px

## Measurements
- components: final 53, mean 43.2, max 53; occupancy final 0.20
- tracks: 238; persistent (alive >= 50% of run): 13; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 29.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 48, 45], H1 [0, 0, 0]
- motion: 79 long-lived tracks moved >= 1 body length; max speed 0.0119/time; max body lengths 8.0
- replication (lineage window K = 20 frames = time 2000, default): splits 49, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 52, merge/split ratio 1.06, nucleations 89
- channel total drift (end/start - 1): [-0.052, None, -0.616, -0.6027, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.46, rim-vs-outside 0.23, heterogeneity 0.25; core [0.485, 0.513, 0.125, 0.53, 0.392] rim [0.365, 0.202, 0.151, 0.389, 0.103]
  - track 33 at frame 65: holes 0, rim-vs-core 0.52, rim-vs-outside 0.22, heterogeneity 0.25; core [0.432, 0.576, 0.145, 0.478, 0.453] rim [0.354, 0.2, 0.162, 0.379, 0.11]
  - track 11 at frame 48: holes 0, rim-vs-core 0.50, rim-vs-outside 0.24, heterogeneity 0.25; core [0.438, 0.574, 0.149, 0.482, 0.439] rim [0.329, 0.231, 0.172, 0.351, 0.119]
  - track 65 at frame 78: holes 0, rim-vs-core 0.53, rim-vs-outside 0.25, heterogeneity 0.25; core [0.476, 0.574, 0.15, 0.542, 0.473] rim [0.362, 0.215, 0.171, 0.404, 0.126]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 278 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 3.93 (aggregate of 278 individuals; 24/278 membrane-like individually; rim level 0.455)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.349, rim/outside 5.66 (aggregate of 278 individuals; 0/278 membrane-like individually; rim level 0.232)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.85 (aggregate of 278 individuals; 0/278 membrane-like individually; rim level 0.169)
  - radial product p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 3.97 (aggregate of 278 individuals; 17/278 membrane-like individually; rim level 0.47)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.303, rim/outside 12 (aggregate of 278 individuals; 5/278 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 6.98): none; #33 (t=6500, R_eq 6.68): none; #11 (t=4800, R_eq 6.75): none; #65 (t=7800, R_eq 6.31): none
- species `prey` (channels ['prey a'], own threshold): components final 49, mean 43.3, max 52; tracks 207, persistent 18; splits 43, persistent splits 18 (K=20), max generation 4, merges 19, merge/split 0.442; moving tracks 77
- species `predator` (channels ['predator b'], own threshold): components final 46, mean 36.3, max 49; tracks 159, persistent 17; splits 25, persistent splits 15 (K=20), max generation 4, merges 9, merge/split 0.36; moving tracks 74

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 278 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
