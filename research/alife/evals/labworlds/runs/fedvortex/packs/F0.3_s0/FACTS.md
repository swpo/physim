# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.3 per sqrt(t): additive on ['Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 145s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/F0.3_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.25 of robust range [0.0, 0.2407], min area 6 px

## Measurements
- components: final 17, mean 26.7, max 49; occupancy final 0.10
- tracks: 111; persistent (alive >= 50% of run): 23; longest 401 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 38.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 18, 16], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.343/time; max body lengths 22.0
- replication (lineage window K = 20 frames = time 60, default): splits 21, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 19, merge/split ratio 0.905, nucleations 1
- channel total drift (end/start - 1): [-0.6848, 0.303, 996.7642, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 202: holes 0, rim-vs-core 0.42, rim-vs-outside 0.25, heterogeneity 0.13; core [0.68, 0.061, 0.849, 0.25] rim [0.363, 0.158, 0.669, 0.069]
  - track 2 at frame 202: holes 0, rim-vs-core 0.68, rim-vs-outside 0.27, heterogeneity 0.20; core [0.779, 0.215, 0.045, 0.609] rim [0.379, 0.354, 0.244, 0.115]
  - track 5 at frame 202: holes 0, rim-vs-core 0.57, rim-vs-outside 0.26, heterogeneity 0.20; core [0.753, 0.132, 0.885, 0.44] rim [0.368, 0.244, 0.672, 0.09]
  - track 59 at frame 198: holes 0, rim-vs-core 0.61, rim-vs-outside 0.28, heterogeneity 0.19; core [0.767, 0.15, 0.893, 0.502] rim [0.382, 0.271, 0.68, 0.105]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 147 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 18.5 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.649)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 4.05, rim/outside 0.817 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.408)
  - radial vorticity (signed): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 1.12 (aggregate of 147 individuals; 0/147 membrane-like individually; rim level 0.52)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 25.3 (aggregate of 147 individuals; 9/147 membrane-like individually; rim level 0.393)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=606, R_eq 5.38): ['eating']; #2 (t=606, R_eq 5.14): none; #5 (t=606, R_eq 3.52): none; #59 (t=594, R_eq 4.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
