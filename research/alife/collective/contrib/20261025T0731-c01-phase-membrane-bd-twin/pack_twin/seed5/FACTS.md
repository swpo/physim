# Evidence pack: phase-membrane-bd-twin (seed 5)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5614], min area 6 px

## Measurements
- components: final 43, mean 30.2, max 43; occupancy final 0.28
- tracks: 106; persistent (alive >= 50% of run): 25; longest 134 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.93 (1 = constant size)
- enclosures: components with a hole mean 1.29, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 43, 43], H1 [42, 17, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 42, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.024, nucleations 0
- channel total drift (end/start - 1): [-0.4668, -0.7299, 0.1843, -0.245]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 94: holes 0, rim-vs-core 0.60, rim-vs-outside 0.77, heterogeneity 0.21; core [0.086, 0.825, 0.764, 0.593] rim [0.294, 0.334, 0.515, 0.69]
  - track 54 at frame 94: holes 0, rim-vs-core 0.44, rim-vs-outside 0.85, heterogeneity 0.20; core [0.089, 0.818, 0.766, 0.648] rim [0.227, 0.457, 0.574, 0.707]
  - track 58 at frame 101: holes 0, rim-vs-core 0.58, rim-vs-outside 0.79, heterogeneity 0.21; core [0.071, 0.816, 0.726, 0.535] rim [0.288, 0.35, 0.526, 0.71]
  - track 90 at frame 129: holes 0, rim-vs-core 0.62, rim-vs-outside 0.83, heterogeneity 0.21; core [0.077, 0.857, 0.781, 0.524] rim [0.285, 0.372, 0.548, 0.739]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 12, rim/outside 0.833 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.497)
  - radial K catalyst: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 30.2 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.684)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 18.8 (aggregate of 196 individuals; 11/196 membrane-like individually; rim level 0.748)
  - radial membrane (wall): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.62, rim/outside 21.7 (aggregate of 196 individuals; 169/196 membrane-like individually; rim level 0.817)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #53 (t=4700, R_eq 6.38): ['membrane (wall)']; #54 (t=4700, R_eq 7.02): none; #58 (t=5050, R_eq 6.7): ['membrane (wall)']; #90 (t=6450, R_eq 6.15): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 196 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
