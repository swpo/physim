# Evidence pack: pcell-yeff-cap (seed 12)

- world: `../../../20261025T1108-c06-pcell-efficiency-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 447s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1108-c06-pcell-efficiency-claim/world.py --out collective/contrib/20261025T1346-c09-review-yeff/rerun/seed12 --seeds 12 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5697], min area 6 px

## Measurements
- components: final 17, mean 21.0, max 28; occupancy final 0.39
- tracks: 73; persistent (alive >= 50% of run): 18; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.44 (1 = constant size)
- enclosures: components with a hole mean 7.96, final 11; holes at thresholds 0.2/0.35/0.5 final [20, 11, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 17, 17], H1 [15, 12, 7]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000538/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 10000, default): splits 19, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.053, nucleations 13
- channel total drift (end/start - 1): [-0.6742, -0.4705, 0.6574, -0.0817, -0.3089]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 104: holes 0, rim-vs-core 0.46, rim-vs-outside 0.90, heterogeneity 0.21; core [0.275, 0.453, 0.82, 0.827, 0.89] rim [0.33, 0.292, 0.556, 0.596, 0.657]
  - track 31 at frame 104: holes 0, rim-vs-core 0.41, rim-vs-outside 1.10, heterogeneity 0.18; core [0.347, 0.52, 0.953, 0.906, 0.819] rim [0.379, 0.371, 0.682, 0.635, 0.797]
  - track 32 at frame 106: holes 1, rim-vs-core 0.25, rim-vs-outside 0.88, heterogeneity 0.22; core [0.168, 0.555, 0.615, 0.442, 0.997] rim [0.234, 0.391, 0.589, 0.568, 0.883]
  - track 60 at frame 173: holes 0, rim-vs-core 0.59, rim-vs-outside 0.86, heterogeneity 0.20; core [0.224, 0.582, 0.758, 0.731, 0.9] rim [0.387, 0.132, 0.481, 0.601, 0.726]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 127 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.37, rim/outside 0.959 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.472)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.707, rim/outside 5.68 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.504)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 4.53 (aggregate of 127 individuals; 53/127 membrane-like individually; rim level 0.736)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.23, rim/outside 3.69 (aggregate of 127 individuals; 112/127 membrane-like individually; rim level 0.683)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 4.58 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.882)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #28 (t=52000, R_eq 5.44): ['L link', 'membrane (wall)']; #31 (t=52000, R_eq 4.3): ['membrane (wall)']; #32 (t=53000, R_eq 12.07, ring): ['membrane (wall)']; #60 (t=86500, R_eq 6): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 46 of 127 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
