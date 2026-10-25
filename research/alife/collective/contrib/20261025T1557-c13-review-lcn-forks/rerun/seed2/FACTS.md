# Evidence pack: lcn (seed 2)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: closed nutrient ledger (losses return to food, no refill) + shell-gated food diffusion, full-domain noise
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [192, 192]; wall 104s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1557-c13-review-lcn-forks/world.py --out collective/contrib/20261025T1557-c13-review-lcn-forks/rerun/seed2 --seeds 2 --spf 50 --frames 200 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 31, mean 24.9, max 40; occupancy final 0.24
- tracks: 969; persistent (alive >= 50% of run): 0; longest 66 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 11.12, final 13; holes at thresholds 0.2/0.35/0.5 final [18, 23, 20]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 42, 32], H1 [46, 41, 14]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 100, default): splits 306, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 338, merge/split ratio 1.1, nucleations 7
- channel total drift (end/start - 1): [-0.6187, -0.3776, -0.2395, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 379 at frame 128: holes 0, rim-vs-core 0.12, rim-vs-outside 0.98, heterogeneity 0.22; core [0.872, 0.296, 0.704, 0.125] rim [0.759, 0.273, 0.694, 0.136]
  - track 415 at frame 124: holes 0, rim-vs-core 0.18, rim-vs-outside 1.11, heterogeneity 0.20; core [0.889, 0.287, 0.749, 0.098] rim [0.752, 0.166, 0.749, 0.099]
  - track 553 at frame 148: holes 0, rim-vs-core 0.16, rim-vs-outside 0.99, heterogeneity 0.21; core [0.884, 0.262, 0.737, 0.092] rim [0.727, 0.26, 0.733, 0.096]
  - track 595 at frame 150: holes 0, rim-vs-core 0.21, rim-vs-outside 0.93, heterogeneity 0.22; core [0.904, 0.282, 0.677, 0.152] rim [0.697, 0.289, 0.676, 0.157]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 167 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 12.4 (aggregate of 167 individuals; 100/167 membrane-like individually; rim level 0.744)
  - radial A1: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 2.19 (aggregate of 167 individuals; 42/167 membrane-like individually; rim level 0.688)
  - radial F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.919 (aggregate of 167 individuals; 0/167 membrane-like individually; rim level 0.449)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 1.13 (aggregate of 167 individuals; 0/167 membrane-like individually; rim level 0.442)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #379 (t=640, R_eq 6.21): ['A0']; #415 (t=620, R_eq 6.15): none; #553 (t=740, R_eq 6.23): ['A0']; #595 (t=750, R_eq 6.26): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 47 of 167 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
