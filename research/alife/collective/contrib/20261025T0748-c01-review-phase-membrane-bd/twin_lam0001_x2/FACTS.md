# Evidence pack: phase-membrane-bd-twin (seed 7)

- world: `../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 200 steps x dt 0.25 (--dt; world META dt 1.0) = time 8000; grid [256, 256]; wall 131s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_pm.py --out collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_lam0001_x2 --seeds 7 --size 256 256 --frames 160 --spf 200 --dt 0.25 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8053], min area 6 px

## Measurements
- components: final 26, mean 18.6, max 77; occupancy final 0.25
- tracks: 149; persistent (alive >= 50% of run): 17; longest 161 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 9.80 (1 = constant size)
- enclosures: components with a hole mean 5.58, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 17]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 26, 26], H1 [38, 15, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.5
- replication (lineage window K = 20 frames = time 1000, default): splits 25, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4246, -0.7344, -0.0329, -0.0963]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 81: holes 1, rim-vs-core 0.14, rim-vs-outside 0.70, heterogeneity 0.25; core [0.086, 0.637, 0.472, 0.7] rim [0.154, 0.562, 0.454, 0.61]
  - track 78 at frame 81: holes 1, rim-vs-core 0.42, rim-vs-outside 0.72, heterogeneity 0.26; core [0.121, 0.907, 0.766, 0.54] rim [0.167, 0.601, 0.486, 0.591]
  - track 112 at frame 81: holes 0, rim-vs-core 0.61, rim-vs-outside 0.84, heterogeneity 0.23; core [0.093, 0.802, 0.601, 0.473] rim [0.235, 0.395, 0.415, 0.859]
  - track 143 at frame 148: holes 0, rim-vs-core 0.40, rim-vs-outside 0.92, heterogeneity 0.22; core [0.083, 0.779, 0.557, 0.47] rim [0.185, 0.532, 0.477, 0.759]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 113 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 3.21, rim/outside 0.722 (aggregate of 113 individuals; 0/113 membrane-like individually; rim level 0.379)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 12.4 (aggregate of 113 individuals; 54/113 membrane-like individually; rim level 0.59)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 10.4 (aggregate of 113 individuals; 77/113 membrane-like individually; rim level 0.475)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.97, rim/outside 5.65 (aggregate of 113 individuals; 83/113 membrane-like individually; rim level 0.573)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #7 (t=4050, R_eq 17.09): ['K catalyst', 'L link']; #78 (t=4050, R_eq 15.98, ring): ['K catalyst', 'L link', 'membrane (wall)']; #112 (t=4050, R_eq 10.28): ['membrane (wall)']; #143 (t=7400, R_eq 14.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 50 of 113 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
