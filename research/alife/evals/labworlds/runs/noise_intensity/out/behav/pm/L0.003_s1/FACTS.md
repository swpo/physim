# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../../../scripts/noisy_world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `nsweep behav pm level 0.003`
- segmentation: matter > 0.35 of robust range [0.0, 1.539], min area 6 px

## Measurements
- components: final 19, mean 16.8, max 26; occupancy final 0.35
- tracks: 164; persistent (alive >= 50% of run): 3; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 49.75 (1 = constant size)
- enclosures: components with a hole mean 10.63, final 13; holes at thresholds 0.2/0.35/0.5 final [0, 13, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 19, 19], H1 [19, 19, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00455/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 64, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.141, nucleations 0
- channel total drift (end/start - 1): [-0.5146, -0.6751, 0.125, 0.1624]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 73: holes 1, rim-vs-core 0.24, rim-vs-outside 0.83, heterogeneity 0.21; core [0.108, 0.848, 0.605, 0.549] rim [0.186, 0.639, 0.537, 0.587]
  - track 87 at frame 94: holes 1, rim-vs-core 0.38, rim-vs-outside 0.81, heterogeneity 0.22; core [0.119, 0.858, 0.641, 0.577] rim [0.247, 0.534, 0.495, 0.58]
  - track 63 at frame 51: holes 1, rim-vs-core 0.18, rim-vs-outside 0.85, heterogeneity 0.18; core [0.096, 0.781, 0.551, 0.619] rim [0.159, 0.618, 0.517, 0.614]
  - track 122 at frame 125: holes 1, rim-vs-core 0.18, rim-vs-outside 0.80, heterogeneity 0.19; core [0.102, 0.773, 0.578, 0.655] rim [0.159, 0.62, 0.514, 0.606]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 100 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 13.4, rim/outside 0.892 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.457)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 4.53 (aggregate of 100 individuals; 0/100 membrane-like individually; rim level 0.709)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.72, rim/outside 3.6 (aggregate of 100 individuals; 84/100 membrane-like individually; rim level 0.548)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.69, rim/outside 3.5 (aggregate of 100 individuals; 85/100 membrane-like individually; rim level 0.631)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #50 (t=3650, R_eq 10.69, ring): ['L link', 'membrane (wall)']; #87 (t=4700, R_eq 8.69, ring): ['L link', 'membrane (wall)']; #63 (t=2550, R_eq 10.23, ring): ['L link', 'membrane (wall)']; #122 (t=6250, R_eq 11.04, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 62 of 100 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
