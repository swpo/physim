# Evidence pack: nrch (seed 3)

- world: `../../20261025T0840-c08-nrch-swimmers/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 592s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0840-c08-nrch-swimmers/world.py --out collective/contrib/20261025T0849-c01-review-nrch/recip --seeds 3 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [-1.3445, 1.4248], min area 6 px

## Measurements
- components: final 20, mean 33.5, max 71; occupancy final 0.30
- tracks: 84; persistent (alive >= 50% of run): 27; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 23.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 20], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 13, merge/split ratio n/a, nucleations 71
- channel total drift (end/start - 1): [0.0, 1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 61: holes 0, rim-vs-core 0.33, rim-vs-outside 0.72, heterogeneity 0.14; core [0.982, 0.036] rim [0.742, 0.266]
  - track 5 at frame 61: holes 0, rim-vs-core 0.26, rim-vs-outside 0.79, heterogeneity 0.14; core [0.986, 0.023] rim [0.8, 0.203]
  - track 14 at frame 62: holes 0, rim-vs-core 0.38, rim-vs-outside 0.54, heterogeneity 0.14; core [0.963, 0.034] rim [0.689, 0.301]
  - track 20 at frame 62: holes 0, rim-vs-core 0.34, rim-vs-outside 0.72, heterogeneity 0.15; core [0.983, 0.019] rim [0.738, 0.257]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 181 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 12.2 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.941)
  - radial psi: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 34.5, rim/outside 0.962 (aggregate of 181 individuals; 0/181 membrane-like individually; rim level 0.87)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3050, R_eq 13.28): none; #5 (t=3050, R_eq 11.48): none; #14 (t=3100, R_eq 9.66): none; #20 (t=3100, R_eq 10.42): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
