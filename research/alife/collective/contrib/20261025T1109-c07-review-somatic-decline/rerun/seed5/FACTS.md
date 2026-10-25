# Evidence pack: pcell-multilevel-lowmu (seed 5)

- world: `../../../20261025T0923-c06-pcell-somatic-decline/world.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 201 frames x 500 steps x dt 1.0 = time 100000; grid [128, 128]; wall 418s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0923-c06-pcell-somatic-decline/world.py --out collective/contrib/_c07rev19/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6234], min area 6 px

## Measurements
- components: final 28, mean 27.3, max 30; occupancy final 0.34
- tracks: 61; persistent (alive >= 50% of run): 28; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.83 (1 = constant size)
- enclosures: components with a hole mean 7.35, final 8; holes at thresholds 0.2/0.35/0.5 final [6, 9, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 28], H1 [22, 10, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.000531/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10000, default): splits 17, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.059, nucleations 1
- channel total drift (end/start - 1): [-0.5436, -0.6285, 0.284, -0.1473, -0.5721]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 101: holes 0, rim-vs-core 0.59, rim-vs-outside 0.74, heterogeneity 0.20; core [0.21, 0.595, 0.805, 0.693, 0.713] rim [0.411, 0.143, 0.534, 0.666, 0.537]
  - track 16 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.76, heterogeneity 0.17; core [0.236, 0.601, 0.824, 0.791, 0.659] rim [0.401, 0.182, 0.521, 0.608, 0.637]
  - track 22 at frame 101: holes 1, rim-vs-core 0.30, rim-vs-outside 0.85, heterogeneity 0.21; core [0.14, 0.565, 0.657, 0.531, 0.814] rim [0.251, 0.322, 0.57, 0.587, 0.713]
  - track 57 at frame 176: holes 1, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.22; core [0.115, 0.544, 0.689, 0.551, 0.994] rim [0.198, 0.339, 0.606, 0.591, 0.872]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 168 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.51, rim/outside 0.904 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.536)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 17.4 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.513)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 14.4 (aggregate of 168 individuals; 125/168 membrane-like individually; rim level 0.81)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.64, rim/outside 12.1 (aggregate of 168 individuals; 158/168 membrane-like individually; rim level 0.839)  MEMBRANE-LIKE
  - radial mean yield / 2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 13.9 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.755)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #15 (t=50500, R_eq 5.92): ['L link', 'membrane (wall)']; #16 (t=50500, R_eq 5.29): ['membrane (wall)']; #22 (t=50500, R_eq 9.47, ring): ['L link', 'membrane (wall)']; #57 (t=88000, R_eq 10.78, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 31 of 168 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
