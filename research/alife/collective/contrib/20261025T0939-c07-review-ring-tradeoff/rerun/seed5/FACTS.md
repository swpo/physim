# Evidence pack: phase-slipdiv (seed 5)

- world: `../../../20261025T0724-c05-ring-motility-tradeoff/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swimdiv; mutation: label-free local phoretic slip (Gaussian-averaged grad S, MUSCL advection) + phase_membrane link ring (chi=1.5), from noise
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 128s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0724-c05-ring-motility-tradeoff/world.py --out collective/contrib/_c07rev12/rerun/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6792], min area 6 px

## Measurements
- components: final 17, mean 12.3, max 18; occupancy final 0.13
- tracks: 110; persistent (alive >= 50% of run): 8; longest 167 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.31 (1 = constant size)
- enclosures: components with a hole mean 0.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [2, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.121/time; max body lengths 54.7
- replication (lineage window K = 20 frames = time 1000, default): splits 39, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 3, merges 9, merge/split ratio 0.231, nucleations 0
- channel total drift (end/start - 1): [-0.2924, -0.8498, -0.1315, -0.6395]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 52 at frame 118: holes 0, rim-vs-core 0.49, rim-vs-outside 0.48, heterogeneity 0.21; core [0.207, 0.584, 0.611, 0.729] rim [0.424, 0.238, 0.372, 0.585]
  - track 84 at frame 143: holes 0, rim-vs-core 0.55, rim-vs-outside 0.45, heterogeneity 0.22; core [0.218, 0.616, 0.645, 0.767] rim [0.368, 0.233, 0.339, 0.556]
  - track 86 at frame 143: holes 0, rim-vs-core 0.54, rim-vs-outside 0.46, heterogeneity 0.19; core [0.243, 0.591, 0.668, 0.808] rim [0.417, 0.237, 0.38, 0.572]
  - track 98 at frame 158: holes 0, rim-vs-core 0.49, rim-vs-outside 0.49, heterogeneity 0.21; core [0.229, 0.596, 0.642, 0.755] rim [0.418, 0.257, 0.392, 0.599]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 5.42, rim/outside 0.84 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.575)
  - radial K catalyst: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 15.2 (aggregate of 76 individuals; 6/76 membrane-like individually; rim level 0.589)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 7.26 (aggregate of 76 individuals; 12/76 membrane-like individually; rim level 0.639)
  - radial membrane (wall): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 20.2 (aggregate of 76 individuals; 3/76 membrane-like individually; rim level 0.695)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #52 (t=5900, R_eq 6): none; #84 (t=7150, R_eq 5.92): none; #86 (t=7150, R_eq 4.82): none; #98 (t=7900, R_eq 5.32): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
