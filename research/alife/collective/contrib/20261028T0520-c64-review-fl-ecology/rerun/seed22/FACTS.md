# Evidence pack: flow-lenia-digestion-ecology (seed 22)

- world: `../../../20261028T0344-c62-flow-lenia-ecology-s-claim/world.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [160, 160]; wall 608s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py --out collective/contrib/20261028T0520-c64-review-fl-ecology/rerun/seed22 --seeds 22 --size 160 160 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0019, 2.161], min area 6 px

## Measurements
- components: final 31, mean 30.6, max 92; occupancy final 0.13
- tracks: 4092; persistent (alive >= 50% of run): 0; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 36, 28], H1 [7, 1, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.891/time; max body lengths 20.3
- replication (lineage window K = 20 frames = time 100, default): splits 1408, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1422, merge/split ratio 1.01, nucleations 182
- channel total drift (end/start - 1): [-0.3244, None, -0.0644, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 442 at frame 86: holes 0, rim-vs-core 0.49, rim-vs-outside 0.08, heterogeneity 0.08; core [0.002, 0.592, 0.954, 0.027] rim [0.003, 0.099, 0.952, 0.017]
  - track 373 at frame 71: holes 0, rim-vs-core 0.43, rim-vs-outside 0.11, heterogeneity 0.09; core [0.006, 0.541, 0.919, 0.082] rim [0.008, 0.116, 0.915, 0.053]
  - track 2225 at frame 358: holes 0, rim-vs-core 0.50, rim-vs-outside 0.05, heterogeneity 0.08; core [0.001, 0.562, 0.84, 0.014] rim [0.001, 0.059, 0.833, 0.01]
  - track 727 at frame 141: holes 0, rim-vs-core 0.55, rim-vs-outside 0.05, heterogeneity 0.10; core [0.008, 0.595, 0.9, 0.116] rim [0.011, 0.051, 0.898, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 7.47 (aggregate of 155 individuals; 27/155 membrane-like individually; rim level 0.178)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 12.8 (aggregate of 155 individuals; 36/155 membrane-like individually; rim level 0.273)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.942 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.765)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 3.49 (aggregate of 155 individuals; 1/155 membrane-like individually; rim level 0.125)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #442 (t=430, R_eq 3.87): none; #373 (t=355, R_eq 4.58): none; #2225 (t=1790, R_eq 3.29): none; #727 (t=705, R_eq 4.33): none
- species `prey` (channels ['prey A'], own threshold): components final 15, mean 14.9, max 51; tracks 861, persistent 0; splits 269, persistent splits 4 (K=20), max generation 3, merges 250, merge/split 0.929; moving tracks 149
- species `predator` (channels ['predator B'], own threshold): components final 31, mean 24.4, max 33; tracks 1987, persistent 0; splits 668, persistent splits 8 (K=20), max generation 4, merges 542, merge/split 0.811; moving tracks 197

## Warnings
- radial: 2 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
