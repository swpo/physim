# Evidence pack: digestion-driven-predators (seed 1)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 405s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/pack128/seed1 --seeds 1 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1563, 1.8002], min area 6 px

## Measurements
- components: final 48, mean 42.4, max 51; occupancy final 0.19
- tracks: 151; persistent (alive >= 50% of run): 28; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 45, 42], H1 [0, 0, 0]
- motion: 81 long-lived tracks moved >= 1 body length; max speed 0.00761/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 2000, default): splits 19, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 29, merge/split ratio 1.53, nucleations 83
- channel total drift (end/start - 1): [-0.0498, None, -0.6097, -0.5959, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 62: holes 0, rim-vs-core 0.50, rim-vs-outside 0.14, heterogeneity 0.24; core [0.376, 0.559, 0.156, 0.412, 0.389] rim [0.318, 0.172, 0.172, 0.336, 0.087]
  - track 15 at frame 63: holes 0, rim-vs-core 0.46, rim-vs-outside 0.17, heterogeneity 0.26; core [0.41, 0.519, 0.187, 0.482, 0.36] rim [0.317, 0.185, 0.206, 0.369, 0.085]
  - track 23 at frame 64: holes 0, rim-vs-core 0.52, rim-vs-outside 0.17, heterogeneity 0.26; core [0.439, 0.528, 0.16, 0.508, 0.416] rim [0.34, 0.161, 0.183, 0.383, 0.082]
  - track 126 at frame 110: holes 0, rim-vs-core 0.47, rim-vs-outside 0.17, heterogeneity 0.25; core [0.472, 0.462, 0.132, 0.518, 0.349] rim [0.354, 0.132, 0.154, 0.38, 0.068]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 271 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 4 (aggregate of 271 individuals; 27/271 membrane-like individually; rim level 0.464)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.341, rim/outside 6.2 (aggregate of 271 individuals; 3/271 membrane-like individually; rim level 0.229)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.846 (aggregate of 271 individuals; 0/271 membrane-like individually; rim level 0.174)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 4.09 (aggregate of 271 individuals; 17/271 membrane-like individually; rim level 0.483)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.291, rim/outside 12.6 (aggregate of 271 individuals; 3/271 membrane-like individually; rim level 0.147)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=6200, R_eq 4.51): none; #15 (t=6300, R_eq 4.37): none; #23 (t=6400, R_eq 4.48): none; #126 (t=11000, R_eq 4.37): none
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 41.9, max 49; tracks 161, persistent 25; splits 27, persistent splits 11 (K=20), max generation 2, merges 11, merge/split 0.407; moving tracks 72
- species `predator` (channels ['predator b'], own threshold): components final 41, mean 34.6, max 49; tracks 122, persistent 25; splits 7, persistent splits 5 (K=20), max generation 2, merges 3, merge/split 0.429; moving tracks 74

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 271 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
