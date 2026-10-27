# Evidence pack: cgle-gain (seed 5)

- world: `../../../20261026T1610-c43-cgle-gain-bigbox/world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 884s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T2152-c47-review-cgle-bigbox/pack_eps1.40/seed5 --seeds 5 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3523], min area 6 px

## Measurements
- components: final 9, mean 14.1, max 19; occupancy final 0.03
- tracks: 47; persistent (alive >= 50% of run): 14; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 33.67 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.0713/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 100, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 14, merge/split ratio 1.4, nucleations 0
- channel total drift (end/start - 1): [-0.9633, -0.8982, -0.079]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 103: holes 0, rim-vs-core 0.46, rim-vs-outside 0.14, heterogeneity 0.18; core [0.701, 0.2, 0.478] rim [0.262, 0.265, 0.583]
  - track 8 at frame 103: holes 0, rim-vs-core 0.17, rim-vs-outside 0.41, heterogeneity 0.19; core [0.68, 0.128, 0.546] rim [0.52, 0.191, 0.56]
  - track 14 at frame 104: holes 0, rim-vs-core 0.52, rim-vs-outside 0.32, heterogeneity 0.20; core [0.872, 0.682, 0.397] rim [0.376, 0.604, 0.531]
  - track 27 at frame 104: holes 0, rim-vs-core 0.47, rim-vs-outside 0.15, heterogeneity 0.18; core [0.714, 0.133, 0.459] rim [0.267, 0.24, 0.579]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 82 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.597, rim/outside 19.9 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.559)
  - radial Re A: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 1.07 (aggregate of 82 individuals; 3/82 membrane-like individually; rim level 0.431)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.76, rim/outside 0.871 (aggregate of 82 individuals; 0/82 membrane-like individually; rim level 0.627)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=515, R_eq 5.41): none; #8 (t=515, R_eq 5.5): none; #14 (t=520, R_eq 6.48): ['Re A']; #27 (t=520, R_eq 5.81): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
