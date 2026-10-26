# Evidence pack: ringswim-dl2 (seed 3)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/_c26work/rev4/label --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5405], min area 6 px

## Measurements
- components: final 7, mean 10.0, max 20; occupancy final 0.17
- tracks: 286; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 7.06, final 6; holes at thresholds 0.2/0.35/0.5 final [1, 6, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [7, 6, 5]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.0416/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 1000, default): splits 95, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 75, merge/split ratio 0.789, nucleations 0
- channel total drift (end/start - 1): [-0.2977, -0.8241, -0.3494, -0.5414]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 30: holes 1, rim-vs-core 0.21, rim-vs-outside 0.79, heterogeneity 0.19; core [0.128, 0.734, 0.628, 0.673] rim [0.182, 0.56, 0.531, 0.62]
  - track 0 at frame 22: holes 1, rim-vs-core 0.40, rim-vs-outside 0.83, heterogeneity 0.24; core [0.139, 0.864, 0.679, 0.534] rim [0.29, 0.515, 0.565, 0.604]
  - track 26 at frame 24: holes 1, rim-vs-core 0.21, rim-vs-outside 0.84, heterogeneity 0.22; core [0.131, 0.771, 0.646, 0.628] rim [0.219, 0.598, 0.571, 0.586]
  - track 68 at frame 61: holes 1, rim-vs-core 0.18, rim-vs-outside 0.82, heterogeneity 0.18; core [0.096, 0.693, 0.53, 0.643] rim [0.178, 0.538, 0.523, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 9.37, rim/outside 0.765 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.506)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 8.73 (aggregate of 54 individuals; 7/54 membrane-like individually; rim level 0.646)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 6.42 (aggregate of 54 individuals; 46/54 membrane-like individually; rim level 0.56)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.63, rim/outside 7.34 (aggregate of 54 individuals; 45/54 membrane-like individually; rim level 0.605)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #43 (t=1500, R_eq 11.55, ring): ['K catalyst', 'L link', 'membrane (wall)']; #0 (t=1100, R_eq 8.59, ring): ['L link', 'membrane (wall)']; #26 (t=1200, R_eq 10.6, ring): ['K catalyst', 'L link', 'membrane (wall)']; #68 (t=3050, R_eq 10.57, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 41 of 54 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
