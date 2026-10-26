# Evidence pack: pps (seed 0)

- world: `../../world.py`, family `particle`
- parent: None; mutation: new class: Schmickl's Primordial Particle System, published parameters
- run: 201 frames x 150 steps x dt 1.0 = time 30000; grid [125, 125]; wall 111s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0230-c29-pps-sighting/world.py --out collective/contrib/20261026T0230-c29-pps-sighting/pack --seeds 0 1 --no-movie`
- segmentation: matter > 0.04 of robust range [0.0, 8.5938], min area 6 px

## Measurements
- components: final 40, mean 27.1, max 83; occupancy final 0.18
- tracks: 1845; persistent (alive >= 50% of run): 2; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.78 (1 = constant size)
- enclosures: components with a hole mean 0.33, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 58, 43], H1 [1, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0021/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 3000, default): splits 649, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 634, merge/split ratio 0.977, nucleations 3
- channel total drift (end/start - 1): [0.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 443 at frame 138: holes 0, rim-vs-core 0.36, rim-vs-outside 0.04, heterogeneity 0.23; core [0.299, 0.069, 0.27] rim [0.034, 0.0, 0.034]
  - track 710 at frame 150: holes 0, rim-vs-core 0.40, rim-vs-outside 0.02, heterogeneity 0.19; core [0.296, 0.0, 0.296] rim [0.013, 0.0, 0.013]
  - track 766 at frame 151: holes 0, rim-vs-core 0.35, rim-vs-outside 0.03, heterogeneity 0.16; core [0.267, 0.0, 0.267] rim [0.026, 0.0, 0.013]
  - track 1148 at frame 166: holes 0, rim-vs-core 0.56, rim-vs-outside 0.01, heterogeneity 0.17; core [0.407, 0.0, 0.407] rim [0.012, 0.0, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 182 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.555, rim/outside 3.08 (aggregate of 182 individuals; 38/182 membrane-like individually; rim level 0.146)
  - radial cell N>35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.174, rim/outside 1.42 (aggregate of 182 individuals; 32/182 membrane-like individually; rim level 0.0071)
  - radial ring 15<N<=35: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.57, rim/outside 5.47 (aggregate of 182 individuals; 53/182 membrane-like individually; rim level 0.136)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #443 (t=20700, R_eq 4.48): none; #710 (t=22500, R_eq 2.65): none; #766 (t=22650, R_eq 2.71): none; #1148 (t=24900, R_eq 2.71): none

## Warnings
- radial: 5 of 182 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
