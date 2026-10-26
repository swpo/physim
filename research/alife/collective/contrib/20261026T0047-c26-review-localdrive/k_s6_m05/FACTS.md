# Evidence pack: ringswim-dl2 (seed 3)

- world: `../../../20261025T2209-c28-ringswim-sibmd-claim/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane + phase_swimdiv; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 57s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2209-c28-ringswim-sibmd-claim/world.py --out collective/contrib/_c26work/rev4/k_s6_m05 --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5572], min area 6 px

## Measurements
- components: final 17, mean 17.3, max 26; occupancy final 0.17
- tracks: 236; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.32, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 17, 17], H1 [14, 12, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.0172/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 1000, default): splits 105, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 9, merges 2, merge/split ratio 0.019, nucleations 0
- channel total drift (end/start - 1): [-0.3021, -0.8576, -0.304, -0.4983]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 130 at frame 156: holes 0, rim-vs-core 0.31, rim-vs-outside 1.05, heterogeneity 0.19; core [0.041, 0.681, 0.438, 0.478] rim [0.202, 0.574, 0.578, 0.674]
  - track 60 at frame 81: holes 0, rim-vs-core 0.42, rim-vs-outside 1.04, heterogeneity 0.20; core [0.096, 0.841, 0.624, 0.601] rim [0.317, 0.519, 0.662, 0.738]
  - track 51 at frame 66: holes 0, rim-vs-core 0.73, rim-vs-outside 0.46, heterogeneity 0.19; core [0.267, 0.764, 0.949, 0.892] rim [0.373, 0.321, 0.589, 0.444]
  - track 202 at frame 188: holes 0, rim-vs-core 0.43, rim-vs-outside 1.13, heterogeneity 0.18; core [0.05, 0.705, 0.467, 0.55] rim [0.286, 0.551, 0.685, 0.789]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 109 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.42, rim/outside 0.863 (aggregate of 109 individuals; 0/109 membrane-like individually; rim level 0.53)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 8.29 (aggregate of 109 individuals; 1/109 membrane-like individually; rim level 0.737)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 6.29 (aggregate of 109 individuals; 68/109 membrane-like individually; rim level 0.755)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 8.09 (aggregate of 109 individuals; 63/109 membrane-like individually; rim level 0.8)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #130 (t=7800, R_eq 13.35): ['K catalyst', 'L link', 'membrane (wall)']; #60 (t=4050, R_eq 8.06): ['L link', 'membrane (wall)']; #51 (t=3300, R_eq 3.99): none; #202 (t=9400, R_eq 10.39): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 109 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
