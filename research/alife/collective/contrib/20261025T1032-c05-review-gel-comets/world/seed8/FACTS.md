# Evidence pack: active-gel-fed-comets (seed 8)

- world: `../../../../contrib/20261025T1016-c09-active-gel-comets-claim/world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1016-c09-active-gel-comets-claim/world.py --out collective/work_c05/rev_gel/world/seed8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0189, 8.5349], min area 6 px

## Measurements
- components: final 8, mean 11.1, max 46; occupancy final 0.01
- tracks: 102; persistent (alive >= 50% of run): 7; longest 175 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.558/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 36, merge/split ratio 5.14, nucleations 52
- channel total drift (end/start - 1): [-0.8338, -0.6845, -0.4274]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 91 at frame 114: holes 0, rim-vs-core 0.45, rim-vs-outside 0.21, heterogeneity 0.12; core [0.776, 0.454, 0.106] rim [0.329, 0.393, 0.158]
  - track 93 at frame 116: holes 0, rim-vs-core 0.49, rim-vs-outside 0.21, heterogeneity 0.13; core [0.786, 0.453, 0.084] rim [0.31, 0.366, 0.143]
  - track 89 at frame 104: holes 0, rim-vs-core 0.43, rim-vs-outside 0.23, heterogeneity 0.11; core [0.782, 0.471, 0.116] rim [0.36, 0.409, 0.164]
  - track 92 at frame 106: holes 0, rim-vs-core 0.37, rim-vs-outside 0.23, heterogeneity 0.09; core [0.729, 0.478, 0.123] rim [0.364, 0.428, 0.164]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.624, rim/outside 17.8 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.593)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 1.56 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.553)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.97, rim/outside 0.681 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.152)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #91 (t=114, R_eq 2.59): none; #93 (t=116, R_eq 2.76): none; #89 (t=104, R_eq 2.46): none; #92 (t=106, R_eq 2.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
