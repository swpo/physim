# Evidence pack: ringswim-dl2 (seed 0)

- world: `../../code/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 233s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28sd/code/world.py --out /tmp/claude-0/c28sd/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5401], min area 6 px

## Measurements
- components: final 32, mean 38.1, max 106; occupancy final 0.19
- tracks: 1012; persistent (alive >= 50% of run): 0; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 26.39, final 20; holes at thresholds 0.2/0.35/0.5 final [9, 25, 33]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 35, 32], H1 [39, 34, 20]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.0458/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 1000, default): splits 329, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 241, merge/split ratio 0.733, nucleations 0
- channel total drift (end/start - 1): [-0.3384, -0.8107, -0.2888, -0.4569]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 114 at frame 44: holes 0, rim-vs-core 0.56, rim-vs-outside 0.96, heterogeneity 0.23; core [0.11, 0.867, 0.624, 0.508] rim [0.346, 0.418, 0.627, 0.753]
  - track 241 at frame 44: holes 1, rim-vs-core 0.18, rim-vs-outside 0.87, heterogeneity 0.20; core [0.082, 0.672, 0.493, 0.684] rim [0.194, 0.559, 0.546, 0.633]
  - track 121 at frame 34: holes 1, rim-vs-core 0.22, rim-vs-outside 0.86, heterogeneity 0.18; core [0.087, 0.731, 0.523, 0.59] rim [0.174, 0.54, 0.521, 0.637]
  - track 789 at frame 156: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.21; core [0.119, 0.714, 0.605, 0.672] rim [0.198, 0.577, 0.549, 0.6]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 220 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 10.8, rim/outside 0.764 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.498)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 7.33 (aggregate of 220 individuals; 32/220 membrane-like individually; rim level 0.629)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 5.5 (aggregate of 220 individuals; 166/220 membrane-like individually; rim level 0.525)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.29, rim/outside 5.8 (aggregate of 220 individuals; 170/220 membrane-like individually; rim level 0.557)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #114 (t=2200, R_eq 7.76): ['L link', 'membrane (wall)']; #241 (t=2200, R_eq 10.57): ['L link', 'membrane (wall)']; #121 (t=1700, R_eq 10.25, ring): ['L link', 'membrane (wall)']; #789 (t=7800, R_eq 11.79, ring): ['K catalyst', 'L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 143 of 220 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
