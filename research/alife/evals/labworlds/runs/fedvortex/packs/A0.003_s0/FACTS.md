# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.003 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 161s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.003_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0001, 0.2073], min area 6 px

## Measurements
- components: final 32, mean 34.9, max 49; occupancy final 0.13
- tracks: 105; persistent (alive >= 50% of run): 28; longest 401 frames; alive start-to-end: 12
- size of persistent tracks: max/min area ratio 9.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 32, 32], H1 [0, 0, 0]
- motion: 68 long-lived tracks moved >= 1 body length; max speed 0.276/time; max body lengths 22.0
- replication (lineage window K = 20 frames = time 60, default): splits 19, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 18, merge/split ratio 0.947, nucleations 0
- channel total drift (end/start - 1): [-0.5486, 0.1699, -80.2804, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 202: holes 0, rim-vs-core 0.70, rim-vs-outside 0.29, heterogeneity 0.18; core [0.779, 0.114, 0.067, 0.593] rim [0.382, 0.362, 0.278, 0.117]
  - track 2 at frame 202: holes 0, rim-vs-core 0.81, rim-vs-outside 0.33, heterogeneity 0.21; core [0.844, 0.13, 0.049, 0.773] rim [0.415, 0.338, 0.26, 0.152]
  - track 8 at frame 202: holes 0, rim-vs-core 0.66, rim-vs-outside 0.28, heterogeneity 0.18; core [0.758, 0.118, 0.079, 0.575] rim [0.382, 0.338, 0.278, 0.118]
  - track 75 at frame 266: holes 0, rim-vs-core 0.60, rim-vs-outside 0.26, heterogeneity 0.16; core [0.725, 0.176, 0.871, 0.577] rim [0.398, 0.278, 0.698, 0.121]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 202 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 15.7 (aggregate of 202 individuals; 0/202 membrane-like individually; rim level 0.696)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13, rim/outside 0.776 (aggregate of 202 individuals; 0/202 membrane-like individually; rim level 0.492)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 1.01 (aggregate of 202 individuals; 0/202 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.699, rim/outside 30.4 (aggregate of 202 individuals; 2/202 membrane-like individually; rim level 0.542)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=606, R_eq 5.44): none; #2 (t=606, R_eq 4.18): none; #8 (t=606, R_eq 5.41): none; #75 (t=798, R_eq 3.34): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
