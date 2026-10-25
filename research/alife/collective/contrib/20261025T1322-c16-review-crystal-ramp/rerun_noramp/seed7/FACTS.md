# Evidence pack: nrch (seed 7)

- world: `../../../20261025T1132-c08-crystal-ramp-negative/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1357s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1132-c08-crystal-ramp-negative/world.py --out collective/contrib/20261025T1322-c16-review-crystal-ramp/rerun_noramp/seed7 --seeds 7 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9016, 0.9024], min area 6 px

## Measurements
- components: final 22, mean 21.9, max 38; occupancy final 0.21
- tracks: 387; persistent (alive >= 50% of run): 22; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.81 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 103.2
- replication (lineage window K = 20 frames = time 1000, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 3, nucleations 377
- channel total drift (end/start - 1): [-0.0788, 47.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 138 at frame 97: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.20; core [0.926, 0.362] rim [0.668, 0.41]
  - track 209 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.37, heterogeneity 0.21; core [0.927, 0.373] rim [0.667, 0.419]
  - track 264 at frame 106: holes 0, rim-vs-core 0.17, rim-vs-outside 0.45, heterogeneity 0.20; core [0.913, 0.359] rim [0.746, 0.405]
  - track 288 at frame 110: holes 0, rim-vs-core 0.18, rim-vs-outside 0.49, heterogeneity 0.20; core [0.92, 0.497] rim [0.784, 0.372]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 131 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 9.98 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.798)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.974 (aggregate of 131 individuals; 0/131 membrane-like individually; rim level 0.575)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #138 (t=4850, R_eq 10.69): none; #209 (t=5050, R_eq 10.87): none; #264 (t=5300, R_eq 10.62): none; #288 (t=5500, R_eq 10.72): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
