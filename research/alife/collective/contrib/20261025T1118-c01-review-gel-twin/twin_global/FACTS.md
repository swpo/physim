# Evidence pack: active-gel-fed-comets-twin (seed 3)

- world: `../../20261025T1046-c09-active-gel-bd-twin/world_twin_global.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1046-c09-active-gel-bd-twin/world_twin_global.py --out collective/contrib/20261025T1118-c01-review-gel-twin/twin_global --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 3.2393], min area 6 px

## Measurements
- components: final 1, mean 5.7, max 43; occupancy final 0.01
- tracks: 222; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 2.85/time; max body lengths 6.0
- replication (lineage window K = 20 frames = time 20, default): splits 91, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 40
- channel total drift (end/start - 1): [-0.9687, -0.7848, -0.1013]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 18: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.08; core [0.902, 0.942, 0.005] rim [0.592, 0.938, 0.03]
  - track 83 at frame 20: holes 0, rim-vs-core 0.10, rim-vs-outside 0.14, heterogeneity 0.03; core [0.627, 0.901, 0.004] rim [0.522, 0.901, 0.01]
  - track 183 at frame 69: holes 0, rim-vs-core 0.26, rim-vs-outside 0.15, heterogeneity 0.09; core [0.751, 0.614, 0.193] rim [0.497, 0.608, 0.229]
  - track 75 at frame 20: holes 0, rim-vs-core 0.16, rim-vs-outside 0.16, heterogeneity 0.05; core [0.717, 0.922, 0.017] rim [0.554, 0.917, 0.029]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 6.36 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.734)
  - radial regulator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.991, rim/outside 1.05 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.659)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.21, rim/outside 0.835 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.22)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #15 (t=18, R_eq 6.89): none; #83 (t=20, R_eq 2.19): none; #183 (t=69, R_eq 4.33): none; #75 (t=20, R_eq 2.71): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
