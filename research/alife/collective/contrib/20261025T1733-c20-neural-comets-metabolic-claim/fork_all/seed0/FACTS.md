# Evidence pack: neural-field-dep-fork (seed 0)

- world: `../../world_fork.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run /tmp/c20nfe/world_fork.py --out /tmp/c20nfe/cut_all --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 21.8, max 69; occupancy final 0.00
- tracks: 477; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 21, 2], H1 [33, 11, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.587/time; max body lengths 28.9
- replication (lineage window K = 20 frames = time 100, default): splits 181, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 47, merge/split ratio 0.26, nucleations 8
- channel total drift (end/start - 1): [-1.0, None, -0.9985, -0.3524]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 253 at frame 59: holes 0, rim-vs-core 0.28, rim-vs-outside 0.88, heterogeneity 0.17; core [0.937, 0.504, 1.0, 0.5] rim [0.68, 0.451, 0.894, 0.528]
  - track 149 at frame 40: holes 0, rim-vs-core 0.31, rim-vs-outside 0.83, heterogeneity 0.16; core [0.903, 0.684, 1.0, 0.454] rim [0.671, 0.518, 0.881, 0.488]
  - track 263 at frame 50: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.17; core [0.926, 0.567, 1.0, 0.46] rim [0.691, 0.512, 0.887, 0.518]
  - track 431 at frame 106: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.937, 0.533, 1.0, 0.442] rim [0.716, 0.433, 0.946, 0.528]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [34, 67, 101]):
  - radial activity u: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.09 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.716)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 2.02 (aggregate of 103 individuals; 4/103 membrane-like individually; rim level 0.548)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 25.2 (aggregate of 103 individuals; 2/103 membrane-like individually; rim level 0.802)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.26, rim/outside 0.927 (aggregate of 103 individuals; 1/103 membrane-like individually; rim level 0.539)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #253 (t=295, R_eq 4.07): none; #149 (t=200, R_eq 3.39): none; #263 (t=250, R_eq 3.14): none; #431 (t=530, R_eq 3.61): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 103 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
