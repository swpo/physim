# Evidence pack: pcell-multilevel (seed 1)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run collective/work/pcell/claim2/world.py --out collective/work/pcell/claim2/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6313], min area 6 px

## Measurements
- components: final 25, mean 24.6, max 29; occupancy final 0.37
- tracks: 106; persistent (alive >= 50% of run): 14; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.64 (1 = constant size)
- enclosures: components with a hole mean 9.00, final 11; holes at thresholds 0.2/0.35/0.5 final [3, 13, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 25, 25], H1 [20, 14, 1]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000702/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 10000, default): splits 32, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.031, nucleations 1
- channel total drift (end/start - 1): [-0.5435, -0.6301, 0.2758, 0.1912, -0.5692]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 1.10, heterogeneity 0.22; core [0.112, 0.72, 0.696, 0.452, 0.745] rim [0.284, 0.334, 0.65, 0.702, 0.641]
  - track 43 at frame 103: holes 0, rim-vs-core 0.54, rim-vs-outside 1.04, heterogeneity 0.20; core [0.157, 0.646, 0.676, 0.577, 0.68] rim [0.36, 0.212, 0.653, 0.787, 0.559]
  - track 51 at frame 106: holes 0, rim-vs-core 0.44, rim-vs-outside 1.13, heterogeneity 0.20; core [0.124, 0.634, 0.631, 0.457, 0.731] rim [0.301, 0.345, 0.673, 0.731, 0.68]
  - track 85 at frame 148: holes 0, rim-vs-core 0.62, rim-vs-outside 0.79, heterogeneity 0.19; core [0.218, 0.636, 0.81, 0.679, 0.625] rim [0.414, 0.133, 0.525, 0.673, 0.549]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.85, rim/outside 0.887 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.529)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 14.6 (aggregate of 152 individuals; 1/152 membrane-like individually; rim level 0.512)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 11.8 (aggregate of 152 individuals; 95/152 membrane-like individually; rim level 0.761)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.22, rim/outside 9.81 (aggregate of 152 individuals; 136/152 membrane-like individually; rim level 0.76)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 11.7 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.73)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #42 (t=50500, R_eq 7.02): ['L link', 'membrane (wall)']; #43 (t=51500, R_eq 6.26): ['L link', 'membrane (wall)']; #51 (t=53000, R_eq 7.23): ['L link', 'membrane (wall)']; #85 (t=74000, R_eq 5.92): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
