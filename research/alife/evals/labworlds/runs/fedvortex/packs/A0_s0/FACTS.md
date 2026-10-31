# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['om', 'Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 131s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/A0_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2058], min area 6 px

## Measurements
- components: final 28, mean 33.2, max 50; occupancy final 0.14
- tracks: 119; persistent (alive >= 50% of run): 28; longest 401 frames; alive start-to-end: 11
- size of persistent tracks: max/min area ratio 7.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 28], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.224/time; max body lengths 17.0
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 3, merges 26, merge/split ratio 1.18, nucleations 0
- channel total drift (end/start - 1): [-0.5674, 0.1659, -1210.0148, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 202: holes 0, rim-vs-core 0.81, rim-vs-outside 0.29, heterogeneity 0.21; core [0.823, 0.147, 0.064, 0.746] rim [0.382, 0.322, 0.283, 0.122]
  - track 13 at frame 202: holes 0, rim-vs-core 0.65, rim-vs-outside 0.33, heterogeneity 0.17; core [0.799, 0.103, 0.913, 0.63] rim [0.438, 0.321, 0.723, 0.174]
  - track 18 at frame 202: holes 0, rim-vs-core 0.72, rim-vs-outside 0.31, heterogeneity 0.19; core [0.814, 0.119, 0.061, 0.687] rim [0.422, 0.31, 0.262, 0.151]
  - track 114 at frame 373: holes 0, rim-vs-core 0.49, rim-vs-outside 0.46, heterogeneity 0.17; core [0.778, 0.095, 0.075, 0.589] rim [0.498, 0.298, 0.222, 0.276]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 18.2 (aggregate of 189 individuals; 1/189 membrane-like individually; rim level 0.691)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.775 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.485)
  - radial vorticity (signed): peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.99 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.482)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.72, rim/outside 30.3 (aggregate of 189 individuals; 5/189 membrane-like individually; rim level 0.54)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=606, R_eq 3.74): none; #13 (t=606, R_eq 5.11): none; #18 (t=606, R_eq 4.48): none; #114 (t=1119, R_eq 5.64): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 189 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
