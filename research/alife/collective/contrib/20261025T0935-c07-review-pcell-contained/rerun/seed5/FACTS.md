# Evidence pack: pcell-multilevel (seed 5)

- world: `../../../20261025T0857-c06-pcell-contained-heredity/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0857-c06-pcell-contained-heredity/world.py --out collective/contrib/_c07rev11/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6328], min area 6 px

## Measurements
- components: final 22, mean 25.0, max 30; occupancy final 0.35
- tracks: 89; persistent (alive >= 50% of run): 14; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.86 (1 = constant size)
- enclosures: components with a hole mean 8.52, final 9; holes at thresholds 0.2/0.35/0.5 final [12, 10, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 22, 22], H1 [16, 11, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00131/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 10000, default): splits 31, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.032, nucleations 2
- channel total drift (end/start - 1): [-0.6206, -0.5652, 0.4953, -0.1387, -0.3885]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 101: holes 0, rim-vs-core 0.66, rim-vs-outside 1.07, heterogeneity 0.21; core [0.136, 0.857, 0.743, 0.608, 0.649] rim [0.343, 0.26, 0.668, 0.766, 0.578]
  - track 30 at frame 103: holes 0, rim-vs-core 0.59, rim-vs-outside 0.80, heterogeneity 0.20; core [0.192, 0.604, 0.832, 0.703, 0.717] rim [0.385, 0.158, 0.518, 0.661, 0.627]
  - track 31 at frame 103: holes 1, rim-vs-core 0.48, rim-vs-outside 1.02, heterogeneity 0.22; core [0.131, 0.596, 0.656, 0.424, 0.794] rim [0.295, 0.257, 0.624, 0.681, 0.657]
  - track 67 at frame 158: holes 0, rim-vs-core 0.52, rim-vs-outside 1.15, heterogeneity 0.18; core [0.131, 0.608, 0.679, 0.532, 0.813] rim [0.327, 0.207, 0.657, 0.798, 0.763]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.59, rim/outside 0.893 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.511)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.693, rim/outside 12.6 (aggregate of 152 individuals; 1/152 membrane-like individually; rim level 0.509)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 10 (aggregate of 152 individuals; 98/152 membrane-like individually; rim level 0.768)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.33, rim/outside 8.3 (aggregate of 152 individuals; 137/152 membrane-like individually; rim level 0.767)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 9.68 (aggregate of 152 individuals; 0/152 membrane-like individually; rim level 0.724)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #24 (t=50500, R_eq 6.08): ['L link', 'membrane (wall)']; #30 (t=51500, R_eq 5.59): ['L link', 'membrane (wall)']; #31 (t=51500, R_eq 8.7): ['L link', 'membrane (wall)']; #67 (t=79000, R_eq 6.51): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
