# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 158s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.01_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0002, 0.214], min area 6 px

## Measurements
- components: final 36, mean 39.4, max 49; occupancy final 0.15
- tracks: 260; persistent (alive >= 50% of run): 24; longest 401 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 7.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 36], H1 [0, 0, 0]
- motion: 112 long-lived tracks moved >= 1 body length; max speed 0.385/time; max body lengths 26.5
- replication (lineage window K = 20 frames = time 60, default): splits 75, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 62, merge/split ratio 0.827, nucleations 1
- channel total drift (end/start - 1): [-0.4051, 0.1088, 249.1583, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 202: holes 0, rim-vs-core 0.56, rim-vs-outside 0.29, heterogeneity 0.16; core [0.719, 0.126, 0.87, 0.517] rim [0.39, 0.261, 0.694, 0.12]
  - track 32 at frame 202: holes 0, rim-vs-core 0.65, rim-vs-outside 0.27, heterogeneity 0.18; core [0.757, 0.115, 0.076, 0.567] rim [0.378, 0.323, 0.275, 0.117]
  - track 33 at frame 202: holes 0, rim-vs-core 0.56, rim-vs-outside 0.57, heterogeneity 0.18; core [0.838, 0.041, 0.932, 0.644] rim [0.512, 0.275, 0.76, 0.286]
  - track 253 at frame 390: holes 0, rim-vs-core 0.64, rim-vs-outside 0.29, heterogeneity 0.17; core [0.761, 0.113, 0.893, 0.563] rim [0.395, 0.329, 0.697, 0.132]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 232 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 8.78 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.637)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.57, rim/outside 0.785 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.464)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 1.04 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.503)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.622, rim/outside 22.6 (aggregate of 232 individuals; 3/232 membrane-like individually; rim level 0.447)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=606, R_eq 4.15): none; #32 (t=606, R_eq 4.92): none; #33 (t=606, R_eq 6.02): none; #253 (t=1170, R_eq 5.05): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
