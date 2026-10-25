# Evidence pack: cips-fuel (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 75s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st_dp02_s1 --seeds 1 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0006, 0.9542], min area 6 px

## Measurements
- components: final 57, mean 70.6, max 109; occupancy final 0.13
- tracks: 215; persistent (alive >= 50% of run): 64; longest 286 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [60, 59, 59], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0116/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 58, merge/split ratio n/a, nucleations 157
- channel total drift (end/start - 1): [0.0, -0.5267, 0.4385]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 159: holes 0, rim-vs-core 0.17, rim-vs-outside 0.45, heterogeneity 0.05; core [0.964, 0.943, 0.01] rim [0.831, 0.863, 0.067]
  - track 13 at frame 159: holes 0, rim-vs-core 0.13, rim-vs-outside 0.40, heterogeneity 0.04; core [0.975, 0.953, 0.007] rim [0.87, 0.883, 0.05]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 384 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 24.2 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.888)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 4.17 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.91)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.4, rim/outside 0.475 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.386)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1590, R_eq 1.69): none; #8 (t=1590, R_eq 2.59): none; #9 (t=1590, R_eq 1.69): none; #13 (t=1590, R_eq 2.59): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 384 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
