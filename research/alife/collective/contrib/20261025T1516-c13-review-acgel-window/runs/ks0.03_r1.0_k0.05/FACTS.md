# Evidence pack: active-gel-fed-comets (seed 2)

- world: `../../world.py`, family `active-gel`
- parent: none (new class); mutation: new class: advection of stress generator and regulator by a contractile active-gel flow
- run: 301 frames x 100 steps x dt 0.01 = time 300; grid [128, 128]; wall 64s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1516-c13-review-acgel-window/world.py --out collective/contrib/20261025T1516-c13-review-acgel-window/runs/ks0.03_r1.0_k0.05 --seeds 2 --frames 300 --no-movie`
- segmentation: matter > 0.18 of robust range [0.0343, 5.5304], min area 6 px

## Measurements
- components: final 9, mean 11.0, max 53; occupancy final 0.02
- tracks: 198; persistent (alive >= 50% of run): 0; longest 141 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 8, 5], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 1.85/time; max body lengths 21.1
- replication (lineage window K = 20 frames = time 20, default): splits 16, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 78, merge/split ratio 4.88, nucleations 90
- channel total drift (end/start - 1): [-0.767, -0.759, -0.3963]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 141 at frame 126: holes 0, rim-vs-core 0.56, rim-vs-outside 0.23, heterogeneity 0.19; core [0.892, 0.338, 0.148] rim [0.35, 0.234, 0.232]
  - track 23 at frame 63: holes 0, rim-vs-core 0.19, rim-vs-outside 0.19, heterogeneity 0.07; core [0.579, 0.498, 0.148] rim [0.411, 0.423, 0.175]
  - track 176 at frame 250: holes 0, rim-vs-core 0.54, rim-vs-outside 0.27, heterogeneity 0.18; core [0.921, 0.362, 0.116] rim [0.395, 0.244, 0.194]
  - track 120 at frame 71: holes 0, rim-vs-core 0.22, rim-vs-outside 0.19, heterogeneity 0.08; core [0.613, 0.441, 0.19] rim [0.406, 0.366, 0.221]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 55 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial generator a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.707, rim/outside 17.1 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.665)
  - radial regulator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 2.18 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.383)
  - radial substrate s: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.92, rim/outside 0.756 (aggregate of 55 individuals; 0/55 membrane-like individually; rim level 0.25)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #141 (t=126, R_eq 3.34): none; #23 (t=63, R_eq 2.11): none; #176 (t=250, R_eq 3.19): none; #120 (t=71, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
