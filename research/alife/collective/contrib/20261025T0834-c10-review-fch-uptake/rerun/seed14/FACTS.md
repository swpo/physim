# Evidence pack: fch-uptake-micelles (seed 14)

- world: `../../../20261025T0810-c01-fch-uptake-cargo/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0752-c03-fch-cargo-fission/world.py; mutation: solute supplied uniformly (kp0 everywhere) instead of made by the amphiphile; partitioning chi=-3 concentrates it in the micelles
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [128, 128]; wall 315s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0810-c01-fch-uptake-cargo/world.py --out collective/contrib/20261025T0834-c10-review-fch-uptake/rerun/seed14 --seeds 14 --no-movie`
- segmentation: matter > 0.13 of robust range [0.1158, 2.9939], min area 6 px

## Measurements
- components: final 79, mean 53.0, max 79; occupancy final 0.41
- tracks: 140; persistent (alive >= 50% of run): 41; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 7.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [80, 80, 80], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.0234/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 80, default): splits 57, persistent splits 50 (0 more failed only because the siblings re-merged within K), max generation 6, merges 1, merge/split ratio 0.018, nucleations 20
- channel total drift (end/start - 1): [1.3183, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.10, heterogeneity 0.28; core [0.614, 0.196] rim [0.163, 0.001]
  - track 5 at frame 101: holes 0, rim-vs-core 0.52, rim-vs-outside 0.10, heterogeneity 0.30; core [0.617, 0.242] rim [0.161, 0.001]
  - track 7 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.13, heterogeneity 0.27; core [0.64, 0.212] rim [0.191, 0.001]
  - track 132 at frame 190: holes 0, rim-vs-core 0.45, rim-vs-outside 0.10, heterogeneity 0.20; core [0.616, 0.079] rim [0.17, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 336 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.515, rim/outside 5.97 (aggregate of 336 individuals; 1/336 membrane-like individually; rim level 0.485)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.037, rim/outside 1.81 (aggregate of 336 individuals; 1/336 membrane-like individually; rim level 0.0137)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=404, R_eq 5.14): none; #5 (t=404, R_eq 5.2): none; #7 (t=404, R_eq 5.2): none; #132 (t=760, R_eq 5.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 336 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
