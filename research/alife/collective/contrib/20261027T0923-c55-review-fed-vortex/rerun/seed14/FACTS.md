# Evidence pack: fed-vortices (seed 14)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 322s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/vort/pack14 --seeds 14 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2039], min area 6 px

## Measurements
- components: final 25, mean 28.4, max 45; occupancy final 0.14
- tracks: 251; persistent (alive >= 50% of run): 13; longest 943 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 29, 27], H1 [0, 0, 0]
- motion: 141 long-lived tracks moved >= 1 body length; max speed 0.445/time; max body lengths 55.5
- replication (lineage window K = 20 frames = time 60, default): splits 71, persistent splits 45 (0 more failed only because the siblings re-merged within K), max generation 8, merges 65, merge/split ratio 0.915, nucleations 0
- channel total drift (end/start - 1): [-0.5628, 0.1767, 33.0499, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 67 at frame 496: holes 0, rim-vs-core 0.71, rim-vs-outside 0.31, heterogeneity 0.18; core [0.808, 0.101, 0.918, 0.641] rim [0.41, 0.332, 0.707, 0.143]
  - track 39 at frame 395: holes 0, rim-vs-core 0.82, rim-vs-outside 0.30, heterogeneity 0.21; core [0.839, 0.116, 0.929, 0.726] rim [0.392, 0.347, 0.697, 0.127]
  - track 16 at frame 387: holes 0, rim-vs-core 0.78, rim-vs-outside 0.31, heterogeneity 0.20; core [0.84, 0.111, 0.052, 0.732] rim [0.413, 0.326, 0.264, 0.148]
  - track 219 at frame 941: holes 0, rim-vs-core 0.77, rim-vs-outside 0.34, heterogeneity 0.20; core [0.846, 0.128, 0.933, 0.778] rim [0.447, 0.287, 0.727, 0.179]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 169 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.766, rim/outside 20.2 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.682)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.2, rim/outside 0.771 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.477)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.98, rim/outside 0.998 (aggregate of 169 individuals; 0/169 membrane-like individually; rim level 0.487)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.722, rim/outside 36 (aggregate of 169 individuals; 1/169 membrane-like individually; rim level 0.53)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #67 (t=1488, R_eq 5.44): none; #39 (t=1185, R_eq 4.75): none; #16 (t=1161, R_eq 4.55): none; #219 (t=2823, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 169 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
