# Evidence pack: phase-slipdiv (seed 3)

- world: `../../20261025T0724-c05-ring-motility-tradeoff/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_swimdiv; mutation: label-free local phoretic slip (Gaussian-averaged grad S, MUSCL advection) + phase_membrane link ring (chi=1.5), from noise
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 74s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0724-c05-ring-motility-tradeoff/world.py --out collective/contrib/20261025T0938-c01-review-ring-motility/rerun --seeds 3 --frames 160 --spf 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.6416], min area 6 px

## Measurements
- components: final 20, mean 18.3, max 23; occupancy final 0.20
- tracks: 163; persistent (alive >= 50% of run): 3; longest 139 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 30.58 (1 = constant size)
- enclosures: components with a hole mean 0.98, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 21, 21], H1 [13, 3, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.0486/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 1000, default): splits 61, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 2, merges 19, merge/split ratio 0.311, nucleations 0
- channel total drift (end/start - 1): [-0.3498, -0.7939, -0.0455, -0.397]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 70: holes 0, rim-vs-core 0.61, rim-vs-outside 0.47, heterogeneity 0.22; core [0.257, 0.686, 0.716, 0.762] rim [0.452, 0.253, 0.388, 0.562]
  - track 66 at frame 89: holes 0, rim-vs-core 0.51, rim-vs-outside 0.80, heterogeneity 0.22; core [0.136, 0.813, 0.65, 0.483] rim [0.27, 0.422, 0.489, 0.738]
  - track 94 at frame 106: holes 0, rim-vs-core 0.54, rim-vs-outside 0.88, heterogeneity 0.21; core [0.133, 0.764, 0.635, 0.517] rim [0.369, 0.363, 0.512, 0.755]
  - track 106 at frame 121: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.16; core [0.257, 0.572, 0.711, 0.88] rim [0.354, 0.289, 0.484, 0.465]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 110 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial S: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 6.84, rim/outside 0.85 (aggregate of 110 individuals; 0/110 membrane-like individually; rim level 0.554)
  - radial K catalyst: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1, rim/outside 9.4 (aggregate of 110 individuals; 4/110 membrane-like individually; rim level 0.605)
  - radial L link: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 6.75 (aggregate of 110 individuals; 53/110 membrane-like individually; rim level 0.599)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 8.55 (aggregate of 110 individuals; 49/110 membrane-like individually; rim level 0.692)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=3500, R_eq 5.23): none; #66 (t=4450, R_eq 7.88): none; #94 (t=5300, R_eq 6.38): ['L link', 'membrane (wall)']; #106 (t=6050, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 110 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
