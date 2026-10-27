# Evidence pack: reacting-thermals (seed 32)

- world: `../../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 1201 frames x 25 steps x dt 0.04 = time 1200; grid [128, 128]; wall 147s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/rev/sel --seeds 31 32 --frames 1200 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.794], min area 6 px

## Measurements
- components: final 24, mean 17.5, max 46; occupancy final 0.02
- tracks: 1020; persistent (alive >= 50% of run): 0; longest 172 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 29, 25], H1 [0, 0, 0]
- motion: 349 long-lived tracks moved >= 1 body length; max speed 1.39/time; max body lengths 35.2
- replication (lineage window K = 20 frames = time 20, default): splits 196, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 7, merges 31, merge/split ratio 0.158, nucleations 571
- channel total drift (end/start - 1): [-0.8664, -0.337, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 866 at frame 1109: holes 0, rim-vs-core 0.30, rim-vs-outside 0.72, heterogeneity 0.11; core [1.0, 0.012, 0.479, 1.0] rim [0.818, 0.051, 0.357, 0.807]
  - track 699 at frame 948: holes 0, rim-vs-core 0.24, rim-vs-outside 0.55, heterogeneity 0.09; core [0.938, 0.013, 0.894, 0.695] rim [0.762, 0.059, 0.763, 0.595]
  - track 248 at frame 524: holes 0, rim-vs-core 0.11, rim-vs-outside 0.58, heterogeneity 0.09; core [0.907, 0.0, 0.237, 0.967] rim [0.802, 0.031, 0.244, 0.935]
  - track 250 at frame 494: holes 0, rim-vs-core 0.31, rim-vs-outside 0.66, heterogeneity 0.12; core [0.993, 0.021, 0.936, 0.659] rim [0.795, 0.067, 0.74, 0.521]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [202, 403, 605, 797, 998, 1200]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.924, rim/outside 5.35 (aggregate of 81 individuals; 3/81 membrane-like individually; rim level 0.72)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 6.71, rim/outside 0.573 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.174)
  - radial label a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 4 (aggregate of 81 individuals; 3/81 membrane-like individually; rim level 0.534)
  - radial label b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 4.6 (aggregate of 81 individuals; 3/81 membrane-like individually; rim level 0.547)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #866 (t=1109, R_eq 2.71): none; #699 (t=948, R_eq 2.59): none; #248 (t=524, R_eq 2.39): none; #250 (t=494, R_eq 3.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
