# Evidence pack: nrch (seed 3)

- world: `../../20261025T0840-c08-nrch-swimmers/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 648s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0840-c08-nrch-swimmers/world.py --out collective/contrib/20261025T0849-c01-review-nrch/rerun --seeds 3 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.06, 1.0675], min area 6 px

## Measurements
- components: final 4, mean 4.8, max 12; occupancy final 0.22
- tracks: 71; persistent (alive >= 50% of run): 1; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.178/time; max body lengths 15.1
- replication (lineage window K = 20 frames = time 1000, default): splits 8, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 1, nucleations 45
- channel total drift (end/start - 1): [0.0, 257.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 62: holes 0, rim-vs-core 0.11, rim-vs-outside 0.49, heterogeneity 0.17; core [0.899, 0.371] rim [0.798, 0.327]
  - track 40 at frame 68: holes 0, rim-vs-core 0.18, rim-vs-outside 0.55, heterogeneity 0.17; core [0.943, 0.325] rim [0.767, 0.316]
  - track 46 at frame 72: holes 0, rim-vs-core 0.23, rim-vs-outside 0.58, heterogeneity 0.17; core [0.967, 0.413] rim [0.777, 0.279]
  - track 47 at frame 72: holes 0, rim-vs-core 0.22, rim-vs-outside 0.54, heterogeneity 0.18; core [0.958, 0.42] rim [0.753, 0.339]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 4.81 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.73)
  - radial psi: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.972 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.525)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=3100, R_eq 13.73): none; #40 (t=3400, R_eq 25.79): none; #46 (t=3600, R_eq 22.55): none; #47 (t=3600, R_eq 29.35): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
