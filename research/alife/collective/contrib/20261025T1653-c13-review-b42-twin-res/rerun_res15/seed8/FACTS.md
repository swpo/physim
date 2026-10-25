# Evidence pack: pcell-mwall-b42 (seed 8)

- world: `../../world_res15.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [192, 192]; wall 907s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1653-c13-review-b42-twin-res/world_res15.py --out collective/contrib/20261025T1653-c13-review-b42-twin-res/rerun_res15/seed8 --seeds 8 --spf 500 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5953], min area 6 px

## Measurements
- components: final 29, mean 26.2, max 32; occupancy final 0.34
- tracks: 60; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 43.00 (1 = constant size)
- enclosures: components with a hole mean 5.36, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 11, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [25, 19, 0]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00227/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 10000, default): splits 12, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 4
- channel total drift (end/start - 1): [-0.4988, -0.6582, 0.1254, -0.0868, -0.6046, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 1.17, heterogeneity 0.23; core [0.138, 0.72, 0.73, 0.633, 0.86, 0.458] rim [0.354, 0.234, 0.608, 0.737, 0.756, 0.573]
  - track 4 at frame 101: holes 0, rim-vs-core 0.77, rim-vs-outside 1.34, heterogeneity 0.23; core [0.088, 0.698, 0.6, 0.453, 0.892, 0.291] rim [0.344, 0.203, 0.637, 0.801, 0.807, 0.673]
  - track 5 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 1.09, heterogeneity 0.20; core [0.195, 0.655, 0.799, 0.751, 0.809, 0.592] rim [0.404, 0.176, 0.548, 0.677, 0.765, 0.558]
  - track 49 at frame 166: holes 2, rim-vs-core 0.41, rim-vs-outside 1.17, heterogeneity 0.23; core [0.071, 0.632, 0.549, 0.384, 0.972, 0.217] rim [0.18, 0.403, 0.588, 0.59, 0.894, 0.454]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.16, rim/outside 0.861 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.558)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.693, rim/outside 25.7 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.565)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 22.8 (aggregate of 162 individuals; 141/162 membrane-like individually; rim level 0.848)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.47, rim/outside 18.7 (aggregate of 162 individuals; 157/162 membrane-like individually; rim level 0.872)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 21.8 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.878)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.91, rim/outside 21.8 (aggregate of 162 individuals; 159/162 membrane-like individually; rim level 0.758)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=50500, R_eq 9.46): ['L link', 'membrane (wall)', 'M wall material']; #4 (t=50500, R_eq 11.97): ['L link', 'membrane (wall)', 'M wall material']; #5 (t=50500, R_eq 8.35): ['L link', 'membrane (wall)', 'M wall material']; #49 (t=83000, R_eq 15.35, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 31 of 162 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
