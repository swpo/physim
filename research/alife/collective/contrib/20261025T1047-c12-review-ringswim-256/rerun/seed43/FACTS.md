# Evidence pack: ringswim-waste-256 (seed 43)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [256, 256]; wall 1025s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1047-c12-review-ringswim-256/world.py --out collective/contrib/20261025T1047-c12-review-ringswim-256/rerun/seed43 --seeds 43 --size 256 256 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5569], min area 6 px

## Measurements
- components: final 36, mean 43.4, max 81; occupancy final 0.19
- tracks: 2264; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 28.59, final 28; holes at thresholds 0.2/0.35/0.5 final [2, 32, 39]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 42, 35], H1 [42, 41, 14]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.0446/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 2000, default): splits 771, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 647, merge/split ratio 0.839, nucleations 10
- channel total drift (end/start - 1): [-0.3363, -0.8113, -0.2525, -0.4424]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1652 at frame 158: holes 1, rim-vs-core 0.28, rim-vs-outside 0.68, heterogeneity 0.20; core [0.124, 0.705, 0.615, 0.678] rim [0.225, 0.5, 0.494, 0.573]
  - track 1110 at frame 106: holes 1, rim-vs-core 0.21, rim-vs-outside 0.82, heterogeneity 0.19; core [0.105, 0.75, 0.585, 0.56] rim [0.181, 0.565, 0.535, 0.614]
  - track 1807 at frame 168: holes 1, rim-vs-core 0.19, rim-vs-outside 0.80, heterogeneity 0.23; core [0.085, 0.729, 0.534, 0.548] rim [0.194, 0.581, 0.549, 0.588]
  - track 2006 at frame 187: holes 0, rim-vs-core 0.55, rim-vs-outside 0.96, heterogeneity 0.22; core [0.115, 0.849, 0.651, 0.496] rim [0.35, 0.435, 0.605, 0.765]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 241 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.77, rim/outside 0.79 (aggregate of 241 individuals; 0/241 membrane-like individually; rim level 0.534)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 9.25 (aggregate of 241 individuals; 9/241 membrane-like individually; rim level 0.652)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 6.93 (aggregate of 241 individuals; 159/241 membrane-like individually; rim level 0.578)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.01, rim/outside 7.84 (aggregate of 241 individuals; 164/241 membrane-like individually; rim level 0.595)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #1652 (t=15800, R_eq 9.97, ring): ['L link', 'membrane (wall)']; #1110 (t=10600, R_eq 10.39, ring): ['L link', 'membrane (wall)']; #1807 (t=16800, R_eq 12.73): none; #2006 (t=18700, R_eq 7.36): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 121 of 241 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
