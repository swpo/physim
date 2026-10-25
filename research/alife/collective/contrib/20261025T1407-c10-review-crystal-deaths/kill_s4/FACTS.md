# Evidence pack: nrch (seed 4)

- world: `../../20261025T1151-c08-crystal-deaths-negative/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 181 frames x 1000 steps x dt 0.05 = time 9000; grid [192, 192]; wall 1291s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1151-c08-crystal-deaths-negative/world.py --out collective/contrib/20261025T1407-c10-review-crystal-deaths/kill_s4 --seeds 4 --frames 180 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.9111, 0.9071], min area 6 px

## Measurements
- components: final 12, mean 16.4, max 38; occupancy final 0.19
- tracks: 443; persistent (alive >= 50% of run): 2; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 12, 12], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.265/time; max body lengths 46.7
- replication (lineage window K = 20 frames = time 1000, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.5, nucleations 423
- channel total drift (end/start - 1): [-0.138, -5.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 365 at frame 127: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.20; core [0.923, 0.355] rim [0.668, 0.392]
  - track 383 at frame 133: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.20; core [0.92, 0.341] rim [0.664, 0.388]
  - track 404 at frame 139: holes 0, rim-vs-core 0.26, rim-vs-outside 0.36, heterogeneity 0.20; core [0.922, 0.34] rim [0.662, 0.389]
  - track 409 at frame 141: holes 0, rim-vs-core 0.19, rim-vs-outside 0.41, heterogeneity 0.20; core [0.92, 0.354] rim [0.737, 0.388]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [30, 61, 91, 119, 150, 180]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.1 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.755)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.935 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.511)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #365 (t=6350, R_eq 13.87): none; #383 (t=6650, R_eq 13.6): none; #404 (t=6950, R_eq 13.61): none; #409 (t=7050, R_eq 13.67): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
