# Evidence pack: flow-lenia-digestion-ecology (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 630s; status ok
- command: `python -m labkit.run /tmp/claude-0/ar/world.py --out /tmp/claude-0/ar/rep6/seed1 --seeds 1 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0016, 2.2202], min area 6 px

## Measurements
- components: final 29, mean 30.4, max 98; occupancy final 0.13
- tracks: 2538; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 10, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 31, 29], H1 [18, 4, 0]
- motion: 184 long-lived tracks moved >= 1 body length; max speed 0.934/time; max body lengths 19.3
- replication (lineage window K = 20 frames = time 100, default): splits 801, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 851, merge/split ratio 1.06, nucleations 221
- channel total drift (end/start - 1): [-0.2154, None, -0.0711, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 706 at frame 141: holes 0, rim-vs-core 0.49, rim-vs-outside 0.04, heterogeneity 0.08; core [0.004, 0.531, 0.947, 0.049] rim [0.005, 0.038, 0.946, 0.028]
  - track 409 at frame 91: holes 0, rim-vs-core 0.55, rim-vs-outside 0.06, heterogeneity 0.08; core [0.005, 0.618, 0.894, 0.036] rim [0.006, 0.063, 0.894, 0.022]
  - track 883 at frame 182: holes 0, rim-vs-core 0.49, rim-vs-outside 0.07, heterogeneity 0.08; core [0.008, 0.556, 0.904, 0.077] rim [0.011, 0.069, 0.902, 0.046]
  - track 2193 at frame 534: holes 0, rim-vs-core 0.52, rim-vs-outside 0.05, heterogeneity 0.09; core [0.006, 0.575, 0.915, 0.074] rim [0.008, 0.053, 0.913, 0.044]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 165 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.58 (aggregate of 165 individuals; 27/165 membrane-like individually; rim level 0.167)
  - radial predator B: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.937, rim/outside 21.8 (aggregate of 165 individuals; 38/165 membrane-like individually; rim level 0.371)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 0.95 (aggregate of 165 individuals; 0/165 membrane-like individually; rim level 0.77)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.722, rim/outside 3.23 (aggregate of 165 individuals; 3/165 membrane-like individually; rim level 0.0925)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #706 (t=705, R_eq 5.32): none; #409 (t=455, R_eq 3.29): none; #883 (t=910, R_eq 3.87): none; #2193 (t=2670, R_eq 5.7): none
- species `prey` (channels ['prey A'], own threshold): components final 14, mean 13.6, max 52; tracks 728, persistent 0; splits 200, persistent splits 2 (K=20), max generation 2, merges 206, merge/split 1.03; moving tracks 124
- species `predator` (channels ['predator B'], own threshold): components final 19, mean 20.8, max 33; tracks 213, persistent 17; splits 46, persistent splits 3 (K=20), max generation 3, merges 64, merge/split 1.39; moving tracks 57

## Warnings
- radial: 1 of 165 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
