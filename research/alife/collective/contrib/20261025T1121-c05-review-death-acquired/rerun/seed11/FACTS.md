# Evidence pack: pcell-multilevel (seed 11)

- world: `../../../../contrib/20261025T0820-c06-pcell-multilevel-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 161 frames x 625 steps x dt 1.0 = time 100000; grid [128, 128]; wall 371s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0820-c06-pcell-multilevel-claim/world.py --out collective/work_c05/rev_da/rerun/seed11 --seeds 11 --frames 160 --spf 625 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6291], min area 6 px

## Measurements
- components: final 25, mean 25.5, max 30; occupancy final 0.34
- tracks: 95; persistent (alive >= 50% of run): 20; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.56 (1 = constant size)
- enclosures: components with a hole mean 8.24, final 5; holes at thresholds 0.2/0.35/0.5 final [9, 5, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 25, 25], H1 [16, 8, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000341/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 12500, default): splits 33, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.212, nucleations 1
- channel total drift (end/start - 1): [-0.5785, -0.6027, 0.3716, -0.038, -0.4863]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 81: holes 0, rim-vs-core 0.37, rim-vs-outside 0.85, heterogeneity 0.21; core [0.203, 0.587, 0.791, 0.7, 0.666] rim [0.325, 0.328, 0.609, 0.653, 0.519]
  - track 25 at frame 81: holes 0, rim-vs-core 0.63, rim-vs-outside 0.79, heterogeneity 0.20; core [0.215, 0.634, 0.867, 0.7, 0.706] rim [0.399, 0.158, 0.511, 0.65, 0.61]
  - track 41 at frame 83: holes 0, rim-vs-core 0.40, rim-vs-outside 1.07, heterogeneity 0.22; core [0.134, 0.655, 0.683, 0.476, 0.76] rim [0.264, 0.36, 0.646, 0.674, 0.646]
  - track 79 at frame 140: holes 0, rim-vs-core 0.54, rim-vs-outside 1.10, heterogeneity 0.20; core [0.156, 0.628, 0.725, 0.536, 0.737] rim [0.335, 0.201, 0.673, 0.79, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.49, rim/outside 0.901 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.508)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.666, rim/outside 12.7 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.492)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 10.6 (aggregate of 155 individuals; 102/155 membrane-like individually; rim level 0.779)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.22, rim/outside 8.97 (aggregate of 155 individuals; 140/155 membrane-like individually; rim level 0.797)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 10.3 (aggregate of 155 individuals; 0/155 membrane-like individually; rim level 0.718)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #24 (t=50625, R_eq 5.94): ['L link', 'membrane (wall)']; #25 (t=50625, R_eq 5.53): ['L link', 'membrane (wall)']; #41 (t=51875, R_eq 7.55): ['L link', 'membrane (wall)']; #79 (t=87500, R_eq 6.21): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 35 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
