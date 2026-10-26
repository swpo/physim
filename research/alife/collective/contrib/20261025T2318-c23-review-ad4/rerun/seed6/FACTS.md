# Evidence pack: ad4-protocell (seed 6)

- world: `../../../../../../threads/active-droplets/worlds/ad4-protocell/world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 161s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad4-protocell/world.py --out collective/contrib/20261025T2318-c23-review-ad4/rerun/seed6 --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0643, 1.4315], min area 6 px

## Measurements
- components: final 12, mean 9.8, max 12; occupancy final 0.12
- tracks: 21; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.34 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [0.107, -0.6094, 3.064, 0.6508, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.64, rim-vs-outside 0.72, heterogeneity 0.14; core [0.968, 0.077, 0.0, 0.958, 0.158] rim [0.702, 0.163, 0.0, 0.611, 0.612]
  - track 8 at frame 103: holes 0, rim-vs-core 0.62, rim-vs-outside 0.69, heterogeneity 0.14; core [0.97, 0.085, 0.0, 0.952, 0.148] rim [0.704, 0.163, 0.0, 0.608, 0.584]
  - track 9 at frame 111: holes 0, rim-vs-core 0.63, rim-vs-outside 0.70, heterogeneity 0.14; core [0.946, 0.024, 0.954, 0.0, 0.169] rim [0.698, 0.111, 0.606, 0.0, 0.63]
  - track 17 at frame 171: holes 0, rim-vs-core 0.36, rim-vs-outside 0.85, heterogeneity 0.14; core [0.965, 0.036, 0.94, 0.0, 0.141] rim [0.818, 0.075, 0.746, 0.0, 0.397]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 66.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.912)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.45, rim/outside 0.711 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.223)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.89, rim/outside 49.7 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.551)
  - radial b (catalyst B): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 32.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.332)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.81, rim/outside 19.8 (aggregate of 62 individuals; 60/62 membrane-like individually; rim level 0.734)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #1 (t=10100, R_eq 7.65): ['psi (amphiphile)']; #8 (t=10300, R_eq 7.16): ['psi (amphiphile)']; #9 (t=11100, R_eq 8.25): ['psi (amphiphile)']; #17 (t=17100, R_eq 6.91): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
