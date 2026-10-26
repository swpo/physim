# Evidence pack: phoretic-colloids (seed 2)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 38s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0315-c32-review-janus/world.py --out collective/contrib/20261026T0315-c32-review-janus/pack --seeds 2 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5719], min area 6 px

## Measurements
- components: final 19, mean 22.8, max 37; occupancy final 0.08
- tracks: 233; persistent (alive >= 50% of run): 12; longest 365 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 23, 16], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.396/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 10, default): splits 9, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 31, merge/split ratio 3.44, nucleations 184
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 218: holes 0, rim-vs-core 0.34, rim-vs-outside 0.32, heterogeneity 0.16; core [0.779, 0.356, 0.546] rim [0.468, 0.441, 0.45]
  - track 20 at frame 218: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.17; core [0.766, 0.54, 0.572] rim [0.472, 0.369, 0.463]
  - track 36 at frame 222: holes 0, rim-vs-core 0.33, rim-vs-outside 0.31, heterogeneity 0.19; core [0.84, 0.347, 0.631] rim [0.536, 0.317, 0.516]
  - track 220 at frame 370: holes 0, rim-vs-core 0.37, rim-vs-outside 0.33, heterogeneity 0.22; core [0.721, 0.57, 0.677] rim [0.382, 0.559, 0.531]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 17.4 (aggregate of 128 individuals; 3/128 membrane-like individually; rim level 0.649)
  - radial B density: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 13.9 (aggregate of 128 individuals; 56/128 membrane-like individually; rim level 0.456)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 2.6 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.575)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=109, R_eq 3.61): ['B density']; #20 (t=109, R_eq 3.7): none; #36 (t=111, R_eq 3.78): ['B density']; #220 (t=185, R_eq 4.3): ['B density']

## Warnings
- radial: 1 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
