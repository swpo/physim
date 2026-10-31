# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.01`
- segmentation: matter > 0.35 of robust range [0.0, 1.5384], min area 6 px

## Measurements
- components: final 16, mean 14.5, max 23; occupancy final 0.35
- tracks: 136; persistent (alive >= 50% of run): 3; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.63 (1 = constant size)
- enclosures: components with a hole mean 9.09, final 10; holes at thresholds 0.2/0.35/0.5 final [2, 10, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [17, 14, 8]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00746/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 48, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.167, nucleations 0
- channel total drift (end/start - 1): [-0.5342, -0.66, 0.1442, -0.0436]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 73 at frame 97: holes 1, rim-vs-core 0.20, rim-vs-outside 0.83, heterogeneity 0.20; core [0.106, 0.814, 0.601, 0.613] rim [0.173, 0.641, 0.538, 0.604]
  - track 90 at frame 109: holes 1, rim-vs-core 0.33, rim-vs-outside 0.86, heterogeneity 0.20; core [0.099, 0.802, 0.57, 0.587] rim [0.237, 0.511, 0.518, 0.623]
  - track 99 at frame 114: holes 1, rim-vs-core 0.23, rim-vs-outside 0.86, heterogeneity 0.21; core [0.105, 0.857, 0.611, 0.562] rim [0.179, 0.656, 0.549, 0.591]
  - track 103 at frame 121: holes 1, rim-vs-core 0.16, rim-vs-outside 0.82, heterogeneity 0.19; core [0.098, 0.767, 0.555, 0.648] rim [0.165, 0.626, 0.527, 0.611]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 89 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.8, rim/outside 0.836 (aggregate of 89 individuals; 0/89 membrane-like individually; rim level 0.461)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 5.53 (aggregate of 89 individuals; 1/89 membrane-like individually; rim level 0.709)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 4.22 (aggregate of 89 individuals; 71/89 membrane-like individually; rim level 0.556)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.31, rim/outside 4.23 (aggregate of 89 individuals; 70/89 membrane-like individually; rim level 0.61)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #73 (t=4850, R_eq 10.14, ring): ['L link', 'membrane (wall)']; #90 (t=5450, R_eq 8.85, ring): ['L link', 'membrane (wall)']; #99 (t=5700, R_eq 10.11, ring): ['L link', 'membrane (wall)']; #103 (t=6050, R_eq 11.03, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 53 of 89 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
