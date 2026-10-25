# Evidence pack: pcell (seed 3)

- world: `../world_y07.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 30s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0910-c01-review-pcell-yield/world_y07.py --out collective/contrib/20261025T0910-c01-review-pcell-yield/rerun_y07 --seeds 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6], min area 6 px

## Measurements
- components: final 22, mean 18.6, max 52; occupancy final 0.30
- tracks: 124; persistent (alive >= 50% of run): 18; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 24.83 (1 = constant size)
- enclosures: components with a hole mean 6.28, final 9; holes at thresholds 0.2/0.35/0.5 final [0, 9, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 22, 22], H1 [17, 13, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 1000, default): splits 24, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.417, nucleations 5
- channel total drift (end/start - 1): [-0.4342, -0.6965, -0.0293, -0.2316]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 72 at frame 103: holes 0, rim-vs-core 0.58, rim-vs-outside 0.87, heterogeneity 0.22; core [0.153, 0.694, 0.679, 0.508] rim [0.384, 0.226, 0.633, 0.767]
  - track 77 at frame 104: holes 0, rim-vs-core 0.25, rim-vs-outside 0.88, heterogeneity 0.21; core [0.138, 0.585, 0.658, 0.54] rim [0.258, 0.404, 0.627, 0.652]
  - track 82 at frame 104: holes 1, rim-vs-core 0.44, rim-vs-outside 0.74, heterogeneity 0.23; core [0.113, 0.65, 0.605, 0.484] rim [0.302, 0.278, 0.553, 0.627]
  - track 116 at frame 185: holes 1, rim-vs-core 0.31, rim-vs-outside 0.74, heterogeneity 0.21; core [0.099, 0.632, 0.616, 0.434] rim [0.207, 0.38, 0.595, 0.574]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 112 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.18, rim/outside 0.832 (aggregate of 112 individuals; 0/112 membrane-like individually; rim level 0.59)
  - radial K particles: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.742, rim/outside 24.8 (aggregate of 112 individuals; 1/112 membrane-like individually; rim level 0.538)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 20.1 (aggregate of 112 individuals; 80/112 membrane-like individually; rim level 0.743)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.84, rim/outside 17.1 (aggregate of 112 individuals; 108/112 membrane-like individually; rim level 0.761)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #72 (t=5150, R_eq 7.11): ['L link', 'membrane (wall)']; #77 (t=5200, R_eq 7.44): ['L link', 'membrane (wall)']; #82 (t=5200, R_eq 9.34, ring): ['L link', 'membrane (wall)']; #116 (t=9250, R_eq 10.72, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 35 of 112 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
