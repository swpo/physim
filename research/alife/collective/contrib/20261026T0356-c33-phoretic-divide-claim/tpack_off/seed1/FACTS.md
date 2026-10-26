# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 115s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/tpack_off --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8689], min area 6 px

## Measurements
- components: final 10, mean 13.8, max 28; occupancy final 0.06
- tracks: 175; persistent (alive >= 50% of run): 6; longest 763 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 11], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.324/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 10, default): splits 6, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 30, merge/split ratio 5, nucleations 133
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 424: holes 0, rim-vs-core 0.19, rim-vs-outside 0.43, heterogeneity 0.16; core [0.874, 0.267, 0.688] rim [0.733, 0.176, 0.594]
  - track 10 at frame 424: holes 0, rim-vs-core 0.25, rim-vs-outside 0.26, heterogeneity 0.16; core [0.745, 0.535, 0.487] rim [0.539, 0.422, 0.41]
  - track 139 at frame 518: holes 0, rim-vs-core 0.36, rim-vs-outside 0.31, heterogeneity 0.19; core [0.811, 0.543, 0.745] rim [0.512, 0.458, 0.557]
  - track 170 at frame 773: holes 0, rim-vs-core 0.36, rim-vs-outside 0.53, heterogeneity 0.25; core [0.784, 0.617, 0.91] rim [0.553, 0.455, 0.682]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 21.2 (aggregate of 78 individuals; 1/78 membrane-like individually; rim level 0.693)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 16 (aggregate of 78 individuals; 27/78 membrane-like individually; rim level 0.413)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 3.12 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.549)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=212, R_eq 4.92): none; #10 (t=212, R_eq 3.52): none; #139 (t=259, R_eq 5.56): none; #170 (t=386.5, R_eq 6.75): none

## Warnings
- radial: 1 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
