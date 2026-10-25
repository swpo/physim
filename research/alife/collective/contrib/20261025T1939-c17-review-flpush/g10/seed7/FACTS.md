# Evidence pack: fl_shell (seed 7)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run world.py --out g10 --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9937], min area 6 px

## Measurements
- components: final 14, mean 6.2, max 16; occupancy final 0.10
- tracks: 197; persistent (alive >= 50% of run): 0; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 17, 14], H1 [11, 4, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 1.05/time; max body lengths 11.3
- replication (lineage window K = 20 frames = time 40, default): splits 71, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 3, merges 58, merge/split ratio 0.817, nucleations 0
- channel total drift (end/start - 1): [5.594, 7.0573, -0.5518, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 81: holes 0, rim-vs-core 0.32, rim-vs-outside 0.34, heterogeneity 0.22; core [0.482, 0.279, 0.283, 0.0] rim [0.241, 0.191, 0.476, 0.0]
  - track 32 at frame 239: holes 0, rim-vs-core 0.31, rim-vs-outside 0.24, heterogeneity 0.20; core [0.318, 0.341, 0.139, 0.0] rim [0.053, 0.206, 0.228, 0.0]
  - track 2 at frame 64: holes 0, rim-vs-core 0.46, rim-vs-outside 0.10, heterogeneity 0.22; core [0.372, 0.335, 0.373, 0.0] rim [0.058, 0.021, 0.509, 0.0]
  - track 97 at frame 343: holes 0, rim-vs-core 0.48, rim-vs-outside 0.03, heterogeneity 0.18; core [0.306, 0.403, 0.086, 0.002] rim [0.019, 0.022, 0.087, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 19.4 (aggregate of 44 individuals; 20/44 membrane-like individually; rim level 0.296)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 19 (aggregate of 44 individuals; 24/44 membrane-like individually; rim level 0.323)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.81, rim/outside 0.844 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.165)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 4.97, rim/outside 0.299 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.0877)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=162, R_eq 6.6): ['A0']; #32 (t=478, R_eq 7.29): ['A1']; #2 (t=128, R_eq 5.92): ['A0']; #97 (t=686, R_eq 4.44): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
