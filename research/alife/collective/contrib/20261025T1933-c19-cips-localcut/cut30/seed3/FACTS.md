# Evidence pack: cips-fuel (seed 3)

- world: `../../../20261025T1845-c23-cips-metabolic-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 251 frames x 100 steps x dt 0.1 = time 2500; grid [256, 256]; wall 279s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1845-c23-cips-metabolic-claim/world.py --out collective/contrib/20261025T1933-c19-cips-localcut/cut30/seed3 --seeds 3 --frames 250 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 0.9986], min area 6 px

## Measurements
- components: final 188, mean 209.0, max 301; occupancy final 0.13
- tracks: 408; persistent (alive >= 50% of run): 209; longest 232 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [192, 190, 188], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00436/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 100, merge/split ratio n/a, nucleations 308
- channel total drift (end/start - 1): [0.0, -0.2274, 0.1051]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 134: holes 0, rim-vs-core 0.31, rim-vs-outside 0.49, heterogeneity 0.10; core [0.969, 0.851, 0.484] rim [0.731, 0.677, 0.57]
  - track 1 at frame 134: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.09; core [0.976, 0.879, 0.445] rim [0.761, 0.698, 0.537]
  - track 2 at frame 134: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.08; core [0.98, 0.886, 0.448] rim [0.792, 0.71, 0.538]
  - track 5 at frame 137: holes 0, rim-vs-core 0.28, rim-vs-outside 0.49, heterogeneity 0.09; core [0.972, 0.851, 0.465] rim [0.76, 0.688, 0.546]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1339 components >= 12 px at frames [42, 84, 126, 166, 208, 250]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 41.5 (aggregate of 1339 individuals; 0/1339 membrane-like individually; rim level 0.932)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 3.72 (aggregate of 1339 individuals; 0/1339 membrane-like individually; rim level 0.813)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.61, rim/outside 0.824 (aggregate of 1339 individuals; 0/1339 membrane-like individually; rim level 0.634)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1340, R_eq 3.29): none; #1 (t=1340, R_eq 3.52): none; #2 (t=1340, R_eq 3.43): none; #5 (t=1370, R_eq 3.24): none

## Warnings
- radial: 1 of 1339 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
