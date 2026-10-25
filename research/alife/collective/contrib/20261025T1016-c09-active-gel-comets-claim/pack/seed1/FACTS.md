# Evidence pack: active-gel-fed-comets (seed 1)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world.py --out /tmp/claude-0/c09/ag/claim/pack --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.02, 8.3475], min area 6 px

## Measurements
- components: final 10, mean 12.1, max 58; occupancy final 0.01
- tracks: 116; persistent (alive >= 50% of run): 7; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.716/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 43, merge/split ratio 6.14, nucleations 58
- channel total drift (end/start - 1): [-0.839, -0.687, -0.4189]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 111: holes 0, rim-vs-core 0.43, rim-vs-outside 0.29, heterogeneity 0.09; core [0.867, 0.481, 0.11] rim [0.446, 0.423, 0.153]
  - track 102 at frame 111: holes 0, rim-vs-core 0.29, rim-vs-outside 0.20, heterogeneity 0.07; core [0.629, 0.496, 0.155] rim [0.346, 0.448, 0.189]
  - track 107 at frame 114: holes 0, rim-vs-core 0.46, rim-vs-outside 0.21, heterogeneity 0.12; core [0.781, 0.431, 0.11] rim [0.33, 0.366, 0.162]
  - track 109 at frame 121: holes 0, rim-vs-core 0.48, rim-vs-outside 0.23, heterogeneity 0.12; core [0.825, 0.482, 0.089] rim [0.352, 0.404, 0.142]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 56 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.605, rim/outside 16 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.574)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 1.51 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.543)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.64, rim/outside 0.699 (aggregate of 56 individuals; 0/56 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=111, R_eq 2.26): none; #102 (t=111, R_eq 2.26): none; #107 (t=114, R_eq 2.59): none; #109 (t=121, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
