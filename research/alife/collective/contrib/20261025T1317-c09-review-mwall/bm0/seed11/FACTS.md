# Evidence pack: pcell-mwall (seed 11)

- world: `../../world_bm0.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 455s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1317-c09-review-mwall/world_bm0.py --out collective/contrib/20261025T1317-c09-review-mwall/bm0/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 1.5506], min area 6 px

## Measurements
- components: final 12, mean 16.6, max 23; occupancy final 0.38
- tracks: 67; persistent (alive >= 50% of run): 14; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.00 (1 = constant size)
- enclosures: components with a hole mean 8.63, final 11; holes at thresholds 0.2/0.35/0.5 final [26, 11, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 12, 12], H1 [16, 12, 7]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.000622/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.1, nucleations 16
- channel total drift (end/start - 1): [-0.6985, -0.4463, 0.7163, -0.0495, -0.2503, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 101: holes 1, rim-vs-core 0.22, rim-vs-outside 0.84, heterogeneity 0.19; core [0.2, 0.543, 0.631, 0.467, 0.949, 0.0] rim [0.269, 0.402, 0.595, 0.558, 0.828, 0.0]
  - track 31 at frame 101: holes 1, rim-vs-core 0.20, rim-vs-outside 0.84, heterogeneity 0.18; core [0.196, 0.544, 0.645, 0.452, 0.999, 0.0] rim [0.247, 0.409, 0.605, 0.543, 0.904, 0.0]
  - track 39 at frame 106: holes 0, rim-vs-core 0.27, rim-vs-outside 1.07, heterogeneity 0.19; core [0.225, 0.559, 0.686, 0.611, 0.906, 0.0] rim [0.301, 0.389, 0.594, 0.599, 0.732, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 2.99, rim/outside 1.01 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.472)
  - radial K particles: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 3.89 (aggregate of 95 individuals; 1/95 membrane-like individually; rim level 0.53)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.12 (aggregate of 95 individuals; 38/95 membrane-like individually; rim level 0.691)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.7, rim/outside 2.61 (aggregate of 95 individuals; 74/95 membrane-like individually; rim level 0.586)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.979, rim/outside 3.19 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.903)
  - radial M wall material: flat profile (no radial structure; level 0; aggregate of 95 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #23 (t=50500, R_eq 13.05, ring): ['membrane (wall)']; #24 (t=50500, R_eq 19.12, ring): none; #31 (t=50500, R_eq 13.88, ring): none; #39 (t=53000, R_eq 7.98): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
