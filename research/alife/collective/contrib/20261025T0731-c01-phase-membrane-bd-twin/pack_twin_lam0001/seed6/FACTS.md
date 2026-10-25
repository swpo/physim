# Evidence pack: phase-membrane-bd-twin (seed 6)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0001 --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9091], min area 6 px

## Measurements
- components: final 51, mean 34.8, max 51; occupancy final 0.33
- tracks: 114; persistent (alive >= 50% of run): 29; longest 161 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 10.89 (1 = constant size)
- enclosures: components with a hole mean 10.38, final 5; holes at thresholds 0.2/0.35/0.5 final [0, 5, 22]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [100, 51, 51], H1 [33, 10, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 1000, default): splits 39, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.103, nucleations 0
- channel total drift (end/start - 1): [-0.5549, -0.653, 0.2583, 0.1026]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 81: holes 1, rim-vs-core 0.44, rim-vs-outside 0.74, heterogeneity 0.25; core [0.075, 0.813, 0.566, 0.361] rim [0.158, 0.51, 0.39, 0.612]
  - track 10 at frame 81: holes 1, rim-vs-core 0.40, rim-vs-outside 0.69, heterogeneity 0.22; core [0.075, 0.787, 0.539, 0.431] rim [0.141, 0.49, 0.363, 0.626]
  - track 25 at frame 81: holes 1, rim-vs-core 0.76, rim-vs-outside 0.43, heterogeneity 0.24; core [0.101, 0.798, 0.61, 0.548] rim [0.215, 0.208, 0.153, 0.628]
  - track 74 at frame 121: holes 0, rim-vs-core 0.86, rim-vs-outside 0.53, heterogeneity 0.24; core [0.102, 0.802, 0.612, 0.535] rim [0.267, 0.136, 0.151, 0.769]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 5.31, rim/outside 0.829 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.4)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 12 (aggregate of 224 individuals; 56/224 membrane-like individually; rim level 0.605)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 10.3 (aggregate of 224 individuals; 122/224 membrane-like individually; rim level 0.464)
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 5.56 (aggregate of 224 individuals; 168/224 membrane-like individually; rim level 0.606)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #4 (t=4050, R_eq 6.75, ring): ['L link', 'membrane (wall)']; #10 (t=4050, R_eq 7.2, ring): ['K catalyst', 'L link', 'membrane (wall)']; #25 (t=4050, R_eq 5.97, ring): ['L link', 'membrane (wall)']; #74 (t=6050, R_eq 5.11): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 78 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
