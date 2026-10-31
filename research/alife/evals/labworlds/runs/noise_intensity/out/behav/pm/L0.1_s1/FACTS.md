# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 31s; status ok
- command: `nsweep behav pm level 0.1`
- segmentation: matter > 0.35 of robust range [0.0, 1.5567], min area 6 px

## Measurements
- components: final 19, mean 9.2, max 26; occupancy final 0.27
- tracks: 215; persistent (alive >= 50% of run): 0; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 5.37, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 9, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 21, 18], H1 [16, 12, 3]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.0101/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 1000, default): splits 68, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 16, merge/split ratio 0.235, nucleations 30
- channel total drift (end/start - 1): [-0.4466, -0.7371, 0.0196, 0.0029]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 148 at frame 132: holes 1, rim-vs-core 0.30, rim-vs-outside 0.66, heterogeneity 0.21; core [0.09, 0.755, 0.534, 0.721] rim [0.201, 0.547, 0.479, 0.539]
  - track 104 at frame 85: holes 1, rim-vs-core 0.41, rim-vs-outside 0.90, heterogeneity 0.25; core [0.113, 0.984, 0.7, 0.469] rim [0.265, 0.64, 0.576, 0.584]
  - track 109 at frame 78: holes 1, rim-vs-core 0.18, rim-vs-outside 0.87, heterogeneity 0.18; core [0.037, 0.626, 0.332, 0.569] rim [0.131, 0.601, 0.472, 0.612]
  - track 169 at frame 143: holes 1, rim-vs-core 0.29, rim-vs-outside 0.95, heterogeneity 0.20; core [0.048, 0.758, 0.444, 0.423] rim [0.166, 0.609, 0.527, 0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.41, rim/outside 0.811 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.461)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 7.13 (aggregate of 62 individuals; 3/62 membrane-like individually; rim level 0.716)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 5.51 (aggregate of 62 individuals; 47/62 membrane-like individually; rim level 0.594)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 4.67 (aggregate of 62 individuals; 47/62 membrane-like individually; rim level 0.63)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #148 (t=6600, R_eq 9.67): ['L link', 'membrane (wall)']; #104 (t=4250, R_eq 8.56): ['L link', 'membrane (wall)']; #109 (t=3900, R_eq 14.46, ring): ['L link', 'membrane (wall)']; #169 (t=7150, R_eq 11.13): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
