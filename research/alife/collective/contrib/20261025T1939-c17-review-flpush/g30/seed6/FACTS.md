# Evidence pack: fl_shell (seed 6)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run world.py --out g30 --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0403], min area 6 px

## Measurements
- components: final 10, mean 6.6, max 14; occupancy final 0.10
- tracks: 175; persistent (alive >= 50% of run): 0; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 16, 11], H1 [9, 3, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.872/time; max body lengths 10.5
- replication (lineage window K = 20 frames = time 40, default): splits 62, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 53, merge/split ratio 0.855, nucleations 1
- channel total drift (end/start - 1): [5.1606, 7.0857, -0.5537, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 148: holes 0, rim-vs-core 0.32, rim-vs-outside 0.19, heterogeneity 0.06; core [0.514, 0.0, 0.0, 0.0] rim [0.191, 0.0, 0.022, 0.0]
  - track 91 at frame 339: holes 0, rim-vs-core 0.39, rim-vs-outside 0.06, heterogeneity 0.17; core [0.253, 0.358, 0.046, 0.0] rim [0.062, 0.014, 0.043, 0.0]
  - track 24 at frame 148: holes 0, rim-vs-core 0.34, rim-vs-outside 0.22, heterogeneity 0.22; core [0.384, 0.359, 0.277, 0.0] rim [0.165, 0.117, 0.388, 0.0]
  - track 44 at frame 239: holes 0, rim-vs-core 0.46, rim-vs-outside 0.05, heterogeneity 0.17; core [0.268, 0.426, 0.118, 0.0] rim [0.022, 0.042, 0.136, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 16.1 (aggregate of 45 individuals; 18/45 membrane-like individually; rim level 0.251)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 23.3 (aggregate of 45 individuals; 23/45 membrane-like individually; rim level 0.313)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.82, rim/outside 0.843 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.185)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 11.8, rim/outside 0.388 (aggregate of 45 individuals; 3/45 membrane-like individually; rim level 0.116)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=296, R_eq 5.38): ['S']; #91 (t=678, R_eq 5.81): ['A0', 'A1']; #24 (t=296, R_eq 8.5): ['A1']; #44 (t=478, R_eq 4.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
