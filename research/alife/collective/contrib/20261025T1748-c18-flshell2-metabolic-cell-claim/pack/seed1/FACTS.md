# Evidence pack: fl_shell2 (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.022], min area 6 px

## Measurements
- components: final 12, mean 7.4, max 15; occupancy final 0.09
- tracks: 204; persistent (alive >= 50% of run): 0; longest 121 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 20, 14], H1 [7, 1, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.987/time; max body lengths 16.7
- replication (lineage window K = 20 frames = time 40, default): splits 72, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 5, merges 63, merge/split ratio 0.875, nucleations 5
- channel total drift (end/start - 1): [5.7667, 6.7565, -0.54, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 182: holes 0, rim-vs-core 0.47, rim-vs-outside 0.07, heterogeneity 0.20; core [0.353, 0.364, 0.356, 0.0] rim [0.054, 0.021, 0.453, 0.0]
  - track 4 at frame 134: holes 0, rim-vs-core 0.44, rim-vs-outside 0.08, heterogeneity 0.21; core [0.247, 0.381, 0.377, 0.0] rim [0.019, 0.031, 0.508, 0.0]
  - track 69 at frame 262: holes 0, rim-vs-core 0.29, rim-vs-outside 0.24, heterogeneity 0.20; core [0.391, 0.346, 0.114, 0.0] rim [0.188, 0.137, 0.15, 0.0]
  - track 156 at frame 373: holes 0, rim-vs-core 0.53, rim-vs-outside 0.05, heterogeneity 0.25; core [0.338, 0.408, 0.039, 0.213] rim [0.038, 0.028, 0.017, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 16.2 (aggregate of 49 individuals; 24/49 membrane-like individually; rim level 0.313)
  - radial A1: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 16.7 (aggregate of 49 individuals; 17/49 membrane-like individually; rim level 0.291)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.73, rim/outside 0.856 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.181)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 0.311 (aggregate of 49 individuals; 3/49 membrane-like individually; rim level 0.107)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=364, R_eq 5.23): none; #4 (t=268, R_eq 5.84): ['A1']; #69 (t=524, R_eq 6.7): ['A0']; #156 (t=746, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
