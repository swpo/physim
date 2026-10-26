# Evidence pack: ad4-protocell (seed 7)

- world: `../../../../threads/active-droplets/worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out collective/contrib/20261025T2304-c21-review-ad4/rerun7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0643, 1.4327], min area 6 px

## Measurements
- components: final 12, mean 10.2, max 12; occupancy final 0.12
- tracks: 21; persistent (alive >= 50% of run): 10; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.85 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.000958/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1118, -0.6167, 3.6781, 0.135, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 104: holes 0, rim-vs-core 0.60, rim-vs-outside 0.71, heterogeneity 0.13; core [0.971, 0.09, 0.0, 0.957, 0.143] rim [0.717, 0.161, 0.0, 0.624, 0.567]
  - track 7 at frame 114: holes 0, rim-vs-core 0.63, rim-vs-outside 0.71, heterogeneity 0.14; core [0.965, 0.031, 0.944, 0.0, 0.15] rim [0.702, 0.108, 0.598, 0.0, 0.603]
  - track 10 at frame 118: holes 0, rim-vs-core 0.64, rim-vs-outside 0.70, heterogeneity 0.14; core [0.952, 0.025, 0.951, 0.0, 0.167] rim [0.698, 0.111, 0.603, 0.0, 0.628]
  - track 17 at frame 136: holes 0, rim-vs-core 0.48, rim-vs-outside 0.78, heterogeneity 0.14; core [0.968, 0.026, 0.956, 0.0, 0.153] rim [0.767, 0.09, 0.683, 0.0, 0.484]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 57 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.91)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.59, rim/outside 0.71 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.213)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 48.7 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.642)
  - radial b (catalyst B): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 23.6 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.237)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.96, rim/outside 19 (aggregate of 64 individuals; 61/64 membrane-like individually; rim level 0.758)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #5 (t=10400, R_eq 6.79): ['psi (amphiphile)']; #7 (t=11400, R_eq 7.25): ['psi (amphiphile)']; #10 (t=11800, R_eq 8.06): ['psi (amphiphile)']; #17 (t=13600, R_eq 7.33): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
