# Evidence pack: cips-fuel (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/../world.py --out /home/user/physim/research/alife/collective/contrib/20261025T2146-c25-cips-slowp/screen/st_dp1 --seeds 0 --size 128 128 --frames 300 --no-movie`
- segmentation: matter > 0.53 of robust range [0.0009, 0.9462], min area 6 px

## Measurements
- components: final 20, mean 21.5, max 39; occupancy final 0.14
- tracks: 68; persistent (alive >= 50% of run): 19; longest 238 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 20, 19], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 23, merge/split ratio n/a, nucleations 45
- channel total drift (end/start - 1): [0.0, -0.5195, 0.4322]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 182: holes 0, rim-vs-core 0.23, rim-vs-outside 0.29, heterogeneity 0.07; core [0.929, 0.881, 0.011] rim [0.731, 0.776, 0.071]
  - track 2 at frame 184: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.07; core [0.925, 0.885, 0.012] rim [0.73, 0.782, 0.07]
  - track 4 at frame 184: holes 0, rim-vs-core 0.27, rim-vs-outside 0.31, heterogeneity 0.08; core [0.945, 0.922, 0.009] rim [0.716, 0.791, 0.078]
  - track 5 at frame 184: holes 0, rim-vs-core 0.24, rim-vs-outside 0.29, heterogeneity 0.07; core [0.918, 0.876, 0.013] rim [0.716, 0.772, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 135 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 10.6 (aggregate of 135 individuals; 1/135 membrane-like individually; rim level 0.78)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 2.72 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.848)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.3, rim/outside 0.503 (aggregate of 135 individuals; 0/135 membrane-like individually; rim level 0.389)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1820, R_eq 4.37): none; #2 (t=1840, R_eq 4.37): none; #4 (t=1840, R_eq 5.23): none; #5 (t=1840, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 135 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
