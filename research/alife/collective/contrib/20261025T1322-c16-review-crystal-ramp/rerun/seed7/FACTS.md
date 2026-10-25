# Evidence pack: nrch (seed 7)

- world: `../../../20261025T1132-c08-crystal-ramp-negative/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1353s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1132-c08-crystal-ramp-negative/world.py --out collective/contrib/20261025T1322-c16-review-crystal-ramp/rerun/seed7 --seeds 7 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-0.9019, 0.9257], min area 6 px

## Measurements
- components: final 22, mean 21.8, max 38; occupancy final 0.27
- tracks: 380; persistent (alive >= 50% of run): 22; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 97.7
- replication (lineage window K = 20 frames = time 1000, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 2.5, nucleations 371
- channel total drift (end/start - 1): [0.1572, 15.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 138 at frame 97: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.923, 0.375] rim [0.664, 0.408]
  - track 209 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.21; core [0.923, 0.378] rim [0.654, 0.418]
  - track 264 at frame 106: holes 0, rim-vs-core 0.16, rim-vs-outside 0.46, heterogeneity 0.20; core [0.912, 0.381] rim [0.749, 0.402]
  - track 274 at frame 107: holes 0, rim-vs-core 0.27, rim-vs-outside 0.37, heterogeneity 0.20; core [0.926, 0.387] rim [0.661, 0.417]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 9.98 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.803)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.97 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.573)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #138 (t=4850, R_eq 11.16): none; #209 (t=5050, R_eq 11.45): none; #264 (t=5300, R_eq 11.17): none; #274 (t=5350, R_eq 11.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
