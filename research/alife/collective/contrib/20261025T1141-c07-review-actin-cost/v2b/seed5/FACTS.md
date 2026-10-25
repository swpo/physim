# Evidence pack: crawler-divide (seed 5)

- world: `../../../20261025T1044-c04-crawler-actin-cost-negative/world.py`, family `phase-field`
- parent: None; mutation: growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction
- run: 241 frames x 50 steps x dt 0.05 = time 600; grid [256, 256]; wall 289s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1044-c04-crawler-actin-cost-negative/world.py --out collective/contrib/_c07rev23/v2b/seed5 --seeds 5 --frames 240 --no-movie`
- segmentation: matter > 0.26 of robust range [-0.0, 0.9716], min area 6 px

## Measurements
- components: final 1, mean 5.3, max 9; occupancy final 0.03
- tracks: 56; persistent (alive >= 50% of run): 2; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 28.26 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.716/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 50, default): splits 22, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.409, nucleations 0
- channel total drift (end/start - 1): [-0.0744, -0.8279, None, -0.2158]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 157: holes 0, rim-vs-core 0.50, rim-vs-outside 0.62, heterogeneity 0.13; core [0.939, 0.272, 0.275, 0.043] rim [0.524, 0.508, 0.153, 0.116]
  - track 28 at frame 161: holes 0, rim-vs-core 0.39, rim-vs-outside 0.61, heterogeneity 0.12; core [0.924, 0.26, 0.24, 0.01] rim [0.598, 0.448, 0.155, 0.052]
  - track 38 at frame 157: holes 0, rim-vs-core 0.45, rim-vs-outside 0.50, heterogeneity 0.11; core [0.841, 0.359, 0.16, 0.08] rim [0.437, 0.523, 0.083, 0.133]
  - track 49 at frame 163: holes 0, rim-vs-core 0.38, rim-vs-outside 0.42, heterogeneity 0.10; core [0.758, 0.385, 0.095, 0.103] rim [0.397, 0.493, 0.05, 0.138]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [40, 81, 121, 159, 200, 240]):
  - radial u (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 11.3 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.732)
  - radial |P| (actin polarization): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.6, rim/outside 10.7 (aggregate of 30 individuals; 29/30 membrane-like individually; rim level 0.505)  MEMBRANE-LIKE
  - radial V/V0 (body content): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 7.25 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.201)
  - radial n (nutrient): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.97, rim/outside 0.846 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.266)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |P| (actin polarization)
- membrane-like channels per top track at mid-life: #25 (t=392.5, R_eq 26.32): ['|P| (actin polarization)']; #28 (t=402.5, R_eq 24.35): ['|P| (actin polarization)']; #38 (t=392.5, R_eq 20.86): ['|P| (actin polarization)']; #49 (t=407.5, R_eq 17.48): ['|P| (actin polarization)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
