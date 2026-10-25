# Evidence pack: nrch (seed 7)

- world: `../../../20261025T1151-c08-crystal-deaths-negative/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1341s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1151-c08-crystal-deaths-negative/world.py --out collective/contrib/20261025T1458-c16-review-crystal-deaths/rerun/seed7 --seeds 7 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9012, 0.9025], min area 6 px

## Measurements
- components: final 21, mean 21.8, max 38; occupancy final 0.20
- tracks: 402; persistent (alive >= 50% of run): 16; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 21, 21], H1 [0, 0, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.271/time; max body lengths 102.6
- replication (lineage window K = 20 frames = time 1000, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 2.5, nucleations 393
- channel total drift (end/start - 1): [-0.1157, -17.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 209 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.38, heterogeneity 0.20; core [0.93, 0.348] rim [0.664, 0.396]
  - track 264 at frame 106: holes 0, rim-vs-core 0.18, rim-vs-outside 0.44, heterogeneity 0.20; core [0.921, 0.38] rim [0.744, 0.412]
  - track 274 at frame 107: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.929, 0.367] rim [0.674, 0.41]
  - track 288 at frame 110: holes 0, rim-vs-core 0.18, rim-vs-outside 0.49, heterogeneity 0.20; core [0.921, 0.494] rim [0.784, 0.372]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 9.73 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.795)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.973 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.575)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #209 (t=5050, R_eq 10.78): none; #264 (t=5300, R_eq 10.85): none; #274 (t=5350, R_eq 10.65): none; #288 (t=5500, R_eq 10.67): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
