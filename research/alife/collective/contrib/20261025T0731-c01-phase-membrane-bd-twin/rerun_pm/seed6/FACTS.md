# Evidence pack: phase-membrane (seed 6)

- world: `../../../../../threads/autopoiesis/worlds/phase_membrane/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 12s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_membrane/world.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/rerun_pm --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5439], min area 6 px

## Measurements
- components: final 19, mean 17.2, max 32; occupancy final 0.34
- tracks: 151; persistent (alive >= 50% of run): 2; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.23 (1 = constant size)
- enclosures: components with a hole mean 10.52, final 14; holes at thresholds 0.2/0.35/0.5 final [1, 14, 19]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [19, 19, 13]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.00925/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 1000, default): splits 58, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.103, nucleations 0
- channel total drift (end/start - 1): [-0.4873, -0.6665, 0.0889, -0.046]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 46 at frame 61: holes 1, rim-vs-core 0.29, rim-vs-outside 0.75, heterogeneity 0.20; core [0.114, 0.813, 0.619, 0.613] rim [0.209, 0.564, 0.499, 0.579]
  - track 51 at frame 54: holes 0, rim-vs-core 0.33, rim-vs-outside 0.86, heterogeneity 0.17; core [0.124, 0.788, 0.596, 0.8] rim [0.28, 0.514, 0.613, 0.693]
  - track 52 at frame 50: holes 0, rim-vs-core 0.38, rim-vs-outside 0.79, heterogeneity 0.17; core [0.126, 0.795, 0.597, 0.793] rim [0.279, 0.483, 0.586, 0.65]
  - track 133 at frame 151: holes 1, rim-vs-core 0.29, rim-vs-outside 0.80, heterogeneity 0.20; core [0.107, 0.825, 0.608, 0.589] rim [0.209, 0.569, 0.518, 0.609]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 101 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 15, rim/outside 0.878 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.478)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 5.06 (aggregate of 101 individuals; 0/101 membrane-like individually; rim level 0.738)
  - radial L link: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.83, rim/outside 4.19 (aggregate of 101 individuals; 89/101 membrane-like individually; rim level 0.588)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.25, rim/outside 4.01 (aggregate of 101 individuals; 89/101 membrane-like individually; rim level 0.676)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #46 (t=3050, R_eq 9.42, ring): ['L link', 'membrane (wall)']; #51 (t=2700, R_eq 7): none; #52 (t=2500, R_eq 6.38): ['L link']; #133 (t=7550, R_eq 8.81, ring): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 66 of 101 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
