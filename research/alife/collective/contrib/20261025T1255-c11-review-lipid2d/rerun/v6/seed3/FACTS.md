# Evidence pack: lipid-2d (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1025-c12-lipid-2d-sighting/world.py`, family `lipid-particle`
- parent: None; mutation: -
- run: 8001 frames x 1 steps x dt 0.3 = time 2400; grid [128, 128]; wall 698s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1025-c12-lipid-2d-sighting/world.py --out /tmp/claude-0/c11rev22/v6 --seeds 3 --frames 8000 --no-movie`
- segmentation: matter > 0.61 of robust range [0.0, 0.8194], min area 6 px

## Measurements
- components: final 56, mean 53.1, max 65; occupancy final 0.04
- tracks: 73389; persistent (alive >= 50% of run): 0; longest 2940 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 46, 29], H1 [0, 0, 0]
- motion: 119 long-lived tracks moved >= 1 body length; max speed 1.28/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 6, default): splits 18112, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 18184, merge/split ratio 1, nucleations 21159
- channel total drift (end/start - 1): [0.0, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35239 at frame 5849: holes 0, rim-vs-core 0.10, rim-vs-outside 0.28, heterogeneity 0.14; core [0.481, 0.949] rim [0.534, 0.864]
  - track 33152 at frame 5580: holes 0, rim-vs-core 0.24, rim-vs-outside 0.34, heterogeneity 0.10; core [0.24, 0.926] rim [0.466, 0.851]
  - track 14214 at frame 3496: holes 0, rim-vs-core 0.30, rim-vs-outside 0.37, heterogeneity 0.15; core [0.221, 1.0] rim [0.499, 0.883]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [1345, 2689, 4034, 5311, 6655, 8000]):
  - radial lipid heads: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 1.38 (aggregate of 158 individuals; 92/158 membrane-like individually; rim level 0.619)
  - radial lipid tails: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 2.9 (aggregate of 158 individuals; 1/158 membrane-like individually; rim level 0.785)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35239 (t=1754.7, R_eq 2.39): none; #33152 (t=1674, R_eq 2.19): ['lipid heads']; #14214 (t=1048.8, R_eq 2.19): ['lipid heads']; #41318 (t=1492.5, R_eq 1.95): ['lipid heads']

## Warnings
- radial: 4 of 158 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
