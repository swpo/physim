# Evidence pack: reacting-thermals (seed 3)

- world: `../../20261027T0024-c49-thermals-controls/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [192, 192]; wall 113s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0024-c49-thermals-controls/world.py --out collective/contrib/20261027T0616-c51-review-thermals-controls/pack_res15_s3 --seeds 3 --size 192 192 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.36 of robust range [0.0, 0.7039], min area 6 px

## Measurements
- components: final 28, mean 15.5, max 44; occupancy final 0.03
- tracks: 311; persistent (alive >= 50% of run): 0; longest 250 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 27], H1 [0, 0, 0]
- motion: 137 long-lived tracks moved >= 1 body length; max speed 1.64/time; max body lengths 36.6
- replication (lineage window K = 20 frames = time 20, default): splits 121, persistent splits 58 (0 more failed only because the siblings re-merged within K), max generation 11, merges 9, merge/split ratio 0.074, nucleations 15
- channel total drift (end/start - 1): [-0.8755, -0.3349, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 173 at frame 479: holes 0, rim-vs-core 0.34, rim-vs-outside 0.50, heterogeneity 0.15; core [0.886, 0.155, 0.549, 0.984] rim [0.65, 0.192, 0.562, 0.741]
  - track 206 at frame 509: holes 0, rim-vs-core 0.19, rim-vs-outside 0.37, heterogeneity 0.10; core [0.767, 0.123, 0.56, 0.824] rim [0.655, 0.145, 0.487, 0.695]
  - track 210 at frame 509: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.16; core [0.858, 0.144, 0.41, 0.931] rim [0.666, 0.183, 0.496, 0.754]
  - track 290 at frame 585: holes 0, rim-vs-core 0.31, rim-vs-outside 0.48, heterogeneity 0.15; core [0.898, 0.122, 0.336, 0.952] rim [0.669, 0.179, 0.377, 0.76]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.882, rim/outside 5.94 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.631)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.19, rim/outside 0.712 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.271)
  - radial vorticity: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.02 (aggregate of 95 individuals; 13/95 membrane-like individually; rim level 0.444)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 7.8 (aggregate of 95 individuals; 3/95 membrane-like individually; rim level 0.668)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #173 (t=479, R_eq 2.82): none; #206 (t=509, R_eq 2.93): none; #210 (t=509, R_eq 3.74): none; #290 (t=585, R_eq 3.43): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
