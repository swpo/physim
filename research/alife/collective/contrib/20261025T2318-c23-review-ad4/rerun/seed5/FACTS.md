# Evidence pack: ad4-protocell (seed 5)

- world: `../../../../../../threads/active-droplets/worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 161s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out collective/contrib/20261025T2318-c23-review-ad4/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0652, 1.4276], min area 6 px

## Measurements
- components: final 11, mean 9.0, max 11; occupancy final 0.12
- tracks: 19; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.82 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0029/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.167, nucleations 0
- channel total drift (end/start - 1): [0.1005, -0.5979, 2.8713, 0.768, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.63, rim-vs-outside 0.71, heterogeneity 0.14; core [0.971, 0.082, 0.0, 0.948, 0.15] rim [0.704, 0.161, 0.0, 0.603, 0.594]
  - track 7 at frame 103: holes 0, rim-vs-core 0.65, rim-vs-outside 0.69, heterogeneity 0.14; core [0.966, 0.075, 0.0, 0.952, 0.16] rim [0.692, 0.164, 0.0, 0.597, 0.628]
  - track 8 at frame 103: holes 0, rim-vs-core 0.64, rim-vs-outside 0.68, heterogeneity 0.14; core [0.948, 0.026, 0.948, 0.0, 0.158] rim [0.698, 0.109, 0.602, 0.0, 0.622]
  - track 13 at frame 139: holes 0, rim-vs-core 0.37, rim-vs-outside 0.84, heterogeneity 0.14; core [0.954, 0.032, 0.937, 0.0, 0.158] rim [0.806, 0.074, 0.742, 0.0, 0.437]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 60.8 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.912)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.32, rim/outside 0.704 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.225)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 45.6 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.537)
  - radial b (catalyst B): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 33.9 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.344)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.58, rim/outside 18.1 (aggregate of 57 individuals; 56/57 membrane-like individually; rim level 0.692)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #2 (t=10100, R_eq 7.25): ['psi (amphiphile)']; #7 (t=10300, R_eq 7.82): ['psi (amphiphile)']; #8 (t=10300, R_eq 8.06): ['psi (amphiphile)']; #13 (t=13900, R_eq 7.69): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
