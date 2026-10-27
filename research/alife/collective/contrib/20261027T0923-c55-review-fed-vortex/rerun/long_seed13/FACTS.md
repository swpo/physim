# Evidence pack: fed-vortices (seed 13)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 2001 frames x 150 steps x dt 0.02 = time 6000; grid [128, 128]; wall 645s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vort/long13 --seeds 13 --frames 2000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2052], min area 6 px

## Measurements
- components: final 28, mean 30.1, max 49; occupancy final 0.14
- tracks: 648; persistent (alive >= 50% of run): 2; longest 1661 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 32, 28], H1 [0, 0, 0]
- motion: 360 long-lived tracks moved >= 1 body length; max speed 0.603/time; max body lengths 75.6
- replication (lineage window K = 20 frames = time 60, default): splits 204, persistent splits 92 (0 more failed only because the siblings re-merged within K), max generation 19, merges 193, merge/split ratio 0.946, nucleations 0
- channel total drift (end/start - 1): [-0.5377, 0.1616, 14748.332, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 121 at frame 1109: holes 0, rim-vs-core 0.78, rim-vs-outside 0.32, heterogeneity 0.20; core [0.838, 0.112, 0.929, 0.728] rim [0.412, 0.326, 0.707, 0.148]
  - track 239 at frame 1311: holes 0, rim-vs-core 0.81, rim-vs-outside 0.34, heterogeneity 0.21; core [0.856, 0.117, 0.936, 0.793] rim [0.431, 0.323, 0.718, 0.172]
  - track 18 at frame 471: holes 0, rim-vs-core 0.45, rim-vs-outside 0.57, heterogeneity 0.15; core [0.773, 0.045, 0.899, 0.539] rim [0.518, 0.29, 0.764, 0.288]
  - track 614 at frame 1966: holes 0, rim-vs-core 0.50, rim-vs-outside 0.42, heterogeneity 0.16; core [0.766, 0.117, 0.078, 0.597] rim [0.483, 0.226, 0.228, 0.227]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 175 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 16.1 (aggregate of 175 individuals; 1/175 membrane-like individually; rim level 0.672)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11, rim/outside 0.768 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.476)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 175 individuals; 0/175 membrane-like individually; rim level 0.493)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.717, rim/outside 26.1 (aggregate of 175 individuals; 7/175 membrane-like individually; rim level 0.508)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #121 (t=3327, R_eq 4.55): none; #239 (t=3933, R_eq 4.15): none; #18 (t=1413, R_eq 6.53): ['eating']; #614 (t=5898, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 175 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
