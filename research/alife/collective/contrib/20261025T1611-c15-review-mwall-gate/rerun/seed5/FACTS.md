# Evidence pack: pcell-mwall-gate (seed 5)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 847s; status ok
- command: `python -m labkit.run /root/rev3/world.py --out /root/rev3/rerun/seed5 --seeds 5 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5192], min area 6 px

## Measurements
- components: final 21, mean 23.0, max 25; occupancy final 0.43
- tracks: 44; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.13 (1 = constant size)
- enclosures: components with a hole mean 6.24, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 14, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 21, 21], H1 [21, 14, 1]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.000412/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 12, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5492, -0.613, 0.3766, -0.1093, -0.5322, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.77, rim-vs-outside 1.19, heterogeneity 0.25; core [0.146, 0.652, 0.76, 0.514, 0.876, 0.378] rim [0.369, 0.135, 0.639, 0.774, 0.584, 0.696]
  - track 12 at frame 101: holes 0, rim-vs-core 0.69, rim-vs-outside 1.21, heterogeneity 0.24; core [0.167, 0.6, 0.751, 0.537, 0.866, 0.377] rim [0.391, 0.143, 0.637, 0.769, 0.613, 0.674]
  - track 14 at frame 101: holes 0, rim-vs-core 0.80, rim-vs-outside 0.72, heterogeneity 0.22; core [0.255, 0.584, 0.931, 0.829, 0.773, 0.728] rim [0.421, 0.104, 0.498, 0.573, 0.471, 0.517]
  - track 35 at frame 143: holes 1, rim-vs-core 0.42, rim-vs-outside 1.08, heterogeneity 0.25; core [0.111, 0.557, 0.621, 0.356, 0.999, 0.228] rim [0.197, 0.343, 0.586, 0.545, 0.812, 0.454]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.91, rim/outside 0.921 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.552)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.544, rim/outside 8.58 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.405)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 8.48 (aggregate of 138 individuals; 63/138 membrane-like individually; rim level 0.755)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.72, rim/outside 8.04 (aggregate of 138 individuals; 123/138 membrane-like individually; rim level 0.759)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 8.35 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.816)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.74, rim/outside 8.53 (aggregate of 138 individuals; 123/138 membrane-like individually; rim level 0.68)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 6.43): ['L link', 'membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 6.13): ['L link', 'membrane (wall)', 'M wall material']; #14 (t=50500, R_eq 4.55): ['membrane (wall)', 'M wall material']; #35 (t=71500, R_eq 11.93, ring): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 26 of 138 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
