# Evidence pack: cips-fuel (seed 2)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS-fuel with a product diffusivity Dp (slow product, fuel-starved cores)
- run: 301 frames x 200 steps x dt 0.05 (--dt; world META dt 0.1) = time 3000; grid [128, 128]; wall 111s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0212-c32-review-cips-slowp/world.py --out collective/contrib/20261026T0212-c32-review-cips-slowp/runs/st_dp02_dthalf --seeds 2 --size 128 128 --frames 300 --spf 200 --dt 0.05 --no-movie`
- segmentation: matter > 0.53 of robust range [0.0006, 0.9518], min area 6 px

## Measurements
- components: final 60, mean 73.8, max 111; occupancy final 0.13
- tracks: 194; persistent (alive >= 50% of run): 65; longest 286 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 63, 61], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.0225/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 51, merge/split ratio n/a, nucleations 143
- channel total drift (end/start - 1): [0.0, -0.5225, 0.4344]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 159: holes 0, rim-vs-core 0.12, rim-vs-outside 0.39, heterogeneity 0.05; core [0.943, 0.909, 0.018] rim [0.844, 0.855, 0.063]
  - track 25 at frame 159: holes 0, rim-vs-core 0.22, rim-vs-outside 0.51, heterogeneity 0.07; core [0.977, 0.968, 0.008] rim [0.802, 0.862, 0.081]
  - track 26 at frame 159: holes 0, rim-vs-core 0.18, rim-vs-outside 0.47, heterogeneity 0.06; core [0.966, 0.949, 0.01] rim [0.82, 0.863, 0.072]
  - track 33 at frame 159: holes 0, rim-vs-core 0.14, rim-vs-outside 0.42, heterogeneity 0.04; core [0.96, 0.936, 0.011] rim [0.852, 0.871, 0.058]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 384 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 20.9 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.873)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 3.96 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.904)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 20.4, rim/outside 0.484 (aggregate of 384 individuals; 0/384 membrane-like individually; rim level 0.389)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=1590, R_eq 1.87): none; #25 (t=1590, R_eq 3.39): none; #26 (t=1590, R_eq 2.71): none; #33 (t=1590, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 1 of 384 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
