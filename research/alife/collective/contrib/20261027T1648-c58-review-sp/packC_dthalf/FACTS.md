# Evidence pack: fed-wave-matter (seed 6)

- world: `../../20261027T0949-c55-schrodinger-poisson-negative/world.py`, family `schrodinger-poisson`
- parent: None; mutation: -
- run: 201 frames x 100 steps x dt 0.2 = time 4000; grid [128, 128]; wall 51s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0949-c55-schrodinger-poisson-negative/world.py --out collective/contrib/20261027T1648-c58-review-sp/packC_dthalf --seeds 6 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0002, 4.1953], min area 6 px

## Measurements
- components: final 5, mean 6.2, max 18; occupancy final 0.04
- tracks: 765; persistent (alive >= 50% of run): 0; longest 11 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 5, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 400, default): splits 187, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 190, merge/split ratio 1.02, nucleations 224
- channel total drift (end/start - 1): [-0.9276, -0.0565, None, 1.0588]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 212 at frame 55: holes 0, rim-vs-core 0.50, rim-vs-outside 0.19, heterogeneity 0.19; core [0.668, 0.38, 0.672, 0.318] rim [0.237, 0.516, 0.596, 0.516]
  - track 438 at frame 118: holes 0, rim-vs-core 0.16, rim-vs-outside 0.04, heterogeneity 0.11; core [0.189, 0.65, 0.29, 0.585] rim [0.159, 0.667, 0.281, 0.429]
  - track 738 at frame 197: holes 0, rim-vs-core 0.25, rim-vs-outside 0.27, heterogeneity 0.08; core [0.463, 0.465, 0.447, 0.652] rim [0.229, 0.552, 0.414, 0.688]
  - track 191 at frame 49: holes 0, rim-vs-core 0.21, rim-vs-outside 0.15, heterogeneity 0.14; core [0.389, 0.447, 0.51, 0.548] rim [0.217, 0.51, 0.487, 0.453]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 27 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial density |psi|^2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.525, rim/outside 5.22 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.278)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.73, rim/outside 0.846 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.477)
  - radial potential -V: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 1.21 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.721)
  - radial phase cos: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.45, rim/outside 0.989 (aggregate of 27 individuals; 0/27 membrane-like individually; rim level 0.467)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #212 (t=1100, R_eq 7.8): none; #438 (t=2360, R_eq 5.78): none; #738 (t=3940, R_eq 7.9): none; #191 (t=980, R_eq 8.97): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
