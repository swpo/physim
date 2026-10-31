# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 126s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2088], min area 6 px

## Measurements
- components: final 32, mean 36.5, max 49; occupancy final 0.13
- tracks: 156; persistent (alive >= 50% of run): 29; longest 401 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 8.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 31], H1 [0, 0, 0]
- motion: 82 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 27.3
- replication (lineage window K = 20 frames = time 60, default): splits 38, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 32, merge/split ratio 0.842, nucleations 0
- channel total drift (end/start - 1): [-0.5678, 0.1766, -186.8676, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 202: holes 0, rim-vs-core 0.67, rim-vs-outside 0.33, heterogeneity 0.17; core [0.805, 0.096, 0.058, 0.624] rim [0.429, 0.332, 0.257, 0.166]
  - track 5 at frame 202: holes 0, rim-vs-core 0.63, rim-vs-outside 0.32, heterogeneity 0.16; core [0.784, 0.094, 0.068, 0.591] rim [0.432, 0.32, 0.255, 0.166]
  - track 17 at frame 202: holes 0, rim-vs-core 0.69, rim-vs-outside 0.31, heterogeneity 0.18; core [0.803, 0.105, 0.06, 0.634] rim [0.416, 0.328, 0.264, 0.153]
  - track 118 at frame 323: holes 0, rim-vs-core 0.73, rim-vs-outside 0.34, heterogeneity 0.19; core [0.838, 0.102, 0.051, 0.706] rim [0.439, 0.32, 0.252, 0.174]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 214 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.737, rim/outside 15.9 (aggregate of 214 individuals; 1/214 membrane-like individually; rim level 0.677)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.1, rim/outside 0.783 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.474)
  - radial vorticity (signed): peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 1 (aggregate of 214 individuals; 0/214 membrane-like individually; rim level 0.488)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 27.3 (aggregate of 214 individuals; 2/214 membrane-like individually; rim level 0.513)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=606, R_eq 5.2): none; #5 (t=606, R_eq 5.35): none; #17 (t=606, R_eq 4.92): none; #118 (t=969, R_eq 4.55): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 214 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
