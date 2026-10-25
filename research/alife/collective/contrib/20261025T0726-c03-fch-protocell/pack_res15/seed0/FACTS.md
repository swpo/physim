# Evidence pack: fch-protocell (seed 0)

- world: `../../world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 101 frames x 400 steps x dt 0.02 = time 800; grid [192, 192]; wall 568s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world_res15.py --out collective/contrib/20261025T0726-c03-fch-protocell/pack_res15/seed0 --seeds 0 --frames 100 --size 192 192 --no-movie`
- segmentation: matter > 0.19 of robust range [0.1094, 2.1245], min area 6 px

## Measurements
- components: final 10, mean 11.0, max 12; occupancy final 0.16
- tracks: 19; persistent (alive >= 50% of run): 11; longest 101 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 49.50 (1 = constant size)
- enclosures: components with a hole mean 1.77, final 7; holes at thresholds 0.2/0.35/0.5 final [7, 7, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 10], H1 [7, 7, 7]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio n/a, nucleations 10
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 50: holes 0, rim-vs-core 0.47, rim-vs-outside 0.19, heterogeneity 0.14; core [0.796, 0.001] rim [0.329, 0.006]
  - track 6 at frame 50: holes 0, rim-vs-core 0.47, rim-vs-outside 0.21, heterogeneity 0.14; core [0.818, 0.001] rim [0.347, 0.005]
  - track 7 at frame 51: holes 0, rim-vs-core 0.24, rim-vs-outside 0.49, heterogeneity 0.25; core [0.756, 0.185] rim [0.582, 0.016]
  - track 8 at frame 51: holes 0, rim-vs-core 0.26, rim-vs-outside 0.48, heterogeneity 0.25; core [0.751, 0.181] rim [0.567, 0.004]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 65 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial amphiphile u (u + 1.6): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 46.8 (aggregate of 65 individuals; 41/65 membrane-like individually; rim level 0.822)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.193, rim/outside 0.736 (aggregate of 65 individuals; 0/65 membrane-like individually; rim level 0.0727)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=400, R_eq 9.39): none; #6 (t=400, R_eq 9.32): none; #7 (t=408, R_eq 14.35): ['amphiphile u (u + 1.6)']; #8 (t=408, R_eq 14.41): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 15 of 65 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
