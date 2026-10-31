# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 159s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.03_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.25 of robust range [0.0006, 0.2352], min area 6 px

## Measurements
- components: final 73, mean 70.6, max 85; occupancy final 0.24
- tracks: 6439; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [113, 71, 38], H1 [7, 0, 0]
- motion: 243 long-lived tracks moved >= 1 body length; max speed 0.601/time; max body lengths 11.9
- replication (lineage window K = 20 frames = time 60, default): splits 1740, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1676, merge/split ratio 0.963, nucleations 1351
- channel total drift (end/start - 1): [-0.0188, -0.0921, -613.8903, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 111 at frame 47: holes 0, rim-vs-core 0.32, rim-vs-outside 0.30, heterogeneity 0.13; core [0.607, 0.41, 0.146, 0.397] rim [0.421, 0.508, 0.246, 0.176]
  - track 5356 at frame 370: holes 0, rim-vs-core 0.40, rim-vs-outside 0.25, heterogeneity 0.15; core [0.618, 0.328, 0.842, 0.395] rim [0.379, 0.436, 0.707, 0.132]
  - track 3986 at frame 269: holes 0, rim-vs-core 0.30, rim-vs-outside 0.22, heterogeneity 0.14; core [0.545, 0.388, 0.176, 0.333] rim [0.377, 0.487, 0.271, 0.12]
  - track 5347 at frame 366: holes 0, rim-vs-core 0.24, rim-vs-outside 0.36, heterogeneity 0.12; core [0.566, 0.542, 0.813, 0.377] rim [0.44, 0.605, 0.741, 0.201]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 380 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.712, rim/outside 2.72 (aggregate of 380 individuals; 11/380 membrane-like individually; rim level 0.451)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.43, rim/outside 0.881 (aggregate of 380 individuals; 0/380 membrane-like individually; rim level 0.566)
  - radial vorticity (signed): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.994 (aggregate of 380 individuals; 0/380 membrane-like individually; rim level 0.479)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.543, rim/outside 5.73 (aggregate of 380 individuals; 44/380 membrane-like individually; rim level 0.227)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #111 (t=141, R_eq 3.24): none; #5356 (t=1110, R_eq 3.66): none; #3986 (t=807, R_eq 3.66): none; #5347 (t=1098, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 380 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
