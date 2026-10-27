# Evidence pack: cgle-gain (seed 5)

- world: `../../../20261026T1610-c43-cgle-gain-bigbox/world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 873s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T2152-c47-review-cgle-bigbox/pack_eps1.43/seed5 --seeds 5 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3576], min area 6 px

## Measurements
- components: final 8, mean 9.7, max 15; occupancy final 0.06
- tracks: 51; persistent (alive >= 50% of run): 6; longest 191 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 92.67 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [5, 5, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.829/time; max body lengths 7.6
- replication (lineage window K = 20 frames = time 100, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 16, merge/split ratio 1.23, nucleations 0
- channel total drift (end/start - 1): [-0.9223, -0.938, -0.1282]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 106: holes 0, rim-vs-core 0.50, rim-vs-outside 0.15, heterogeneity 0.21; core [0.747, 0.173, 0.51] rim [0.291, 0.342, 0.62]
  - track 12 at frame 82: holes 0, rim-vs-core 0.51, rim-vs-outside 0.45, heterogeneity 0.26; core [0.966, 0.484, 0.308] rim [0.496, 0.345, 0.439]
  - track 20 at frame 82: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.23; core [0.853, 0.667, 0.306] rim [0.461, 0.489, 0.417]
  - track 31 at frame 128: holes 0, rim-vs-core 0.50, rim-vs-outside 0.29, heterogeneity 0.23; core [0.836, 0.447, 0.218] rim [0.369, 0.426, 0.391]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 21.2 (aggregate of 58 individuals; 4/58 membrane-like individually; rim level 0.625)
  - radial Re A: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.902, rim/outside 1.04 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.435)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.06, rim/outside 0.839 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.577)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=530, R_eq 5.97): none; #12 (t=410, R_eq 11.78, ring): ['|A|']; #20 (t=410, R_eq 7.38): none; #31 (t=640, R_eq 7.09): ['|A|']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
