# Evidence pack: digestion-driven-predators (seed 8)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 279s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/fed128_s8 --seeds 8 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1527, 1.7993], min area 6 px

## Measurements
- components: final 47, mean 39.1, max 51; occupancy final 0.20
- tracks: 155; persistent (alive >= 50% of run): 16; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 45, 39], H1 [0, 0, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.00815/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 34, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 28, merge/split ratio 0.824, nucleations 59
- channel total drift (end/start - 1): [-0.0522, None, -0.6147, -0.603, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 41: holes 0, rim-vs-core 0.44, rim-vs-outside 0.14, heterogeneity 0.26; core [0.395, 0.491, 0.168, 0.444, 0.341] rim [0.32, 0.165, 0.187, 0.348, 0.073]
  - track 15 at frame 43: holes 0, rim-vs-core 0.48, rim-vs-outside 0.17, heterogeneity 0.27; core [0.48, 0.469, 0.138, 0.533, 0.39] rim [0.353, 0.16, 0.166, 0.381, 0.082]
  - track 30 at frame 44: holes 0, rim-vs-core 0.44, rim-vs-outside 0.15, heterogeneity 0.25; core [0.379, 0.505, 0.187, 0.437, 0.326] rim [0.303, 0.168, 0.205, 0.34, 0.072]
  - track 73 at frame 62: holes 0, rim-vs-core 0.47, rim-vs-outside 0.17, heterogeneity 0.27; core [0.525, 0.427, 0.125, 0.578, 0.374] rim [0.378, 0.141, 0.16, 0.407, 0.073]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 253 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.51 (aggregate of 253 individuals; 57/253 membrane-like individually; rim level 0.437)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.365, rim/outside 6.25 (aggregate of 253 individuals; 6/253 membrane-like individually; rim level 0.248)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.863 (aggregate of 253 individuals; 0/253 membrane-like individually; rim level 0.186)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 3.59 (aggregate of 253 individuals; 39/253 membrane-like individually; rim level 0.46)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.321, rim/outside 12.6 (aggregate of 253 individuals; 6/253 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=4100, R_eq 4.89): none; #15 (t=4300, R_eq 4.79): none; #30 (t=4400, R_eq 4.72): none; #73 (t=6200, R_eq 4.98): none
- species `prey` (channels ['prey a'], own threshold): components final 45, mean 39.5, max 47; tracks 134, persistent 27; splits 28, persistent splits 11 (K=20), max generation 2, merges 8, merge/split 0.286; moving tracks 50
- species `predator` (channels ['predator b'], own threshold): components final 45, mean 30.5, max 47; tracks 108, persistent 22; splits 15, persistent splits 7 (K=20), max generation 2, merges 2, merge/split 0.133; moving tracks 49

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 253 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
