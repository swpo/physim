# Evidence pack: pcell-ring (seed 2)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 382s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1526-c13-review-ring-tilt/world.py --out collective/contrib/20261025T1526-c13-review-ring-tilt/rerun/seed2 --seeds 2 --spf 500 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7708], min area 6 px

## Measurements
- components: final 16, mean 21.5, max 36; occupancy final 0.27
- tracks: 48; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 35.50 (1 = constant size)
- enclosures: components with a hole mean 5.32, final 7; holes at thresholds 0.2/0.35/0.5 final [14, 7, 9]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 16, 16], H1 [9, 7, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.000345/time; max body lengths 3.8
- replication (lineage window K = 20 frames = time 10000, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5519, -0.5816, 0.4156, -0.293, -0.4609]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.94, heterogeneity 0.20; core [0.225, 0.578, 0.818, 0.843, 0.864] rim [0.321, 0.381, 0.538, 0.643, 0.806]
  - track 10 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.89, heterogeneity 0.17; core [0.233, 0.655, 0.812, 0.794, 0.86] rim [0.414, 0.197, 0.473, 0.617, 0.86]
  - track 44 at frame 139: holes 1, rim-vs-core 0.19, rim-vs-outside 0.94, heterogeneity 0.20; core [0.124, 0.522, 0.479, 0.539, 0.972] rim [0.2, 0.399, 0.524, 0.622, 0.902]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 120 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 4.6, rim/outside 0.787 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.52)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.66, rim/outside 24.5 (aggregate of 120 individuals; 2/120 membrane-like individually; rim level 0.506)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 24.2 (aggregate of 120 individuals; 70/120 membrane-like individually; rim level 0.754)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.14, rim/outside 17.9 (aggregate of 120 individuals; 100/120 membrane-like individually; rim level 0.755)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 23.6 (aggregate of 120 individuals; 0/120 membrane-like individually; rim level 0.892)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #1 (t=50500, R_eq 5.23): ['L link', 'membrane (wall)']; #4 (t=50500, R_eq 14.15, ring): ['membrane (wall)']; #10 (t=50500, R_eq 5.2): ['L link', 'membrane (wall)']; #44 (t=69500, R_eq 10.72, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 120 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
