# Evidence pack: marangoni-droplets (seed 0)

- world: `../../../../contrib/20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 286s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/work_c05/rev_mg/a0_f005/seed0 --seeds 0 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0476, 1.2709], min area 6 px

## Measurements
- components: final 16, mean 11.4, max 16; occupancy final 0.12
- tracks: 30; persistent (alive >= 50% of run): 8; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.38 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00223/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 2000, default): splits 14, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1637, -0.6338, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 121: holes 0, rim-vs-core 0.18, rim-vs-outside 0.44, heterogeneity 0.07; core [0.928, 0.043, 0.074] rim [0.753, 0.068, 0.062]
  - track 13 at frame 121: holes 0, rim-vs-core 0.23, rim-vs-outside 0.40, heterogeneity 0.07; core [0.947, 0.035, 0.065] rim [0.719, 0.08, 0.074]
  - track 14 at frame 128: holes 0, rim-vs-core 0.23, rim-vs-outside 0.54, heterogeneity 0.09; core [0.972, 0.019, 0.235] rim [0.754, 0.082, 0.232]
  - track 22 at frame 151: holes 0, rim-vs-core 0.23, rim-vs-outside 0.54, heterogeneity 0.07; core [0.976, 0.019, 0.059] rim [0.757, 0.08, 0.06]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 46.3 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.917)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.3, rim/outside 0.686 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.163)
  - radial |v| (flow speed): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 3.19 (aggregate of 78 individuals; 46/78 membrane-like individually; rim level 0.227)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=12100, R_eq 6): ['|v| (flow speed)']; #13 (t=12100, R_eq 5.97): ['|v| (flow speed)']; #14 (t=12800, R_eq 6.48): ['|v| (flow speed)']; #22 (t=15100, R_eq 6.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
