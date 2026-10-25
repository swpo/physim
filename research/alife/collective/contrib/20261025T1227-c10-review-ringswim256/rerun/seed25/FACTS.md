# Evidence pack: ringswim-waste-256 (seed 25)

- world: `../../../20261025T0922-c07-ringswim-256/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 604s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0922-c07-ringswim-256/world.py --out collective/contrib/20261025T1227-c10-review-ringswim256/rerun/seed25 --seeds 25 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5558], min area 6 px

## Measurements
- components: final 32, mean 39.4, max 73; occupancy final 0.20
- tracks: 2027; persistent (alive >= 50% of run): 0; longest 32 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 27.26, final 29; holes at thresholds 0.2/0.35/0.5 final [4, 34, 35]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 36, 32], H1 [38, 36, 18]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0372/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 2000, default): splits 671, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 591, merge/split ratio 0.881, nucleations 8
- channel total drift (end/start - 1): [-0.3282, -0.8034, -0.2716, -0.4675]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 970 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.87, heterogeneity 0.22; core [0.11, 0.788, 0.613, 0.526] rim [0.294, 0.454, 0.529, 0.644]
  - track 1190 at frame 124: holes 1, rim-vs-core 0.19, rim-vs-outside 0.82, heterogeneity 0.18; core [0.064, 0.637, 0.426, 0.621] rim [0.167, 0.487, 0.485, 0.658]
  - track 116 at frame 13: holes 0, rim-vs-core 0.37, rim-vs-outside 0.78, heterogeneity 0.20; core [0.11, 0.719, 0.543, 0.658] rim [0.305, 0.409, 0.527, 0.676]
  - track 123 at frame 13: holes 1, rim-vs-core 0.28, rim-vs-outside 0.76, heterogeneity 0.20; core [0.128, 0.753, 0.656, 0.618] rim [0.226, 0.528, 0.524, 0.594]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 8.91, rim/outside 0.774 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.532)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 9.74 (aggregate of 214 individuals; 12/214 membrane-like individually; rim level 0.65)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 7.17 (aggregate of 214 individuals; 152/214 membrane-like individually; rim level 0.556)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.08, rim/outside 7.96 (aggregate of 214 individuals; 154/214 membrane-like individually; rim level 0.575)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #970 (t=10100, R_eq 8.29, ring): ['L link', 'membrane (wall)']; #1190 (t=12400, R_eq 11.58): none; #116 (t=1300, R_eq 7.63): ['L link', 'membrane (wall)']; #123 (t=1300, R_eq 8.9, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 117 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
