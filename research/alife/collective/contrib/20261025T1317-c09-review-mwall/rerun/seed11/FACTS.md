# Evidence pack: pcell-mwall (seed 11)

- world: `../../../20261025T1345-c14-pcell-mwall-claim/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 507s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1345-c14-pcell-mwall-claim/world.py --out collective/contrib/20261025T1317-c09-review-mwall/rerun/seed11 --seeds 11 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5638], min area 6 px

## Measurements
- components: final 18, mean 17.2, max 21; occupancy final 0.40
- tracks: 66; persistent (alive >= 50% of run): 17; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 16.92 (1 = constant size)
- enclosures: components with a hole mean 6.60, final 10; holes at thresholds 0.2/0.35/0.5 final [7, 12, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 18, 18], H1 [16, 14, 3]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.000782/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10000, default): splits 16, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.25, nucleations 8
- channel total drift (end/start - 1): [-0.6307, -0.5449, 0.5171, 0.0449, -0.3963, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 101: holes 0, rim-vs-core 0.76, rim-vs-outside 0.91, heterogeneity 0.22; core [0.236, 0.667, 0.917, 0.746, 0.921, 0.521] rim [0.397, 0.143, 0.503, 0.61, 0.672, 0.384]
  - track 22 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 1.22, heterogeneity 0.21; core [0.184, 0.614, 0.658, 0.506, 0.927, 0.274] rim [0.37, 0.205, 0.634, 0.769, 0.782, 0.558]
  - track 25 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.76, heterogeneity 0.22; core [0.265, 0.582, 0.864, 0.708, 0.827, 0.547] rim [0.432, 0.135, 0.472, 0.608, 0.514, 0.427]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 3.7, rim/outside 0.954 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.494)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.701, rim/outside 6.08 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.506)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 5.21 (aggregate of 103 individuals; 53/103 membrane-like individually; rim level 0.74)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.26, rim/outside 4.63 (aggregate of 103 individuals; 84/103 membrane-like individually; rim level 0.716)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 4.93 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.86)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.15, rim/outside 4.63 (aggregate of 103 individuals; 87/103 membrane-like individually; rim level 0.557)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #7 (t=50500, R_eq 5.14): ['membrane (wall)', 'M wall material']; #22 (t=50500, R_eq 7.44): ['L link', 'membrane (wall)', 'M wall material']; #25 (t=50500, R_eq 5.61): ['L link', 'membrane (wall)', 'M wall material']; #57 (t=94000, R_eq 14.09, ring): ['membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
