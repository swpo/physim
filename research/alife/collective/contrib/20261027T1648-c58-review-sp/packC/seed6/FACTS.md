# Evidence pack: fed-wave-matter (seed 6)

- world: `../../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 50 steps x dt 0.2 = time 2000; grid [128, 128]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/20261027T1648-c58-review-sp/packC --seeds 6 7 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0001, 4.229], min area 6 px

## Measurements
- components: final 7, mean 6.0, max 17; occupancy final 0.05
- tracks: 728; persistent (alive >= 50% of run): 0; longest 13 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 200, default): splits 173, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 176, merge/split ratio 1.02, nucleations 215
- channel total drift (end/start - 1): [-0.9177, -0.0529, None, 0.9633]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 332 at frame 87: holes 0, rim-vs-core 0.25, rim-vs-outside 0.38, heterogeneity 0.09; core [0.439, 0.529, 0.544, 0.95] rim [0.224, 0.591, 0.51, 0.842]
  - track 348 at frame 94: holes 0, rim-vs-core 0.17, rim-vs-outside 0.21, heterogeneity 0.08; core [0.212, 0.589, 0.407, 0.822] rim [0.183, 0.623, 0.397, 0.657]
  - track 353 at frame 96: holes 0, rim-vs-core 0.15, rim-vs-outside 0.26, heterogeneity 0.08; core [0.305, 0.54, 0.48, 0.79] rim [0.201, 0.584, 0.466, 0.694]
  - track 221 at frame 57: holes 0, rim-vs-core 0.27, rim-vs-outside 0.27, heterogeneity 0.12; core [0.375, 0.534, 0.409, 0.9] rim [0.237, 0.577, 0.399, 0.671]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.546, rim/outside 3.77 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.254)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.73, rim/outside 0.883 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.509)
  - radial potential -V: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 1.19 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.674)
  - radial phase cos: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.07 (aggregate of 38 individuals; 0/38 membrane-like individually; rim level 0.496)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #332 (t=870, R_eq 7.61): none; #348 (t=940, R_eq 6.53): none; #353 (t=960, R_eq 8.23): none; #221 (t=570, R_eq 7.78): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
