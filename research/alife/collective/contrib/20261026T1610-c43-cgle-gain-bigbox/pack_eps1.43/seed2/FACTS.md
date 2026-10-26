# Evidence pack: cgle-gain (seed 2)

- world: `../../world.py`, family `cgle`
- parent: collective/contrib/20261025T0841-c03-cgle-solitons; mutation: the CGLE linear gain becomes a local gain medium g, depleted by |A|^2 and regrowing toward g0
- run: 201 frames x 500 steps x dt 0.01 = time 1000; grid [192, 192]; wall 1230s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1610-c43-cgle-gain-bigbox/world.py --out collective/contrib/20261026T1610-c43-cgle-gain-bigbox/pack_eps1.43/seed2 --seeds 2 --size 192 192 --frames 200 --no-movie`
- segmentation: matter > 0.21 of robust range [0.0, 2.3534], min area 6 px

## Measurements
- components: final 6, mean 5.2, max 8; occupancy final 0.04
- tracks: 51; persistent (alive >= 50% of run): 1; longest 160 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 42.44 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 6], H1 [1, 1, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.363/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 100, default): splits 16, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.938, nucleations 1
- channel total drift (end/start - 1): [-0.9445, -1.1178, -0.0876]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 89: holes 0, rim-vs-core 0.53, rim-vs-outside 0.28, heterogeneity 0.26; core [0.871, 0.611, 0.465] rim [0.379, 0.438, 0.583]
  - track 34 at frame 166: holes 0, rim-vs-core 0.53, rim-vs-outside 0.14, heterogeneity 0.21; core [0.727, 0.723, 0.37] rim [0.28, 0.462, 0.46]
  - track 19 at frame 99: holes 0, rim-vs-core 0.55, rim-vs-outside 0.26, heterogeneity 0.23; core [0.853, 0.165, 0.45] rim [0.349, 0.338, 0.57]
  - track 41 at frame 180: holes 0, rim-vs-core 0.44, rim-vs-outside 0.16, heterogeneity 0.14; core [0.715, 0.603, 0.415] rim [0.29, 0.555, 0.507]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial |A|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 14.6 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.527)
  - radial Re A: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 1.02 (aggregate of 31 individuals; 1/31 membrane-like individually; rim level 0.425)
  - radial g: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.96, rim/outside 0.849 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.61)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=445, R_eq 7.2): none; #34 (t=830, R_eq 5.75): none; #19 (t=495, R_eq 6.6): none; #41 (t=900, R_eq 4.58): ['Re A']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
