# Evidence pack: fl_shell (seed 3)

- world: `../../../20261025T1727-c18-flshell-push-no-antifusion/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 86s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1727-c18-flshell-push-no-antifusion/world.py --out collective/contrib/20261025T1939-c19-review-flshell-push/g0 --seeds 3 4 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9532], min area 6 px

## Measurements
- components: final 5, mean 4.6, max 7; occupancy final 0.08
- tracks: 86; persistent (alive >= 50% of run): 1; longest 205 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.75 (1 = constant size)
- enclosures: components with a hole mean 0.53, final 1; holes at thresholds 0.2/0.35/0.5 final [4, 3, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 8, 6], H1 [8, 5, 3]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.837/time; max body lengths 8.4
- replication (lineage window K = 20 frames = time 40, default): splits 29, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 26, merge/split ratio 0.897, nucleations 0
- channel total drift (end/start - 1): [2.7126, 6.5752, -0.4231, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.25, heterogeneity 0.20; core [0.338, 0.382, 0.11, 0.0] rim [0.099, 0.211, 0.181, 0.0]
  - track 70 at frame 316: holes 0, rim-vs-core 0.40, rim-vs-outside 0.09, heterogeneity 0.17; core [0.28, 0.394, 0.167, 0.0] rim [0.08, 0.046, 0.196, 0.0]
  - track 78 at frame 333: holes 0, rim-vs-core 0.20, rim-vs-outside 0.37, heterogeneity 0.17; core [0.275, 0.391, 0.014, 0.0] rim [0.078, 0.354, 0.022, 0.0]
  - track 74 at frame 296: holes 0, rim-vs-core 0.35, rim-vs-outside 0.19, heterogeneity 0.18; core [0.264, 0.427, 0.196, 0.0] rim [0.157, 0.091, 0.214, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 15.5 (aggregate of 29 individuals; 13/29 membrane-like individually; rim level 0.269)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 3.51, rim/outside 31.4 (aggregate of 29 individuals; 26/29 membrane-like individually; rim level 0.371)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.49, rim/outside 0.782 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.327)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 10.6, rim/outside 0.378 (aggregate of 29 individuals; 6/29 membrane-like individually; rim level 0.0961)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #4 (t=322, R_eq 7.18): ['A1']; #70 (t=632, R_eq 5.29): ['A0', 'A1']; #78 (t=666, R_eq 12.49): ['A1', 'S']; #74 (t=592, R_eq 5.56): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
