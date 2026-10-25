# Evidence pack: phase-membrane-bd-twin (seed 5)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0 --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9977], min area 6 px

## Measurements
- components: final 39, mean 36.8, max 39; occupancy final 0.24
- tracks: 88; persistent (alive >= 50% of run): 38; longest 161 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 8.55 (1 = constant size)
- enclosures: components with a hole mean 8.66, final 10; holes at thresholds 0.2/0.35/0.5 final [0, 10, 27]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 40, 39], H1 [29, 20, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 1000, default): splits 31, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 0.097, nucleations 0
- channel total drift (end/start - 1): [-0.4484, -0.7204, 0.0167, -0.3558]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 81: holes 0, rim-vs-core 0.98, rim-vs-outside 0.48, heterogeneity 0.27; core [0.103, 0.809, 0.588, 0.454] rim [0.294, 0.071, 0.069, 0.782]
  - track 5 at frame 81: holes 0, rim-vs-core 1.04, rim-vs-outside 0.50, heterogeneity 0.29; core [0.124, 0.882, 0.681, 0.422] rim [0.315, 0.115, 0.111, 0.795]
  - track 7 at frame 81: holes 0, rim-vs-core 1.14, rim-vs-outside 0.50, heterogeneity 0.29; core [0.126, 0.886, 0.691, 0.42] rim [0.33, 0.041, 0.04, 0.783]
  - track 84 at frame 106: holes 0, rim-vs-core 0.55, rim-vs-outside 0.82, heterogeneity 0.25; core [0.078, 0.768, 0.503, 0.432] rim [0.214, 0.402, 0.348, 0.793]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 230 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 8.4, rim/outside 0.798 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.441)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 22.8 (aggregate of 230 individuals; 54/230 membrane-like individually; rim level 0.751)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.77, rim/outside 20.1 (aggregate of 230 individuals; 179/230 membrane-like individually; rim level 0.574)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.88, rim/outside 9.47 (aggregate of 230 individuals; 191/230 membrane-like individually; rim level 0.69)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #3 (t=4050, R_eq 5.14): ['L link', 'membrane (wall)']; #5 (t=4050, R_eq 4.65): ['L link', 'membrane (wall)']; #7 (t=4050, R_eq 4.82): ['L link', 'membrane (wall)']; #84 (t=5300, R_eq 6.72): ['K catalyst', 'L link']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 81 of 230 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
