# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 167s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0.01_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0002, 0.2143], min area 6 px

## Measurements
- components: final 29, mean 37.1, max 50; occupancy final 0.15
- tracks: 243; persistent (alive >= 50% of run): 26; longest 401 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 7.37 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 29, 29], H1 [0, 0, 0]
- motion: 95 long-lived tracks moved >= 1 body length; max speed 0.305/time; max body lengths 25.8
- replication (lineage window K = 20 frames = time 60, default): splits 65, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 64, merge/split ratio 0.985, nucleations 1
- channel total drift (end/start - 1): [-0.4195, 0.1456, 1726.627, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 202: holes 0, rim-vs-core 0.63, rim-vs-outside 0.30, heterogeneity 0.18; core [0.782, 0.089, 0.903, 0.582] rim [0.418, 0.279, 0.707, 0.145]
  - track 2 at frame 202: holes 0, rim-vs-core 0.66, rim-vs-outside 0.31, heterogeneity 0.18; core [0.787, 0.108, 0.062, 0.612] rim [0.405, 0.318, 0.258, 0.152]
  - track 20 at frame 202: holes 0, rim-vs-core 0.69, rim-vs-outside 0.32, heterogeneity 0.19; core [0.798, 0.108, 0.91, 0.642] rim [0.415, 0.316, 0.705, 0.152]
  - track 209 at frame 370: holes 0, rim-vs-core 0.40, rim-vs-outside 0.40, heterogeneity 0.16; core [0.693, 0.137, 0.856, 0.487] rim [0.46, 0.271, 0.73, 0.222]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 211 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.744, rim/outside 9.96 (aggregate of 211 individuals; 4/211 membrane-like individually; rim level 0.652)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.1, rim/outside 0.782 (aggregate of 211 individuals; 0/211 membrane-like individually; rim level 0.474)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.971, rim/outside 1.07 (aggregate of 211 individuals; 0/211 membrane-like individually; rim level 0.514)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.656, rim/outside 28.9 (aggregate of 211 individuals; 7/211 membrane-like individually; rim level 0.472)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=606, R_eq 5.01): none; #2 (t=606, R_eq 4.62): none; #20 (t=606, R_eq 4.62): none; #209 (t=1110, R_eq 4.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 211 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
