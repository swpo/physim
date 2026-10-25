# Evidence pack: fch-uptake-micelles (seed 13)

- world: `../../20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [192, 192]; wall 374s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/20261025T0834-c10-review-fch-uptake/ctl_res15 --seeds 13 --frames 100 --size 192 192 --no-movie`
- segmentation: matter > 0.14 of robust range [0.104, 2.9882], min area 6 px

## Measurements
- components: final 55, mean 40.5, max 55; occupancy final 0.25
- tracks: 82; persistent (alive >= 50% of run): 37; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [55, 55, 55], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 80, default): splits 18, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 37
- channel total drift (end/start - 1): [0.6685, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 51: holes 0, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.27; core [0.653, 0.112] rim [0.446, 0.14]
  - track 10 at frame 51: holes 0, rim-vs-core 0.56, rim-vs-outside 0.24, heterogeneity 0.30; core [0.747, 0.37] rim [0.311, 0.022]
  - track 11 at frame 51: holes 0, rim-vs-core 0.22, rim-vs-outside 0.39, heterogeneity 0.28; core [0.65, 0.139] rim [0.435, 0.143]
  - track 47 at frame 81: holes 0, rim-vs-core 0.51, rim-vs-outside 0.16, heterogeneity 0.24; core [0.706, 0.175] rim [0.229, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 256 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.544, rim/outside 15.8 (aggregate of 256 individuals; 2/256 membrane-like individually; rim level 0.516)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.042, rim/outside 2.57 (aggregate of 256 individuals; 2/256 membrane-like individually; rim level 0.0195)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=204, R_eq 7.48): none; #10 (t=204, R_eq 7.55): none; #11 (t=204, R_eq 7.51): none; #47 (t=324, R_eq 7.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
