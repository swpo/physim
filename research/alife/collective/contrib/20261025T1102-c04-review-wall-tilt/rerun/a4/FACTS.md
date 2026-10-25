# Evidence pack: ringswim-waste (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 47s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/fba552f4-82e1-5fd3-8aee-1d1a9784fecc/scratchpad/rev12/a4 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5816], min area 6 px

## Measurements
- components: final 3, mean 8.8, max 23; occupancy final 0.07
- tracks: 221; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.84, final 3; holes at thresholds 0.2/0.35/0.5 final [1, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 3, 3], H1 [3, 3, 3]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0154/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 1000, default): splits 91, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.077, nucleations 0
- channel total drift (end/start - 1): [-0.1089, -0.9254, -0.7501, -0.819]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 22: holes 1, rim-vs-core 0.23, rim-vs-outside 0.82, heterogeneity 0.22; core [0.131, 0.793, 0.674, 0.567] rim [0.202, 0.607, 0.557, 0.586]
  - track 154 at frame 118: holes 0, rim-vs-core 0.69, rim-vs-outside 1.02, heterogeneity 0.26; core [0.126, 0.979, 0.762, 0.447] rim [0.396, 0.458, 0.618, 0.772]
  - track 171 at frame 131: holes 1, rim-vs-core 0.19, rim-vs-outside 0.72, heterogeneity 0.20; core [0.066, 0.677, 0.445, 0.667] rim [0.178, 0.527, 0.474, 0.626]
  - track 201 at frame 187: holes 0, rim-vs-core 0.49, rim-vs-outside 0.78, heterogeneity 0.18; core [0.183, 0.753, 0.782, 0.951] rim [0.304, 0.475, 0.616, 0.604]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 6.3, rim/outside 0.698 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.505)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 10.5 (aggregate of 47 individuals; 13/47 membrane-like individually; rim level 0.645)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 7.8 (aggregate of 47 individuals; 30/47 membrane-like individually; rim level 0.598)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 7.76 (aggregate of 47 individuals; 30/47 membrane-like individually; rim level 0.527)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #5 (t=1100, R_eq 10.98, ring): ['K catalyst', 'L link', 'membrane (wall)']; #154 (t=5900, R_eq 6.63): ['L link', 'membrane (wall)']; #171 (t=6550, R_eq 13.52): ['K catalyst', 'L link']; #201 (t=9350, R_eq 7.8, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 20 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
