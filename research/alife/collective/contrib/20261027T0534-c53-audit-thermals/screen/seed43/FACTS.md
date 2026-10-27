# Evidence pack: reacting-thermals (seed 43)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 201 frames x 25 steps x dt 0.04 = time 200; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie`
- segmentation: matter > 0.34 of robust range [0.0, 0.7279], min area 6 px

## Measurements
- components: final 12, mean 7.9, max 43; occupancy final 0.02
- tracks: 139; persistent (alive >= 50% of run): 0; longest 82 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 11], H1 [0, 0, 0]
- motion: 27 long-lived tracks moved >= 1 body length; max speed 1.08/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 20, default): splits 43, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.163, nucleations 15
- channel total drift (end/start - 1): [-0.8582, -0.2032, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 110 at frame 136: holes 0, rim-vs-core 0.20, rim-vs-outside 0.49, heterogeneity 0.15; core [0.719, 0.174, 0.516, 0.773] rim [0.57, 0.234, 0.453, 0.667]
  - track 108 at frame 116: holes 0, rim-vs-core 0.22, rim-vs-outside 0.51, heterogeneity 0.16; core [0.778, 0.173, 0.548, 0.844] rim [0.615, 0.226, 0.474, 0.721]
  - track 123 at frame 180: holes 0, rim-vs-core 0.27, rim-vs-outside 0.60, heterogeneity 0.16; core [0.789, 0.206, 0.419, 0.912] rim [0.596, 0.253, 0.427, 0.734]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 35 components >= 12 px at frames [67, 101, 133, 166, 200]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.889, rim/outside 4.62 (aggregate of 35 individuals; 2/35 membrane-like individually; rim level 0.472)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.82, rim/outside 0.747 (aggregate of 35 individuals; 0/35 membrane-like individually; rim level 0.36)
  - radial vorticity: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.04 (aggregate of 35 individuals; 5/35 membrane-like individually; rim level 0.501)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 5.21 (aggregate of 35 individuals; 5/35 membrane-like individually; rim level 0.526)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #110 (t=136, R_eq 3.66, ring): ['burn r']; #108 (t=116, R_eq 3.24): ['burn r']; #113 (t=168, R_eq 2.71): none; #123 (t=180, R_eq 3.24, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 35 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
