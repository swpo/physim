# Evidence pack: fl_drive (seed 1)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 301 frames x 10 steps x dt 0.2 = time 600; grid [128, 128]; wall 36s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/dnb/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/dnb/pack_bg02 --seeds 0 1 --frames 300 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0006, 1.7868], min area 6 px

## Measurements
- components: final 9, mean 9.3, max 14; occupancy final 0.07
- tracks: 169; persistent (alive >= 50% of run): 0; longest 65 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 11, 9], H1 [5, 2, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.963/time; max body lengths 11.1
- replication (lineage window K = 20 frames = time 40, default): splits 55, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 53, merge/split ratio 0.964, nucleations 7
- channel total drift (end/start - 1): [0.0, 0.0, -0.0701, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 49 at frame 141: holes 0, rim-vs-core 0.49, rim-vs-outside 0.14, heterogeneity 0.24; core [0.399, 0.306, 0.198, 0.0] rim [0.096, 0.021, 0.455, 0.0]
  - track 26 at frame 91: holes 0, rim-vs-core 0.53, rim-vs-outside 0.19, heterogeneity 0.12; core [0.248, 0.495, 0.295, 0.0] rim [0.194, 0.0, 0.481, 0.0]
  - track 19 at frame 88: holes 0, rim-vs-core 0.55, rim-vs-outside 0.20, heterogeneity 0.13; core [0.258, 0.509, 0.275, 0.0] rim [0.204, 0.001, 0.466, 0.0]
  - track 124 at frame 250: holes 0, rim-vs-core 0.46, rim-vs-outside 0.23, heterogeneity 0.24; core [0.378, 0.417, 0.29, 0.0] rim [0.144, 0.045, 0.433, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 16.5 (aggregate of 61 individuals; 18/61 membrane-like individually; rim level 0.281)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 30.5 (aggregate of 61 individuals; 34/61 membrane-like individually; rim level 0.344)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.01, rim/outside 0.824 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.596)
  - radial S: flat profile (no radial structure; level 0; aggregate of 61 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #49 (t=282, R_eq 5.84): ['A0']; #26 (t=182, R_eq 3.19): none; #19 (t=176, R_eq 3.19): none; #124 (t=500, R_eq 4.98): ['A1']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
