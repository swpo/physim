# Evidence pack: reacting-thermals (seed 11)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 50 steps x dt 0.02 (--dt; world META dt 0.04) = time 600; grid [128, 128]; wall 108s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out /tmp/claude-0/th/dthalf --seeds 11 --frames 600 --spf 50 --dt 0.02 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7598], min area 6 px

## Measurements
- components: final 28, mean 14.5, max 40; occupancy final 0.03
- tracks: 441; persistent (alive >= 50% of run): 0; longest 211 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 31, 28], H1 [0, 0, 0]
- motion: 151 long-lived tracks moved >= 1 body length; max speed 1.19/time; max body lengths 22.1
- replication (lineage window K = 20 frames = time 20, default): splits 98, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 6, merges 14, merge/split ratio 0.143, nucleations 203
- channel total drift (end/start - 1): [-0.8583, -0.3287, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 267: holes 0, rim-vs-core 0.36, rim-vs-outside 0.58, heterogeneity 0.15; core [0.966, 0.106, 0.276, 0.977] rim [0.713, 0.135, 0.417, 0.765]
  - track 255 at frame 509: holes 0, rim-vs-core 0.17, rim-vs-outside 0.56, heterogeneity 0.16; core [0.945, 0.089, 0.459, 0.979] rim [0.804, 0.136, 0.427, 0.893]
  - track 104 at frame 161: holes 0, rim-vs-core 0.34, rim-vs-outside 0.49, heterogeneity 0.14; core [0.957, 0.094, 0.264, 0.97] rim [0.71, 0.129, 0.365, 0.758]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 5.34 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.653)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.64, rim/outside 0.639 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.246)
  - radial vorticity: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 1.05 (aggregate of 64 individuals; 14/64 membrane-like individually; rim level 0.476)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 6.22 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.675)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #182 (t=454, R_eq 1.95): none; #109 (t=267, R_eq 3.61): none; #255 (t=509, R_eq 2.19): none; #104 (t=161, R_eq 3.39, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.02 only relabels time (world META dt 0.04): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 5 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
