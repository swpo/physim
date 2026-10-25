# Evidence pack: fch-protocell (seed 2)

- world: `../../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [128, 128]; wall 253s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/contrib/20261025T0726-c03-fch-protocell/pack/seed2 --seeds 2 --frames 100 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1078, 1.8277], min area 6 px

## Measurements
- components: final 5, mean 5.1, max 9; occupancy final 0.16
- tracks: 14; persistent (alive >= 50% of run): 5; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 118.18 (1 = constant size)
- enclosures: components with a hole mean 1.47, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 2, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 5], H1 [6, 6, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 50: holes 0, rim-vs-core 0.12, rim-vs-outside 0.58, heterogeneity 0.15; core [0.742, 0.126] rim [0.639, 0.057]
  - track 9 at frame 51: holes 0, rim-vs-core 0.40, rim-vs-outside 0.30, heterogeneity 0.27; core [0.774, 0.152] rim [0.402, 0.008]
  - track 10 at frame 51: holes 0, rim-vs-core 0.43, rim-vs-outside 0.39, heterogeneity 0.27; core [0.881, 0.031] rim [0.469, 0.152]
  - track 11 at frame 51: holes 1, rim-vs-core 0.45, rim-vs-outside 0.38, heterogeneity 0.27; core [0.887, 0.023] rim [0.46, 0.157]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.71, rim/outside 22.4 (aggregate of 30 individuals; 18/30 membrane-like individually; rim level 0.828)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.307, rim/outside 0.926 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.152)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #8 (t=400, R_eq 17.63): none; #9 (t=408, R_eq 9.93): ['amphiphile u (u + 1.6)']; #10 (t=408, R_eq 10.19, ring): ['amphiphile u (u + 1.6)']; #11 (t=408, R_eq 10.31, ring): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 8 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
