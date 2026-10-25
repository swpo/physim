# Evidence pack: active-gel-fed-comets (seed 6)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out /tmp/claude-0/c11rev9/world --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0201, 8.0089], min area 6 px

## Measurements
- components: final 9, mean 12.3, max 50; occupancy final 0.01
- tracks: 102; persistent (alive >= 50% of run): 7; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 9], H1 [0, 0, 0]
- motion: 31 long-lived tracks moved >= 1 body length; max speed 0.593/time; max body lengths 8.7
- replication (lineage window K = 20 frames = time 20, default): splits 6, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 6.17, nucleations 55
- channel total drift (end/start - 1): [-0.8386, -0.6876, -0.4199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 89 at frame 114: holes 0, rim-vs-core 0.42, rim-vs-outside 0.24, heterogeneity 0.11; core [0.794, 0.491, 0.111] rim [0.38, 0.42, 0.158]
  - track 91 at frame 118: holes 0, rim-vs-core 0.49, rim-vs-outside 0.23, heterogeneity 0.12; core [0.821, 0.43, 0.096] rim [0.343, 0.361, 0.151]
  - track 93 at frame 118: holes 0, rim-vs-core 0.46, rim-vs-outside 0.24, heterogeneity 0.13; core [0.824, 0.453, 0.079] rim [0.372, 0.388, 0.131]
  - track 94 at frame 129: holes 0, rim-vs-core 0.48, rim-vs-outside 0.24, heterogeneity 0.13; core [0.824, 0.47, 0.087] rim [0.351, 0.382, 0.144]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.603, rim/outside 15.6 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.571)
  - radial regulator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 1.49 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.544)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.85, rim/outside 0.69 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.149)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #89 (t=114, R_eq 2.39): none; #91 (t=118, R_eq 2.59): none; #93 (t=118, R_eq 2.59): none; #94 (t=129, R_eq 2.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
