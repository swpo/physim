# Evidence pack: ringswim-waste (seed 3)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 101 frames x 100 steps x dt 1.0 = time 10000; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0949-c07-wall-tilt-drive-negative/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev6/a3 --seeds 3 --frames 100 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5793], min area 6 px

## Measurements
- components: final 11, mean 13.6, max 19; occupancy final 0.17
- tracks: 224; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.65, final 4; holes at thresholds 0.2/0.35/0.5 final [2, 4, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 11], H1 [7, 6, 3]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0115/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 96, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.031, nucleations 1
- channel total drift (end/start - 1): [-0.3034, -0.8304, -0.2871, -0.4996]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 57: holes 1, rim-vs-core 0.19, rim-vs-outside 0.76, heterogeneity 0.20; core [0.101, 0.636, 0.54, 0.752] rim [0.182, 0.552, 0.509, 0.611]
  - track 26 at frame 13: holes 1, rim-vs-core 0.21, rim-vs-outside 0.75, heterogeneity 0.20; core [0.134, 0.741, 0.66, 0.62] rim [0.194, 0.579, 0.537, 0.596]
  - track 64 at frame 25: holes 1, rim-vs-core 0.37, rim-vs-outside 0.76, heterogeneity 0.23; core [0.14, 0.823, 0.718, 0.568] rim [0.257, 0.533, 0.519, 0.582]
  - track 139 at frame 64: holes 0, rim-vs-core 0.29, rim-vs-outside 0.93, heterogeneity 0.19; core [0.063, 0.701, 0.434, 0.6] rim [0.223, 0.505, 0.517, 0.722]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 8.33, rim/outside 0.796 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.537)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 8.53 (aggregate of 77 individuals; 13/77 membrane-like individually; rim level 0.714)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 7.29 (aggregate of 77 individuals; 63/77 membrane-like individually; rim level 0.689)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.55, rim/outside 7.22 (aggregate of 77 individuals; 64/77 membrane-like individually; rim level 0.687)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #105 (t=5700, R_eq 11.99, ring): ['K catalyst', 'L link', 'membrane (wall)']; #26 (t=1300, R_eq 12.42, ring): ['K catalyst', 'L link', 'membrane (wall)']; #64 (t=2500, R_eq 8.78, ring): ['L link', 'membrane (wall)']; #139 (t=6400, R_eq 12.91, ring): ['K catalyst', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 35 of 77 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
