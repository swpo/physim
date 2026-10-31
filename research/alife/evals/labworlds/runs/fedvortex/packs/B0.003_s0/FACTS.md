# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 157s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.003_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2071], min area 6 px

## Measurements
- components: final 28, mean 34.3, max 49; occupancy final 0.14
- tracks: 110; persistent (alive >= 50% of run): 30; longest 401 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 6.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 30, 27], H1 [0, 0, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.226/time; max body lengths 20.8
- replication (lineage window K = 20 frames = time 60, default): splits 19, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 23, merge/split ratio 1.21, nucleations 0
- channel total drift (end/start - 1): [-0.5351, 0.173, 646.9741, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 202: holes 0, rim-vs-core 0.74, rim-vs-outside 0.32, heterogeneity 0.20; core [0.828, 0.111, 0.055, 0.704] rim [0.424, 0.32, 0.257, 0.158]
  - track 13 at frame 202: holes 0, rim-vs-core 0.76, rim-vs-outside 0.31, heterogeneity 0.20; core [0.821, 0.119, 0.92, 0.708] rim [0.407, 0.311, 0.703, 0.141]
  - track 16 at frame 202: holes 0, rim-vs-core 0.74, rim-vs-outside 0.31, heterogeneity 0.20; core [0.815, 0.118, 0.058, 0.683] rim [0.404, 0.332, 0.267, 0.144]
  - track 83 at frame 289: holes 0, rim-vs-core 0.70, rim-vs-outside 0.28, heterogeneity 0.19; core [0.795, 0.111, 0.908, 0.638] rim [0.402, 0.311, 0.701, 0.129]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 13.2 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.671)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.779 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.48)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.01 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.492)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 25 (aggregate of 196 individuals; 3/196 membrane-like individually; rim level 0.506)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=606, R_eq 4.41): none; #13 (t=606, R_eq 4.18): none; #16 (t=606, R_eq 4.58): none; #83 (t=867, R_eq 4.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 196 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
