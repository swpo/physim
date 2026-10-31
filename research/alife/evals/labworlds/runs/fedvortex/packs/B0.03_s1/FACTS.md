# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 166s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.03_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.26 of robust range [0.0006, 0.2334], min area 6 px

## Measurements
- components: final 71, mean 69.7, max 87; occupancy final 0.21
- tracks: 6444; persistent (alive >= 50% of run): 0; longest 99 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.22, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [102, 66, 32], H1 [10, 0, 0]
- motion: 237 long-lived tracks moved >= 1 body length; max speed 0.635/time; max body lengths 13.1
- replication (lineage window K = 20 frames = time 60, default): splits 1754, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1644, merge/split ratio 0.937, nucleations 1376
- channel total drift (end/start - 1): [-0.07, -0.0579, -901.0931, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 897 at frame 104: holes 0, rim-vs-core 0.41, rim-vs-outside 0.24, heterogeneity 0.14; core [0.612, 0.256, 0.138, 0.361] rim [0.361, 0.395, 0.281, 0.099]
  - track 1438 at frame 134: holes 0, rim-vs-core 0.22, rim-vs-outside 0.34, heterogeneity 0.12; core [0.557, 0.521, 0.17, 0.349] rim [0.424, 0.587, 0.245, 0.2]
  - track 5158 at frame 363: holes 0, rim-vs-core 0.61, rim-vs-outside 0.37, heterogeneity 0.20; core [0.754, 0.194, 0.907, 0.584] rim [0.422, 0.419, 0.731, 0.158]
  - track 3212 at frame 245: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.17; core [0.713, 0.227, 0.087, 0.512] rim [0.393, 0.376, 0.263, 0.128]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 377 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.717, rim/outside 2.76 (aggregate of 377 individuals; 15/377 membrane-like individually; rim level 0.467)
  - radial fuel Y: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 2.49, rim/outside 0.878 (aggregate of 377 individuals; 0/377 membrane-like individually; rim level 0.571)
  - radial vorticity (signed): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.993 (aggregate of 377 individuals; 0/377 membrane-like individually; rim level 0.476)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.554, rim/outside 5.92 (aggregate of 377 individuals; 40/377 membrane-like individually; rim level 0.247)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #897 (t=312, R_eq 3.04): none; #1438 (t=402, R_eq 2.71): none; #5158 (t=1089, R_eq 3.48): none; #3212 (t=735, R_eq 3.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 377 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
