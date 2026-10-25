# Evidence pack: pcell-mwall-gate (seed 6)

- world: `../../../20261025T1430-c14-mwall-gate-work/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 603s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1430-c14-mwall-gate-work/world.py --out collective/contrib/20261025T1543-c16-review-gate-work/rerun/seed6 --seeds 6 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5463], min area 6 px

## Measurements
- components: final 24, mean 21.8, max 25; occupancy final 0.40
- tracks: 48; persistent (alive >= 50% of run): 20; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 10.63 (1 = constant size)
- enclosures: components with a hole mean 6.25, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 18, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 24, 24], H1 [21, 14, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00037/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 10000, default): splits 13, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.308, nucleations 1
- channel total drift (end/start - 1): [-0.522, -0.6451, 0.289, -0.0005, -0.5764, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 101: holes 0, rim-vs-core 0.76, rim-vs-outside 1.20, heterogeneity 0.25; core [0.163, 0.72, 0.813, 0.536, 0.85, 0.433] rim [0.387, 0.152, 0.624, 0.755, 0.598, 0.661]
  - track 12 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 1.19, heterogeneity 0.24; core [0.131, 0.599, 0.693, 0.473, 0.894, 0.353] rim [0.262, 0.342, 0.647, 0.631, 0.756, 0.54]
  - track 13 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 1.18, heterogeneity 0.24; core [0.144, 0.573, 0.692, 0.492, 0.927, 0.327] rim [0.362, 0.121, 0.595, 0.76, 0.639, 0.646]
  - track 42 at frame 165: holes 1, rim-vs-core 0.60, rim-vs-outside 1.18, heterogeneity 0.25; core [0.087, 0.566, 0.552, 0.283, 0.974, 0.19] rim [0.231, 0.301, 0.609, 0.613, 0.759, 0.522]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.98, rim/outside 0.92 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.551)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.555, rim/outside 9.21 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.407)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 8.74 (aggregate of 133 individuals; 61/133 membrane-like individually; rim level 0.738)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.19, rim/outside 7.96 (aggregate of 133 individuals; 108/133 membrane-like individually; rim level 0.746)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 8.87 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.798)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.13, rim/outside 8.38 (aggregate of 133 individuals; 110/133 membrane-like individually; rim level 0.654)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #6 (t=50500, R_eq 6.02): ['membrane (wall)', 'M wall material']; #12 (t=50500, R_eq 7.74): ['L link', 'membrane (wall)', 'M wall material']; #13 (t=50500, R_eq 7.2): ['L link', 'membrane (wall)', 'M wall material']; #42 (t=82500, R_eq 12.13): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
