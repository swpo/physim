# Evidence pack: active-gel-fed-comets-twin (seed 7)

- world: `../../../../contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_global.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 54s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_global.py --out collective/work_c05/rev_gt/global/seed7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 3.245], min area 6 px

## Measurements
- components: final 1, mean 5.6, max 41; occupancy final 0.00
- tracks: 190; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 1.63/time; max body lengths 5.3
- replication (lineage window K = 20 frames = time 20, default): splits 74, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 42
- channel total drift (end/start - 1): [-0.9802, -0.7895, -0.0828]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 189 at frame 168: holes 0, rim-vs-core 0.28, rim-vs-outside 0.18, heterogeneity 0.10; core [0.796, 0.172, 0.294] rim [0.525, 0.154, 0.374]
  - track 185 at frame 111: holes 0, rim-vs-core 0.36, rim-vs-outside 0.22, heterogeneity 0.12; core [0.897, 0.358, 0.261] rim [0.546, 0.346, 0.329]
  - track 62 at frame 20: holes 0, rim-vs-core 0.20, rim-vs-outside 0.14, heterogeneity 0.06; core [0.721, 0.917, 0.021] rim [0.52, 0.914, 0.039]
  - track 72 at frame 22: holes 0, rim-vs-core 0.28, rim-vs-outside 0.18, heterogeneity 0.07; core [0.814, 0.937, 0.019] rim [0.532, 0.923, 0.038]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 7.04 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.7)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 1.06 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.696)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.43, rim/outside 0.807 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.186)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #189 (t=168, R_eq 4.65): none; #185 (t=111, R_eq 4.79): none; #62 (t=20, R_eq 4.58): none; #72 (t=22, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
