# Evidence pack: ringswim-waste (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev12/a3 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5829], min area 6 px

## Measurements
- components: final 14, mean 13.4, max 23; occupancy final 0.20
- tracks: 258; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.04, final 5; holes at thresholds 0.2/0.35/0.5 final [1, 5, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 14], H1 [14, 9, 4]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0152/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 1000, default): splits 110, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.036, nucleations 0
- channel total drift (end/start - 1): [-0.311, -0.817, -0.3019, -0.4855]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 142 at frame 119: holes 1, rim-vs-core 0.28, rim-vs-outside 0.87, heterogeneity 0.22; core [0.113, 0.819, 0.659, 0.547] rim [0.217, 0.589, 0.554, 0.599]
  - track 152 at frame 123: holes 1, rim-vs-core 0.24, rim-vs-outside 0.86, heterogeneity 0.18; core [0.059, 0.679, 0.418, 0.605] rim [0.196, 0.51, 0.496, 0.676]
  - track 185 at frame 161: holes 0, rim-vs-core 0.48, rim-vs-outside 0.72, heterogeneity 0.20; core [0.324, 0.7, 0.919, 0.905] rim [0.383, 0.434, 0.634, 0.64]
  - track 209 at frame 180: holes 0, rim-vs-core 0.56, rim-vs-outside 0.44, heterogeneity 0.16; core [0.255, 0.683, 0.854, 0.824] rim [0.357, 0.392, 0.642, 0.412]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.65, rim/outside 0.834 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.553)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 9.67 (aggregate of 81 individuals; 4/81 membrane-like individually; rim level 0.741)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 7.63 (aggregate of 81 individuals; 56/81 membrane-like individually; rim level 0.733)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.86, rim/outside 8.09 (aggregate of 81 individuals; 51/81 membrane-like individually; rim level 0.732)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #142 (t=5950, R_eq 8.31, ring): ['L link', 'membrane (wall)']; #152 (t=6150, R_eq 12.3): none; #185 (t=8050, R_eq 4.07): none; #209 (t=9000, R_eq 4.72): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
