# Evidence pack: pcell-ring (seed 3)

- world: `../../../20261025T1250-c14-pcell-ring-tilt-negative/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 504s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1250-c14-pcell-ring-tilt-negative/world.py --out collective/contrib/20261025T1429-c16-review-ringtilt/rerun/seed3 --seeds 3 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7504], min area 6 px

## Measurements
- components: final 13, mean 19.7, max 37; occupancy final 0.24
- tracks: 50; persistent (alive >= 50% of run): 16; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 33.16 (1 = constant size)
- enclosures: components with a hole mean 4.21, final 6; holes at thresholds 0.2/0.35/0.5 final [9, 6, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 13, 13], H1 [7, 6, 0]
- motion: 17 long-lived tracks moved >= 1 body length; max speed 0.000403/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 10000, default): splits 8, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5799, -0.5352, 0.4562, -0.3277, -0.3945]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 1.24, heterogeneity 0.23; core [0.139, 0.73, 0.603, 0.529, 0.957] rim [0.301, 0.334, 0.628, 0.749, 0.853]
  - track 19 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.94, heterogeneity 0.20; core [0.257, 0.559, 0.806, 0.847, 0.886] rim [0.361, 0.348, 0.604, 0.697, 0.8]
  - track 21 at frame 101: holes 0, rim-vs-core 0.37, rim-vs-outside 0.99, heterogeneity 0.15; core [0.294, 0.488, 0.853, 0.908, 0.839] rim [0.368, 0.366, 0.604, 0.675, 0.839]
  - track 46 at frame 188: holes 0, rim-vs-core 0.65, rim-vs-outside 1.12, heterogeneity 0.23; core [0.114, 0.648, 0.517, 0.468, 0.967] rim [0.338, 0.183, 0.577, 0.787, 0.74]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 4.36, rim/outside 0.799 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.535)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.634, rim/outside 21.2 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.498)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 24 (aggregate of 109 individuals; 66/109 membrane-like individually; rim level 0.777)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.04, rim/outside 18.4 (aggregate of 109 individuals; 88/109 membrane-like individually; rim level 0.771)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 19.6 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.879)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #13 (t=50500, R_eq 6.58): ['L link', 'membrane (wall)']; #19 (t=50500, R_eq 4.98): ['L link', 'membrane (wall)']; #21 (t=50500, R_eq 4.51): none; #46 (t=94000, R_eq 8.39): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 27 of 109 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
