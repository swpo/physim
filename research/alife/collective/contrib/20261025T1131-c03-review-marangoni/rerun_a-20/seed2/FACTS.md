# Evidence pack: marangoni-droplets (seed 2)

- world: `../../../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 278s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out /tmp/claude-0/-home-user-physim/ca3fe853-e88d-58ad-9551-2586c1b06c34/scratchpad/rev/mar/a-20/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0489, 1.2695], min area 6 px

## Measurements
- components: final 8, mean 4.2, max 8; occupancy final 0.10
- tracks: 14; persistent (alive >= 50% of run): 2; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.25 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1066, -0.5077, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 139: holes 0, rim-vs-core 0.17, rim-vs-outside 0.55, heterogeneity 0.14; core [0.906, 0.033, 0.502] rim [0.749, 0.088, 0.453]
  - track 5 at frame 139: holes 0, rim-vs-core 0.18, rim-vs-outside 0.59, heterogeneity 0.14; core [0.879, 0.033, 0.574] rim [0.793, 0.079, 0.42]
  - track 0 at frame 39: holes 0, rim-vs-core 0.40, rim-vs-outside 0.65, heterogeneity 0.18; core [0.954, 0.018, 0.765] rim [0.789, 0.08, 0.41]
  - track 10 at frame 180: holes 0, rim-vs-core 0.25, rim-vs-outside 0.53, heterogeneity 0.09; core [0.974, 0.024, 0.194] rim [0.739, 0.098, 0.128]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 14.3 (aggregate of 28 individuals; 4/28 membrane-like individually; rim level 0.753)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.3, rim/outside 0.646 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.221)
  - radial |v| (flow speed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 2.6 (aggregate of 28 individuals; 2/28 membrane-like individually; rim level 0.253)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=13900, R_eq 9.22): none; #5 (t=13900, R_eq 9.22): none; #0 (t=3900, R_eq 13.04, ring): ['phi (droplet material)']; #10 (t=18000, R_eq 7.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
