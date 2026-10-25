# Evidence pack: pcell-mwall-b42 (seed 2)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 420s; status ok
- command: `python -m labkit.run collective/contrib/c17-b42-wip/world.py --out collective/contrib/c17-b42-wip/fed/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6364], min area 6 px

## Measurements
- components: final 30, mean 27.5, max 30; occupancy final 0.33
- tracks: 61; persistent (alive >= 50% of run): 25; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 43.87 (1 = constant size)
- enclosures: components with a hole mean 5.98, final 6; holes at thresholds 0.2/0.35/0.5 final [0, 6, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 30, 30], H1 [23, 14, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00116/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 10000, default): splits 17, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.4736, -0.6823, 0.0998, -0.1964, -0.635, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.85, heterogeneity 0.20; core [0.221, 0.64, 0.891, 0.799, 0.759, 0.773] rim [0.426, 0.193, 0.497, 0.579, 0.728, 0.546]
  - track 7 at frame 101: holes 0, rim-vs-core 0.67, rim-vs-outside 1.35, heterogeneity 0.22; core [0.11, 0.572, 0.639, 0.438, 0.941, 0.326] rim [0.353, 0.193, 0.65, 0.788, 0.861, 0.663]
  - track 17 at frame 101: holes 1, rim-vs-core 0.25, rim-vs-outside 1.14, heterogeneity 0.22; core [0.129, 0.487, 0.656, 0.562, 0.956, 0.374] rim [0.227, 0.354, 0.591, 0.602, 0.842, 0.495]
  - track 57 at frame 185: holes 0, rim-vs-core 0.36, rim-vs-outside 1.24, heterogeneity 0.24; core [0.122, 0.616, 0.668, 0.506, 0.974, 0.354] rim [0.24, 0.361, 0.605, 0.613, 0.848, 0.493]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 168 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.71, rim/outside 0.864 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.563)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.674, rim/outside 25.6 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.516)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 22.7 (aggregate of 168 individuals; 117/168 membrane-like individually; rim level 0.811)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.25, rim/outside 19.3 (aggregate of 168 individuals; 158/168 membrane-like individually; rim level 0.851)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 23.1 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.872)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.73, rim/outside 20.2 (aggregate of 168 individuals; 158/168 membrane-like individually; rim level 0.754)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 4.89): ['membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 7.84): ['L link', 'membrane (wall)', 'M wall material']; #17 (t=50500, R_eq 8.54, ring): ['L link', 'membrane (wall)', 'M wall material']; #57 (t=92500, R_eq 8.21): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 168 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
