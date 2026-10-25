# Evidence pack: nrch (seed 4)

- world: `../../20261025T1017-c08-nrch-no-persistent-division/world.py`, family `active-emulsion`
- parent: None; mutation: reference: nonreciprocal Cahn-Hilliard (Brauns-Marchetti 2024), phi phase-separating, psi diffusive
- run: 121 frames x 1000 steps x dt 0.05 = time 6000; grid [192, 192]; wall 636s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1017-c08-nrch-no-persistent-division/world.py --out collective/contrib/20261025T1129-c01-review-nrch-division/rerun --seeds 4 --frames 120 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-1.0103, 1.0173], min area 6 px

## Measurements
- components: final 4, mean 4.9, max 12; occupancy final 0.23
- tracks: 32; persistent (alive >= 50% of run): 2; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 17.59 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.129/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 1000, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 6, merge/split ratio 1, nucleations 15
- channel total drift (end/start - 1): [0.0, 129.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 70: holes 0, rim-vs-core 0.15, rim-vs-outside 0.56, heterogeneity 0.17; core [0.942, 0.328] rim [0.793, 0.363]
  - track 28 at frame 90: holes 0, rim-vs-core 0.19, rim-vs-outside 0.62, heterogeneity 0.17; core [0.966, 0.375] rim [0.78, 0.375]
  - track 29 at frame 95: holes 0, rim-vs-core 0.20, rim-vs-outside 0.62, heterogeneity 0.18; core [0.97, 0.359] rim [0.778, 0.311]
  - track 4 at frame 43: holes 0, rim-vs-core 0.20, rim-vs-outside 0.58, heterogeneity 0.18; core [0.96, 0.375] rim [0.774, 0.455]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 7.47 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.818)
  - radial psi: peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.75, rim/outside 1 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.604)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3500, R_eq 14.3): none; #28 (t=4500, R_eq 25.67): none; #29 (t=4750, R_eq 25.26): none; #4 (t=2150, R_eq 18.81): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
