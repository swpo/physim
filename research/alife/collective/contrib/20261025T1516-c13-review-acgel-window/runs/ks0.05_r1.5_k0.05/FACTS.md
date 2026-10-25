# Evidence pack: active-gel-fed-comets (seed 2)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 65s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1516-c13-review-acgel-window/world.py --out collective/contrib/20261025T1516-c13-review-acgel-window/runs/ks0.05_r1.5_k0.05 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.19 of robust range [0.0439, 5.1598], min area 6 px

## Measurements
- components: final 15, mean 14.8, max 39; occupancy final 0.04
- tracks: 244; persistent (alive >= 50% of run): 1; longest 162 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 11], H1 [0, 0, 0]
- motion: 73 long-lived tracks moved >= 1 body length; max speed 1.9/time; max body lengths 19.9
- replication (lineage window K = 20 frames = time 20, default): splits 34, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 85, merge/split ratio 2.5, nucleations 92
- channel total drift (end/start - 1): [-0.63, -0.6318, -0.3689]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 153 at frame 219: holes 0, rim-vs-core 0.52, rim-vs-outside 0.23, heterogeneity 0.20; core [0.87, 0.434, 0.088] rim [0.372, 0.318, 0.19]
  - track 56 at frame 66: holes 0, rim-vs-core 0.41, rim-vs-outside 0.19, heterogeneity 0.16; core [0.726, 0.524, 0.104] rim [0.353, 0.385, 0.184]
  - track 106 at frame 86: holes 0, rim-vs-core 0.45, rim-vs-outside 0.21, heterogeneity 0.18; core [0.774, 0.41, 0.145] rim [0.344, 0.295, 0.227]
  - track 188 at frame 222: holes 0, rim-vs-core 0.53, rim-vs-outside 0.22, heterogeneity 0.18; core [0.85, 0.378, 0.097] rim [0.35, 0.244, 0.205]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.667, rim/outside 12.5 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.577)
  - radial regulator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 1.99 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.478)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.58, rim/outside 0.763 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.278)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #153 (t=219, R_eq 3.99): none; #56 (t=66, R_eq 3.7): none; #106 (t=86, R_eq 3.52): none; #188 (t=222, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
