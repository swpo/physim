# Evidence pack: pcell-mwall (seed 9)

- world: `../../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 844s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1338-c12-review-pcell-mwall/world.py --out collective/contrib/20261025T1338-c12-review-pcell-mwall/rerun/seed9 --seeds 9 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.582], min area 6 px

## Measurements
- components: final 18, mean 21.5, max 27; occupancy final 0.40
- tracks: 74; persistent (alive >= 50% of run): 17; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.00 (1 = constant size)
- enclosures: components with a hole mean 7.92, final 11; holes at thresholds 0.2/0.35/0.5 final [7, 15, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 18, 18], H1 [17, 11, 3]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.000374/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 21, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.238, nucleations 4
- channel total drift (end/start - 1): [-0.6341, -0.5331, 0.5356, 0.1212, -0.3903, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 101: holes 0, rim-vs-core 0.75, rim-vs-outside 0.89, heterogeneity 0.20; core [0.235, 0.657, 0.913, 0.812, 0.832, 0.683] rim [0.407, 0.172, 0.492, 0.568, 0.765, 0.451]
  - track 35 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 0.70, heterogeneity 0.21; core [0.227, 0.644, 0.838, 0.797, 0.793, 0.601] rim [0.39, 0.151, 0.494, 0.577, 0.525, 0.511]
  - track 36 at frame 101: holes 2, rim-vs-core 0.39, rim-vs-outside 1.07, heterogeneity 0.23; core [0.119, 0.658, 0.595, 0.422, 0.922, 0.254] rim [0.211, 0.388, 0.59, 0.566, 0.813, 0.441]
  - track 68 at frame 171: holes 0, rim-vs-core 0.61, rim-vs-outside 1.25, heterogeneity 0.22; core [0.14, 0.729, 0.76, 0.591, 0.921, 0.372] rim [0.325, 0.23, 0.646, 0.749, 0.782, 0.55]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 4.63, rim/outside 0.916 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.475)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.683, rim/outside 7.2 (aggregate of 126 individuals; 1/126 membrane-like individually; rim level 0.493)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 6.26 (aggregate of 126 individuals; 61/126 membrane-like individually; rim level 0.734)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.89, rim/outside 5.49 (aggregate of 126 individuals; 110/126 membrane-like individually; rim level 0.707)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 5.99 (aggregate of 126 individuals; 1/126 membrane-like individually; rim level 0.843)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.06, rim/outside 5.61 (aggregate of 126 individuals; 116/126 membrane-like individually; rim level 0.589)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #26 (t=50500, R_eq 4.79): ['membrane (wall)', 'M wall material']; #35 (t=50500, R_eq 5.17): ['membrane (wall)', 'M wall material']; #36 (t=50500, R_eq 11.53, ring): ['membrane (wall)', 'M wall material']; #68 (t=85500, R_eq 6.1): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 43 of 126 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
