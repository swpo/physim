# Evidence pack: fl_drive (seed 0)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 301 frames x 10 steps x dt 0.2 = time 600; grid [128, 128]; wall 45s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/dnb/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/dnb/pack_bg02 --seeds 0 1 --frames 300 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0005, 1.7894], min area 6 px

## Measurements
- components: final 11, mean 8.7, max 14; occupancy final 0.07
- tracks: 168; persistent (alive >= 50% of run): 0; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 12, 11], H1 [6, 1, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.959/time; max body lengths 13.1
- replication (lineage window K = 20 frames = time 40, default): splits 54, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 51, merge/split ratio 0.944, nucleations 8
- channel total drift (end/start - 1): [0.0, -0.0, -0.071, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 80 at frame 194: holes 0, rim-vs-core 0.42, rim-vs-outside 0.31, heterogeneity 0.24; core [0.388, 0.393, 0.131, 0.0] rim [0.175, 0.132, 0.374, 0.0]
  - track 14 at frame 93: holes 0, rim-vs-core 0.55, rim-vs-outside 0.20, heterogeneity 0.13; core [0.26, 0.521, 0.264, 0.0] rim [0.205, 0.003, 0.45, 0.0]
  - track 2 at frame 38: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.23; core [0.407, 0.374, 0.064, 0.0] rim [0.192, 0.117, 0.288, 0.0]
  - track 145 at frame 287: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.23; core [0.323, 0.388, 0.167, 0.0] rim [0.116, 0.19, 0.392, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.942, rim/outside 16.2 (aggregate of 58 individuals; 13/58 membrane-like individually; rim level 0.289)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 20.1 (aggregate of 58 individuals; 33/58 membrane-like individually; rim level 0.33)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 4.17, rim/outside 0.818 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.605)
  - radial S: flat profile (no radial structure; level 0; aggregate of 58 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #80 (t=388, R_eq 6.38): ['A0']; #14 (t=186, R_eq 3.19): none; #2 (t=76, R_eq 6.93): ['A0']; #145 (t=574, R_eq 6.31): ['A1']

## Warnings
- radial: 1 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
