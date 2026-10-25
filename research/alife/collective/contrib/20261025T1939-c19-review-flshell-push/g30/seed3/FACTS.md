# Evidence pack: fl_shell (seed 3)

- world: `../../../20261025T1727-c18-flshell-push-no-antifusion/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 87s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1727-c18-flshell-push-no-antifusion/world.py --out collective/contrib/20261025T1939-c19-review-flshell-push/g30 --seeds 3 4 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.126], min area 6 px

## Measurements
- components: final 15, mean 8.8, max 19; occupancy final 0.10
- tracks: 212; persistent (alive >= 50% of run): 0; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 24, 17], H1 [8, 3, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.748/time; max body lengths 10.3
- replication (lineage window K = 20 frames = time 40, default): splits 75, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 6, merges 62, merge/split ratio 0.827, nucleations 0
- channel total drift (end/start - 1): [4.8215, 7.4058, -0.5545, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 71: holes 0, rim-vs-core 0.28, rim-vs-outside 0.31, heterogeneity 0.22; core [0.35, 0.354, 0.303, 0.0] rim [0.193, 0.184, 0.458, 0.0]
  - track 2 at frame 54: holes 0, rim-vs-core 0.17, rim-vs-outside 0.41, heterogeneity 0.22; core [0.251, 0.35, 0.323, 0.0] rim [0.282, 0.198, 0.384, 0.0]
  - track 102 at frame 326: holes 0, rim-vs-core 0.50, rim-vs-outside 0.20, heterogeneity 0.18; core [0.195, 0.532, 0.048, 0.0] rim [0.202, 0.028, 0.041, 0.0]
  - track 181 at frame 387: holes 0, rim-vs-core 0.39, rim-vs-outside 0.07, heterogeneity 0.17; core [0.26, 0.361, 0.031, 0.0] rim [0.064, 0.026, 0.026, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 21.5 (aggregate of 57 individuals; 27/57 membrane-like individually; rim level 0.276)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.22, rim/outside 29 (aggregate of 57 individuals; 46/57 membrane-like individually; rim level 0.354)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.93, rim/outside 0.838 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.167)
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 5.86, rim/outside 0.182 (aggregate of 57 individuals; 2/57 membrane-like individually; rim level 0.0593)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #1 (t=142, R_eq 7.11): ['A0']; #2 (t=108, R_eq 6.38): ['A0']; #102 (t=652, R_eq 4.48): none; #181 (t=774, R_eq 5.26): ['A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 57 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
