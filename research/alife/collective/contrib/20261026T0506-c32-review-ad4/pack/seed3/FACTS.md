# Evidence pack: ad4-protocell (seed 3)

- world: `../../world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 166s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0506-c32-review-ad4/world.py --out collective/contrib/20261026T0506-c32-review-ad4/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.0647, 1.4302], min area 6 px

## Measurements
- components: final 12, mean 9.9, max 12; occupancy final 0.12
- tracks: 21; persistent (alive >= 50% of run): 11; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 2.71 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00121/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [0.1068, -0.6089, 3.2906, 0.4225, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.70, heterogeneity 0.14; core [0.97, 0.077, 0.0, 0.957, 0.157] rim [0.716, 0.158, 0.0, 0.624, 0.587]
  - track 5 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.79, heterogeneity 0.14; core [0.976, 0.073, 0.0, 0.966, 0.161] rim [0.772, 0.141, 0.0, 0.7, 0.485]
  - track 9 at frame 113: holes 0, rim-vs-core 0.63, rim-vs-outside 0.71, heterogeneity 0.14; core [0.951, 0.024, 0.954, 0.0, 0.162] rim [0.701, 0.107, 0.607, 0.0, 0.611]
  - track 15 at frame 141: holes 0, rim-vs-core 0.63, rim-vs-outside 0.70, heterogeneity 0.14; core [0.962, 0.027, 0.947, 0.0, 0.155] rim [0.7, 0.106, 0.6, 0.0, 0.606]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.94, rim/outside 59.7 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.922)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.19, rim/outside 0.716 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.219)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 45.8 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.567)
  - radial b (catalyst B): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 30.5 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.32)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4, rim/outside 18.5 (aggregate of 64 individuals; 64/64 membrane-like individually; rim level 0.74)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #3 (t=10100, R_eq 7.42): ['psi (amphiphile)']; #5 (t=10100, R_eq 7.59): ['psi (amphiphile)']; #9 (t=11300, R_eq 8.14): ['psi (amphiphile)']; #15 (t=14100, R_eq 7.48): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
