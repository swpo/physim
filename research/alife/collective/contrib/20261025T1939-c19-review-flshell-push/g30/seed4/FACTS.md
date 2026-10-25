# Evidence pack: fl_shell (seed 4)

- world: `../../../20261025T1727-c18-flshell-push-no-antifusion/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 73s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1727-c18-flshell-push-no-antifusion/world.py --out collective/contrib/20261025T1939-c19-review-flshell-push/g30 --seeds 3 4 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0431], min area 6 px

## Measurements
- components: final 13, mean 6.8, max 14; occupancy final 0.10
- tracks: 153; persistent (alive >= 50% of run): 2; longest 240 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.80 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 19, 13], H1 [10, 4, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.789/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 40, default): splits 54, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 5, merges 44, merge/split ratio 0.815, nucleations 0
- channel total drift (end/start - 1): [4.2326, 6.8832, -0.5406, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 182: holes 0, rim-vs-core 0.31, rim-vs-outside 0.31, heterogeneity 0.19; core [0.334, 0.32, 0.114, 0.0] rim [0.029, 0.301, 0.184, 0.0]
  - track 4 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.25, heterogeneity 0.19; core [0.334, 0.349, 0.094, 0.0] rim [0.054, 0.231, 0.172, 0.0]
  - track 15 at frame 239: holes 0, rim-vs-core 0.38, rim-vs-outside 0.09, heterogeneity 0.19; core [0.267, 0.365, 0.258, 0.0] rim [0.033, 0.072, 0.333, 0.0]
  - track 110 at frame 387: holes 0, rim-vs-core 0.47, rim-vs-outside 0.06, heterogeneity 0.17; core [0.331, 0.409, 0.088, 0.008] rim [0.053, 0.034, 0.073, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 12.4 (aggregate of 44 individuals; 20/44 membrane-like individually; rim level 0.224)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 2.23, rim/outside 22.7 (aggregate of 44 individuals; 34/44 membrane-like individually; rim level 0.353)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.02, rim/outside 0.805 (aggregate of 44 individuals; 0/44 membrane-like individually; rim level 0.193)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 9.17, rim/outside 0.319 (aggregate of 44 individuals; 6/44 membrane-like individually; rim level 0.086)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #5 (t=364, R_eq 7.76): ['A1']; #4 (t=322, R_eq 7.18): ['A1']; #15 (t=478, R_eq 5.32): ['A0', 'A1']; #110 (t=774, R_eq 4.33): ['A0']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
