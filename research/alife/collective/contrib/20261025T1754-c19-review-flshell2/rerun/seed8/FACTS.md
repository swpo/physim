# Evidence pack: fl_shell2 (seed 8)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 88s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T1754-c19-review-flshell2/rerun/seed8 --seeds 8 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0972], min area 6 px

## Measurements
- components: final 13, mean 8.6, max 16; occupancy final 0.09
- tracks: 203; persistent (alive >= 50% of run): 0; longest 136 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 19, 15], H1 [5, 2, 0]
- motion: 41 long-lived tracks moved >= 1 body length; max speed 0.803/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 40, default): splits 70, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 7, merges 59, merge/split ratio 0.843, nucleations 2
- channel total drift (end/start - 1): [5.3151, 6.5639, -0.5166, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 86 at frame 316: holes 0, rim-vs-core 0.43, rim-vs-outside 0.06, heterogeneity 0.18; core [0.297, 0.385, 0.054, 0.0] rim [0.031, 0.046, 0.046, 0.0]
  - track 1 at frame 54: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.23; core [0.336, 0.412, 0.315, 0.0] rim [0.256, 0.069, 0.433, 0.0]
  - track 83 at frame 289: holes 0, rim-vs-core 0.37, rim-vs-outside 0.24, heterogeneity 0.20; core [0.472, 0.344, 0.112, 0.0] rim [0.231, 0.066, 0.115, 0.0]
  - track 175 at frame 390: holes 0, rim-vs-core 0.41, rim-vs-outside 0.08, heterogeneity 0.18; core [0.266, 0.399, 0.048, 0.0] rim [0.075, 0.034, 0.05, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 19.3 (aggregate of 54 individuals; 31/54 membrane-like individually; rim level 0.301)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 23.3 (aggregate of 54 individuals; 24/54 membrane-like individually; rim level 0.326)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2, rim/outside 0.811 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.184)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 2.74, rim/outside 0.235 (aggregate of 54 individuals; 1/54 membrane-like individually; rim level 0.0778)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #86 (t=632, R_eq 4.75): ['A0']; #1 (t=108, R_eq 6.43): ['A0']; #83 (t=578, R_eq 6.72): ['A0']; #175 (t=780, R_eq 5.61): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 54 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
