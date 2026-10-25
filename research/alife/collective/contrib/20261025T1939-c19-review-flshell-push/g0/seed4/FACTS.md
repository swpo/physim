# Evidence pack: fl_shell (seed 4)

- world: `../../../20261025T1727-c18-flshell-push-no-antifusion/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 70s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1727-c18-flshell-push-no-antifusion/world.py --out collective/contrib/20261025T1939-c19-review-flshell-push/g0 --seeds 3 4 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0456], min area 6 px

## Measurements
- components: final 13, mean 6.7, max 15; occupancy final 0.10
- tracks: 166; persistent (alive >= 50% of run): 0; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 5, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 19, 15], H1 [8, 3, 1]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.863/time; max body lengths 7.6
- replication (lineage window K = 20 frames = time 40, default): splits 60, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 6, merges 48, merge/split ratio 0.8, nucleations 0
- channel total drift (end/start - 1): [4.3808, 6.7793, -0.5424, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 77: holes 0, rim-vs-core 0.32, rim-vs-outside 0.27, heterogeneity 0.20; core [0.3, 0.365, 0.172, 0.0] rim [0.096, 0.195, 0.344, 0.0]
  - track 6 at frame 114: holes 0, rim-vs-core 0.34, rim-vs-outside 0.26, heterogeneity 0.23; core [0.361, 0.367, 0.377, 0.0] rim [0.206, 0.096, 0.515, 0.0]
  - track 26 at frame 215: holes 0, rim-vs-core 0.29, rim-vs-outside 0.25, heterogeneity 0.19; core [0.33, 0.363, 0.185, 0.0] rim [0.094, 0.211, 0.262, 0.0]
  - track 104 at frame 356: holes 0, rim-vs-core 0.43, rim-vs-outside 0.05, heterogeneity 0.18; core [0.309, 0.377, 0.068, 0.0] rim [0.033, 0.041, 0.074, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.742, rim/outside 24.5 (aggregate of 44 individuals; 19/44 membrane-like individually; rim level 0.251)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.19, rim/outside 33.7 (aggregate of 44 individuals; 34/44 membrane-like individually; rim level 0.338)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.99, rim/outside 0.814 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.182)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 2.48, rim/outside 0.301 (aggregate of 44 individuals; 3/44 membrane-like individually; rim level 0.0957)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #1 (t=154, R_eq 7.27): ['A1']; #6 (t=228, R_eq 7.96): none; #26 (t=430, R_eq 6.51): ['A1']; #104 (t=712, R_eq 5.11): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
