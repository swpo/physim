# Evidence pack: fch-protocell (seed 1)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 256s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/contrib/20261025T0726-c03-fch-protocell/pack/seed1 --seeds 1 --frames 100 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1076, 1.8519], min area 6 px

## Measurements
- components: final 4, mean 4.3, max 5; occupancy final 0.16
- tracks: 7; persistent (alive >= 50% of run): 4; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.61 (1 = constant size)
- enclosures: components with a hole mean 3.34, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 4], H1 [4, 4, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 51: holes 1, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.19; core [0.921, 0.001] rim [0.476, 0.05]
  - track 4 at frame 51: holes 1, rim-vs-core 0.39, rim-vs-outside 0.50, heterogeneity 0.16; core [0.933, 0.001] rim [0.547, 0.018]
  - track 5 at frame 51: holes 1, rim-vs-core 0.44, rim-vs-outside 0.44, heterogeneity 0.15; core [0.934, 0.001] rim [0.492, 0.017]
  - track 6 at frame 66: holes 0, rim-vs-core 0.10, rim-vs-outside 0.57, heterogeneity 0.12; core [0.699, 0.068] rim [0.624, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.2, rim/outside 28.6 (aggregate of 25 individuals; 20/25 membrane-like individually; rim level 0.828)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.11, rim/outside 0.886 (aggregate of 25 individuals; 2/25 membrane-like individually; rim level 0.0576)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #1 (t=408, R_eq 11.52, ring): ['amphiphile u (u + 1.6)']; #4 (t=408, R_eq 12.63, ring): ['amphiphile u (u + 1.6)']; #5 (t=408, R_eq 13.03, ring): ['amphiphile u (u + 1.6)']; #6 (t=528, R_eq 19.98): none

## Warnings
- radial: 18 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
