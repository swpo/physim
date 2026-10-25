# Evidence pack: fch-protocell-lowD (seed 3)

- world: `../world_lowD.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 233s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0756-c01-review-fch-protocell/world_lowD.py --out collective/contrib/20261025T0756-c01-review-fch-protocell/lowD001 --seeds 3 --frames 100 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1075, 1.8318], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 5; occupancy final 0.16
- tracks: 9; persistent (alive >= 50% of run): 5; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.79 (1 = constant size)
- enclosures: components with a hole mean 1.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 5, 5], H1 [7, 5, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 51: holes 1, rim-vs-core 0.40, rim-vs-outside 0.53, heterogeneity 0.20; core [0.906, 0.704] rim [0.542, 0.543]
  - track 5 at frame 51: holes 0, rim-vs-core 0.44, rim-vs-outside 0.33, heterogeneity 0.20; core [0.775, 0.662] rim [0.39, 0.443]
  - track 6 at frame 51: holes 0, rim-vs-core 0.48, rim-vs-outside 0.33, heterogeneity 0.21; core [0.787, 0.663] rim [0.394, 0.388]
  - track 7 at frame 51: holes 0, rim-vs-core 0.35, rim-vs-outside 0.58, heterogeneity 0.19; core [0.745, 0.656] rim [0.579, 0.351]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 37.9 (aggregate of 30 individuals; 18/30 membrane-like individually; rim level 0.89)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 14.9 (aggregate of 30 individuals; 8/30 membrane-like individually; rim level 0.711)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #4 (t=408, R_eq 10.37, ring): ['amphiphile u (u + 1.6)', 'solute c']; #5 (t=408, R_eq 10): ['amphiphile u (u + 1.6)', 'solute c']; #6 (t=408, R_eq 9.66): ['amphiphile u (u + 1.6)']; #7 (t=408, R_eq 16.53): none

## Warnings
- radial: 7 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
