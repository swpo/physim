# Evidence pack: flow-lenia-digestion-ecology (seed 21)

- world: `../ctrl_world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 401 frames x 25 steps x dt 0.2 = time 2000; grid [160, 160]; wall 416s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0520-c63-review-flow-lenia-ecology/ctrl_world.py --out collective/contrib/20261028T0520-c63-review-flow-lenia-ecology/ctrl_bodies --seeds 21 --size 160 160 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0013, 2.021], min area 6 px

## Measurements
- components: final 21, mean 24.6, max 91; occupancy final 0.16
- tracks: 2189; persistent (alive >= 50% of run): 0; longest 55 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 19, 10], H1 [6, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.927/time; max body lengths 12.5
- replication (lineage window K = 20 frames = time 100, default): splits 715, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 673, merge/split ratio 0.941, nucleations 201
- channel total drift (end/start - 1): [-0.1702, None, -0.0773, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 459 at frame 87: holes 0, rim-vs-core 0.38, rim-vs-outside 0.24, heterogeneity 0.12; core [0.012, 0.597, 0.867, 0.256] rim [0.015, 0.231, 0.867, 0.171]
  - track 58 at frame 37: holes 0, rim-vs-core 0.41, rim-vs-outside 0.12, heterogeneity 0.08; core [0.507, 0.001, 0.446, 0.007] rim [0.122, 0.001, 0.574, 0.007]
  - track 355 at frame 71: holes 0, rim-vs-core 0.53, rim-vs-outside 0.10, heterogeneity 0.10; core [0.003, 0.63, 0.896, 0.047] rim [0.004, 0.103, 0.877, 0.031]
  - track 412 at frame 74: holes 0, rim-vs-core 0.69, rim-vs-outside 0.08, heterogeneity 0.10; core [0.008, 0.77, 0.872, 0.126] rim [0.011, 0.081, 0.866, 0.077]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 8.11 (aggregate of 141 individuals; 21/141 membrane-like individually; rim level 0.211)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 7.12 (aggregate of 141 individuals; 31/141 membrane-like individually; rim level 0.243)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 0.944 (aggregate of 141 individuals; 1/141 membrane-like individually; rim level 0.758)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.731, rim/outside 2.88 (aggregate of 141 individuals; 3/141 membrane-like individually; rim level 0.0952)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #459 (t=435, R_eq 6.68): ['predator B']; #58 (t=185, R_eq 3.09): none; #355 (t=355, R_eq 4.37): ['predator B']; #412 (t=370, R_eq 4.07): none
- species `prey` (channels ['prey A'], own threshold): components final 16, mean 16.2, max 54; tracks 575, persistent 0; splits 167, persistent splits 4 (K=20), max generation 3, merges 159, merge/split 0.952; moving tracks 104
- species `predator` (channels ['predator B'], own threshold): components final 10, mean 11.9, max 28; tracks 660, persistent 0; splits 157, persistent splits 2 (K=20), max generation 1, merges 147, merge/split 0.936; moving tracks 44

## Warnings
- radial: 5 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
