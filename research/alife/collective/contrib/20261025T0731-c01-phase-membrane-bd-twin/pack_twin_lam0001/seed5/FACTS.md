# Evidence pack: phase-membrane-bd-twin (seed 5)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0001 --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9214], min area 6 px

## Measurements
- components: final 53, mean 41.7, max 53; occupancy final 0.33
- tracks: 119; persistent (alive >= 50% of run): 39; longest 161 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 10.94 (1 = constant size)
- enclosures: components with a hole mean 11.17, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 33]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [94, 53, 53], H1 [42, 12, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 46, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.065, nucleations 0
- channel total drift (end/start - 1): [-0.5648, -0.6448, 0.2674, -0.0576]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 81: holes 0, rim-vs-core 0.75, rim-vs-outside 0.46, heterogeneity 0.24; core [0.092, 0.745, 0.546, 0.535] rim [0.24, 0.153, 0.132, 0.688]
  - track 7 at frame 81: holes 1, rim-vs-core 0.39, rim-vs-outside 0.59, heterogeneity 0.24; core [0.094, 0.745, 0.547, 0.564] rim [0.186, 0.427, 0.341, 0.615]
  - track 9 at frame 81: holes 1, rim-vs-core 0.38, rim-vs-outside 0.75, heterogeneity 0.24; core [0.078, 0.803, 0.555, 0.406] rim [0.153, 0.53, 0.405, 0.617]
  - track 93 at frame 120: holes 0, rim-vs-core 0.79, rim-vs-outside 0.52, heterogeneity 0.23; core [0.105, 0.774, 0.589, 0.601] rim [0.251, 0.152, 0.157, 0.766]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 266 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.84, rim/outside 0.847 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.403)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 13.7 (aggregate of 266 individuals; 45/266 membrane-like individually; rim level 0.669)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 11.8 (aggregate of 266 individuals; 169/266 membrane-like individually; rim level 0.515)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.11, rim/outside 5.86 (aggregate of 266 individuals; 202/266 membrane-like individually; rim level 0.655)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #5 (t=4050, R_eq 6): ['L link', 'membrane (wall)']; #7 (t=4050, R_eq 5.92, ring): ['L link', 'membrane (wall)']; #9 (t=4050, R_eq 6.08, ring): ['K catalyst', 'L link', 'membrane (wall)']; #93 (t=6000, R_eq 5.44): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 78 of 266 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
