# Evidence pack: active-gel-fed-comets (seed 3)

- world: `../../20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 48s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out collective/contrib/20261025T1118-c01-review-gel-twin/world --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0203, 7.9846], min area 6 px

## Measurements
- components: final 9, mean 12.2, max 48; occupancy final 0.01
- tracks: 111; persistent (alive >= 50% of run): 7; longest 182 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.519/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 20, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 4.11, nucleations 57
- channel total drift (end/start - 1): [-0.8351, -0.6879, -0.4197]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 90 at frame 111: holes 0, rim-vs-core 0.39, rim-vs-outside 0.22, heterogeneity 0.10; core [0.75, 0.481, 0.117] rim [0.366, 0.425, 0.161]
  - track 100 at frame 124: holes 0, rim-vs-core 0.51, rim-vs-outside 0.24, heterogeneity 0.13; core [0.853, 0.41, 0.085] rim [0.353, 0.334, 0.144]
  - track 101 at frame 124: holes 0, rim-vs-core 0.46, rim-vs-outside 0.26, heterogeneity 0.12; core [0.837, 0.443, 0.097] rim [0.39, 0.357, 0.15]
  - track 103 at frame 138: holes 0, rim-vs-core 0.47, rim-vs-outside 0.25, heterogeneity 0.13; core [0.844, 0.394, 0.096] rim [0.377, 0.347, 0.146]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.602, rim/outside 16.4 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.575)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.45 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.535)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.84, rim/outside 0.7 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.152)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #90 (t=111, R_eq 2.39): none; #100 (t=124, R_eq 2.65): none; #101 (t=124, R_eq 2.46): none; #103 (t=138, R_eq 2.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
