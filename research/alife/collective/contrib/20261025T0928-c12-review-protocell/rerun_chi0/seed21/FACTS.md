# Evidence pack: fch-protocell (seed 21)

- world: `../../world_chi0.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 201 frames x 400 steps x dt 0.02 = time 1600; grid [128, 128]; wall 783s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0928-c12-review-protocell/world_chi0.py --out collective/contrib/20261025T0928-c12-review-protocell/rerun_chi0/seed21 --seeds 21 --no-movie`
- segmentation: matter > 0.23 of robust range [0.1069, 1.8309], min area 6 px

## Measurements
- components: final 5, mean 5.4, max 8; occupancy final 0.16
- tracks: 14; persistent (alive >= 50% of run): 5; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 39.33 (1 = constant size)
- enclosures: components with a hole mean 1.43, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 5], H1 [5, 5, 4]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 101: holes 0, rim-vs-core 0.42, rim-vs-outside 0.27, heterogeneity 0.14; core [0.789, 0.555] rim [0.374, 0.535]
  - track 8 at frame 101: holes 0, rim-vs-core 0.35, rim-vs-outside 0.33, heterogeneity 0.14; core [0.789, 0.562] rim [0.437, 0.543]
  - track 9 at frame 101: holes 0, rim-vs-core 0.08, rim-vs-outside 0.61, heterogeneity 0.11; core [0.714, 0.736] rim [0.66, 0.681]
  - track 11 at frame 101: holes 0, rim-vs-core 0.41, rim-vs-outside 0.28, heterogeneity 0.14; core [0.787, 0.576] rim [0.381, 0.556]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.91, rim/outside 42.8 (aggregate of 32 individuals; 24/32 membrane-like individually; rim level 0.887)  MEMBRANE-LIKE
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 1.16 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.599)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u (u + 1.6)
- membrane-like channels per top track at mid-life: #5 (t=808, R_eq 9.52): ['amphiphile u (u + 1.6)']; #8 (t=808, R_eq 9.46): ['amphiphile u (u + 1.6)']; #9 (t=808, R_eq 19.73): none; #11 (t=808, R_eq 9.49): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 8 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
