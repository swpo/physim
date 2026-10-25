# Evidence pack: thinfilm-active (seed 8)

- world: `../../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 154s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2103-c21-review-thinfilm/rerun_g2 --seeds 7 8 --frames 80 --no-movie`
- segmentation: matter > 0.08 of robust range [0.034, 5.7603], min area 6 px

## Measurements
- components: final 1, mean 2.6, max 14; occupancy final 0.25
- tracks: 69; persistent (alive >= 50% of run): 1; longest 53 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.29 (1 = constant size)
- enclosures: components with a hole mean 0.41, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 2, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0546/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 22, merge/split ratio 1.1, nucleations 1
- channel total drift (end/start - 1): [0.0, 4.224, 152.3443, 95.6168]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 54: holes 0, rim-vs-core 0.66, rim-vs-outside 0.56, heterogeneity 0.26; core [0.959, 0.648, 0.664, 0.557] rim [0.362, 0.897, 0.55, 0.48]
  - track 26 at frame 12: holes 0, rim-vs-core 0.12, rim-vs-outside 0.11, heterogeneity 0.06; core [0.225, 0.907, 0.286, 0.058] rim [0.129, 0.853, 0.296, 0.092]
  - track 29 at frame 13: holes 0, rim-vs-core 0.17, rim-vs-outside 0.26, heterogeneity 0.15; core [0.374, 0.77, 0.71, 0.791] rim [0.216, 0.807, 0.734, 0.774]
  - track 20 at frame 11: holes 0, rim-vs-core 0.14, rim-vs-outside 0.28, heterogeneity 0.10; core [0.29, 0.902, 0.523, 0.963] rim [0.194, 0.826, 0.516, 0.902]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.526, rim/outside 3.32 (aggregate of 15 individuals; 2/15 membrane-like individually; rim level 0.217)
  - radial |p| polar order: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.44 (aggregate of 15 individuals; 1/15 membrane-like individually; rim level 0.755)
  - radial p_x: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.04 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.521)
  - radial p_y: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1.05 (aggregate of 15 individuals; 1/15 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #67 (t=2700, R_eq 36.99): none; #26 (t=600, R_eq 6.89): none; #29 (t=650, R_eq 9.47): none; #20 (t=550, R_eq 12.02): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 15 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 15 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
