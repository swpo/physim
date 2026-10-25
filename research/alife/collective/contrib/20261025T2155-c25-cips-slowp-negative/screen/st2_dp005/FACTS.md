# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 80s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st2_dp005 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.73 of robust range [0.0022, 0.6868], min area 6 px

## Measurements
- components: final 54, mean 46.3, max 66; occupancy final 0.11
- tracks: 124; persistent (alive >= 50% of run): 47; longest 272 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 59, 56], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00389/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 27, merge/split ratio n/a, nucleations 97
- channel total drift (end/start - 1): [0.0, -0.4742, 0.6695]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 166: holes 0, rim-vs-core 0.03, rim-vs-outside 0.16, heterogeneity 0.01; core [1.0, 0.998, 0.0] rim [0.969, 0.987, 0.005]
  - track 1 at frame 169: holes 0, rim-vs-core 0.04, rim-vs-outside 0.17, heterogeneity 0.01; core [0.997, 0.997, 0.0] rim [0.961, 0.984, 0.006]
  - track 2 at frame 171: holes 0, rim-vs-core 0.05, rim-vs-outside 0.21, heterogeneity 0.01; core [0.991, 0.997, 0.0] rim [0.94, 0.98, 0.01]
  - track 5 at frame 174: holes 0, rim-vs-core 0.06, rim-vs-outside 0.19, heterogeneity 0.02; core [0.985, 0.997, 0.001] rim [0.931, 0.981, 0.011]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.945, rim/outside 4.97 (aggregate of 226 individuals; 2/226 membrane-like individually; rim level 0.894)
  - radial p: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 2.53 (aggregate of 226 individuals; 1/226 membrane-like individually; rim level 0.963)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.6, rim/outside 0.384 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1660, R_eq 1.87): none; #1 (t=1690, R_eq 1.95): none; #2 (t=1710, R_eq 2.65): none; #5 (t=1740, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 226 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
