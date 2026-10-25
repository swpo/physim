# Evidence pack: fch-protocell (seed 0)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 254s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/contrib/20261025T0726-c03-fch-protocell/pack/seed0 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1079, 1.8348], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 6; occupancy final 0.16
- tracks: 10; persistent (alive >= 50% of run): 6; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 43.89 (1 = constant size)
- enclosures: components with a hole mean 2.87, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 3, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 6], H1 [6, 6, 5]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 50: holes 1, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.25; core [0.875, 0.014] rim [0.459, 0.127]
  - track 5 at frame 51: holes 1, rim-vs-core 0.42, rim-vs-outside 0.39, heterogeneity 0.25; core [0.876, 0.011] rim [0.472, 0.127]
  - track 6 at frame 51: holes 0, rim-vs-core 0.12, rim-vs-outside 0.56, heterogeneity 0.12; core [0.743, 0.058] rim [0.626, 0.026]
  - track 7 at frame 51: holes 1, rim-vs-core 0.44, rim-vs-outside 0.38, heterogeneity 0.25; core [0.887, 0.008] rim [0.462, 0.12]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.52, rim/outside 81.3 (aggregate of 36 individuals; 30/36 membrane-like individually; rim level 0.935)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.125, rim/outside 0.891 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.0672)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #3 (t=400, R_eq 10.37, ring): ['amphiphile u (u + 1.6)']; #5 (t=408, R_eq 10.28, ring): ['amphiphile u (u + 1.6)']; #6 (t=408, R_eq 16.97): none; #7 (t=408, R_eq 10.52, ring): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 18 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
