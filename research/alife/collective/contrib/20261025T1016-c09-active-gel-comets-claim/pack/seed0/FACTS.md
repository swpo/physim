# Evidence pack: active-gel-fed-comets (seed 0)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 201 frames x 100 steps x dt 0.01 = time 200; grid [128, 128]; wall 44s; status ok
- command: `python -m labkit.run /tmp/claude-0/c09/ag/claim/world.py --out /tmp/claude-0/c09/ag/claim/pack --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.12 of robust range [0.0193, 8.2627], min area 6 px

## Measurements
- components: final 11, mean 11.3, max 49; occupancy final 0.01
- tracks: 108; persistent (alive >= 50% of run): 5; longest 180 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 11], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.55/time; max body lengths 11.1
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 38, merge/split ratio 5.43, nucleations 51
- channel total drift (end/start - 1): [-0.8463, -0.6862, -0.4164]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 88 at frame 111: holes 0, rim-vs-core 0.48, rim-vs-outside 0.24, heterogeneity 0.12; core [0.815, 0.45, 0.096] rim [0.346, 0.363, 0.155]
  - track 89 at frame 111: holes 0, rim-vs-core 0.45, rim-vs-outside 0.22, heterogeneity 0.12; core [0.77, 0.496, 0.103] rim [0.329, 0.426, 0.155]
  - track 99 at frame 129: holes 0, rim-vs-core 0.51, rim-vs-outside 0.18, heterogeneity 0.14; core [0.783, 0.402, 0.079] rim [0.286, 0.321, 0.143]
  - track 100 at frame 134: holes 0, rim-vs-core 0.53, rim-vs-outside 0.26, heterogeneity 0.14; core [0.897, 0.386, 0.07] rim [0.375, 0.332, 0.127]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.598, rim/outside 16.7 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.566)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.852, rim/outside 1.52 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.505)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.76, rim/outside 0.716 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.164)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #88 (t=111, R_eq 2.65): none; #89 (t=111, R_eq 2.65): none; #99 (t=129, R_eq 2.76): none; #100 (t=134, R_eq 2.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
