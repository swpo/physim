# Evidence pack: active-gel-fed-comets (seed 4)

- world: `../../20261025T1016-c09-active-gel-comets-claim/world_starve.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 59s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world_starve.py --out collective/contrib/20261025T1028-c06-review-c09-gel-comets/rerun_starve --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0, 8.2903], min area 6 px

## Measurements
- components: final 0, mean 8.8, max 53; occupancy final 0.00
- tracks: 104; persistent (alive >= 50% of run): 3; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.621/time; max body lengths 5.8
- replication (lineage window K = 20 frames = time 20, default): splits 9, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 4.22, nucleations 47
- channel total drift (end/start - 1): [-0.9999, -0.7733, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 91 at frame 72: holes 0, rim-vs-core 0.23, rim-vs-outside 0.23, heterogeneity 0.06; core [0.669, 0.568, 0.358] rim [0.437, 0.542, 0.375]
  - track 96 at frame 74: holes 0, rim-vs-core 0.25, rim-vs-outside 0.23, heterogeneity 0.06; core [0.664, 0.532, 0.36] rim [0.42, 0.494, 0.38]
  - track 99 at frame 77: holes 0, rim-vs-core 0.35, rim-vs-outside 0.26, heterogeneity 0.08; core [0.788, 0.572, 0.332] rim [0.446, 0.52, 0.357]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 15.3 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.655)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 1.27 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.704)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.862 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.342)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #91 (t=72, R_eq 1.95): none; #94 (t=74, R_eq 1.69): none; #96 (t=74, R_eq 2.03): none; #99 (t=77, R_eq 2.19): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
