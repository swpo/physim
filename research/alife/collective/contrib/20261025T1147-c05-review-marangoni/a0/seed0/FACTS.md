# Evidence pack: marangoni-droplets (seed 0)

- world: `../../../../contrib/20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/work_c05/rev_mg/a0/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0519, 1.305], min area 6 px

## Measurements
- components: final 2, mean 2.0, max 2; occupancy final 0.09
- tracks: 2; persistent (alive >= 50% of run): 2; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 6.68 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 2, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0768, -0.457, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.72, heterogeneity 0.17; core [0.958, 0.005, 0.849] rim [0.81, 0.061, 0.382]
  - track 1 at frame 101: holes 0, rim-vs-core 0.51, rim-vs-outside 0.72, heterogeneity 0.17; core [0.963, 0.005, 0.872] rim [0.814, 0.059, 0.392]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.45, rim/outside 2.82 (aggregate of 12 individuals; 12/12 membrane-like individually; rim level 0.326)  MEMBRANE-LIKE
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.58, rim/outside 0.651 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.252)
  - radial |v| (flow speed): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 1.16 (aggregate of 12 individuals; 2/12 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): phi (droplet material)
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 14.87, ring): ['phi (droplet material)']; #1 (t=10100, R_eq 14.91, ring): ['phi (droplet material)']

## Warnings
- radial: 12 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
