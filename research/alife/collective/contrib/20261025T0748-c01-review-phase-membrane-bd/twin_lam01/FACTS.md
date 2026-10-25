# Evidence pack: phase-membrane-bd-twin (seed 7)

- world: `../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_pm.py --out collective/contrib/20261025T0748-c01-review-phase-membrane-bd/twin_lam01 --seeds 7 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5572], min area 6 px

## Measurements
- components: final 42, mean 28.9, max 42; occupancy final 0.28
- tracks: 96; persistent (alive >= 50% of run): 25; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.03 (1 = constant size)
- enclosures: components with a hole mean 1.30, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 42, 42], H1 [40, 28, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00263/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 35, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.464, -0.7321, 0.1765, -0.0462]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 91: holes 0, rim-vs-core 0.43, rim-vs-outside 0.85, heterogeneity 0.21; core [0.107, 0.838, 0.809, 0.66] rim [0.215, 0.492, 0.578, 0.639]
  - track 45 at frame 95: holes 0, rim-vs-core 0.45, rim-vs-outside 0.88, heterogeneity 0.21; core [0.077, 0.846, 0.763, 0.523] rim [0.237, 0.491, 0.607, 0.677]
  - track 50 at frame 108: holes 0, rim-vs-core 0.45, rim-vs-outside 0.67, heterogeneity 0.21; core [0.131, 0.773, 0.776, 0.646] rim [0.277, 0.403, 0.557, 0.659]
  - track 83 at frame 133: holes 0, rim-vs-core 0.73, rim-vs-outside 0.46, heterogeneity 0.21; core [0.151, 0.78, 0.824, 0.723] rim [0.335, 0.225, 0.427, 0.549]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 13.1, rim/outside 0.832 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.503)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 34.4 (aggregate of 186 individuals; 1/186 membrane-like individually; rim level 0.708)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 21.3 (aggregate of 186 individuals; 19/186 membrane-like individually; rim level 0.764)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.02, rim/outside 25.2 (aggregate of 186 individuals; 169/186 membrane-like individually; rim level 0.838)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #42 (t=4550, R_eq 6.56): ['membrane (wall)']; #45 (t=4750, R_eq 6.21): ['membrane (wall)']; #50 (t=5400, R_eq 5.75): ['membrane (wall)']; #83 (t=6650, R_eq 5.35): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 186 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
