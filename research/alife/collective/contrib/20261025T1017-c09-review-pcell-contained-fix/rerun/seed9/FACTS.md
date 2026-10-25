# Evidence pack: pcell-multilevel (seed 9)

- world: `../../../20261025T0857-c06-pcell-contained-heredity/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 391s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0857-c06-pcell-contained-heredity/world.py --out collective/contrib/20261025T0950-c09-review-pcell-contained/rerun/seed9 --seeds 9 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6157], min area 6 px

## Measurements
- components: final 17, mean 22.8, max 29; occupancy final 0.25
- tracks: 101; persistent (alive >= 50% of run): 16; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 25.05 (1 = constant size)
- enclosures: components with a hole mean 6.57, final 2; holes at thresholds 0.2/0.35/0.5 final [16, 3, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 17, 17], H1 [13, 3, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.00133/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 10000, default): splits 30, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.067, nucleations 3
- channel total drift (end/start - 1): [-0.6956, -0.4704, 0.6608, -0.2296, -0.1861]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 101: holes 1, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.20; core [0.15, 0.544, 0.612, 0.496, 0.787] rim [0.237, 0.336, 0.589, 0.605, 0.699]
  - track 30 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.67, heterogeneity 0.19; core [0.258, 0.55, 0.768, 0.744, 0.582] rim [0.437, 0.131, 0.466, 0.588, 0.451]
  - track 34 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 1.01, heterogeneity 0.20; core [0.151, 0.532, 0.635, 0.483, 0.762] rim [0.345, 0.192, 0.615, 0.775, 0.615]
  - track 68 at frame 139: holes 0, rim-vs-core 0.59, rim-vs-outside 0.80, heterogeneity 0.19; core [0.221, 0.559, 0.851, 0.738, 0.717] rim [0.395, 0.155, 0.492, 0.6, 0.642]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 141 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 4.37, rim/outside 0.907 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.501)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.675, rim/outside 11.1 (aggregate of 141 individuals; 1/141 membrane-like individually; rim level 0.504)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 8.86 (aggregate of 141 individuals; 76/141 membrane-like individually; rim level 0.779)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.97, rim/outside 7.49 (aggregate of 141 individuals; 124/141 membrane-like individually; rim level 0.782)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 8.29 (aggregate of 141 individuals; 0/141 membrane-like individually; rim level 0.691)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #29 (t=50500, R_eq 10.12, ring): ['L link', 'membrane (wall)']; #30 (t=50500, R_eq 5.78): ['L link', 'membrane (wall)']; #34 (t=50500, R_eq 7.67): ['L link', 'membrane (wall)']; #68 (t=69500, R_eq 5.56): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 141 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
