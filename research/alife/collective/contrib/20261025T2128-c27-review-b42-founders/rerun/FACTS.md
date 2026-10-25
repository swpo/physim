# Evidence pack: pcell-mwall-b42 (seed 21)

- world: `../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 398s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27f/world.py --out collective/contrib/wip-c27f/rerun --seeds 21 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6179], min area 6 px

## Measurements
- components: final 29, mean 25.6, max 30; occupancy final 0.33
- tracks: 72; persistent (alive >= 50% of run): 20; longest 201 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 22.92 (1 = constant size)
- enclosures: components with a hole mean 6.30, final 7; holes at thresholds 0.2/0.35/0.5 final [0, 7, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 29, 29], H1 [25, 17, 0]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.00163/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 10000, default): splits 24, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.478, -0.6789, 0.0959, -0.1015, -0.6255, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 1.23, heterogeneity 0.21; core [0.151, 0.619, 0.764, 0.702, 0.837, 0.512] rim [0.264, 0.419, 0.65, 0.682, 0.776, 0.565]
  - track 9 at frame 101: holes 0, rim-vs-core 0.65, rim-vs-outside 1.26, heterogeneity 0.22; core [0.146, 0.666, 0.723, 0.585, 0.875, 0.404] rim [0.359, 0.189, 0.646, 0.772, 0.731, 0.705]
  - track 11 at frame 101: holes 0, rim-vs-core 0.71, rim-vs-outside 0.86, heterogeneity 0.20; core [0.226, 0.662, 0.851, 0.856, 0.766, 0.744] rim [0.422, 0.156, 0.528, 0.591, 0.64, 0.623]
  - track 61 at frame 156: holes 1, rim-vs-core 0.35, rim-vs-outside 1.01, heterogeneity 0.22; core [0.119, 0.542, 0.636, 0.582, 0.998, 0.354] rim [0.232, 0.304, 0.566, 0.617, 0.868, 0.52]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 156 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 8.2, rim/outside 0.874 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.563)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 21.3 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.514)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 18.2 (aggregate of 156 individuals; 123/156 membrane-like individually; rim level 0.809)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.57, rim/outside 15.6 (aggregate of 156 individuals; 148/156 membrane-like individually; rim level 0.839)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 18.5 (aggregate of 156 individuals; 0/156 membrane-like individually; rim level 0.884)
  - radial M wall material: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 4.08, rim/outside 16.3 (aggregate of 156 individuals; 150/156 membrane-like individually; rim level 0.738)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall), M wall material
- membrane-like channels per top track at mid-life: #5 (t=50500, R_eq 6.26): ['L link', 'membrane (wall)', 'M wall material']; #9 (t=50500, R_eq 6.15): ['L link', 'membrane (wall)', 'M wall material']; #11 (t=50500, R_eq 4.69): ['membrane (wall)', 'M wall material']; #61 (t=78000, R_eq 9.1, ring): ['L link', 'membrane (wall)', 'M wall material']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 32 of 156 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
