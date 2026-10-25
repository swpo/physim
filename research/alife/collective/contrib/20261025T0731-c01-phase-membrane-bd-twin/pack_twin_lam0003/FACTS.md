# Evidence pack: phase-membrane-bd-twin (seed 5)

- world: `../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0003 --seeds 5 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8497], min area 6 px

## Measurements
- components: final 64, mean 45.7, max 64; occupancy final 0.35
- tracks: 138; persistent (alive >= 50% of run): 38; longest 161 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 23.17 (1 = constant size)
- enclosures: components with a hole mean 7.34, final 4; holes at thresholds 0.2/0.35/0.5 final [0, 4, 23]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [96, 64, 64], H1 [43, 10, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 58, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.034, nucleations 1
- channel total drift (end/start - 1): [-0.5795, -0.6391, 0.3191, 0.0005]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 81: holes 1, rim-vs-core 0.37, rim-vs-outside 0.73, heterogeneity 0.22; core [0.064, 0.755, 0.517, 0.469] rim [0.145, 0.479, 0.379, 0.646]
  - track 11 at frame 81: holes 0, rim-vs-core 0.41, rim-vs-outside 0.78, heterogeneity 0.23; core [0.059, 0.751, 0.503, 0.425] rim [0.163, 0.464, 0.386, 0.667]
  - track 40 at frame 83: holes 1, rim-vs-core 0.39, rim-vs-outside 0.73, heterogeneity 0.22; core [0.071, 0.774, 0.547, 0.495] rim [0.146, 0.472, 0.373, 0.645]
  - track 122 at frame 143: holes 0, rim-vs-core 0.81, rim-vs-outside 0.54, heterogeneity 0.24; core [0.092, 0.778, 0.6, 0.543] rim [0.261, 0.151, 0.176, 0.763]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 296 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7, rim/outside 0.879 (aggregate of 296 individuals; 0/296 membrane-like individually; rim level 0.392)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 13 (aggregate of 296 individuals; 32/296 membrane-like individually; rim level 0.68)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 11.3 (aggregate of 296 individuals; 151/296 membrane-like individually; rim level 0.563)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.11, rim/outside 5.66 (aggregate of 296 individuals; 228/296 membrane-like individually; rim level 0.703)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #8 (t=4050, R_eq 6.63, ring): ['K catalyst', 'L link', 'membrane (wall)']; #11 (t=4050, R_eq 6.02, ring): ['L link', 'membrane (wall)']; #40 (t=4150, R_eq 6.72, ring): ['L link', 'membrane (wall)']; #122 (t=7150, R_eq 5.64): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 296 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
