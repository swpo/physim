# Evidence pack: pcell-multilevel-res15 (seed 1)

- world: `../../world_res15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 125 steps x dt 1.0 = time 20000; grid [192, 192]; wall 214s; status ok
- command: `python -m labkit.run collective/work/pcell/W/world_res15.py --out collective/work/pcell/W/pack_res15 --seeds 0 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4946], min area 6 px

## Measurements
- components: final 23, mean 18.3, max 28; occupancy final 0.36
- tracks: 82; persistent (alive >= 50% of run): 18; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.03 (1 = constant size)
- enclosures: components with a hole mean 11.89, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 11, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 23, 23], H1 [23, 20, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 2500, default): splits 19, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.211, nucleations 3
- channel total drift (end/start - 1): [-0.4954, -0.6568, 0.1071, 0.2313, -0.653]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 83: holes 1, rim-vs-core 0.29, rim-vs-outside 0.99, heterogeneity 0.23; core [0.111, 0.658, 0.605, 0.472, 0.964] rim [0.202, 0.425, 0.588, 0.569, 0.861]
  - track 41 at frame 83: holes 1, rim-vs-core 0.36, rim-vs-outside 1.05, heterogeneity 0.22; core [0.11, 0.696, 0.605, 0.456, 0.913] rim [0.218, 0.401, 0.597, 0.602, 0.821]
  - track 49 at frame 85: holes 1, rim-vs-core 0.51, rim-vs-outside 1.17, heterogeneity 0.23; core [0.087, 0.733, 0.559, 0.384, 0.917] rim [0.247, 0.359, 0.625, 0.659, 0.8]
  - track 67 at frame 117: holes 0, rim-vs-core 0.33, rim-vs-outside 1.21, heterogeneity 0.22; core [0.143, 0.735, 0.753, 0.629, 0.857] rim [0.263, 0.463, 0.651, 0.66, 0.774]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.933 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.545)
  - radial K particles: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 12.3 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.614)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 8.08 (aggregate of 118 individuals; 87/118 membrane-like individually; rim level 0.71)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 5.66, rim/outside 6.65 (aggregate of 118 individuals; 113/118 membrane-like individually; rim level 0.713)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 8.85 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.871)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #36 (t=10375, R_eq 16.17, ring): ['L link', 'membrane (wall)']; #41 (t=10375, R_eq 15.83, ring): ['membrane (wall)']; #49 (t=10625, R_eq 14.21, ring): ['L link', 'membrane (wall)']; #67 (t=14625, R_eq 10.09): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
