# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 163s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.003_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2093], min area 6 px

## Measurements
- components: final 31, mean 38.4, max 49; occupancy final 0.14
- tracks: 156; persistent (alive >= 50% of run): 35; longest 401 frames; alive start-to-end: 8
- size of persistent tracks: max/min area ratio 21.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 31], H1 [0, 0, 0]
- motion: 77 long-lived tracks moved >= 1 body length; max speed 0.385/time; max body lengths 25.5
- replication (lineage window K = 20 frames = time 60, default): splits 37, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 33, merge/split ratio 0.892, nucleations 0
- channel total drift (end/start - 1): [-0.512, 0.1488, -60.5498, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 202: holes 0, rim-vs-core 0.65, rim-vs-outside 0.31, heterogeneity 0.17; core [0.794, 0.104, 0.064, 0.636] rim [0.436, 0.291, 0.25, 0.167]
  - track 3 at frame 202: holes 0, rim-vs-core 0.77, rim-vs-outside 0.28, heterogeneity 0.20; core [0.801, 0.135, 0.909, 0.704] rim [0.387, 0.309, 0.692, 0.119]
  - track 8 at frame 202: holes 0, rim-vs-core 0.71, rim-vs-outside 0.29, heterogeneity 0.19; core [0.796, 0.108, 0.909, 0.642] rim [0.402, 0.303, 0.7, 0.131]
  - track 151 at frame 387: holes 0, rim-vs-core 0.59, rim-vs-outside 0.29, heterogeneity 0.16; core [0.734, 0.122, 0.877, 0.552] rim [0.397, 0.283, 0.698, 0.126]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 225 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.732, rim/outside 15.1 (aggregate of 225 individuals; 1/225 membrane-like individually; rim level 0.672)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.5, rim/outside 0.783 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.465)
  - radial vorticity (signed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.976, rim/outside 1.01 (aggregate of 225 individuals; 0/225 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.637, rim/outside 31 (aggregate of 225 individuals; 4/225 membrane-like individually; rim level 0.506)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=606, R_eq 4.33): none; #3 (t=606, R_eq 3.83): none; #8 (t=606, R_eq 4.44): none; #151 (t=1161, R_eq 5.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 225 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
