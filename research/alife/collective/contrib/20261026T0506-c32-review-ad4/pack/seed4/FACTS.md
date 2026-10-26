# Evidence pack: ad4-protocell (seed 4)

- world: `../../world.py`, family `phase-field`
- parent: ad2-catalysts + ad3-membrane; mutation: merge: catalyst-driven production (heredity) with amphiphile synthesis and interface binding (membrane)
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 168s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0506-c32-review-ad4/world.py --out collective/contrib/20261026T0506-c32-review-ad4/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.43 of robust range [-1.064, 1.4352], min area 6 px

## Measurements
- components: final 12, mean 10.2, max 12; occupancy final 0.12
- tracks: 21; persistent (alive >= 50% of run): 10; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.99 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00179/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [0.109, -0.6125, 3.125, 0.6251, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.69, heterogeneity 0.13; core [0.968, 0.103, 0.0, 0.937, 0.129] rim [0.701, 0.165, 0.0, 0.595, 0.548]
  - track 8 at frame 103: holes 0, rim-vs-core 0.62, rim-vs-outside 0.71, heterogeneity 0.14; core [0.969, 0.078, 0.0, 0.959, 0.153] rim [0.712, 0.159, 0.0, 0.62, 0.592]
  - track 11 at frame 114: holes 0, rim-vs-core 0.64, rim-vs-outside 0.70, heterogeneity 0.14; core [0.948, 0.025, 0.948, 0.0, 0.161] rim [0.694, 0.107, 0.6, 0.0, 0.629]
  - track 15 at frame 138: holes 0, rim-vs-core 0.59, rim-vs-outside 0.69, heterogeneity 0.13; core [0.961, 0.026, 0.95, 0.0, 0.155] rim [0.724, 0.102, 0.625, 0.0, 0.576]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 65.2 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.911)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.05, rim/outside 0.714 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.217)
  - radial a (catalyst A): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 50.7 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.562)
  - radial b (catalyst B): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 30.7 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.317)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4, rim/outside 19.8 (aggregate of 64 individuals; 62/64 membrane-like individually; rim level 0.757)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 6.15): ['psi (amphiphile)']; #8 (t=10300, R_eq 7.33): ['psi (amphiphile)']; #11 (t=11400, R_eq 7.9): ['psi (amphiphile)']; #15 (t=13800, R_eq 7.33): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
