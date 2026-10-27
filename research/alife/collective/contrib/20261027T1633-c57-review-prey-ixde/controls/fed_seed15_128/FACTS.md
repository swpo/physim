# Evidence pack: digestion-driven-predators (seed 15)

- world: `../../20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 71 frames x 500 steps x dt 0.2 = time 7000; grid [128, 128]; wall 224s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out collective/contrib/c57-w12/fed128 --seeds 15 --frames 70 --no-movie`
- segmentation: matter > 0.21 of robust range [0.151, 1.809], min area 6 px

## Measurements
- components: final 54, mean 40.8, max 54; occupancy final 0.20
- tracks: 125; persistent (alive >= 50% of run): 32; longest 68 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 49, 46], H1 [1, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.00811/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 21, merge/split ratio 1.05, nucleations 65
- channel total drift (end/start - 1): [-0.0584, None, -0.6153, -0.6056, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 37: holes 0, rim-vs-core 0.43, rim-vs-outside 0.13, heterogeneity 0.23; core [0.334, 0.525, 0.185, 0.376, 0.312] rim [0.279, 0.174, 0.199, 0.305, 0.073]
  - track 11 at frame 37: holes 0, rim-vs-core 0.49, rim-vs-outside 0.15, heterogeneity 0.25; core [0.409, 0.511, 0.159, 0.458, 0.388] rim [0.327, 0.157, 0.18, 0.354, 0.079]
  - track 19 at frame 37: holes 0, rim-vs-core 0.53, rim-vs-outside 0.18, heterogeneity 0.24; core [0.351, 0.614, 0.198, 0.412, 0.432] rim [0.298, 0.2, 0.211, 0.34, 0.108]
  - track 49 at frame 52: holes 0, rim-vs-core 0.31, rim-vs-outside 0.11, heterogeneity 0.19; core [0.367, 0.428, 0.148, 0.386, 0.184] rim [0.32, 0.161, 0.16, 0.328, 0.047]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 269 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial prey a: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 4.17 (aggregate of 269 individuals; 33/269 membrane-like individually; rim level 0.476)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.35, rim/outside 5.16 (aggregate of 269 individuals; 3/269 membrane-like individually; rim level 0.233)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.849 (aggregate of 269 individuals; 0/269 membrane-like individually; rim level 0.186)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 4.24 (aggregate of 269 individuals; 19/269 membrane-like individually; rim level 0.503)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.337, rim/outside 14.7 (aggregate of 269 individuals; 4/269 membrane-like individually; rim level 0.185)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=3700, R_eq 4.98): ['prey a']; #11 (t=3700, R_eq 4.79): none; #19 (t=3700, R_eq 4.33): none; #49 (t=5200, R_eq 4.55): none
- species `prey` (channels ['prey a'], own threshold): components final 49, mean 41.5, max 50; tracks 122, persistent 32; splits 21, persistent splits 8 (K=20), max generation 1, merges 8, merge/split 0.381; moving tracks 51
- species `predator` (channels ['predator b'], own threshold): components final 49, mean 29.4, max 49; tracks 100, persistent 20; splits 12, persistent splits 7 (K=20), max generation 1, merges 4, merge/split 0.333; moving tracks 52

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 269 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
