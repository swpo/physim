# Evidence pack: digestion-driven-predators (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [128, 128]; wall 407s; status ok
- command: `python -m labkit.run c52work/world.py --out c52work/pack128b/seed2 --seeds 2 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1644, 1.7894], min area 6 px

## Measurements
- components: final 46, mean 42.9, max 51; occupancy final 0.21
- tracks: 198; persistent (alive >= 50% of run): 21; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 47, 40], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.00791/time; max body lengths 6.9
- replication (lineage window K = 20 frames = time 2000, default): splits 41, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 40, merge/split ratio 0.976, nucleations 76
- channel total drift (end/start - 1): [-0.048, None, -0.6217, -0.6067, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 63: holes 0, rim-vs-core 0.42, rim-vs-outside 0.17, heterogeneity 0.25; core [0.468, 0.44, 0.159, 0.52, 0.298] rim [0.331, 0.163, 0.184, 0.364, 0.067]
  - track 23 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 0.17, heterogeneity 0.24; core [0.382, 0.544, 0.197, 0.445, 0.36] rim [0.314, 0.177, 0.21, 0.357, 0.093]
  - track 4 at frame 57: holes 0, rim-vs-core 0.42, rim-vs-outside 0.16, heterogeneity 0.23; core [0.557, 0.362, 0.096, 0.575, 0.285] rim [0.374, 0.131, 0.132, 0.379, 0.059]
  - track 120 at frame 94: holes 0, rim-vs-core 0.48, rim-vs-outside 0.19, heterogeneity 0.25; core [0.479, 0.497, 0.162, 0.545, 0.393] rim [0.349, 0.175, 0.185, 0.391, 0.095]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 280 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 3.87 (aggregate of 280 individuals; 40/280 membrane-like individually; rim level 0.452)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.362, rim/outside 6.23 (aggregate of 280 individuals; 4/280 membrane-like individually; rim level 0.235)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.4, rim/outside 0.868 (aggregate of 280 individuals; 0/280 membrane-like individually; rim level 0.182)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.941, rim/outside 3.93 (aggregate of 280 individuals; 24/280 membrane-like individually; rim level 0.467)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.297, rim/outside 11.7 (aggregate of 280 individuals; 3/280 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=6300, R_eq 4.62): none; #23 (t=6300, R_eq 4.18): none; #4 (t=5700, R_eq 5.17): none; #120 (t=9400, R_eq 4.26): none
- species `prey` (channels ['prey a'], own threshold): components final 47, mean 43.0, max 50; tracks 191, persistent 22; splits 44, persistent splits 17 (K=20), max generation 3, merges 16, merge/split 0.364; moving tracks 79
- species `predator` (channels ['predator b'], own threshold): components final 46, mean 35.9, max 48; tracks 138, persistent 23; splits 17, persistent splits 11 (K=20), max generation 2, merges 1, merge/split 0.059; moving tracks 76

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 280 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
