# Evidence pack: active-gel-fed-comets (seed 4)

- world: `../../20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 58s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out collective/contrib/20261025T1028-c06-review-c09-gel-comets/rerun --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0199, 8.2903], min area 6 px

## Measurements
- components: final 12, mean 12.3, max 53; occupancy final 0.01
- tracks: 108; persistent (alive >= 50% of run): 8; longest 183 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.40 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.621/time; max body lengths 10.3
- replication (lineage window K = 20 frames = time 20, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 4.22, nucleations 51
- channel total drift (end/start - 1): [-0.8334, -0.6871, -0.4248]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 91 at frame 109: holes 0, rim-vs-core 0.38, rim-vs-outside 0.21, heterogeneity 0.09; core [0.71, 0.51, 0.131] rim [0.335, 0.44, 0.176]
  - track 94 at frame 111: holes 0, rim-vs-core 0.34, rim-vs-outside 0.23, heterogeneity 0.08; core [0.702, 0.519, 0.125] rim [0.369, 0.454, 0.164]
  - track 99 at frame 114: holes 0, rim-vs-core 0.37, rim-vs-outside 0.24, heterogeneity 0.09; core [0.748, 0.482, 0.131] rim [0.383, 0.417, 0.173]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.616, rim/outside 16 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.582)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 1.5 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.513)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.47, rim/outside 0.72 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.169)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #91 (t=109, R_eq 2.46): none; #94 (t=111, R_eq 2.33): none; #96 (t=113, R_eq 2.52): none; #99 (t=114, R_eq 2.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
