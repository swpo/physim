# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.03`
- segmentation: matter > 0.35 of robust range [0.0, 1.5394], min area 6 px

## Measurements
- components: final 14, mean 14.3, max 46; occupancy final 0.32
- tracks: 176; persistent (alive >= 50% of run): 1; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.66 (1 = constant size)
- enclosures: components with a hole mean 9.53, final 9; holes at thresholds 0.2/0.35/0.5 final [5, 9, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 14], H1 [13, 11, 9]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0134/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 60, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 11, merge/split ratio 0.183, nucleations 17
- channel total drift (end/start - 1): [-0.5388, -0.641, 0.1233, 0.0895]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 108 at frame 101: holes 1, rim-vs-core 0.29, rim-vs-outside 0.81, heterogeneity 0.19; core [0.088, 0.767, 0.528, 0.593] rim [0.213, 0.509, 0.504, 0.625]
  - track 97 at frame 51: holes 1, rim-vs-core 0.28, rim-vs-outside 0.72, heterogeneity 0.20; core [0.106, 0.781, 0.581, 0.648] rim [0.209, 0.55, 0.493, 0.573]
  - track 101 at frame 59: holes 1, rim-vs-core 0.31, rim-vs-outside 0.74, heterogeneity 0.20; core [0.113, 0.807, 0.613, 0.631] rim [0.213, 0.551, 0.495, 0.57]
  - track 121 at frame 95: holes 0, rim-vs-core 0.60, rim-vs-outside 0.47, heterogeneity 0.16; core [0.23, 0.731, 0.769, 0.896] rim [0.352, 0.376, 0.576, 0.466]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 15.2, rim/outside 0.828 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.449)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 4.64 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.699)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 3.71 (aggregate of 83 individuals; 72/83 membrane-like individually; rim level 0.524)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.72, rim/outside 3.33 (aggregate of 83 individuals; 70/83 membrane-like individually; rim level 0.572)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #108 (t=5050, R_eq 9.89, ring): ['L link', 'membrane (wall)']; #97 (t=2550, R_eq 9.64, ring): ['L link', 'membrane (wall)']; #101 (t=2950, R_eq 9.67, ring): ['L link', 'membrane (wall)']; #121 (t=4750, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
