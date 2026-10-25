# Evidence pack: phase-membrane-bd-twin (seed 5)

- world: `../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 200 steps x dt 0.25 (--dt; world META dt 1.0) = time 8000; grid [256, 256]; wall 131s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0001_x2 --seeds 5 --size 256 256 --frames 160 --spf 200 --dt 0.25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8206], min area 6 px

## Measurements
- components: final 37, mean 23.9, max 87; occupancy final 0.31
- tracks: 190; persistent (alive >= 50% of run): 19; longest 161 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 15.33 (1 = constant size)
- enclosures: components with a hole mean 8.05, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 18]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 37, 37], H1 [51, 23, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 33, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 2, merge/split ratio 0.061, nucleations 0
- channel total drift (end/start - 1): [-0.5455, -0.6595, 0.2407, 0.1055]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 60 at frame 81: holes 1, rim-vs-core 0.27, rim-vs-outside 0.72, heterogeneity 0.25; core [0.11, 0.797, 0.635, 0.618] rim [0.166, 0.586, 0.473, 0.599]
  - track 91 at frame 81: holes 1, rim-vs-core 0.42, rim-vs-outside 0.71, heterogeneity 0.24; core [0.117, 0.891, 0.73, 0.516] rim [0.16, 0.583, 0.464, 0.604]
  - track 118 at frame 81: holes 1, rim-vs-core 0.39, rim-vs-outside 0.70, heterogeneity 0.25; core [0.119, 0.882, 0.726, 0.554] rim [0.163, 0.591, 0.468, 0.595]
  - track 176 at frame 148: holes 0, rim-vs-core 0.64, rim-vs-outside 0.83, heterogeneity 0.24; core [0.101, 0.826, 0.633, 0.459] rim [0.244, 0.395, 0.416, 0.857]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 148 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 3.01, rim/outside 0.728 (aggregate of 148 individuals; 0/148 membrane-like individually; rim level 0.376)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 12.6 (aggregate of 148 individuals; 75/148 membrane-like individually; rim level 0.59)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 10.8 (aggregate of 148 individuals; 105/148 membrane-like individually; rim level 0.481)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.37, rim/outside 5.84 (aggregate of 148 individuals; 118/148 membrane-like individually; rim level 0.602)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #60 (t=4050, R_eq 15.17, ring): ['K catalyst', 'L link', 'membrane (wall)']; #91 (t=4050, R_eq 16.41, ring): ['K catalyst', 'L link', 'membrane (wall)']; #118 (t=4050, R_eq 16.81, ring): ['K catalyst', 'L link', 'membrane (wall)']; #176 (t=7400, R_eq 10.05): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 81 of 148 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
