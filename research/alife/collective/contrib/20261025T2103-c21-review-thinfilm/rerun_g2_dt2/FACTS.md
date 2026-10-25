# Evidence pack: thinfilm-active (seed 7)

- world: `../../20261025T1915-c24-thinfilm-sighting/world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 301s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T2103-c21-review-thinfilm/rerun_g2_dt2 --seeds 7 --frames 80 --spf 400 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0433, 4.5397], min area 6 px

## Measurements
- components: final 2, mean 3.0, max 17; occupancy final 0.27
- tracks: 77; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 2, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.03/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 2000, default): splits 23, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 23, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [-0.0, 4.8779, -665.0123, -106.0453]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 73 at frame 58: holes 0, rim-vs-core 0.60, rim-vs-outside 0.66, heterogeneity 0.24; core [0.961, 0.938, 0.118, 0.237] rim [0.438, 0.913, 0.353, 0.423]
  - track 59 at frame 20: holes 0, rim-vs-core 0.30, rim-vs-outside 0.26, heterogeneity 0.15; core [0.497, 0.917, 0.162, 0.198] rim [0.214, 0.846, 0.204, 0.256]
  - track 62 at frame 21: holes 0, rim-vs-core 0.18, rim-vs-outside 0.33, heterogeneity 0.14; core [0.448, 0.946, 0.186, 0.882] rim [0.317, 0.863, 0.257, 0.842]
  - track 57 at frame 17: holes 0, rim-vs-core 0.13, rim-vs-outside 0.14, heterogeneity 0.07; core [0.275, 0.875, 0.048, 0.45] rim [0.162, 0.819, 0.09, 0.447]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.655, rim/outside 3.01 (aggregate of 17 individuals; 3/17 membrane-like individually; rim level 0.267)
  - radial |p| polar order: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.928, rim/outside 1.43 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.755)
  - radial p_x: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.25, rim/outside 0.857 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.333)
  - radial p_y: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.997 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.465)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #73 (t=5800, R_eq 38.52, ring): ['height above precursor h - ha', '|p| polar order']; #59 (t=2000, R_eq 12.8): none; #62 (t=2100, R_eq 13.37): none; #57 (t=1700, R_eq 6.15): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 17 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 4 of 17 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
