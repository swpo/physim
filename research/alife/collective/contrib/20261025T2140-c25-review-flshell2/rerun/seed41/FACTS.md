# Evidence pack: fl_shell2 (seed 41)

- world: `../../../20261025T1748-c18-flshell2-metabolic-cell-claim/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 96s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1748-c18-flshell2-metabolic-cell-claim/world.py --out collective/contrib/20261025T2140-c25-review-flshell2/rerun --seeds 41 42 --frames 400 --no-movie`
- segmentation: matter > 0.08 of robust range [0.0, 1.9139], min area 6 px

## Measurements
- components: final 10, mean 4.9, max 13; occupancy final 0.09
- tracks: 126; persistent (alive >= 50% of run): 2; longest 244 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.32 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [4, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 14, 11], H1 [8, 3, 1]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.948/time; max body lengths 14.8
- replication (lineage window K = 20 frames = time 40, default): splits 43, persistent splits 6 (1 more failed only because the siblings re-merged within K), max generation 3, merges 35, merge/split ratio 0.814, nucleations 2
- channel total drift (end/start - 1): [5.6197, 6.1992, -0.5335, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 131: holes 0, rim-vs-core 0.37, rim-vs-outside 0.25, heterogeneity 0.22; core [0.357, 0.395, 0.255, 0.0] rim [0.222, 0.062, 0.349, 0.0]
  - track 2 at frame 121: holes 0, rim-vs-core 0.17, rim-vs-outside 0.39, heterogeneity 0.21; core [0.305, 0.363, 0.221, 0.0] rim [0.28, 0.211, 0.284, 0.0]
  - track 44 at frame 316: holes 0, rim-vs-core 0.41, rim-vs-outside 0.06, heterogeneity 0.18; core [0.289, 0.373, 0.053, 0.0] rim [0.046, 0.04, 0.06, 0.0]
  - track 99 at frame 383: holes 0, rim-vs-core 0.50, rim-vs-outside 0.04, heterogeneity 0.18; core [0.369, 0.385, 0.068, 0.0] rim [0.036, 0.006, 0.072, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.55, rim/outside 16.6 (aggregate of 34 individuals; 20/34 membrane-like individually; rim level 0.318)  MEMBRANE-LIKE
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.777, rim/outside 19.6 (aggregate of 34 individuals; 6/34 membrane-like individually; rim level 0.262)
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.64, rim/outside 0.814 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.151)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 2.95, rim/outside 0.36 (aggregate of 34 individuals; 8/34 membrane-like individually; rim level 0.0877)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #1 (t=262, R_eq 9.27): ['S']; #2 (t=242, R_eq 10.06): ['S']; #44 (t=632, R_eq 5.35): ['A0', 'A1']; #99 (t=766, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
