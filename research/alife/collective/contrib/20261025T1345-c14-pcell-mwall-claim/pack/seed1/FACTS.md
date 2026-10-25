# Evidence pack: pcell-mwall (seed 1)

- world: `../../world_m.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 1115s; status ok
- command: `python -m labkit.run scratch/c14/world_m.py --out scratch/c14/mpack/seed1 --seeds 1 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5842], min area 6 px

## Measurements
- components: final 16, mean 19.6, max 27; occupancy final 0.35
- tracks: 72; persistent (alive >= 50% of run): 17; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 18.92 (1 = constant size)
- enclosures: components with a hole mean 8.11, final 8; holes at thresholds 0.2/0.35/0.5 final [21, 8, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 16, 16], H1 [13, 10, 2]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000533/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 10000, default): splits 18, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.222, nucleations 4
- channel total drift (end/start - 1): [-0.6573, -0.5062, 0.5735, 0.0966, -0.3271, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 101: holes 1, rim-vs-core 0.30, rim-vs-outside 0.99, heterogeneity 0.24; core [0.149, 0.597, 0.652, 0.508, 0.959, 0.316] rim [0.227, 0.38, 0.608, 0.575, 0.827, 0.438]
  - track 37 at frame 101: holes 1, rim-vs-core 0.25, rim-vs-outside 0.91, heterogeneity 0.24; core [0.165, 0.528, 0.656, 0.556, 0.998, 0.347] rim [0.211, 0.363, 0.59, 0.573, 0.846, 0.428]
  - track 60 at frame 131: holes 0, rim-vs-core 0.72, rim-vs-outside 0.84, heterogeneity 0.22; core [0.223, 0.613, 0.826, 0.738, 0.842, 0.507] rim [0.385, 0.13, 0.441, 0.574, 0.589, 0.387]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 118 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 4.4, rim/outside 0.904 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.484)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.71, rim/outside 7.74 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.508)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 6.43 (aggregate of 118 individuals; 54/118 membrane-like individually; rim level 0.73)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.11, rim/outside 5.5 (aggregate of 118 individuals; 96/118 membrane-like individually; rim level 0.689)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 6.44 (aggregate of 118 individuals; 0/118 membrane-like individually; rim level 0.863)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.96, rim/outside 5.67 (aggregate of 118 individuals; 102/118 membrane-like individually; rim level 0.571)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #13 (t=50500, R_eq 14, ring): ['membrane (wall)', 'M wall material']; #16 (t=50500, R_eq 10.4, ring): ['membrane (wall)', 'M wall material']; #37 (t=50500, R_eq 11.97, ring): ['membrane (wall)', 'M wall material']; #60 (t=65500, R_eq 5.61): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 44 of 118 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
