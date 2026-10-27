# Evidence pack: cgle-gain (seed 2)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 1231s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T1610-c43-cgle-gain-bigbox/pack_eps1.42/seed2 --seeds 2 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3591], min area 6 px

## Measurements
- components: final 6, mean 8.5, max 12; occupancy final 0.03
- tracks: 49; persistent (alive >= 50% of run): 6; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 77.19 (1 = constant size)
- enclosures: components with a hole mean 0.80, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [2, 2, 1]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.118/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 100, default): splits 12, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 1.33, nucleations 0
- channel total drift (end/start - 1): [-0.9624, -1.3681, -0.0694]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 103: holes 1, rim-vs-core 0.51, rim-vs-outside 0.30, heterogeneity 0.24; core [0.86, 0.446, 0.155] rim [0.368, 0.413, 0.279]
  - track 13 at frame 104: holes 0, rim-vs-core 0.49, rim-vs-outside 0.16, heterogeneity 0.17; core [0.72, 0.065, 0.478] rim [0.281, 0.269, 0.577]
  - track 20 at frame 97: holes 0, rim-vs-core 0.44, rim-vs-outside 0.17, heterogeneity 0.17; core [0.732, 0.228, 0.416] rim [0.305, 0.255, 0.514]
  - track 34 at frame 139: holes 0, rim-vs-core 0.50, rim-vs-outside 0.30, heterogeneity 0.24; core [0.841, 0.443, 0.229] rim [0.378, 0.412, 0.408]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 50 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.757, rim/outside 23.2 (aggregate of 50 individuals; 6/50 membrane-like individually; rim level 0.617)
  - radial Re A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 1.25 (aggregate of 50 individuals; 2/50 membrane-like individually; rim level 0.513)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.92, rim/outside 0.845 (aggregate of 50 individuals; 0/50 membrane-like individually; rim level 0.594)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=515, R_eq 9.46, ring): ['|A|']; #13 (t=520, R_eq 5.5): none; #20 (t=485, R_eq 5.17): none; #34 (t=695, R_eq 7.09): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 50 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
