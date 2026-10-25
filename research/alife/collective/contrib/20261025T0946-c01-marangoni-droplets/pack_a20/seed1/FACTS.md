# Evidence pack: marangoni-droplets (seed 1)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 266s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T0946-c01-marangoni-droplets/pack_a20 --seeds 0 1 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0397, 1.2834], min area 6 px

## Measurements
- components: final 22, mean 19.2, max 22; occupancy final 0.12
- tracks: 46; persistent (alive >= 50% of run): 20; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.0067/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 19, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1816, -0.6651, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.06; core [0.93, 0.029, 0.021] rim [0.636, 0.075, 0.013]
  - track 15 at frame 109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.06; core [0.928, 0.029, 0.023] rim [0.631, 0.076, 0.014]
  - track 17 at frame 109: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.933, 0.027, 0.025] rim [0.643, 0.075, 0.016]
  - track 42 at frame 148: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.931, 0.03, 0.023] rim [0.644, 0.075, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 52.9 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.906)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.5, rim/outside 0.704 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.127)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.737, rim/outside 2.54 (aggregate of 123 individuals; 1/123 membrane-like individually; rim level 0.0473)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=10900, R_eq 5.23): none; #15 (t=10900, R_eq 5.23): none; #17 (t=10900, R_eq 5.32): none; #42 (t=14800, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
