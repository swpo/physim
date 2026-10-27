# Evidence pack: digestion-driven-predators (seed 7)

- world: `../../../collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T2103-c46-hunting-ecology-claim; mutation: predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py --out c56work/py/fed128_s7 --seeds 7 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1496, 1.8052], min area 6 px

## Measurements
- components: final 46, mean 40.5, max 49; occupancy final 0.20
- tracks: 135; persistent (alive >= 50% of run): 25; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 44, 37], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.00834/time; max body lengths 5.2
- replication (lineage window K = 20 frames = time 2000, default): splits 19, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 28, merge/split ratio 1.47, nucleations 69
- channel total drift (end/start - 1): [-0.0478, None, -0.612, -0.5975, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 41: holes 0, rim-vs-core 0.45, rim-vs-outside 0.14, heterogeneity 0.26; core [0.403, 0.488, 0.165, 0.446, 0.343] rim [0.333, 0.154, 0.187, 0.358, 0.065]
  - track 16 at frame 42: holes 0, rim-vs-core 0.45, rim-vs-outside 0.13, heterogeneity 0.26; core [0.435, 0.486, 0.167, 0.487, 0.35] rim [0.334, 0.173, 0.189, 0.368, 0.075]
  - track 11 at frame 42: holes 0, rim-vs-core 0.52, rim-vs-outside 0.18, heterogeneity 0.23; core [0.429, 0.531, 0.162, 0.467, 0.411] rim [0.245, 0.251, 0.204, 0.258, 0.081]
  - track 61 at frame 57: holes 0, rim-vs-core 0.36, rim-vs-outside 0.11, heterogeneity 0.16; core [0.281, 0.518, 0.201, 0.304, 0.21] rim [0.277, 0.191, 0.207, 0.293, 0.059]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 3.48 (aggregate of 261 individuals; 37/261 membrane-like individually; rim level 0.442)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.379, rim/outside 7.13 (aggregate of 261 individuals; 5/261 membrane-like individually; rim level 0.257)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.868 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.192)
  - radial product p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.959, rim/outside 3.55 (aggregate of 261 individuals; 24/261 membrane-like individually; rim level 0.461)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.312, rim/outside 12.9 (aggregate of 261 individuals; 4/261 membrane-like individually; rim level 0.151)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=4100, R_eq 5.08): none; #16 (t=4200, R_eq 4.69): none; #11 (t=4200, R_eq 4.62): none; #61 (t=5700, R_eq 4.41): none
- species `prey` (channels ['prey a'], own threshold): components final 45, mean 39.9, max 48; tracks 129, persistent 27; splits 18, persistent splits 4 (K=20), max generation 2, merges 7, merge/split 0.389; moving tracks 53
- species `predator` (channels ['predator b'], own threshold): components final 44, mean 30.2, max 46; tracks 107, persistent 21; splits 8, persistent splits 4 (K=20), max generation 2, merges 3, merge/split 0.375; moving tracks 47

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 261 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
