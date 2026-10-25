# Evidence pack: fl_shell (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.081], min area 6 px

## Measurements
- components: final 14, mean 7.1, max 15; occupancy final 0.09
- tracks: 129; persistent (alive >= 50% of run): 0; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 19, 14], H1 [6, 4, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.752/time; max body lengths 11.5
- replication (lineage window K = 20 frames = time 40, default): splits 48, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 5, merges 35, merge/split ratio 0.729, nucleations 0
- channel total drift (end/start - 1): [4.2201, 7.9714, -0.5217, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 53 at frame 336: holes 0, rim-vs-core 0.30, rim-vs-outside 0.22, heterogeneity 0.18; core [0.353, 0.35, 0.056, 0.0] rim [0.096, 0.196, 0.078, 0.0]
  - track 4 at frame 108: holes 0, rim-vs-core 0.35, rim-vs-outside 0.25, heterogeneity 0.21; core [0.336, 0.364, 0.305, 0.0] rim [0.063, 0.201, 0.46, 0.0]
  - track 47 at frame 309: holes 0, rim-vs-core 0.37, rim-vs-outside 0.10, heterogeneity 0.18; core [0.269, 0.371, 0.116, 0.0] rim [0.082, 0.055, 0.137, 0.0]
  - track 39 at frame 289: holes 0, rim-vs-core 0.30, rim-vs-outside 0.24, heterogeneity 0.18; core [0.307, 0.34, 0.038, 0.0] rim [0.026, 0.234, 0.064, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 18.4 (aggregate of 47 individuals; 20/47 membrane-like individually; rim level 0.27)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.71, rim/outside 25.4 (aggregate of 47 individuals; 34/47 membrane-like individually; rim level 0.329)  MEMBRANE-LIKE
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.02, rim/outside 0.822 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.184)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.289 (aggregate of 47 individuals; 1/47 membrane-like individually; rim level 0.0997)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #53 (t=672, R_eq 6.13): ['A1']; #4 (t=216, R_eq 6.72): ['A1']; #47 (t=618, R_eq 5.73): ['A0', 'A1']; #39 (t=578, R_eq 8.54): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
