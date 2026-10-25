# Evidence pack: fl_shell2 (seed 11)

- world: `../../world.py`, family `flow-lenia`
- parent: flow-lenia/fl_food (rule from motion search screens/mot/C2_r202); mutation: fl_forager plus a set-point shell channel S (r-two56 k4 idea) that feeds back on the matter growth field through a disk kernel (r-two56 k5 idea), h5 0.3
- run: 401 frames x 10 steps x dt 0.2 = time 800; grid [128, 128]; wall 68s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27d/world.py --out collective/contrib/wip-c27d/rerun --seeds 11 12 --frames 400 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0, 2.1038], min area 6 px

## Measurements
- components: final 16, mean 8.6, max 18; occupancy final 0.09
- tracks: 164; persistent (alive >= 50% of run): 0; longest 145 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 23, 20], H1 [4, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.903/time; max body lengths 9.9
- replication (lineage window K = 20 frames = time 40, default): splits 59, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 5, merges 45, merge/split ratio 0.763, nucleations 0
- channel total drift (end/start - 1): [5.6749, 7.1626, -0.5384, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 222: holes 0, rim-vs-core 0.47, rim-vs-outside 0.05, heterogeneity 0.18; core [0.279, 0.427, 0.126, 0.0] rim [0.043, 0.023, 0.155, 0.0]
  - track 7 at frame 168: holes 0, rim-vs-core 0.40, rim-vs-outside 0.07, heterogeneity 0.19; core [0.249, 0.367, 0.193, 0.0] rim [0.02, 0.047, 0.266, 0.0]
  - track 20 at frame 269: holes 0, rim-vs-core 0.45, rim-vs-outside 0.09, heterogeneity 0.19; core [0.33, 0.41, 0.146, 0.0] rim [0.072, 0.043, 0.174, 0.0]
  - track 87 at frame 366: holes 0, rim-vs-core 0.46, rim-vs-outside 0.06, heterogeneity 0.19; core [0.327, 0.394, 0.061, 0.0] rim [0.053, 0.024, 0.071, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 18.6 (aggregate of 57 individuals; 23/57 membrane-like individually; rim level 0.274)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.58, rim/outside 24.4 (aggregate of 57 individuals; 37/57 membrane-like individually; rim level 0.343)  MEMBRANE-LIKE
  - radial food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.13, rim/outside 0.8 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.177)
  - radial S: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.216 (aggregate of 57 individuals; 1/57 membrane-like individually; rim level 0.0768)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1 (peak at rho=0.45, outside the peak band)
- membrane-like channels per top track at mid-life: #14 (t=444, R_eq 5.23): ['A0', 'A1']; #7 (t=336, R_eq 5.86): ['A1']; #20 (t=538, R_eq 4.79): ['A0', 'A1']; #87 (t=732, R_eq 5.11): ['A0', 'A1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
