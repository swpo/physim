# Evidence pack: fl_shell (seed 6)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a non-flowing shell channel S that grows where a ring-convolved body density hits a set point (r-two56's k4 idea)
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 66s; status ok
- command: `python -m labkit.run world.py --out g0 --seeds 6 7 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.0197], min area 6 px

## Measurements
- components: final 17, mean 6.6, max 18; occupancy final 0.10
- tracks: 122; persistent (alive >= 50% of run): 0; longest 132 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 4, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 22, 18], H1 [7, 1, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.722/time; max body lengths 12.0
- replication (lineage window K = 20 frames = time 40, default): splits 44, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 5, merges 30, merge/split ratio 0.682, nucleations 0
- channel total drift (end/start - 1): [4.2876, 7.624, -0.5358, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 134: holes 0, rim-vs-core 0.27, rim-vs-outside 0.35, heterogeneity 0.23; core [0.331, 0.405, 0.338, 0.0] rim [0.244, 0.159, 0.415, 0.0]
  - track 24 at frame 279: holes 0, rim-vs-core 0.32, rim-vs-outside 0.21, heterogeneity 0.18; core [0.313, 0.366, 0.038, 0.0] rim [0.034, 0.206, 0.075, 0.0]
  - track 4 at frame 74: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.21; core [0.537, 0.299, 0.207, 0.0] rim [0.193, 0.21, 0.389, 0.0]
  - track 92 at frame 383: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.29; core [0.221, 0.555, 0.057, 0.606] rim [0.259, 0.094, 0.042, 0.386]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 16 (aggregate of 47 individuals; 17/47 membrane-like individually; rim level 0.261)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 19.6 (aggregate of 47 individuals; 23/47 membrane-like individually; rim level 0.318)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.93, rim/outside 0.79 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.152)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 0.663, rim/outside 0.293 (aggregate of 47 individuals; 1/47 membrane-like individually; rim level 0.0948)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=268, R_eq 7.9): none; #24 (t=558, R_eq 8.04): ['A1']; #4 (t=148, R_eq 6.48): ['A0']; #92 (t=766, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
