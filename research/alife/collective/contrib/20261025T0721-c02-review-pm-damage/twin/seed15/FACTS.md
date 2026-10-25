# Evidence pack: phase-membrane (seed 15)

- world: `../../../../../../../../home/user/physim/research/alife/threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 22s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0721-c02-review-pm-damage/twin/seed15 --seeds 15 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5388], min area 6 px

## Measurements
- components: final 16, mean 15.5, max 21; occupancy final 0.28
- tracks: 137; persistent (alive >= 50% of run): 3; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.39 (1 = constant size)
- enclosures: components with a hole mean 9.83, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 10, 12]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 16, 16], H1 [15, 15, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0133/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 55, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.145, nucleations 0
- channel total drift (end/start - 1): [-0.4511, -0.7384, -0.0399, -0.2666]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 73: holes 1, rim-vs-core 0.18, rim-vs-outside 0.84, heterogeneity 0.19; core [0.102, 0.789, 0.571, 0.617] rim [0.175, 0.627, 0.534, 0.605]
  - track 80 at frame 109: holes 0, rim-vs-core 0.59, rim-vs-outside 0.98, heterogeneity 0.24; core [0.138, 0.972, 0.733, 0.548] rim [0.338, 0.467, 0.603, 0.748]
  - track 83 at frame 109: holes 1, rim-vs-core 0.27, rim-vs-outside 0.77, heterogeneity 0.19; core [0.106, 0.788, 0.586, 0.637] rim [0.202, 0.55, 0.5, 0.592]
  - track 101 at frame 130: holes 1, rim-vs-core 0.18, rim-vs-outside 0.79, heterogeneity 0.17; core [0.091, 0.743, 0.524, 0.673] rim [0.147, 0.588, 0.49, 0.624]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 15, rim/outside 0.845 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.471)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 5.04 (aggregate of 88 individuals; 1/88 membrane-like individually; rim level 0.727)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 4.12 (aggregate of 88 individuals; 76/88 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.12, rim/outside 4.06 (aggregate of 88 individuals; 76/88 membrane-like individually; rim level 0.639)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #50 (t=3650, R_eq 10.43, ring): ['L link', 'membrane (wall)']; #80 (t=5450, R_eq 6.05): ['L link', 'membrane (wall)']; #83 (t=5450, R_eq 9.36, ring): ['L link', 'membrane (wall)']; #101 (t=6500, R_eq 11.48, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 63 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
