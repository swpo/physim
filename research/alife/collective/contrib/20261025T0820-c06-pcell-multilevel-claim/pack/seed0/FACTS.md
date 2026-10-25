# Evidence pack: pcell-multilevel (seed 0)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 458s; status ok
- command: `python -m labkit.run collective/work/pcell/claim2/world.py --out collective/work/pcell/claim2/pack --seeds 0 1 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5949], min area 6 px

## Measurements
- components: final 25, mean 24.7, max 30; occupancy final 0.38
- tracks: 79; persistent (alive >= 50% of run): 23; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.89 (1 = constant size)
- enclosures: components with a hole mean 8.78, final 10; holes at thresholds 0.2/0.35/0.5 final [6, 10, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 25, 25], H1 [23, 16, 3]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.000892/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10000, default): splits 26, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.038, nucleations 5
- channel total drift (end/start - 1): [-0.5871, -0.5892, 0.4121, -0.0127, -0.4739]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.95, heterogeneity 0.19; core [0.234, 0.644, 0.9, 0.844, 0.673] rim [0.302, 0.411, 0.605, 0.607, 0.66]
  - track 36 at frame 103: holes 0, rim-vs-core 0.31, rim-vs-outside 1.11, heterogeneity 0.20; core [0.164, 0.615, 0.715, 0.563, 0.735] rim [0.271, 0.378, 0.642, 0.701, 0.664]
  - track 37 at frame 103: holes 0, rim-vs-core 0.65, rim-vs-outside 0.74, heterogeneity 0.17; core [0.255, 0.64, 0.917, 0.856, 0.677] rim [0.391, 0.187, 0.547, 0.599, 0.648]
  - track 65 at frame 168: holes 0, rim-vs-core 0.56, rim-vs-outside 1.14, heterogeneity 0.20; core [0.147, 0.712, 0.734, 0.558, 0.782] rim [0.333, 0.235, 0.652, 0.77, 0.711]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.28, rim/outside 0.949 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.488)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.686, rim/outside 7.83 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.501)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 6.09 (aggregate of 148 individuals; 90/148 membrane-like individually; rim level 0.754)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.45, rim/outside 5.16 (aggregate of 148 individuals; 130/148 membrane-like individually; rim level 0.753)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 6 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.744)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #20 (t=50500, R_eq 4.98): ['membrane (wall)']; #36 (t=51500, R_eq 6.6): ['L link', 'membrane (wall)']; #37 (t=51500, R_eq 4.37): ['membrane (wall)']; #65 (t=84000, R_eq 6.23): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 148 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
