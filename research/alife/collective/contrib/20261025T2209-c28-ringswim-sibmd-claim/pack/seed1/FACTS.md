# Evidence pack: ringswim-dl2 (seed 1)

- world: `../../code/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [256, 256]; wall 210s; status ok
- command: `python -m labkit.run /tmp/claude-0/c28sd/code/world.py --out /tmp/claude-0/c28sd/pack --seeds 0 1 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5411], min area 6 px

## Measurements
- components: final 25, mean 40.7, max 124; occupancy final 0.18
- tracks: 1149; persistent (alive >= 50% of run): 0; longest 80 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 27.49, final 20; holes at thresholds 0.2/0.35/0.5 final [5, 25, 29]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 25, 25], H1 [32, 30, 21]
- motion: 68 long-lived tracks moved >= 1 body length; max speed 0.0568/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 1000, default): splits 361, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 301, merge/split ratio 0.834, nucleations 2
- channel total drift (end/start - 1): [-0.3067, -0.8234, -0.3418, -0.4466]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 198 at frame 42: holes 1, rim-vs-core 0.26, rim-vs-outside 0.73, heterogeneity 0.18; core [0.101, 0.686, 0.552, 0.675] rim [0.209, 0.47, 0.493, 0.598]
  - track 304 at frame 54: holes 0, rim-vs-core 0.34, rim-vs-outside 0.76, heterogeneity 0.17; core [0.099, 0.69, 0.526, 0.737] rim [0.276, 0.408, 0.543, 0.651]
  - track 766 at frame 141: holes 1, rim-vs-core 0.33, rim-vs-outside 0.76, heterogeneity 0.22; core [0.136, 0.804, 0.665, 0.598] rim [0.252, 0.519, 0.539, 0.581]
  - track 908 at frame 165: holes 0, rim-vs-core 0.23, rim-vs-outside 0.76, heterogeneity 0.14; core [0.087, 0.612, 0.444, 0.799] rim [0.212, 0.46, 0.521, 0.701]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.57, rim/outside 0.792 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.507)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 7.1 (aggregate of 224 individuals; 20/224 membrane-like individually; rim level 0.634)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 5.25 (aggregate of 224 individuals; 170/224 membrane-like individually; rim level 0.535)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.22, rim/outside 5.82 (aggregate of 224 individuals; 171/224 membrane-like individually; rim level 0.581)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #198 (t=2100, R_eq 9.69, ring): ['L link', 'membrane (wall)']; #304 (t=2700, R_eq 7.9): ['L link', 'membrane (wall)']; #766 (t=7050, R_eq 9.32, ring): ['L link', 'membrane (wall)']; #908 (t=8250, R_eq 8.61): ['L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 128 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
