# Evidence pack: ringswim-waste-chi0 (seed 23)

- world: `../../../20261025T0806-c07-ringswim-claim/world_chi0.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0806-c07-ringswim-claim/world_chi0.py --out collective/contrib/20261025T1030-c09-review-ringswim/chi0/seed23 --seeds 23 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5611], min area 6 px

## Measurements
- components: final 21, mean 21.5, max 27; occupancy final 0.23
- tracks: 224; persistent (alive >= 50% of run): 6; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.91 (1 = constant size)
- enclosures: components with a hole mean 2.59, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 21], H1 [21, 20, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.0365/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 1000, default): splits 70, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 49, merge/split ratio 0.7, nucleations 0
- channel total drift (end/start - 1): [-0.3733, -0.7881, -0.0952, -0.2095]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 102 at frame 128: holes 1, rim-vs-core 0.27, rim-vs-outside 0.84, heterogeneity 0.17; core [0.093, 0.716, 0.659, 0.676] rim [0.218, 0.499, 0.617, 0.597]
  - track 46 at frame 72: holes 0, rim-vs-core 0.42, rim-vs-outside 0.94, heterogeneity 0.19; core [0.091, 0.777, 0.719, 0.59] rim [0.301, 0.448, 0.64, 0.732]
  - track 122 at frame 136: holes 0, rim-vs-core 0.46, rim-vs-outside 1.01, heterogeneity 0.21; core [0.111, 0.878, 0.837, 0.465] rim [0.254, 0.543, 0.66, 0.695]
  - track 103 at frame 113: holes 0, rim-vs-core 0.56, rim-vs-outside 0.50, heterogeneity 0.17; core [0.192, 0.695, 0.762, 0.798] rim [0.37, 0.309, 0.623, 0.465]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 15.1, rim/outside 0.849 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.536)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 11.4 (aggregate of 129 individuals; 1/129 membrane-like individually; rim level 0.727)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 9.01 (aggregate of 129 individuals; 1/129 membrane-like individually; rim level 0.737)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.55, rim/outside 9.83 (aggregate of 129 individuals; 118/129 membrane-like individually; rim level 0.808)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #102 (t=6400, R_eq 8.06, ring): ['membrane (wall)']; #46 (t=3600, R_eq 7.8): ['membrane (wall)']; #122 (t=6800, R_eq 6.93): ['membrane (wall)']; #103 (t=5650, R_eq 5.94): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 19 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
