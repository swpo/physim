# Evidence pack: pcell-mwall (seed 5)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 499s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1358-c13-review-pcell-mwall/world.py --out collective/contrib/20261025T1358-c13-review-pcell-mwall/rerun/seed5 --seeds 5 --spf 500 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5606], min area 6 px

## Measurements
- components: final 21, mean 21.8, max 24; occupancy final 0.42
- tracks: 65; persistent (alive >= 50% of run): 21; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.69 (1 = constant size)
- enclosures: components with a hole mean 9.49, final 14; holes at thresholds 0.2/0.35/0.5 final [2, 14, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 21, 21], H1 [19, 15, 1]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.000862/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10000, default): splits 19, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.158, nucleations 10
- channel total drift (end/start - 1): [-0.6257, -0.553, 0.5297, -0.0503, -0.4076, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 101: holes 0, rim-vs-core 0.70, rim-vs-outside 0.88, heterogeneity 0.21; core [0.248, 0.604, 0.9, 0.774, 0.861, 0.615] rim [0.401, 0.136, 0.506, 0.588, 0.672, 0.488]
  - track 19 at frame 101: holes 2, rim-vs-core 0.29, rim-vs-outside 1.06, heterogeneity 0.23; core [0.125, 0.608, 0.618, 0.423, 1.0, 0.264] rim [0.205, 0.421, 0.6, 0.535, 0.902, 0.416]
  - track 26 at frame 101: holes 0, rim-vs-core 0.62, rim-vs-outside 0.85, heterogeneity 0.20; core [0.254, 0.539, 0.869, 0.761, 0.833, 0.588] rim [0.409, 0.136, 0.508, 0.622, 0.648, 0.493]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 4.35, rim/outside 0.969 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.467)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 5.42 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.497)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 4.47 (aggregate of 131 individuals; 68/131 membrane-like individually; rim level 0.718)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.39, rim/outside 3.83 (aggregate of 131 individuals; 114/131 membrane-like individually; rim level 0.686)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 4.57 (aggregate of 131 individuals; 1/131 membrane-like individually; rim level 0.881)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.28, rim/outside 3.88 (aggregate of 131 individuals; 120/131 membrane-like individually; rim level 0.556)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #16 (t=50500, R_eq 5.11): ['membrane (wall)', 'M wall material']; #19 (t=50500, R_eq 10.91): ['membrane (wall)', 'M wall material']; #26 (t=50500, R_eq 5.17): ['membrane (wall)', 'M wall material']; #45 (t=73000, R_eq 15.15, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 48 of 131 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
