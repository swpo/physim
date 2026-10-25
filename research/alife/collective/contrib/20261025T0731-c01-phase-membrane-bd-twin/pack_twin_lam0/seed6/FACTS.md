# Evidence pack: phase-membrane-bd-twin (seed 6)

- world: `../../twin_pm.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell_noise; mutation: links adsorb to the wall (drift chi up grad of 4 phi(1-phi)); parent: unstructured initial condition: smoothed Gaussian noise phi (mean 0, sd 0.2), uniform random K in [0,0.6] and L in [0,0.1] everywhere
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/twin_pm.py --out collective/contrib/20261025T0731-c01-phase-membrane-bd-twin/pack_twin_lam0 --seeds 5 6 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9689], min area 6 px

## Measurements
- components: final 32, mean 30.7, max 32; occupancy final 0.24
- tracks: 77; persistent (alive >= 50% of run): 30; longest 161 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 6.17 (1 = constant size)
- enclosures: components with a hole mean 11.15, final 11; holes at thresholds 0.2/0.35/0.5 final [1, 11, 27]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 32, 31], H1 [30, 14, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 19, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.263, nucleations 0
- channel total drift (end/start - 1): [-0.4479, -0.7187, 0.0073, -0.2217]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 81: holes 1, rim-vs-core 0.45, rim-vs-outside 0.68, heterogeneity 0.25; core [0.1, 0.856, 0.612, 0.417] rim [0.156, 0.519, 0.374, 0.596]
  - track 4 at frame 81: holes 0, rim-vs-core 1.10, rim-vs-outside 0.50, heterogeneity 0.28; core [0.115, 0.848, 0.647, 0.439] rim [0.319, 0.03, 0.03, 0.773]
  - track 10 at frame 81: holes 1, rim-vs-core 0.42, rim-vs-outside 0.67, heterogeneity 0.25; core [0.091, 0.827, 0.572, 0.429] rim [0.148, 0.506, 0.355, 0.581]
  - track 73 at frame 104: holes 0, rim-vs-core 0.61, rim-vs-outside 0.57, heterogeneity 0.24; core [0.089, 0.729, 0.507, 0.542] rim [0.247, 0.257, 0.245, 0.771]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.91, rim/outside 0.779 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.435)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 22 (aggregate of 188 individuals; 61/188 membrane-like individually; rim level 0.67)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.8, rim/outside 19.2 (aggregate of 188 individuals; 138/188 membrane-like individually; rim level 0.501)  MEMBRANE-LIKE
  - radial membrane (wall): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.71, rim/outside 10 (aggregate of 188 individuals; 162/188 membrane-like individually; rim level 0.614)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): L link, membrane (wall)
- membrane-like channels per top track at mid-life: #2 (t=4050, R_eq 6.41, ring): ['K catalyst', 'L link', 'membrane (wall)']; #4 (t=4050, R_eq 5.5): ['membrane (wall)']; #10 (t=4050, R_eq 6.72, ring): ['K catalyst', 'L link', 'membrane (wall)']; #73 (t=5200, R_eq 5.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 86 of 188 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
