# Evidence pack: ringswim-waste-chi0 (seed 7)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [128, 128]; wall 263s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out collective/contrib/20261025T1028-c02-review-c07-ringswim-c2/chi0/seed7 --seeds 7 --spf 100 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5583], min area 6 px

## Measurements
- components: final 24, mean 22.5, max 27; occupancy final 0.23
- tracks: 261; persistent (alive >= 50% of run): 4; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.34 (1 = constant size)
- enclosures: components with a hole mean 2.04, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [23, 20, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.0249/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 2000, default): splits 92, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 62, merge/split ratio 0.674, nucleations 0
- channel total drift (end/start - 1): [-0.3765, -0.7946, -0.0876, -0.2715]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 123 at frame 136: holes 0, rim-vs-core 0.44, rim-vs-outside 0.91, heterogeneity 0.20; core [0.086, 0.776, 0.733, 0.554] rim [0.305, 0.434, 0.631, 0.703]
  - track 52 at frame 84: holes 0, rim-vs-core 0.56, rim-vs-outside 0.54, heterogeneity 0.16; core [0.161, 0.723, 0.791, 0.779] rim [0.335, 0.309, 0.61, 0.503]
  - track 87 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 1.01, heterogeneity 0.22; core [0.125, 0.844, 0.848, 0.673] rim [0.239, 0.603, 0.718, 0.602]
  - track 138 at frame 136: holes 0, rim-vs-core 0.44, rim-vs-outside 0.90, heterogeneity 0.19; core [0.082, 0.786, 0.751, 0.569] rim [0.288, 0.436, 0.634, 0.702]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 139 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 15.1, rim/outside 0.846 (aggregate of 139 individuals; 0/139 membrane-like individually; rim level 0.535)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 13.2 (aggregate of 139 individuals; 0/139 membrane-like individually; rim level 0.735)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 10.4 (aggregate of 139 individuals; 0/139 membrane-like individually; rim level 0.772)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.42, rim/outside 12.4 (aggregate of 139 individuals; 126/139 membrane-like individually; rim level 0.823)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #123 (t=13600, R_eq 7.36): ['membrane (wall)']; #52 (t=8400, R_eq 5.86): ['membrane (wall)']; #87 (t=10100, R_eq 6.68): ['membrane (wall)']; #138 (t=13600, R_eq 7.25): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 139 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
