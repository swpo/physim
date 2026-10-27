# Evidence pack: fed-wave-matter (seed 45)

- world: `../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/c57-w17/packC --seeds 45 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0002, 4.216], min area 6 px

## Measurements
- components: final 6, mean 6.7, max 27; occupancy final 0.07
- tracks: 791; persistent (alive >= 50% of run): 0; longest 12 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.16, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 2, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 200, default): splits 177, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 190, merge/split ratio 1.07, nucleations 256
- channel total drift (end/start - 1): [-0.9026, -0.07, None, 1.0271]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 284 at frame 64: holes 0, rim-vs-core 0.04, rim-vs-outside 0.20, heterogeneity 0.06; core [0.202, 0.579, 0.287, 0.204] rim [0.17, 0.594, 0.284, 0.205]
  - track 325 at frame 77: holes 0, rim-vs-core 0.54, rim-vs-outside 0.20, heterogeneity 0.19; core [0.696, 0.347, 0.606, 0.267] rim [0.243, 0.496, 0.543, 0.506]
  - track 79 at frame 12: holes 0, rim-vs-core 0.54, rim-vs-outside 0.12, heterogeneity 0.21; core [0.684, 0.198, 0.599, 0.537] rim [0.164, 0.331, 0.55, 0.521]
  - track 452 at frame 116: holes 0, rim-vs-core 0.43, rim-vs-outside 0.13, heterogeneity 0.16; core [0.559, 0.492, 0.605, 0.721] rim [0.173, 0.597, 0.565, 0.561]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.53, rim/outside 4.06 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.254)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.71, rim/outside 0.873 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.51)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 1.2 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.635)
  - radial phase cos: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.1 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #284 (t=640, R_eq 4.33): none; #325 (t=770, R_eq 7.38): none; #79 (t=120, R_eq 5.01): none; #452 (t=1160, R_eq 5.41): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
