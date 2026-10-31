# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 152s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.003_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2098], min area 6 px

## Measurements
- components: final 34, mean 39.2, max 49; occupancy final 0.14
- tracks: 182; persistent (alive >= 50% of run): 32; longest 401 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 13.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 36, 34], H1 [0, 0, 0]
- motion: 89 long-lived tracks moved >= 1 body length; max speed 0.34/time; max body lengths 25.6
- replication (lineage window K = 20 frames = time 60, default): splits 46, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 5, merges 41, merge/split ratio 0.891, nucleations 0
- channel total drift (end/start - 1): [-0.5046, 0.1373, -96.8322, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 202: holes 0, rim-vs-core 0.67, rim-vs-outside 0.31, heterogeneity 0.17; core [0.755, 0.195, 0.081, 0.657] rim [0.395, 0.319, 0.272, 0.133]
  - track 3 at frame 202: holes 0, rim-vs-core 0.80, rim-vs-outside 0.27, heterogeneity 0.21; core [0.808, 0.128, 0.914, 0.707] rim [0.372, 0.329, 0.685, 0.105]
  - track 5 at frame 202: holes 0, rim-vs-core 0.63, rim-vs-outside 0.30, heterogeneity 0.17; core [0.765, 0.106, 0.076, 0.567] rim [0.405, 0.343, 0.266, 0.145]
  - track 159 at frame 350: holes 0, rim-vs-core 0.80, rim-vs-outside 0.29, heterogeneity 0.21; core [0.816, 0.133, 0.062, 0.724] rim [0.388, 0.34, 0.276, 0.123]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 230 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.724, rim/outside 14.6 (aggregate of 230 individuals; 1/230 membrane-like individually; rim level 0.662)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.784 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.477)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1.02 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.495)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.621, rim/outside 29.5 (aggregate of 230 individuals; 3/230 membrane-like individually; rim level 0.493)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=606, R_eq 4.26): none; #3 (t=606, R_eq 4.03): none; #5 (t=606, R_eq 5.44): none; #159 (t=1050, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 230 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
