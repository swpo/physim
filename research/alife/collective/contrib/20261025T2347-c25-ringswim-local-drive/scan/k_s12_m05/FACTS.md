# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 81s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s12_m05 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5331], min area 6 px

## Measurements
- components: final 17, mean 15.3, max 30; occupancy final 0.31
- tracks: 185; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.72 (1 = constant size)
- enclosures: components with a hole mean 7.85, final 14; holes at thresholds 0.2/0.35/0.5 final [0, 14, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [17, 17, 13]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0134/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 1000, default): splits 72, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 3, merges 5, merge/split ratio 0.069, nucleations 1
- channel total drift (end/start - 1): [-0.4087, -0.734, -0.0627, -0.172]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 116 at frame 134: holes 0, rim-vs-core 0.40, rim-vs-outside 0.79, heterogeneity 0.17; core [0.119, 0.79, 0.67, 0.814] rim [0.287, 0.47, 0.632, 0.642]
  - track 106 at frame 114: holes 1, rim-vs-core 0.29, rim-vs-outside 0.81, heterogeneity 0.21; core [0.103, 0.796, 0.624, 0.627] rim [0.222, 0.536, 0.562, 0.608]
  - track 122 at frame 143: holes 0, rim-vs-core 0.21, rim-vs-outside 0.85, heterogeneity 0.18; core [0.089, 0.722, 0.56, 0.679] rim [0.194, 0.552, 0.555, 0.632]
  - track 131 at frame 153: holes 1, rim-vs-core 0.17, rim-vs-outside 0.78, heterogeneity 0.19; core [0.089, 0.693, 0.541, 0.699] rim [0.172, 0.582, 0.543, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 91 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 14.6, rim/outside 0.894 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.524)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 6.11 (aggregate of 91 individuals; 0/91 membrane-like individually; rim level 0.73)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.87, rim/outside 5.1 (aggregate of 91 individuals; 77/91 membrane-like individually; rim level 0.679)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.23, rim/outside 5.06 (aggregate of 91 individuals; 70/91 membrane-like individually; rim level 0.726)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #116 (t=6700, R_eq 7.2): none; #106 (t=5700, R_eq 9.2, ring): ['L link', 'membrane (wall)']; #122 (t=7150, R_eq 9.44): ['L link', 'membrane (wall)']; #131 (t=7650, R_eq 12.77, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 44 of 91 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
