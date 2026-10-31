# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.3 per sqrt(t): additive on [], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 145s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/G0.3_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.27 of robust range [0.0, 0.2191], min area 6 px

## Measurements
- components: final 27, mean 32.9, max 49; occupancy final 0.12
- tracks: 136; persistent (alive >= 50% of run): 24; longest 401 frames; alive start-to-end: 6
- size of persistent tracks: max/min area ratio 9.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 27], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.285/time; max body lengths 27.4
- replication (lineage window K = 20 frames = time 60, default): splits 29, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 29, merge/split ratio 1, nucleations 0
- channel total drift (end/start - 1): [-0.6101, 0.2022, 1442.1553, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 202: holes 0, rim-vs-core 0.40, rim-vs-outside 0.42, heterogeneity 0.15; core [0.756, 0.055, 0.067, 0.464] rim [0.499, 0.157, 0.206, 0.209]
  - track 8 at frame 202: holes 0, rim-vs-core 0.66, rim-vs-outside 0.29, heterogeneity 0.18; core [0.795, 0.088, 0.058, 0.594] rim [0.401, 0.242, 0.259, 0.129]
  - track 10 at frame 202: holes 0, rim-vs-core 0.79, rim-vs-outside 0.29, heterogeneity 0.20; core [0.838, 0.108, 0.047, 0.728] rim [0.395, 0.248, 0.262, 0.121]
  - track 88 at frame 276: holes 0, rim-vs-core 0.80, rim-vs-outside 0.28, heterogeneity 0.21; core [0.833, 0.127, 0.928, 0.714] rim [0.379, 0.271, 0.688, 0.116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 184 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 17.7 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.654)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.35, rim/outside 0.79 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.361)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.969, rim/outside 1.02 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.685, rim/outside 28.4 (aggregate of 184 individuals; 4/184 membrane-like individually; rim level 0.461)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=606, R_eq 5.47): none; #8 (t=606, R_eq 4.07): none; #10 (t=606, R_eq 4.03): none; #88 (t=828, R_eq 4.89): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
