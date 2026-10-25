# Evidence pack: apfc (seed 5)

- world: `../world.py`, family `active-pfc`
- parent: new class (Menzel & Loewen 2013 active phase-field crystal); mutation: none (benchmark model)
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 48s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c13-review-apfc-births/world.py --out collective/contrib/20261025T1225-c13-review-apfc-births/rerun_fed --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.6074], min area 6 px

## Measurements
- components: final 6, mean 5.9, max 10; occupancy final 0.49
- tracks: 210; persistent (alive >= 50% of run): 0; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.29, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 10, 5], H1 [4, 1, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.3/time; max body lengths 9.6
- replication (lineage window K = 20 frames = time 100, default): splits 70, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 70, merge/split ratio 1, nucleations 9
- channel total drift (end/start - 1): [-0.0753, 0.0576, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 35: holes 0, rim-vs-core 0.55, rim-vs-outside 0.17, heterogeneity 0.25; core [0.716, 0.432, 0.655] rim [0.446, 0.088, 0.317]
  - track 8 at frame 24: holes 0, rim-vs-core 0.57, rim-vs-outside 0.29, heterogeneity 0.26; core [0.815, 0.432, 0.662] rim [0.484, 0.112, 0.32]
  - track 5 at frame 22: holes 0, rim-vs-core 0.54, rim-vs-outside 0.28, heterogeneity 0.26; core [0.796, 0.416, 0.637] rim [0.48, 0.112, 0.32]
  - track 13 at frame 39: holes 0, rim-vs-core 0.55, rim-vs-outside 0.16, heterogeneity 0.25; core [0.7, 0.416, 0.642] rim [0.426, 0.086, 0.297]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial crystal amplitude (smoothed (phi - mean)^2): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 4.13 (aggregate of 36 individuals; 2/36 membrane-like individually; rim level 0.584)
  - radial density phi: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.529, rim/outside 1.25 (aggregate of 36 individuals; 5/36 membrane-like individually; rim level 0.253)
  - radial |P|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 4.58 (aggregate of 36 individuals; 3/36 membrane-like individually; rim level 0.475)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=175, R_eq 5.35): none; #8 (t=120, R_eq 7.96): ['density phi']; #5 (t=110, R_eq 8.14): ['density phi']; #13 (t=195, R_eq 5.47): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: 3 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 2 of 36 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
