# Evidence pack: fl_shell2 (seed 2)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 53s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9996], min area 6 px

## Measurements
- components: final 15, mean 6.2, max 16; occupancy final 0.09
- tracks: 151; persistent (alive >= 50% of run): 0; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 18, 12], H1 [6, 5, 1]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.818/time; max body lengths 15.5
- replication (lineage window K = 20 frames = time 40, default): splits 51, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 5, merges 42, merge/split ratio 0.824, nucleations 8
- channel total drift (end/start - 1): [6.243, 6.1454, -0.5287, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 289: holes 0, rim-vs-core 0.33, rim-vs-outside 0.23, heterogeneity 0.19; core [0.389, 0.352, 0.153, 0.0] rim [0.097, 0.205, 0.185, 0.0]
  - track 10 at frame 205: holes 0, rim-vs-core 0.26, rim-vs-outside 0.30, heterogeneity 0.21; core [0.438, 0.333, 0.188, 0.0] rim [0.229, 0.182, 0.249, 0.0]
  - track 73 at frame 360: holes 0, rim-vs-core 0.33, rim-vs-outside 0.25, heterogeneity 0.19; core [0.376, 0.391, 0.081, 0.0] rim [0.237, 0.096, 0.068, 0.0]
  - track 109 at frame 380: holes 0, rim-vs-core 0.45, rim-vs-outside 0.08, heterogeneity 0.18; core [0.425, 0.307, 0.035, 0.0] rim [0.084, 0.022, 0.022, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 42 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 16.6 (aggregate of 42 individuals; 23/42 membrane-like individually; rim level 0.347)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 18.2 (aggregate of 42 individuals; 12/42 membrane-like individually; rim level 0.253)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.79, rim/outside 0.832 (aggregate of 42 individuals; 0/42 membrane-like individually; rim level 0.171)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.7, rim/outside 0.364 (aggregate of 42 individuals; 3/42 membrane-like individually; rim level 0.104)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0
- membrane-like channels per top track at mid-life: #27 (t=578, R_eq 4.98): ['A0']; #10 (t=410, R_eq 7.86): ['A0']; #73 (t=720, R_eq 6.63): ['A0']; #109 (t=760, R_eq 6): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 42 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
