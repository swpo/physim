# Evidence pack: reacting-thermals (seed 11)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 55s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out /tmp/claude-0/th/fork --seeds 11 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7598], min area 6 px

## Measurements
- components: final 0, mean 5.0, max 39; occupancy final 0.00
- tracks: 189; persistent (alive >= 50% of run): 0; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.927/time; max body lengths 14.5
- replication (lineage window K = 20 frames = time 20, default): splits 59, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.169, nucleations 28
- channel total drift (end/start - 1): [-1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 132 at frame 353: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.18; core [0.903, 0.342, 0.463, 0.959] rim [0.702, 0.379, 0.472, 0.823]
  - track 108 at frame 247: holes 0, rim-vs-core 0.18, rim-vs-outside 0.53, heterogeneity 0.17; core [0.936, 0.326, 0.493, 0.973] rim [0.808, 0.368, 0.443, 0.871]
  - track 146 at frame 368: holes 0, rim-vs-core 0.29, rim-vs-outside 0.75, heterogeneity 0.18; core [0.996, 0.35, 0.493, 1.0] rim [0.74, 0.418, 0.5, 0.885]
  - track 149 at frame 368: holes 0, rim-vs-core 0.21, rim-vs-outside 0.66, heterogeneity 0.16; core [0.948, 0.343, 0.254, 0.991] rim [0.795, 0.372, 0.364, 0.9]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [101, 202, 303, 398]):
  - radial heat T: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 4.65 (aggregate of 30 individuals; 2/30 membrane-like individually; rim level 0.618)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 0.834 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.476)
  - radial vorticity: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.04 (aggregate of 30 individuals; 5/30 membrane-like individually; rim level 0.458)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 5.25 (aggregate of 30 individuals; 2/30 membrane-like individually; rim level 0.673)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #132 (t=353, R_eq 2.33): none; #108 (t=247, R_eq 3.24): none; #146 (t=368, R_eq 2.99): none; #149 (t=368, R_eq 2.76): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
