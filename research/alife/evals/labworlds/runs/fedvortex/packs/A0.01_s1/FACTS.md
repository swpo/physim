# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 163s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.01_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0002, 0.2145], min area 6 px

## Measurements
- components: final 32, mean 37.5, max 49; occupancy final 0.15
- tracks: 296; persistent (alive >= 50% of run): 25; longest 401 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 35, 32], H1 [0, 0, 0]
- motion: 109 long-lived tracks moved >= 1 body length; max speed 0.386/time; max body lengths 26.0
- replication (lineage window K = 20 frames = time 60, default): splits 86, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 5, merges 76, merge/split ratio 0.884, nucleations 0
- channel total drift (end/start - 1): [-0.4214, 0.1263, -309.5916, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 202: holes 0, rim-vs-core 0.74, rim-vs-outside 0.30, heterogeneity 0.20; core [0.815, 0.125, 0.922, 0.71] rim [0.415, 0.328, 0.713, 0.157]
  - track 13 at frame 202: holes 0, rim-vs-core 0.53, rim-vs-outside 0.27, heterogeneity 0.16; core [0.697, 0.155, 0.865, 0.506] rim [0.397, 0.303, 0.703, 0.127]
  - track 43 at frame 198: holes 0, rim-vs-core 0.54, rim-vs-outside 0.26, heterogeneity 0.16; core [0.688, 0.141, 0.115, 0.476] rim [0.378, 0.32, 0.281, 0.114]
  - track 238 at frame 309: holes 0, rim-vs-core 0.74, rim-vs-outside 0.28, heterogeneity 0.20; core [0.798, 0.124, 0.064, 0.669] rim [0.388, 0.328, 0.275, 0.124]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.733, rim/outside 8.42 (aggregate of 214 individuals; 1/214 membrane-like individually; rim level 0.618)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.76, rim/outside 0.781 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.478)
  - radial vorticity (signed): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.988 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.477)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.63, rim/outside 20.6 (aggregate of 214 individuals; 8/214 membrane-like individually; rim level 0.43)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=606, R_eq 4.07): none; #13 (t=606, R_eq 4.51): none; #43 (t=594, R_eq 5.56): none; #238 (t=927, R_eq 4.22): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
