# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 29s; status ok
- command: `nsweep behav pm level 0.003`
- segmentation: matter > 0.35 of robust range [0.0, 1.5422], min area 6 px

## Measurements
- components: final 14, mean 13.8, max 27; occupancy final 0.29
- tracks: 146; persistent (alive >= 50% of run): 3; longest 105 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.05 (1 = constant size)
- enclosures: components with a hole mean 8.41, final 10; holes at thresholds 0.2/0.35/0.5 final [2, 10, 14]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [14, 14, 9]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00865/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 50, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 8, merge/split ratio 0.16, nucleations 0
- channel total drift (end/start - 1): [-0.4438, -0.7018, -0.0471, -0.2373]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 58 at frame 59: holes 1, rim-vs-core 0.20, rim-vs-outside 0.87, heterogeneity 0.18; core [0.084, 0.742, 0.49, 0.631] rim [0.176, 0.568, 0.507, 0.62]
  - track 74 at frame 85: holes 0, rim-vs-core 0.46, rim-vs-outside 0.89, heterogeneity 0.21; core [0.125, 0.878, 0.651, 0.62] rim [0.323, 0.473, 0.606, 0.715]
  - track 103 at frame 121: holes 1, rim-vs-core 0.17, rim-vs-outside 0.78, heterogeneity 0.19; core [0.083, 0.721, 0.462, 0.7] rim [0.164, 0.603, 0.498, 0.607]
  - track 117 at frame 133: holes 1, rim-vs-core 0.26, rim-vs-outside 0.85, heterogeneity 0.21; core [0.102, 0.87, 0.585, 0.497] rim [0.183, 0.648, 0.545, 0.593]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 9.71, rim/outside 0.817 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.473)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1, rim/outside 6.92 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.705)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 4.96 (aggregate of 86 individuals; 65/86 membrane-like individually; rim level 0.565)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.91, rim/outside 5.11 (aggregate of 86 individuals; 60/86 membrane-like individually; rim level 0.598)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #58 (t=2950, R_eq 10.67, ring): ['L link', 'membrane (wall)']; #74 (t=4250, R_eq 7.31): ['membrane (wall)']; #103 (t=6050, R_eq 10.43, ring): ['L link', 'membrane (wall)']; #117 (t=6650, R_eq 10.69, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 38 of 86 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
