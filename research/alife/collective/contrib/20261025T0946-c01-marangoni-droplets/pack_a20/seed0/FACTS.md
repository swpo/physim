# Evidence pack: marangoni-droplets (seed 0)

- world: `../../world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 283s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T0946-c01-marangoni-droplets/pack_a20 --seeds 0 1 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0379, 1.2826], min area 6 px

## Measurements
- components: final 22, mean 19.9, max 22; occupancy final 0.12
- tracks: 40; persistent (alive >= 50% of run): 22; longest 184 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.05 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 22, 22], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00824/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 2000, default): splits 16, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1814, -0.665, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 109: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.06; core [0.932, 0.03, 0.02] rim [0.653, 0.073, 0.013]
  - track 15 at frame 109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.07; core [0.925, 0.033, 0.017] rim [0.626, 0.075, 0.01]
  - track 16 at frame 109: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.06; core [0.933, 0.026, 0.023] rim [0.654, 0.073, 0.015]
  - track 34 at frame 123: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.07; core [0.928, 0.026, 0.024] rim [0.627, 0.075, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 53.8 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.913)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.91, rim/outside 0.709 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.125)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 2.28 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.0499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=10900, R_eq 4.95): none; #15 (t=10900, R_eq 4.98): none; #16 (t=10900, R_eq 5.29): none; #34 (t=12300, R_eq 5.47): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
