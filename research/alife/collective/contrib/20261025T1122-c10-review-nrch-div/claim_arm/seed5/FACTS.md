# Evidence pack: nrch (seed 5)

- world: `../../../20261025T1017-c08-nrch-no-persistent-division/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 816s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py --out collective/contrib/20261025T1122-c10-review-nrch-div/claim_arm/seed5 --seeds 5 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0686, 1.0719], min area 6 px

## Measurements
- components: final 4, mean 5.0, max 15; occupancy final 0.22
- tracks: 81; persistent (alive >= 50% of run): 0; longest 58 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.167/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 1000, default): splits 12, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 14, merge/split ratio 1.17, nucleations 42
- channel total drift (end/start - 1): [0.0, 257.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 69: holes 0, rim-vs-core 0.25, rim-vs-outside 0.43, heterogeneity 0.17; core [0.949, 0.383] rim [0.698, 0.358]
  - track 37 at frame 65: holes 0, rim-vs-core 0.24, rim-vs-outside 0.32, heterogeneity 0.17; core [0.882, 0.424] rim [0.653, 0.502]
  - track 72 at frame 101: holes 0, rim-vs-core 0.21, rim-vs-outside 0.39, heterogeneity 0.16; core [0.884, 0.431] rim [0.681, 0.483]
  - track 40 at frame 55: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.17; core [0.931, 0.282] rim [0.712, 0.352]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 5.95 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.757)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.958 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.541)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=3450, R_eq 17.97): none; #37 (t=3250, R_eq 12.23): none; #72 (t=5050, R_eq 14.87): none; #40 (t=2750, R_eq 21.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
