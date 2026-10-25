# Evidence pack: phase-membrane-bd-twin (seed 9)

- world: `../../../20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 11s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/_c07rev15/rerun_twin_lam0001/seed9 --seeds 9 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9216], min area 6 px

## Measurements
- components: final 55, mean 38.1, max 55; occupancy final 0.33
- tracks: 129; persistent (alive >= 50% of run): 39; longest 161 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.10 (1 = constant size)
- enclosures: components with a hole mean 11.63, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 4, 20]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [89, 56, 55], H1 [25, 8, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 46, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 2, merges 5, merge/split ratio 0.109, nucleations 0
- channel total drift (end/start - 1): [-0.5621, -0.6513, 0.2845, 0.1621]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 81: holes 1, rim-vs-core 0.44, rim-vs-outside 0.76, heterogeneity 0.24; core [0.084, 0.848, 0.599, 0.353] rim [0.155, 0.545, 0.413, 0.595]
  - track 28 at frame 81: holes 0, rim-vs-core 0.81, rim-vs-outside 0.55, heterogeneity 0.24; core [0.099, 0.79, 0.587, 0.512] rim [0.264, 0.165, 0.174, 0.782]
  - track 39 at frame 81: holes 1, rim-vs-core 0.37, rim-vs-outside 0.78, heterogeneity 0.23; core [0.062, 0.715, 0.459, 0.406] rim [0.173, 0.486, 0.392, 0.663]
  - track 85 at frame 108: holes 0, rim-vs-core 0.53, rim-vs-outside 0.86, heterogeneity 0.23; core [0.083, 0.787, 0.545, 0.477] rim [0.205, 0.422, 0.383, 0.802]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 243 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 6.01, rim/outside 0.83 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.398)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 11.8 (aggregate of 243 individuals; 55/243 membrane-like individually; rim level 0.627)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 10.2 (aggregate of 243 individuals; 146/243 membrane-like individually; rim level 0.477)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.81, rim/outside 5.5 (aggregate of 243 individuals; 170/243 membrane-like individually; rim level 0.619)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #14 (t=4050, R_eq 6.26, ring): ['K catalyst', 'L link', 'membrane (wall)']; #28 (t=4050, R_eq 5.2): ['L link', 'membrane (wall)']; #39 (t=4050, R_eq 6.93): ['L link', 'membrane (wall)']; #85 (t=5400, R_eq 6.91): ['K catalyst', 'L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 76 of 243 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
