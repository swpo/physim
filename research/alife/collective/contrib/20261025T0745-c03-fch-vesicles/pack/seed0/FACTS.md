# Evidence pack: fch-vesicles (seed 0)

- world: `../../world.py`, family `fch-bilayer`
- parent: None; mutation: new class: functionalized Cahn-Hilliard (Promislow/Gavish) with an asymmetric double well, O(1) functionalization
- run: 101 frames x 200 steps x dt 0.02 = time 400; grid [128, 128]; wall 42s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0745-c03-fch-vesicles/world.py --out collective/contrib/20261025T0745-c03-fch-vesicles/pack --seeds 0 1 --frames 100 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1349, 1.86], min area 6 px

## Measurements
- components: final 4, mean 4.0, max 5; occupancy final 0.14
- tracks: 9; persistent (alive >= 50% of run): 4; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.22 (1 = constant size)
- enclosures: components with a hole mean 3.80, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [4, 4, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 80, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 51: holes 1, rim-vs-core 0.41, rim-vs-outside 0.51, heterogeneity 0.28; core [0.976] rim [0.564]
  - track 6 at frame 51: holes 1, rim-vs-core 0.47, rim-vs-outside 0.38, heterogeneity 0.28; core [0.915] rim [0.446]
  - track 7 at frame 51: holes 1, rim-vs-core 0.38, rim-vs-outside 0.53, heterogeneity 0.28; core [0.973] rim [0.595]
  - track 8 at frame 51: holes 1, rim-vs-core 0.39, rim-vs-outside 0.46, heterogeneity 0.27; core [0.928] rim [0.535]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (shifted, u + 1.6): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 29.4, rim/outside 87.8 (aggregate of 24 individuals; 24/24 membrane-like individually; rim level 0.922)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (shifted, u + 1.6)
- membrane-like channels per top track at mid-life: #5 (t=204, R_eq 14.09, ring): ['amphiphile u (shifted, u + 1.6)']; #6 (t=204, R_eq 13.17, ring): ['amphiphile u (shifted, u + 1.6)']; #7 (t=204, R_eq 14.04, ring): ['amphiphile u (shifted, u + 1.6)']; #8 (t=204, R_eq 13.35, ring): ['amphiphile u (shifted, u + 1.6)']

## Warnings
- radial: 24 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
