# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.02 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.02_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.27 of robust range [0.0004, 0.2249], min area 6 px

## Measurements
- components: final 38, mean 40.5, max 57; occupancy final 0.17
- tracks: 985; persistent (alive >= 50% of run): 6; longest 396 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.38 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 43, 34], H1 [0, 0, 0]
- motion: 181 long-lived tracks moved >= 1 body length; max speed 0.517/time; max body lengths 23.1
- replication (lineage window K = 20 frames = time 60, default): splits 312, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 278, merge/split ratio 0.891, nucleations 37
- channel total drift (end/start - 1): [-0.2678, 0.0552, -41.2963, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 57 at frame 202: holes 0, rim-vs-core 0.54, rim-vs-outside 0.27, heterogeneity 0.18; core [0.697, 0.114, 0.103, 0.456] rim [0.368, 0.314, 0.275, 0.113]
  - track 42 at frame 145: holes 0, rim-vs-core 0.73, rim-vs-outside 0.30, heterogeneity 0.22; core [0.782, 0.134, 0.906, 0.641] rim [0.373, 0.358, 0.69, 0.129]
  - track 61 at frame 124: holes 0, rim-vs-core 0.54, rim-vs-outside 0.27, heterogeneity 0.16; core [0.689, 0.211, 0.865, 0.513] rim [0.389, 0.386, 0.699, 0.129]
  - track 865 at frame 370: holes 0, rim-vs-core 0.29, rim-vs-outside 0.49, heterogeneity 0.15; core [0.649, 0.111, 0.125, 0.398] rim [0.482, 0.258, 0.212, 0.233]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 232 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.724, rim/outside 4.73 (aggregate of 232 individuals; 5/232 membrane-like individually; rim level 0.543)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 4.99, rim/outside 0.799 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.479)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.479)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.609, rim/outside 13.3 (aggregate of 232 individuals; 9/232 membrane-like individually; rim level 0.332)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #57 (t=606, R_eq 5.41): none; #42 (t=435, R_eq 4.11): none; #61 (t=372, R_eq 4.44): none; #865 (t=1110, R_eq 7.67): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 232 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
