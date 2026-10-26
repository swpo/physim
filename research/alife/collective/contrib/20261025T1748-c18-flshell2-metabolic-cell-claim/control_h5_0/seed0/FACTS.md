# Evidence pack: fl_shell (seed 0)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.1218], min area 6 px

## Measurements
- components: final 11, mean 7.8, max 15; occupancy final 0.09
- tracks: 139; persistent (alive >= 50% of run): 0; longest 147 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 18, 11], H1 [8, 2, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.691/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 40, default): splits 49, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 4, merges 40, merge/split ratio 0.816, nucleations 0
- channel total drift (end/start - 1): [3.9682, 7.0193, -0.5266, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 81: holes 0, rim-vs-core 0.31, rim-vs-outside 0.28, heterogeneity 0.22; core [0.381, 0.354, 0.325, 0.0] rim [0.209, 0.132, 0.458, 0.0]
  - track 81 at frame 339: holes 0, rim-vs-core 0.49, rim-vs-outside 0.04, heterogeneity 0.17; core [0.286, 0.441, 0.084, 0.0] rim [0.042, 0.013, 0.079, 0.0]
  - track 19 at frame 178: holes 0, rim-vs-core 0.44, rim-vs-outside 0.06, heterogeneity 0.18; core [0.281, 0.395, 0.142, 0.0] rim [0.055, 0.023, 0.185, 0.0]
  - track 89 at frame 336: holes 0, rim-vs-core 0.41, rim-vs-outside 0.05, heterogeneity 0.17; core [0.254, 0.385, 0.071, 0.0] rim [0.044, 0.029, 0.075, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 21.7 (aggregate of 50 individuals; 19/50 membrane-like individually; rim level 0.267)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.47, rim/outside 33 (aggregate of 50 individuals; 41/50 membrane-like individually; rim level 0.372)  MEMBRANE-LIKE
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.08, rim/outside 0.797 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.197)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.75, rim/outside 0.182 (aggregate of 50 individuals; 2/50 membrane-like individually; rim level 0.0591)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #2 (t=162, R_eq 7.07): ['A0']; #81 (t=678, R_eq 4.44): ['A0']; #19 (t=356, R_eq 5.32): ['A0', 'A1']; #89 (t=672, R_eq 5.41): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
