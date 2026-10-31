# Evidence pack: fed-vortices-noise (seed 1)

- world: `../../fv_noise.py`, family `fed-vortex`
- parent: collective/contrib/20261027T0712-c53-fed-vortex-claim; mutation: dynamics noise sd 0.02 per sqrt(t): additive on ['om'], proportional on ['Y']
- run: 401 frames x 150 steps x dt 0.02 = time 1200; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/fv_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/packs/B0.02_s1 --seeds 1 --frames 400 --spf 150 --no-movie`
- segmentation: matter > 0.26 of robust range [0.0004, 0.226], min area 6 px

## Measurements
- components: final 38, mean 39.7, max 61; occupancy final 0.18
- tracks: 1045; persistent (alive >= 50% of run): 2; longest 225 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.71 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [50, 42, 38], H1 [0, 0, 0]
- motion: 184 long-lived tracks moved >= 1 body length; max speed 0.583/time; max body lengths 18.0
- replication (lineage window K = 20 frames = time 60, default): splits 340, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 6, merges 284, merge/split ratio 0.835, nucleations 30
- channel total drift (end/start - 1): [-0.231, 0.0553, -449.9934, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 194 at frame 145: holes 0, rim-vs-core 0.64, rim-vs-outside 0.36, heterogeneity 0.18; core [0.793, 0.101, 0.06, 0.634] rim [0.434, 0.252, 0.242, 0.166]
  - track 46 at frame 104: holes 0, rim-vs-core 0.60, rim-vs-outside 0.31, heterogeneity 0.18; core [0.724, 0.12, 0.886, 0.518] rim [0.374, 0.332, 0.695, 0.124]
  - track 40 at frame 101: holes 0, rim-vs-core 0.47, rim-vs-outside 0.33, heterogeneity 0.15; core [0.688, 0.158, 0.868, 0.476] rim [0.42, 0.324, 0.721, 0.166]
  - track 978 at frame 383: holes 0, rim-vs-core 0.60, rim-vs-outside 0.28, heterogeneity 0.19; core [0.726, 0.167, 0.092, 0.56] rim [0.387, 0.355, 0.268, 0.131]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 237 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.718, rim/outside 4.56 (aggregate of 237 individuals; 2/237 membrane-like individually; rim level 0.543)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 5.33, rim/outside 0.8 (aggregate of 237 individuals; 0/237 membrane-like individually; rim level 0.476)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 0.994 (aggregate of 237 individuals; 0/237 membrane-like individually; rim level 0.482)
  - radial eating: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.6, rim/outside 11.7 (aggregate of 237 individuals; 12/237 membrane-like individually; rim level 0.332)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #194 (t=435, R_eq 3.66): none; #46 (t=312, R_eq 5.44): none; #40 (t=303, R_eq 4.69): none; #978 (t=1149, R_eq 4.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 237 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
