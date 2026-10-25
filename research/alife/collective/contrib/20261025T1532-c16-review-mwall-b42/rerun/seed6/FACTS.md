# Evidence pack: pcell-mwall-b42 (seed 6)

- world: `../../../20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 543s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1508-c14-pcell-mwall-b42-metabolic-claim/world.py --out collective/contrib/20261025T1532-c16-review-mwall-b42/rerun/seed6 --seeds 6 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6276], min area 6 px

## Measurements
- components: final 31, mean 27.2, max 31; occupancy final 0.33
- tracks: 57; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 14.17 (1 = constant size)
- enclosures: components with a hole mean 4.69, final 7; holes at thresholds 0.2/0.35/0.5 final [0, 7, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 31, 31], H1 [23, 15, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.000499/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 2
- channel total drift (end/start - 1): [-0.4753, -0.6843, 0.0963, -0.0597, -0.6426, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 0, rim-vs-core 0.64, rim-vs-outside 0.89, heterogeneity 0.22; core [0.239, 0.554, 0.837, 0.725, 0.832, 0.643] rim [0.444, 0.113, 0.506, 0.65, 0.594, 0.584]
  - track 7 at frame 101: holes 0, rim-vs-core 0.72, rim-vs-outside 1.28, heterogeneity 0.24; core [0.117, 0.678, 0.702, 0.486, 0.898, 0.377] rim [0.36, 0.178, 0.644, 0.785, 0.74, 0.682]
  - track 9 at frame 101: holes 0, rim-vs-core 0.56, rim-vs-outside 0.88, heterogeneity 0.20; core [0.229, 0.484, 0.791, 0.752, 0.828, 0.618] rim [0.417, 0.118, 0.513, 0.638, 0.605, 0.571]
  - track 49 at frame 165: holes 0, rim-vs-core 0.67, rim-vs-outside 1.30, heterogeneity 0.22; core [0.129, 0.737, 0.72, 0.567, 0.854, 0.416] rim [0.347, 0.224, 0.66, 0.775, 0.774, 0.699]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 168 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.21, rim/outside 0.863 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.566)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 23.6 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.512)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 22.1 (aggregate of 168 individuals; 124/168 membrane-like individually; rim level 0.834)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 19.4 (aggregate of 168 individuals; 163/168 membrane-like individually; rim level 0.878)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 21.9 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.878)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.1, rim/outside 20.6 (aggregate of 168 individuals; 162/168 membrane-like individually; rim level 0.783)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #1 (t=50500, R_eq 5.41): ['membrane (wall)', 'M wall material']; #7 (t=50500, R_eq 6.84): ['L link', 'membrane (wall)', 'M wall material']; #9 (t=50500, R_eq 5.56): ['L link', 'membrane (wall)', 'M wall material']; #49 (t=82500, R_eq 6.28): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 24 of 168 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
