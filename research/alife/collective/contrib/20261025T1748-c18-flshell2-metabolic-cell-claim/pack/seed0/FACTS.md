# Evidence pack: fl_shell2 (seed 0)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls2/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0544], min area 6 px

## Measurements
- components: final 14, mean 8.7, max 17; occupancy final 0.10
- tracks: 174; persistent (alive >= 50% of run): 0; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 20, 15], H1 [5, 3, 1]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.981/time; max body lengths 15.2
- replication (lineage window K = 20 frames = time 40, default): splits 62, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 5, merges 51, merge/split ratio 0.823, nucleations 0
- channel total drift (end/start - 1): [5.4111, 6.0788, -0.5491, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 81: holes 0, rim-vs-core 0.35, rim-vs-outside 0.27, heterogeneity 0.22; core [0.38, 0.374, 0.277, 0.0] rim [0.226, 0.075, 0.378, 0.0]
  - track 16 at frame 192: holes 0, rim-vs-core 0.36, rim-vs-outside 0.27, heterogeneity 0.21; core [0.391, 0.368, 0.26, 0.0] rim [0.253, 0.04, 0.325, 0.0]
  - track 61 at frame 323: holes 0, rim-vs-core 0.47, rim-vs-outside 0.05, heterogeneity 0.18; core [0.346, 0.388, 0.071, 0.0] rim [0.017, 0.047, 0.078, 0.0]
  - track 117 at frame 366: holes 0, rim-vs-core 0.34, rim-vs-outside 0.20, heterogeneity 0.18; core [0.309, 0.426, 0.04, 0.0] rim [0.152, 0.126, 0.031, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.71, rim/outside 27.2 (aggregate of 57 individuals; 30/57 membrane-like individually; rim level 0.339)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 28.9 (aggregate of 57 individuals; 14/57 membrane-like individually; rim level 0.321)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.74, rim/outside 0.801 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.164)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.195 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.0684)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #1 (t=162, R_eq 6.6): ['A0']; #16 (t=384, R_eq 7.76): ['A0']; #61 (t=646, R_eq 4.75): none; #117 (t=732, R_eq 6.13): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 57 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
