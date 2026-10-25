# Evidence pack: pcell-ring (seed 0)

- world: `../world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 495s; status ok
- command: `python -m labkit.run scratch/c14/world.py --out scratch/c14/pack --seeds 0 --frames 200 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7934], min area 6 px

## Measurements
- components: final 12, mean 23.7, max 34; occupancy final 0.25
- tracks: 44; persistent (alive >= 50% of run): 23; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 19.05 (1 = constant size)
- enclosures: components with a hole mean 4.75, final 5; holes at thresholds 0.2/0.35/0.5 final [17, 5, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 12, 12], H1 [8, 7, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.000717/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 10000, default): splits 3, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 1
- channel total drift (end/start - 1): [-0.5355, -0.5889, 0.3551, -0.2818, -0.4711]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.78, heterogeneity 0.21; core [0.22, 0.572, 0.719, 0.751, 0.929] rim [0.412, 0.141, 0.447, 0.64, 0.747]
  - track 6 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 1.13, heterogeneity 0.22; core [0.137, 0.631, 0.588, 0.559, 0.939] rim [0.27, 0.354, 0.537, 0.638, 0.851]
  - track 16 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.92, heterogeneity 0.20; core [0.122, 0.537, 0.502, 0.517, 0.999] rim [0.196, 0.374, 0.508, 0.614, 0.949]
  - track 18 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.77, heterogeneity 0.19; core [0.262, 0.558, 0.787, 0.833, 0.833] rim [0.442, 0.155, 0.476, 0.635, 0.7]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 4.06, rim/outside 0.796 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.529)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.619, rim/outside 25.5 (aggregate of 132 individuals; 1/132 membrane-like individually; rim level 0.484)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 29.6 (aggregate of 132 individuals; 70/132 membrane-like individually; rim level 0.782)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.92, rim/outside 21.9 (aggregate of 132 individuals; 98/132 membrane-like individually; rim level 0.781)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 26.9 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 0.88)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #3 (t=50500, R_eq 5.81): ['L link', 'membrane (wall)']; #6 (t=50500, R_eq 7.82, ring): ['L link', 'membrane (wall)']; #16 (t=50500, R_eq 10.78, ring): ['K particles', 'L link', 'membrane (wall)']; #18 (t=50500, R_eq 4.79): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 132 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
