# Evidence pack: ringswim-dl2 (seed 2)

- world: `../../code/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 208s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28sd/code/world.py --out /tmp/claude-0/c28sd/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5391], min area 6 px

## Measurements
- components: final 29, mean 34.7, max 100; occupancy final 0.19
- tracks: 1022; persistent (alive >= 50% of run): 0; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 24.44, final 25; holes at thresholds 0.2/0.35/0.5 final [10, 29, 28]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 29, 28], H1 [30, 28, 19]
- motion: 63 long-lived tracks moved >= 1 body length; max speed 0.0512/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 1000, default): splits 323, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 255, merge/split ratio 0.789, nucleations 0
- channel total drift (end/start - 1): [-0.3346, -0.8057, -0.2931, -0.4182]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 485 at frame 103: holes 0, rim-vs-core 0.64, rim-vs-outside 0.47, heterogeneity 0.18; core [0.173, 0.719, 0.725, 0.835] rim [0.32, 0.282, 0.46, 0.477]
  - track 375 at frame 72: holes 1, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.19; core [0.074, 0.69, 0.462, 0.601] rim [0.168, 0.53, 0.504, 0.643]
  - track 804 at frame 171: holes 1, rim-vs-core 0.22, rim-vs-outside 0.84, heterogeneity 0.21; core [0.103, 0.747, 0.559, 0.61] rim [0.205, 0.557, 0.542, 0.619]
  - track 267 at frame 37: holes 0, rim-vs-core 0.40, rim-vs-outside 0.80, heterogeneity 0.20; core [0.087, 0.735, 0.522, 0.59] rim [0.28, 0.405, 0.56, 0.696]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 191 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.81, rim/outside 0.762 (aggregate of 191 individuals; 0/191 membrane-like individually; rim level 0.5)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 7.07 (aggregate of 191 individuals; 18/191 membrane-like individually; rim level 0.62)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.62, rim/outside 5.31 (aggregate of 191 individuals; 147/191 membrane-like individually; rim level 0.518)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.44, rim/outside 5.9 (aggregate of 191 individuals; 153/191 membrane-like individually; rim level 0.554)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #485 (t=5150, R_eq 5.89): none; #375 (t=3600, R_eq 10.57, ring): ['L link', 'membrane (wall)']; #804 (t=8550, R_eq 10.05, ring): ['L link', 'membrane (wall)']; #267 (t=1850, R_eq 8.96): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 128 of 191 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
