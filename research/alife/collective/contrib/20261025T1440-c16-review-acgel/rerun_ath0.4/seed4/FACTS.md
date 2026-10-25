# Evidence pack: active-gel-ac-cells (seed 4)

- world: `../../../20261025T1249-c09-ac-gel-cells-bistable/world.py`, family `active-gel`
- parent: 20261025T1016-c09-active-gel-comets-claim; mutation: the gel lives inside Allen-Cahn cells that it holds up and carries
- run: 101 frames x 300 steps x dt 0.01 = time 300; grid [128, 128]; wall 201s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1249-c09-ac-gel-cells-bistable/world.py --out collective/contrib/20261025T1440-c16-review-acgel/rerun_ath0.4/seed4 --seeds 4 --frames 100 --spf 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 0.9, max 38; occupancy final 0.00
- tracks: 44; persistent (alive >= 50% of run): 0; longest 17 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -0.8979, -0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 42 at frame 11: holes 0, rim-vs-core 0.46, rim-vs-outside 0.75, heterogeneity 0.23; core [0.997, 0.545, 0.939, 0.012] rim [0.837, 0.261, 0.621, 0.086]
  - track 40 at frame 10: holes 0, rim-vs-core 0.68, rim-vs-outside 0.46, heterogeneity 0.23; core [0.981, 0.598, 0.86, 0.006] rim [0.703, 0.146, 0.447, 0.102]
  - track 43 at frame 9: holes 0, rim-vs-core 0.85, rim-vs-outside 0.46, heterogeneity 0.24; core [0.96, 0.774, 0.902, 0.003] rim [0.686, 0.101, 0.476, 0.09]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [17]):
  - radial cell phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 6.89 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.761)
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 8.11 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.825)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.32 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 1)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 15.9, rim/outside 0.458 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #42 (t=33, R_eq 15.52): none; #40 (t=30, R_eq 13.87): none; #43 (t=27, R_eq 10.33): none; #41 (t=9, R_eq 1.49): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
