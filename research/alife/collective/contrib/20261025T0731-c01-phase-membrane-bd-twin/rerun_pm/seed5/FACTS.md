# Evidence pack: phase-membrane (seed 5)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 11s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/rerun_pm --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5395], min area 6 px

## Measurements
- components: final 14, mean 14.1, max 21; occupancy final 0.34
- tracks: 132; persistent (alive >= 50% of run): 1; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.88 (1 = constant size)
- enclosures: components with a hole mean 9.25, final 10; holes at thresholds 0.2/0.35/0.5 final [5, 10, 13]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 14], H1 [14, 14, 10]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00804/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 1000, default): splits 55, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 3, merge/split ratio 0.055, nucleations 0
- channel total drift (end/start - 1): [-0.5577, -0.6306, 0.146, -0.1468]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 81 at frame 118: holes 1, rim-vs-core 0.29, rim-vs-outside 0.72, heterogeneity 0.20; core [0.112, 0.793, 0.6, 0.644] rim [0.211, 0.555, 0.491, 0.562]
  - track 42 at frame 52: holes 1, rim-vs-core 0.19, rim-vs-outside 0.85, heterogeneity 0.19; core [0.1, 0.803, 0.566, 0.604] rim [0.168, 0.632, 0.528, 0.606]
  - track 84 at frame 116: holes 1, rim-vs-core 0.21, rim-vs-outside 0.82, heterogeneity 0.19; core [0.1, 0.809, 0.568, 0.584] rim [0.17, 0.623, 0.523, 0.61]
  - track 106 at frame 129: holes 1, rim-vs-core 0.16, rim-vs-outside 0.84, heterogeneity 0.19; core [0.094, 0.754, 0.529, 0.655] rim [0.171, 0.621, 0.527, 0.608]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.84 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.473)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 5.46 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.738)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 4.3 (aggregate of 88 individuals; 70/88 membrane-like individually; rim level 0.577)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.91, rim/outside 4.38 (aggregate of 88 individuals; 74/88 membrane-like individually; rim level 0.639)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #81 (t=5900, R_eq 9.82, ring): ['L link', 'membrane (wall)']; #42 (t=2600, R_eq 10.4, ring): ['L link', 'membrane (wall)']; #84 (t=5800, R_eq 11.35, ring): ['L link', 'membrane (wall)']; #106 (t=6450, R_eq 10.2, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
