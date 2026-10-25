# Evidence pack: active-gel-fed-comets (seed 2)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 63s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1516-c13-review-acgel-window/world.py --out collective/contrib/20261025T1516-c13-review-acgel-window/runs/ks0.04_r2.0_k0.1 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.64 of robust range [0.0742, 1.531], min area 6 px

## Measurements
- components: final 13, mean 4.3, max 14; occupancy final 0.02
- tracks: 76; persistent (alive >= 50% of run): 0; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 14, 10], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 1.53/time; max body lengths 20.1
- replication (lineage window K = 20 frames = time 20, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 62
- channel total drift (end/start - 1): [-0.6272, -0.6268, -0.4661]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 270: holes 0, rim-vs-core 0.01, rim-vs-outside 0.18, heterogeneity 0.05; core [1.0, 0.332, 0.184] rim [0.999, 0.339, 0.187]
  - track 45 at frame 270: holes 0, rim-vs-core 0.05, rim-vs-outside 0.17, heterogeneity 0.05; core [1.0, 0.549, 0.156] rim [1.0, 0.501, 0.169]
  - track 40 at frame 262: holes 0, rim-vs-core 0.08, rim-vs-outside 0.24, heterogeneity 0.08; core [1.0, 0.491, 0.168] rim [0.994, 0.416, 0.194]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 3.06 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.982)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 1.61 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.458)
  - radial substrate s: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.51, rim/outside 0.841 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 0.203)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=270, R_eq 2.52): none; #45 (t=270, R_eq 2.26): none; #32 (t=239, R_eq 1.78): none; #40 (t=262, R_eq 2.76): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
