# Evidence pack: pcell-mwall-b42 (seed 5)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 388s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev8/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev8/rerun/seed5 --seeds 5 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6103], min area 6 px

## Measurements
- components: final 30, mean 25.2, max 30; occupancy final 0.34
- tracks: 62; persistent (alive >= 50% of run): 20; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 12.33 (1 = constant size)
- enclosures: components with a hole mean 5.47, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 30, 30], H1 [22, 18, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.000402/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 10000, default): splits 19, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 4, merges 1, merge/split ratio 0.053, nucleations 1
- channel total drift (end/start - 1): [-0.4896, -0.6767, 0.1255, -0.1787, -0.6158, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 1.01, heterogeneity 0.20; core [0.221, 0.604, 0.847, 0.857, 0.795, 0.734] rim [0.314, 0.373, 0.614, 0.625, 0.723, 0.572]
  - track 6 at frame 101: holes 0, rim-vs-core 0.67, rim-vs-outside 1.30, heterogeneity 0.23; core [0.092, 0.631, 0.632, 0.454, 0.955, 0.32] rim [0.341, 0.212, 0.635, 0.768, 0.828, 0.623]
  - track 11 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 1.29, heterogeneity 0.22; core [0.132, 0.582, 0.635, 0.513, 0.881, 0.346] rim [0.299, 0.346, 0.674, 0.712, 0.8, 0.606]
  - track 58 at frame 180: holes 1, rim-vs-core 0.43, rim-vs-outside 1.09, heterogeneity 0.24; core [0.125, 0.599, 0.678, 0.533, 0.995, 0.368] rim [0.258, 0.286, 0.587, 0.619, 0.827, 0.536]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.68, rim/outside 0.871 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.566)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.701, rim/outside 24.8 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.529)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 21 (aggregate of 157 individuals; 121/157 membrane-like individually; rim level 0.822)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.83, rim/outside 17.6 (aggregate of 157 individuals; 152/157 membrane-like individually; rim level 0.85)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.985, rim/outside 21.9 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.895)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.24, rim/outside 18.2 (aggregate of 157 individuals; 152/157 membrane-like individually; rim level 0.746)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #3 (t=50500, R_eq 5.2): ['membrane (wall)', 'M wall material']; #6 (t=50500, R_eq 8.2): ['L link', 'membrane (wall)', 'M wall material']; #11 (t=50500, R_eq 6.79): ['L link', 'membrane (wall)', 'M wall material']; #58 (t=90000, R_eq 8.69, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 157 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
