# Evidence pack: fl_shell (seed 7)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run world.py --out g30 --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0003], min area 6 px

## Measurements
- components: final 11, mean 6.2, max 12; occupancy final 0.09
- tracks: 134; persistent (alive >= 50% of run): 0; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 13, 11], H1 [11, 6, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.885/time; max body lengths 12.5
- replication (lineage window K = 20 frames = time 40, default): splits 49, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 3, merges 39, merge/split ratio 0.796, nucleations 0
- channel total drift (end/start - 1): [5.8992, 6.4694, -0.5402, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 108: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.23; core [0.487, 0.32, 0.387, 0.0] rim [0.18, 0.206, 0.52, 0.0]
  - track 19 at frame 161: holes 0, rim-vs-core 0.32, rim-vs-outside 0.24, heterogeneity 0.20; core [0.25, 0.432, 0.253, 0.0] rim [0.113, 0.171, 0.364, 0.0]
  - track 66 at frame 319: holes 0, rim-vs-core 0.42, rim-vs-outside 0.05, heterogeneity 0.16; core [0.253, 0.385, 0.071, 0.001] rim [0.012, 0.045, 0.065, 0.0]
  - track 100 at frame 363: holes 0, rim-vs-core 0.36, rim-vs-outside 0.21, heterogeneity 0.19; core [0.335, 0.397, 0.061, 0.0] rim [0.201, 0.064, 0.05, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 23.4 (aggregate of 42 individuals; 26/42 membrane-like individually; rim level 0.336)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 18.6 (aggregate of 42 individuals; 15/42 membrane-like individually; rim level 0.292)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.77, rim/outside 0.837 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.201)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.5, rim/outside 0.393 (aggregate of 42 individuals; 3/42 membrane-like individually; rim level 0.111)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=216, R_eq 7.63): none; #19 (t=322, R_eq 6.26): ['A1']; #66 (t=638, R_eq 4.75): ['A0', 'A1']; #100 (t=726, R_eq 7.27): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 42 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
