# Evidence pack: fl_shell (seed 6)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 67s; status ok
- command: `python -m labkit.run world.py --out g10 --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0416], min area 6 px

## Measurements
- components: final 11, mean 7.1, max 15; occupancy final 0.10
- tracks: 195; persistent (alive >= 50% of run): 0; longest 97 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 8, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 15, 11], H1 [11, 6, 0]
- motion: 43 long-lived tracks moved >= 1 body length; max speed 0.908/time; max body lengths 19.4
- replication (lineage window K = 20 frames = time 40, default): splits 70, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 4, merges 59, merge/split ratio 0.843, nucleations 0
- channel total drift (end/start - 1): [5.3577, 6.9867, -0.5587, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 65 at frame 266: holes 0, rim-vs-core 0.41, rim-vs-outside 0.05, heterogeneity 0.16; core [0.257, 0.372, 0.092, 0.0] rim [0.043, 0.017, 0.106, 0.0]
  - track 39 at frame 232: holes 0, rim-vs-core 0.46, rim-vs-outside 0.04, heterogeneity 0.19; core [0.338, 0.368, 0.244, 0.0] rim [0.045, 0.016, 0.288, 0.0]
  - track 119 at frame 353: holes 0, rim-vs-core 0.41, rim-vs-outside 0.06, heterogeneity 0.17; core [0.276, 0.382, 0.048, 0.0] rim [0.056, 0.037, 0.044, 0.0]
  - track 157 at frame 366: holes 0, rim-vs-core 0.36, rim-vs-outside 0.19, heterogeneity 0.17; core [0.283, 0.393, 0.019, 0.0] rim [0.192, 0.041, 0.015, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 13.8 (aggregate of 48 individuals; 23/48 membrane-like individually; rim level 0.316)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 17.1 (aggregate of 48 individuals; 25/48 membrane-like individually; rim level 0.305)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.853 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.164)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.81, rim/outside 0.279 (aggregate of 48 individuals; 3/48 membrane-like individually; rim level 0.0779)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #65 (t=532, R_eq 5.56): ['A0', 'A1']; #39 (t=464, R_eq 4.85): ['A0']; #119 (t=706, R_eq 5.44): ['A0', 'A1']; #157 (t=732, R_eq 5.32): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
