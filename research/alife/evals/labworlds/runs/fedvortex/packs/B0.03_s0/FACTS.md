# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 162s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.03_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.25 of robust range [0.0006, 0.2337], min area 6 px

## Measurements
- components: final 72, mean 69.7, max 83; occupancy final 0.23
- tracks: 6503; persistent (alive >= 50% of run): 0; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.32, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [105, 62, 33], H1 [8, 0, 0]
- motion: 233 long-lived tracks moved >= 1 body length; max speed 0.641/time; max body lengths 17.0
- replication (lineage window K = 20 frames = time 60, default): splits 1779, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1721, merge/split ratio 0.967, nucleations 1336
- channel total drift (end/start - 1): [-0.0422, -0.0836, -2357.5513, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 857 at frame 128: holes 0, rim-vs-core 0.61, rim-vs-outside 0.26, heterogeneity 0.20; core [0.725, 0.113, 0.887, 0.474] rim [0.359, 0.359, 0.681, 0.106]
  - track 2100 at frame 192: holes 0, rim-vs-core 0.53, rim-vs-outside 0.36, heterogeneity 0.19; core [0.695, 0.277, 0.091, 0.521] rim [0.405, 0.484, 0.245, 0.158]
  - track 1149 at frame 124: holes 0, rim-vs-core 0.83, rim-vs-outside 0.35, heterogeneity 0.25; core [0.849, 0.225, 0.938, 0.782] rim [0.403, 0.476, 0.71, 0.166]
  - track 4691 at frame 333: holes 0, rim-vs-core 0.60, rim-vs-outside 0.27, heterogeneity 0.20; core [0.695, 0.267, 0.871, 0.524] rim [0.364, 0.487, 0.688, 0.112]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 354 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.71, rim/outside 2.78 (aggregate of 354 individuals; 9/354 membrane-like individually; rim level 0.457)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.48, rim/outside 0.871 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.571)
  - radial vorticity (signed): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.99 (aggregate of 354 individuals; 0/354 membrane-like individually; rim level 0.47)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.547, rim/outside 6.01 (aggregate of 354 individuals; 39/354 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #857 (t=384, R_eq 4.22): none; #2100 (t=576, R_eq 3.7): none; #1149 (t=372, R_eq 3.09): none; #4691 (t=999, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 354 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
