# Evidence pack: fl_shell (seed 2)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 53s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/fls/pack --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.981], min area 6 px

## Measurements
- components: final 10, mean 5.0, max 10; occupancy final 0.09
- tracks: 109; persistent (alive >= 50% of run): 0; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 14, 10], H1 [12, 4, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.771/time; max body lengths 7.1
- replication (lineage window K = 20 frames = time 40, default): splits 40, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 6, merges 29, merge/split ratio 0.725, nucleations 0
- channel total drift (end/start - 1): [3.8935, 7.6874, -0.491, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 51 at frame 319: holes 0, rim-vs-core 0.30, rim-vs-outside 0.25, heterogeneity 0.20; core [0.304, 0.405, 0.208, 0.0] rim [0.124, 0.187, 0.312, 0.0]
  - track 2 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.28, heterogeneity 0.22; core [0.362, 0.367, 0.277, 0.0] rim [0.093, 0.238, 0.443, 0.0]
  - track 55 at frame 309: holes 0, rim-vs-core 0.28, rim-vs-outside 0.30, heterogeneity 0.19; core [0.303, 0.309, 0.019, 0.0] rim [0.027, 0.298, 0.066, 0.0]
  - track 65 at frame 346: holes 0, rim-vs-core 0.44, rim-vs-outside 0.06, heterogeneity 0.19; core [0.304, 0.387, 0.112, 0.0] rim [0.045, 0.037, 0.144, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 18.7 (aggregate of 35 individuals; 14/35 membrane-like individually; rim level 0.268)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 3.39, rim/outside 18.9 (aggregate of 35 individuals; 31/35 membrane-like individually; rim level 0.368)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.38, rim/outside 0.795 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.229)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 7.27, rim/outside 0.234 (aggregate of 35 individuals; 1/35 membrane-like individually; rim level 0.0627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #51 (t=638, R_eq 6.56): ['A1']; #2 (t=122, R_eq 6.51): ['A1']; #55 (t=618, R_eq 9.47): ['A1']; #65 (t=692, R_eq 5.73): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
