# Evidence pack: active-gel-fed-comets (seed 2)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world.py --out /tmp/claude-0/c09/ag/claim/pack --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0196, 8.4101], min area 6 px

## Measurements
- components: final 9, mean 12.4, max 49; occupancy final 0.01
- tracks: 103; persistent (alive >= 50% of run): 9; longest 183 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.496/time; max body lengths 12.1
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 37, merge/split ratio 5.29, nucleations 52
- channel total drift (end/start - 1): [-0.8322, -0.6884, -0.4206]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 85 at frame 109: holes 0, rim-vs-core 0.34, rim-vs-outside 0.26, heterogeneity 0.08; core [0.746, 0.484, 0.138] rim [0.412, 0.427, 0.176]
  - track 87 at frame 111: holes 0, rim-vs-core 0.42, rim-vs-outside 0.22, heterogeneity 0.11; core [0.756, 0.486, 0.116] rim [0.341, 0.407, 0.166]
  - track 93 at frame 113: holes 0, rim-vs-core 0.44, rim-vs-outside 0.28, heterogeneity 0.11; core [0.829, 0.485, 0.105] rim [0.402, 0.407, 0.154]
  - track 95 at frame 114: holes 0, rim-vs-core 0.34, rim-vs-outside 0.25, heterogeneity 0.08; core [0.743, 0.525, 0.134] rim [0.412, 0.474, 0.17]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.598, rim/outside 16 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.566)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 1.51 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.534)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.67, rim/outside 0.723 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.169)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #85 (t=109, R_eq 2.19): none; #87 (t=111, R_eq 2.52): none; #93 (t=113, R_eq 2.52): none; #95 (t=114, R_eq 2.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
