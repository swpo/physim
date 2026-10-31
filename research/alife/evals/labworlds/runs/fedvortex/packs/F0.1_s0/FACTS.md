# Evidence pack: fed-vortices-noise (seed 0)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['Y'], proportional on []
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 151s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/F0.1_s0 --seeds 0 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2144], min area 6 px

## Measurements
- components: final 29, mean 34.4, max 49; occupancy final 0.13
- tracks: 126; persistent (alive >= 50% of run): 30; longest 401 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 15.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 28], H1 [0, 0, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.397/time; max body lengths 30.2
- replication (lineage window K = 20 frames = time 60, default): splits 26, persistent splits 10 (0 more failed only because the siblings re-merged within K), max generation 2, merges 25, merge/split ratio 0.962, nucleations 0
- channel total drift (end/start - 1): [-0.5905, 0.1909, -1828.3387, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 202: holes 0, rim-vs-core 0.67, rim-vs-outside 0.31, heterogeneity 0.18; core [0.803, 0.137, 0.056, 0.649] rim [0.432, 0.335, 0.251, 0.161]
  - track 2 at frame 202: holes 0, rim-vs-core 0.77, rim-vs-outside 0.31, heterogeneity 0.20; core [0.839, 0.135, 0.049, 0.736] rim [0.418, 0.308, 0.259, 0.147]
  - track 3 at frame 202: holes 0, rim-vs-core 0.68, rim-vs-outside 0.27, heterogeneity 0.19; core [0.764, 0.145, 0.898, 0.572] rim [0.365, 0.347, 0.684, 0.105]
  - track 66 at frame 239: holes 0, rim-vs-core 0.81, rim-vs-outside 0.28, heterogeneity 0.21; core [0.836, 0.139, 0.93, 0.728] rim [0.393, 0.317, 0.7, 0.12]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 198 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.753, rim/outside 18.5 (aggregate of 198 individuals; 1/198 membrane-like individually; rim level 0.669)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.18, rim/outside 0.786 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.454)
  - radial vorticity (signed): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.993 (aggregate of 198 individuals; 0/198 membrane-like individually; rim level 0.481)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 31.3 (aggregate of 198 individuals; 5/198 membrane-like individually; rim level 0.49)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=606, R_eq 4.37): none; #2 (t=606, R_eq 3.91): none; #3 (t=606, R_eq 4.72): none; #66 (t=717, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 198 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
