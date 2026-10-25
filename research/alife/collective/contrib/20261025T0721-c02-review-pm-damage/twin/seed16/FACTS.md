# Evidence pack: phase-membrane (seed 16)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/twin/seed16 --seeds 16 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5464], min area 6 px

## Measurements
- components: final 19, mean 18.0, max 23; occupancy final 0.35
- tracks: 148; persistent (alive >= 50% of run): 3; longest 96 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.22 (1 = constant size)
- enclosures: components with a hole mean 10.12, final 13; holes at thresholds 0.2/0.35/0.5 final [2, 13, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [17, 17, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00466/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 57, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 7, merge/split ratio 0.123, nucleations 0
- channel total drift (end/start - 1): [-0.5477, -0.6577, 0.1789, 0.1061]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 64 at frame 75: holes 0, rim-vs-core 0.86, rim-vs-outside 0.54, heterogeneity 0.24; core [0.298, 0.885, 0.943, 0.784] rim [0.478, 0.245, 0.431, 0.574]
  - track 56 at frame 56: holes 0, rim-vs-core 0.64, rim-vs-outside 0.45, heterogeneity 0.17; core [0.197, 0.744, 0.718, 0.848] rim [0.351, 0.316, 0.5, 0.453]
  - track 80 at frame 98: holes 0, rim-vs-core 0.43, rim-vs-outside 0.84, heterogeneity 0.20; core [0.103, 0.819, 0.565, 0.599] rim [0.303, 0.457, 0.565, 0.695]
  - track 124 at frame 140: holes 0, rim-vs-core 0.60, rim-vs-outside 0.45, heterogeneity 0.16; core [0.183, 0.719, 0.665, 0.856] rim [0.327, 0.342, 0.501, 0.448]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.887 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.474)
  - radial K catalyst: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 5.4 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.731)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 4.44 (aggregate of 114 individuals; 94/114 membrane-like individually; rim level 0.609)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.52, rim/outside 4.26 (aggregate of 114 individuals; 95/114 membrane-like individually; rim level 0.676)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #64 (t=3750, R_eq 4.51): ['membrane (wall)']; #56 (t=2800, R_eq 5.89): none; #80 (t=4900, R_eq 7.69): ['L link', 'membrane (wall)']; #124 (t=7000, R_eq 5.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 114 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
