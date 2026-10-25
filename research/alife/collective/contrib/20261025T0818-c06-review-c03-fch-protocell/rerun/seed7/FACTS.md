# Evidence pack: fch-protocell (seed 7)

- world: `../../../20261025T0726-c03-fch-protocell/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 320s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/contrib/20261025T0818-c06-review-c03-fch-protocell/rerun/seed7 --seeds 7 --frames 100 --no-movie`
- segmentation: matter > 0.20 of robust range [0.1093, 2.0213], min area 6 px

## Measurements
- components: final 6, mean 6.5, max 8; occupancy final 0.16
- tracks: 14; persistent (alive >= 50% of run): 6; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 71.00 (1 = constant size)
- enclosures: components with a hole mean 4.41, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 7, 6], H1 [6, 4, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 7
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 50: holes 1, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.17; core [0.917, 0.001] rim [0.469, 0.031]
  - track 6 at frame 51: holes 1, rim-vs-core 0.36, rim-vs-outside 0.48, heterogeneity 0.17; core [0.913, 0.001] rim [0.556, 0.03]
  - track 7 at frame 51: holes 1, rim-vs-core 0.44, rim-vs-outside 0.40, heterogeneity 0.17; core [0.909, 0.001] rim [0.47, 0.037]
  - track 8 at frame 51: holes 1, rim-vs-core 0.40, rim-vs-outside 0.46, heterogeneity 0.17; core [0.922, 0.001] rim [0.525, 0.026]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 38 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.27, rim/outside 29 (aggregate of 38 individuals; 25/38 membrane-like individually; rim level 0.812)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.102, rim/outside 0.87 (aggregate of 38 individuals; 1/38 membrane-like individually; rim level 0.0405)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #1 (t=400, R_eq 11.62, ring): ['amphiphile u (u + 1.6)']; #6 (t=408, R_eq 11.28, ring): ['amphiphile u (u + 1.6)']; #7 (t=408, R_eq 11.47, ring): ['amphiphile u (u + 1.6)']; #8 (t=408, R_eq 11.86, ring): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 25 of 38 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
