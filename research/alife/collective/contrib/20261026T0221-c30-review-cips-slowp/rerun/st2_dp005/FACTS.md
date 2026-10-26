# Evidence pack: cips-fuel (seed 5)

- world: `../../../20261026T0146-c25-cips-slowp-negative-fix/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 71s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0146-c25-cips-slowp-negative-fix/world.py --out collective/contrib/20261026T0221-c30-review-cips-slowp/rerun/st2_dp005 --seeds 5 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.73 of robust range [0.0022, 0.6855], min area 6 px

## Measurements
- components: final 64, mean 48.6, max 69; occupancy final 0.11
- tracks: 154; persistent (alive >= 50% of run): 43; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 58, 55], H1 [1, 1, 1]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.0066/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 200, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 30, merge/split ratio 10, nucleations 118
- channel total drift (end/start - 1): [0.0, -0.4708, 0.6643]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 166: holes 0, rim-vs-core 0.04, rim-vs-outside 0.19, heterogeneity 0.01; core [0.986, 0.996, 0.0] rim [0.948, 0.983, 0.008]
  - track 3 at frame 174: holes 0, rim-vs-core 0.05, rim-vs-outside 0.22, heterogeneity 0.01; core [0.999, 0.997, 0.0] rim [0.95, 0.981, 0.008]
  - track 7 at frame 176: holes 0, rim-vs-core 0.04, rim-vs-outside 0.20, heterogeneity 0.01; core [0.999, 0.999, 0.0] rim [0.96, 0.985, 0.006]
  - track 142 at frame 270: holes 0, rim-vs-core 0.03, rim-vs-outside 0.16, heterogeneity 0.01; core [0.95, 0.991, 0.005] rim [0.919, 0.981, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 243 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 4.68 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.879)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 2.41 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.96)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.7, rim/outside 0.409 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.242)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1660, R_eq 2.39): none; #3 (t=1740, R_eq 1.95): none; #7 (t=1760, R_eq 2.46): none; #142 (t=2700, R_eq 3.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 243 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
