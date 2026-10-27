# Evidence pack: fed-wave-matter (seed 6)

- world: `../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 25s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/20261027T1648-c58-review-sp/pack0 --seeds 6 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.01 of robust range [0.0033, 31.7636], min area 6 px

## Measurements
- components: final 26, mean 26.7, max 48; occupancy final 0.65
- tracks: 4088; persistent (alive >= 50% of run): 0; longest 7 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.05, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 200, default): splits 426, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 428, merge/split ratio 1, nucleations 2132
- channel total drift (end/start - 1): [0.0, -0.3803, None, 0.9689]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 923 at frame 57: holes 0, rim-vs-core 0.03, rim-vs-outside 0.08, heterogeneity 0.07; core [0.037, 0.78, 0.058, 0.418] rim [0.027, 0.784, 0.054, 0.389]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.394, rim/outside 1.69 (aggregate of 84 individuals; 21/84 membrane-like individually; rim level 0.0289)
  - radial fuel Y: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 1.01 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.745)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.594, rim/outside 1.16 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.132)
  - radial phase cos: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1 (aggregate of 84 individuals; 7/84 membrane-like individually; rim level 0.503)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1400 (t=810, R_eq 2.19, ring): ['density |psi|^2']; #417 (t=340, R_eq 1.95, ring): ['density |psi|^2']; #448 (t=350, R_eq 1.78): ['phase cos']; #923 (t=570, R_eq 3.14): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 84 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
