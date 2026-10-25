# Evidence pack: pcell-multilevel (seed 7)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T0857-c06-pcell-contained-heredity/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 362s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0857-c06-pcell-contained-heredity/world.py --out /tmp/claude-0/c11rev6/rerun --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6287], min area 6 px

## Measurements
- components: final 27, mean 25.8, max 30; occupancy final 0.34
- tracks: 90; persistent (alive >= 50% of run): 22; longest 198 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.57 (1 = constant size)
- enclosures: components with a hole mean 8.02, final 10; holes at thresholds 0.2/0.35/0.5 final [5, 10, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 27, 27], H1 [23, 13, 2]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.000659/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 10000, default): splits 32, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 2, merge/split ratio 0.062, nucleations 1
- channel total drift (end/start - 1): [-0.5283, -0.6444, 0.2272, 0.0858, -0.5893]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 103: holes 1, rim-vs-core 0.24, rim-vs-outside 0.95, heterogeneity 0.21; core [0.128, 0.551, 0.623, 0.432, 0.843] rim [0.204, 0.395, 0.61, 0.583, 0.772]
  - track 35 at frame 103: holes 1, rim-vs-core 0.32, rim-vs-outside 0.85, heterogeneity 0.22; core [0.129, 0.554, 0.663, 0.527, 0.883] rim [0.24, 0.307, 0.574, 0.596, 0.749]
  - track 37 at frame 106: holes 1, rim-vs-core 0.27, rim-vs-outside 0.90, heterogeneity 0.22; core [0.114, 0.605, 0.636, 0.495, 0.849] rim [0.205, 0.379, 0.6, 0.578, 0.77]
  - track 80 at frame 180: holes 0, rim-vs-core 0.56, rim-vs-outside 1.06, heterogeneity 0.21; core [0.143, 0.671, 0.7, 0.566, 0.755] rim [0.338, 0.201, 0.655, 0.773, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.94, rim/outside 0.901 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.516)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.689, rim/outside 13.3 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.506)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 10.8 (aggregate of 160 individuals; 105/160 membrane-like individually; rim level 0.779)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.39, rim/outside 9.07 (aggregate of 160 individuals; 146/160 membrane-like individually; rim level 0.786)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 10.6 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.756)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #33 (t=51500, R_eq 10.34, ring): ['L link', 'membrane (wall)']; #35 (t=51500, R_eq 9.41, ring): ['L link', 'membrane (wall)']; #37 (t=53000, R_eq 10.49, ring): ['L link', 'membrane (wall)']; #80 (t=90000, R_eq 6.41): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
