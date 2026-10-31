# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.01`
- segmentation: matter > 0.35 of robust range [0.0, 1.5442], min area 6 px

## Measurements
- components: final 19, mean 18.5, max 30; occupancy final 0.32
- tracks: 173; persistent (alive >= 50% of run): 4; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.00 (1 = constant size)
- enclosures: components with a hole mean 10.76, final 13; holes at thresholds 0.2/0.35/0.5 final [2, 13, 16]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [17, 16, 9]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00811/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 1000, default): splits 65, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 11, merge/split ratio 0.169, nucleations 2
- channel total drift (end/start - 1): [-0.4929, -0.6805, 0.0849, 0.043]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 61: holes 1, rim-vs-core 0.22, rim-vs-outside 0.79, heterogeneity 0.19; core [0.1, 0.824, 0.574, 0.576] rim [0.156, 0.622, 0.508, 0.604]
  - track 81 at frame 78: holes 1, rim-vs-core 0.30, rim-vs-outside 0.71, heterogeneity 0.20; core [0.108, 0.789, 0.598, 0.636] rim [0.197, 0.545, 0.475, 0.565]
  - track 89 at frame 86: holes 1, rim-vs-core 0.35, rim-vs-outside 0.84, heterogeneity 0.21; core [0.093, 0.801, 0.559, 0.58] rim [0.237, 0.492, 0.495, 0.619]
  - track 147 at frame 136: holes 0, rim-vs-core 0.29, rim-vs-outside 0.96, heterogeneity 0.18; core [0.117, 0.801, 0.602, 0.731] rim [0.246, 0.544, 0.583, 0.709]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 111 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.9, rim/outside 0.896 (aggregate of 111 individuals; 0/111 membrane-like individually; rim level 0.473)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.81 (aggregate of 111 individuals; 0/111 membrane-like individually; rim level 0.732)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 4 (aggregate of 111 individuals; 92/111 membrane-like individually; rim level 0.587)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.65, rim/outside 3.71 (aggregate of 111 individuals; 93/111 membrane-like individually; rim level 0.656)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #26 (t=3050, R_eq 12.14, ring): ['L link', 'membrane (wall)']; #81 (t=3900, R_eq 9.98, ring): ['L link', 'membrane (wall)']; #89 (t=4300, R_eq 9.34, ring): ['L link', 'membrane (wall)']; #147 (t=6800, R_eq 8.27): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 60 of 111 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
