# Evidence pack: phase-membrane-bd-twin (seed 6)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5557], min area 6 px

## Measurements
- components: final 42, mean 27.6, max 42; occupancy final 0.28
- tracks: 99; persistent (alive >= 50% of run): 17; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.89 (1 = constant size)
- enclosures: components with a hole mean 1.30, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 42, 42], H1 [42, 19, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 35, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.029, nucleations 0
- channel total drift (end/start - 1): [-0.4633, -0.7306, 0.1738, -0.1252]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 48 at frame 99: holes 0, rim-vs-core 0.53, rim-vs-outside 0.82, heterogeneity 0.20; core [0.07, 0.802, 0.704, 0.518] rim [0.278, 0.39, 0.566, 0.747]
  - track 49 at frame 102: holes 0, rim-vs-core 0.58, rim-vs-outside 0.84, heterogeneity 0.20; core [0.082, 0.86, 0.787, 0.542] rim [0.275, 0.4, 0.577, 0.76]
  - track 54 at frame 106: holes 0, rim-vs-core 0.59, rim-vs-outside 0.82, heterogeneity 0.21; core [0.079, 0.839, 0.758, 0.527] rim [0.287, 0.372, 0.551, 0.73]
  - track 93 at frame 144: holes 0, rim-vs-core 0.62, rim-vs-outside 0.81, heterogeneity 0.22; core [0.088, 0.864, 0.802, 0.556] rim [0.294, 0.361, 0.544, 0.711]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 180 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 12.6, rim/outside 0.829 (aggregate of 180 individuals; 0/180 membrane-like individually; rim level 0.506)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.859, rim/outside 33.2 (aggregate of 180 individuals; 3/180 membrane-like individually; rim level 0.706)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 20.3 (aggregate of 180 individuals; 17/180 membrane-like individually; rim level 0.764)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.83, rim/outside 23.3 (aggregate of 180 individuals; 159/180 membrane-like individually; rim level 0.821)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #48 (t=4950, R_eq 6.77): ['membrane (wall)']; #49 (t=5100, R_eq 6.02): ['membrane (wall)']; #54 (t=5300, R_eq 6.38): ['membrane (wall)']; #93 (t=7200, R_eq 6.08): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 180 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
