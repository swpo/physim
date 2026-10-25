# Evidence pack: fch-protocell (seed 9)

- world: `../../../../contrib/20261025T0726-c03-fch-protocell/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 244s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/work_c05/rev_fch/rerun/seed9 --seeds 9 --frames 100 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1072, 1.8289], min area 6 px

## Measurements
- components: final 4, mean 4.0, max 7; occupancy final 0.16
- tracks: 11; persistent (alive >= 50% of run): 4; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.78 (1 = constant size)
- enclosures: components with a hole mean 0.70, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 4, 4], H1 [5, 4, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 51: holes 0, rim-vs-core 0.46, rim-vs-outside 0.33, heterogeneity 0.29; core [0.8, 0.208] rim [0.38, 0.026]
  - track 8 at frame 51: holes 0, rim-vs-core 0.39, rim-vs-outside 0.68, heterogeneity 0.24; core [0.726, 0.401] rim [0.644, 0.02]
  - track 9 at frame 51: holes 0, rim-vs-core 0.37, rim-vs-outside 0.60, heterogeneity 0.25; core [0.754, 0.351] rim [0.582, 0.02]
  - track 10 at frame 51: holes 0, rim-vs-core 0.28, rim-vs-outside 0.45, heterogeneity 0.29; core [0.79, 0.22] rim [0.545, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 63 (aggregate of 24 individuals; 12/24 membrane-like individually; rim level 0.87)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.712, rim/outside 0.962 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.446)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #7 (t=408, R_eq 9.51): ['amphiphile u (u + 1.6)']; #8 (t=408, R_eq 18.61): none; #9 (t=408, R_eq 17.5): none; #10 (t=408, R_eq 9.66): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 4 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
