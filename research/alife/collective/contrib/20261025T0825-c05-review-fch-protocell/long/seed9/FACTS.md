# Evidence pack: fch-protocell (seed 9)

- world: `../../../../contrib/20261025T0726-c03-fch-protocell/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0745-c03-fch-vesicles/world.py; mutation: add a solute made by the bilayer, excluded from it by chi c u (barrier), decaying everywhere
- run: 201 frames x 400 steps x dt 0.02 = time 1600; grid [128, 128]; wall 479s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0726-c03-fch-protocell/world.py --out collective/work_c05/rev_fch/long/seed9 --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.23 of robust range [0.107, 1.8094], min area 6 px

## Measurements
- components: final 4, mean 4.0, max 7; occupancy final 0.16
- tracks: 11; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.05 (1 = constant size)
- enclosures: components with a hole mean 0.35, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 4, 4], H1 [5, 4, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 160, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 4
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 101: holes 0, rim-vs-core 0.43, rim-vs-outside 0.38, heterogeneity 0.27; core [0.823, 0.16] rim [0.411, 0.029]
  - track 8 at frame 101: holes 0, rim-vs-core 0.32, rim-vs-outside 0.75, heterogeneity 0.21; core [0.737, 0.332] rim [0.654, 0.022]
  - track 9 at frame 101: holes 0, rim-vs-core 0.33, rim-vs-outside 0.67, heterogeneity 0.23; core [0.763, 0.305] rim [0.587, 0.024]
  - track 10 at frame 101: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.26; core [0.809, 0.171] rim [0.556, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u (u + 1.6): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 63.1 (aggregate of 24 individuals; 12/24 membrane-like individually; rim level 0.855)
  - radial solute c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.914 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.588)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=808, R_eq 8.88): ['amphiphile u (u + 1.6)']; #8 (t=808, R_eq 19.06): none; #9 (t=808, R_eq 17.7): none; #10 (t=808, R_eq 8.94): ['amphiphile u (u + 1.6)']

## Warnings
- radial: 2 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
