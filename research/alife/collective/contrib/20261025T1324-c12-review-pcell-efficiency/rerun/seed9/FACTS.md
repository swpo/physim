# Evidence pack: pcell-yeff-cap (seed 9)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 724s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1324-c12-review-pcell-efficiency/world.py --out collective/contrib/20261025T1324-c12-review-pcell-efficiency/rerun/seed9 --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5602], min area 6 px

## Measurements
- components: final 14, mean 18.5, max 25; occupancy final 0.35
- tracks: 88; persistent (alive >= 50% of run): 14; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.66 (1 = constant size)
- enclosures: components with a hole mean 7.68, final 6; holes at thresholds 0.2/0.35/0.5 final [25, 6, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 14, 14], H1 [13, 9, 5]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000587/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 10000, default): splits 23, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.217, nucleations 8
- channel total drift (end/start - 1): [-0.6962, -0.4422, 0.6931, -0.0388, -0.2525]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 101: holes 0, rim-vs-core 0.81, rim-vs-outside 0.62, heterogeneity 0.24; core [0.267, 0.521, 0.783, 0.719, 0.931] rim [0.418, 0.089, 0.435, 0.57, 0.378]
  - track 26 at frame 101: holes 1, rim-vs-core 0.31, rim-vs-outside 0.95, heterogeneity 0.22; core [0.2, 0.582, 0.648, 0.505, 0.952] rim [0.286, 0.341, 0.582, 0.583, 0.82]
  - track 29 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.87, heterogeneity 0.18; core [0.284, 0.582, 0.929, 0.821, 0.899] rim [0.394, 0.19, 0.567, 0.623, 0.823]
  - track 64 at frame 129: holes 0, rim-vs-core 0.61, rim-vs-outside 1.13, heterogeneity 0.22; core [0.216, 0.723, 0.732, 0.587, 0.877] rim [0.388, 0.201, 0.658, 0.776, 0.717]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 3.08, rim/outside 0.986 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.487)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.733, rim/outside 5.51 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.522)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 4.38 (aggregate of 110 individuals; 56/110 membrane-like individually; rim level 0.739)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.35, rim/outside 3.57 (aggregate of 110 individuals; 92/110 membrane-like individually; rim level 0.682)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 4.42 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.89)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #23 (t=50500, R_eq 6): ['L link', 'membrane (wall)']; #26 (t=50500, R_eq 9.59, ring): ['L link', 'membrane (wall)']; #29 (t=50500, R_eq 4.51): ['membrane (wall)']; #64 (t=64500, R_eq 6.08): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 110 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
