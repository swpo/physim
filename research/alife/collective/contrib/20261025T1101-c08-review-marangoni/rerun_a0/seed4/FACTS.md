# Evidence pack: marangoni-droplets (seed 4)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 281s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out /tmp/claude-0/-home-user-physim/b3c8c7c9-06fe-5142-8c86-74065d022b56/scratchpad/rev5/a0 --seeds 4 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0486, 1.2708], min area 6 px

## Measurements
- components: final 14, mean 9.7, max 14; occupancy final 0.11
- tracks: 26; persistent (alive >= 50% of run): 10; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.93 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 14, 14], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00402/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1564, -0.6198, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 138: holes 0, rim-vs-core 0.23, rim-vs-outside 0.54, heterogeneity 0.10; core [0.967, 0.023, 0.418] rim [0.745, 0.089, 0.424]
  - track 11 at frame 138: holes 0, rim-vs-core 0.27, rim-vs-outside 0.53, heterogeneity 0.07; core [0.977, 0.025, 0.039] rim [0.718, 0.089, 0.049]
  - track 12 at frame 138: holes 0, rim-vs-core 0.26, rim-vs-outside 0.53, heterogeneity 0.07; core [0.978, 0.024, 0.04] rim [0.729, 0.087, 0.049]
  - track 22 at frame 166: holes 0, rim-vs-core 0.24, rim-vs-outside 0.53, heterogeneity 0.08; core [0.975, 0.022, 0.165] rim [0.744, 0.088, 0.174]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 42.9 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.92)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.9, rim/outside 0.681 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.175)
  - radial |v| (flow speed): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.31 (aggregate of 66 individuals; 40/66 membrane-like individually; rim level 0.276)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=13800, R_eq 6.7): ['|v| (flow speed)']; #11 (t=13800, R_eq 6.41): ['|v| (flow speed)']; #12 (t=13800, R_eq 6.36): ['|v| (flow speed)']; #22 (t=16600, R_eq 6.6): ['|v| (flow speed)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
