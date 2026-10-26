# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 78s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2347-c25-ringswim-local-drive/scan/k_s6_m15 --seeds 0 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5727], min area 6 px

## Measurements
- components: final 1, mean 2.8, max 31; occupancy final 0.32
- tracks: 173; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.37, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 1, 1], H1 [2, 2, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.034/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 1000, default): splits 45, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 0.822, nucleations 4
- channel total drift (end/start - 1): [-0.4884, -0.7174, 0.1516, -0.0984]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 12: holes 0, rim-vs-core 0.63, rim-vs-outside 0.43, heterogeneity 0.16; core [0.29, 0.677, 0.777, 0.886] rim [0.478, 0.307, 0.542, 0.477]
  - track 59 at frame 13: holes 0, rim-vs-core 0.59, rim-vs-outside 0.36, heterogeneity 0.14; core [0.275, 0.612, 0.704, 0.887] rim [0.461, 0.329, 0.565, 0.429]
  - track 4 at frame 8: holes 0, rim-vs-core 0.44, rim-vs-outside 0.82, heterogeneity 0.18; core [0.267, 0.788, 0.835, 0.865] rim [0.41, 0.456, 0.648, 0.685]
  - track 23 at frame 10: holes 0, rim-vs-core 0.44, rim-vs-outside 0.83, heterogeneity 0.17; core [0.196, 0.735, 0.708, 0.865] rim [0.405, 0.417, 0.616, 0.663]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 2.49, rim/outside 0.898 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.538)
  - radial K catalyst: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.716, rim/outside 2.71 (aggregate of 12 individuals; 1/12 membrane-like individually; rim level 0.332)
  - radial L link: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 2.33 (aggregate of 12 individuals; 1/12 membrane-like individually; rim level 0.347)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 2.82 (aggregate of 12 individuals; 2/12 membrane-like individually; rim level 0.371)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35 (t=600, R_eq 5.38): none; #59 (t=650, R_eq 5.86): none; #4 (t=400, R_eq 4.79): none; #23 (t=500, R_eq 6.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 3 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
