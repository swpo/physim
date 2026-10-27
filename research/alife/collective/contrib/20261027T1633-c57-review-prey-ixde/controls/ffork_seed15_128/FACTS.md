# Evidence pack: digestion-driven-predators (seed 15)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 225s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-w12/ffork128 --seeds 15 --frames 70 --no-movie`
- segmentation: matter > 0.21 of robust range [0.151, 1.7906], min area 6 px

## Measurements
- components: final 41, mean 40.0, max 51; occupancy final 0.12
- tracks: 101; persistent (alive >= 50% of run): 33; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 43, 31], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.00551/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 17, merge/split ratio 1.21, nucleations 57
- channel total drift (end/start - 1): [-0.0149, None, -1.0, -1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 37: holes 0, rim-vs-core 0.45, rim-vs-outside 0.13, heterogeneity 0.23; core [0.334, 0.537, 0.369, 0.432, 0.336] rim [0.279, 0.178, 0.379, 0.366, 0.079]
  - track 11 at frame 37: holes 0, rim-vs-core 0.50, rim-vs-outside 0.15, heterogeneity 0.25; core [0.409, 0.521, 0.348, 0.506, 0.413] rim [0.327, 0.161, 0.365, 0.411, 0.085]
  - track 18 at frame 37: holes 0, rim-vs-core 0.39, rim-vs-outside 0.20, heterogeneity 0.11; core [0.724, 0.16, 0.282, 0.784, 0.109] rim [0.455, 0.077, 0.314, 0.526, 0.025]
  - track 49 at frame 52: holes 0, rim-vs-core 0.32, rim-vs-outside 0.11, heterogeneity 0.18; core [0.367, 0.439, 0.34, 0.441, 0.2] rim [0.32, 0.165, 0.349, 0.388, 0.051]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 256 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 3.55 (aggregate of 256 individuals; 29/256 membrane-like individually; rim level 0.451)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.386, rim/outside 5.15 (aggregate of 256 individuals; 3/256 membrane-like individually; rim level 0.247)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.929 (aggregate of 256 individuals; 0/256 membrane-like individually; rim level 0.308)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 2.95 (aggregate of 256 individuals; 8/256 membrane-like individually; rim level 0.478)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.367, rim/outside 14.4 (aggregate of 256 individuals; 4/256 membrane-like individually; rim level 0.182)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=3700, R_eq 4.98): ['prey a']; #11 (t=3700, R_eq 4.79): none; #18 (t=3700, R_eq 4.44): none; #49 (t=5200, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 34.8, max 50; tracks 107, persistent 21; splits 19, persistent splits 7 (K=20), max generation 1, merges 6, merge/split 0.316; moving tracks 46
- species `predator` (channels ['predator b'], own threshold): components final 32, mean 28.5, max 48; tracks 86, persistent 19; splits 10, persistent splits 7 (K=20), max generation 1, merges 3, merge/split 0.3; moving tracks 52

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 256 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
