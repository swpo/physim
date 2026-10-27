# Evidence pack: reacting-thermals (seed 45)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7249], min area 6 px

## Measurements
- components: final 12, mean 9.6, max 40; occupancy final 0.02
- tracks: 173; persistent (alive >= 50% of run): 2; longest 132 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.50 (1 = constant size)
- enclosures: components with a hole mean 0.08, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 14, 13], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 1.07/time; max body lengths 18.8
- replication (lineage window K = 20 frames = time 20, default): splits 50, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 15, merge/split ratio 0.3, nucleations 21
- channel total drift (end/start - 1): [-0.8963, -0.1991, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 116 at frame 114: holes 0, rim-vs-core 0.18, rim-vs-outside 0.46, heterogeneity 0.15; core [0.69, 0.223, 0.521, 0.8] rim [0.564, 0.269, 0.462, 0.689]
  - track 133 at frame 150: holes 0, rim-vs-core 0.22, rim-vs-outside 0.45, heterogeneity 0.15; core [0.714, 0.218, 0.434, 0.825] rim [0.568, 0.26, 0.5, 0.68]
  - track 127 at frame 138: holes 0, rim-vs-core 0.21, rim-vs-outside 0.51, heterogeneity 0.18; core [0.714, 0.196, 0.421, 0.774] rim [0.566, 0.263, 0.518, 0.685]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 41 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 5.28 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.496)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.69, rim/outside 0.77 (aggregate of 41 individuals; 0/41 membrane-like individually; rim level 0.369)
  - radial vorticity: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.01 (aggregate of 41 individuals; 8/41 membrane-like individually; rim level 0.451)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.872, rim/outside 6.37 (aggregate of 41 individuals; 1/41 membrane-like individually; rim level 0.562)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #116 (t=114, R_eq 2.82): ['burn r']; #133 (t=150, R_eq 2.26): ['vorticity']; #127 (t=138, R_eq 2.88): ['vorticity']; #145 (t=168, R_eq 1.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 41 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
