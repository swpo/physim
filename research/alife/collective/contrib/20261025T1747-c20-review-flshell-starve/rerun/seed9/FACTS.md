# Evidence pack: fl_shell (seed 9)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 134s; status ok
- command: `python -m labkit.run /tmp/c20fl/world.py --out /tmp/c20fl/pack --seeds 8 9 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0897], min area 6 px

## Measurements
- components: final 13, mean 6.7, max 13; occupancy final 0.09
- tracks: 118; persistent (alive >= 50% of run): 0; longest 133 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 16, 14], H1 [10, 2, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.856/time; max body lengths 7.6
- replication (lineage window K = 20 frames = time 40, default): splits 42, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 8, merges 32, merge/split ratio 0.762, nucleations 0
- channel total drift (end/start - 1): [4.2146, 7.208, -0.5182, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 124: holes 0, rim-vs-core 0.45, rim-vs-outside 0.11, heterogeneity 0.19; core [0.277, 0.42, 0.212, 0.0] rim [0.094, 0.01, 0.291, 0.0]
  - track 11 at frame 131: holes 0, rim-vs-core 0.41, rim-vs-outside 0.08, heterogeneity 0.19; core [0.266, 0.388, 0.182, 0.0] rim [0.026, 0.064, 0.248, 0.0]
  - track 62 at frame 306: holes 0, rim-vs-core 0.37, rim-vs-outside 0.15, heterogeneity 0.18; core [0.291, 0.419, 0.156, 0.0] rim [0.106, 0.102, 0.173, 0.0]
  - track 94 at frame 376: holes 0, rim-vs-core 0.46, rim-vs-outside 0.03, heterogeneity 0.18; core [0.316, 0.377, 0.093, 0.0] rim [0.024, 0.016, 0.113, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 45 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.944, rim/outside 18.9 (aggregate of 45 individuals; 20/45 membrane-like individually; rim level 0.274)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.02, rim/outside 22.4 (aggregate of 45 individuals; 35/45 membrane-like individually; rim level 0.335)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.02, rim/outside 0.803 (aggregate of 45 individuals; 0/45 membrane-like individually; rim level 0.203)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 0.192 (aggregate of 45 individuals; 2/45 membrane-like individually; rim level 0.0614)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #6 (t=248, R_eq 4.92): ['A0', 'A1']; #11 (t=262, R_eq 5.92): ['A1']; #62 (t=612, R_eq 5.61): ['A0', 'A1']; #94 (t=752, R_eq 5.11): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 45 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
