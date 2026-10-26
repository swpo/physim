# Evidence pack: pps (seed 1)

- world: `../world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 94s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0215-c29-pps-lineage/world.py --out collective/contrib/20261026T0215-c29-pps-lineage/pack_beta0 --seeds 1 --no-movie`
- segmentation: matter > 0.15 of robust range [0.0, 2.3438], min area 6 px

## Measurements
- components: final 90, mean 90.0, max 90; occupancy final 0.10
- tracks: 90; persistent (alive >= 50% of run): 90; longest 201 frames; alive start-to-end: 90
- size of persistent tracks: max/min area ratio 1.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [121, 32, 1], H1 [86, 8, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 3000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.19, rim-vs-outside 0.10, heterogeneity 0.12; core [0.417, 0.0, 0.0] rim [0.222, 0.0, 0.0]
  - track 1 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.10, heterogeneity 0.10; core [0.583, 0.0, 0.0] rim [0.281, 0.0, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.09, rim-vs-outside 0.13, heterogeneity 0.12; core [0.364, 0.0, 0.0] rim [0.275, 0.0, 0.0]
  - track 3 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.02, heterogeneity 0.13; core [0.625, 0.0, 0.0] rim [0.208, 0.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 330 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 2.06 (aggregate of 330 individuals; 114/330 membrane-like individually; rim level 0.302)
  - radial cell N>35: flat profile (no radial structure; level 0; aggregate of 330 individuals)
  - radial ring 15<N<=35: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 1 (aggregate of 330 individuals; 0/330 membrane-like individually; rim level 0)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=15150, R_eq 2.76): none; #1 (t=15150, R_eq 2.65): none; #2 (t=15150, R_eq 4.82): ['particles']; #3 (t=15150, R_eq 2.26): none

## Warnings
- radial: 6 of 330 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
