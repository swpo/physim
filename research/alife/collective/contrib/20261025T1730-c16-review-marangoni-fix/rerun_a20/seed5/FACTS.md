# Evidence pack: marangoni-droplets (seed 5)

- world: `../../../20261025T0946-c01-marangoni-droplets/world.py`, family `phase-field`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: self-generated Brinkman flow from a fuel-dependent interfacial stress advects droplets and fuel
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0946-c01-marangoni-droplets/world.py --out collective/contrib/20261025T1401-c16-review-marangoni/rerun_a20/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0387, 1.2819], min area 6 px

## Measurements
- components: final 24, mean 21.4, max 24; occupancy final 0.12
- tracks: 49; persistent (alive >= 50% of run): 24; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.00495/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.1848, -0.67, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 111: holes 0, rim-vs-core 0.30, rim-vs-outside 0.32, heterogeneity 0.06; core [0.928, 0.026, 0.016] rim [0.627, 0.071, 0.011]
  - track 21 at frame 111: holes 0, rim-vs-core 0.31, rim-vs-outside 0.32, heterogeneity 0.06; core [0.929, 0.026, 0.016] rim [0.626, 0.071, 0.011]
  - track 22 at frame 111: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.06; core [0.922, 0.031, 0.012] rim [0.626, 0.072, 0.008]
  - track 45 at frame 129: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.06; core [0.931, 0.022, 0.022] rim [0.643, 0.069, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 138 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 56.6 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.908)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.72, rim/outside 0.709 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.118)
  - radial |v| (flow speed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.662, rim/outside 2.32 (aggregate of 138 individuals; 0/138 membrane-like individually; rim level 0.0442)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=11100, R_eq 5.08): none; #21 (t=11100, R_eq 5.08): none; #22 (t=11100, R_eq 4.79): none; #45 (t=12900, R_eq 5.44): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
