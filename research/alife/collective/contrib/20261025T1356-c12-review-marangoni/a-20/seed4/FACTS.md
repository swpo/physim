# Evidence pack: marangoni-droplets (seed 4)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 410s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1356-c12-review-marangoni/world.py --out collective/contrib/20261025T1356-c12-review-marangoni/a-20/seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0497, 1.275], min area 6 px

## Measurements
- components: final 6, mean 3.6, max 6; occupancy final 0.10
- tracks: 13; persistent (alive >= 50% of run): 2; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.51 (1 = constant size)
- enclosures: components with a hole mean 0.49, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 6], H1 [4, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio 0.2, nucleations 0
- channel total drift (end/start - 1): [0.1011, -0.4936, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 61: holes 0, rim-vs-core 0.28, rim-vs-outside 0.69, heterogeneity 0.16; core [0.954, 0.018, 0.72] rim [0.823, 0.073, 0.482]
  - track 4 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.66, heterogeneity 0.16; core [0.95, 0.016, 0.743] rim [0.803, 0.083, 0.43]
  - track 7 at frame 158: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.15; core [0.906, 0.029, 0.367] rim [0.722, 0.121, 0.263]
  - track 8 at frame 158: holes 0, rim-vs-core 0.23, rim-vs-outside 0.52, heterogeneity 0.15; core [0.906, 0.029, 0.368] rim [0.722, 0.121, 0.263]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 19.6 (aggregate of 24 individuals; 8/24 membrane-like individually; rim level 0.801)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.82, rim/outside 0.632 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.238)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 3.08 (aggregate of 24 individuals; 2/24 membrane-like individually; rim level 0.277)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=6100, R_eq 12.69, ring): ['phi (droplet material)', '|v| (flow speed)']; #4 (t=6100, R_eq 12.69, ring): ['phi (droplet material)', '|v| (flow speed)']; #7 (t=15800, R_eq 9.03): none; #8 (t=15800, R_eq 9.03): none

## Warnings
- radial: 8 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
