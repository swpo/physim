# Evidence pack: active-nematic-rodsource (seed 0)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5
- run: 121 frames x 100 steps x dt 0.05 = time 600; grid [192, 192]; wall 538s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0200-c34-rodsource/world.py --out collective/contrib/20261026T0200-c34-rodsource/res15 --seeds 0 --size 192 192 --frames 120 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8238, 0.6126], min area 6 px

## Measurements
- components: final 25, mean 15.2, max 25; occupancy final 0.06
- tracks: 60; persistent (alive >= 50% of run): 8; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 25, 24], H1 [0, 0, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.119/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 100, default): splits 24, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.167, nucleations 8
- channel total drift (end/start - 1): [-0.5023, -0.4583, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 75: holes 0, rim-vs-core 0.43, rim-vs-outside 0.23, heterogeneity 0.15; core [0.908, 0.737, 0.423] rim [0.72, 0.505, 0.732]
  - track 6 at frame 55: holes 0, rim-vs-core 0.51, rim-vs-outside 0.24, heterogeneity 0.17; core [0.913, 0.788, 0.421] rim [0.697, 0.504, 0.781]
  - track 20 at frame 85: holes 0, rim-vs-core 0.31, rim-vs-outside 0.36, heterogeneity 0.17; core [0.895, 0.812, 0.484] rim [0.762, 0.643, 0.701]
  - track 44 at frame 109: holes 0, rim-vs-core 0.50, rim-vs-outside 0.27, heterogeneity 0.17; core [0.917, 0.858, 0.45] rim [0.707, 0.578, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 104 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.61 (aggregate of 104 individuals; 1/104 membrane-like individually; rim level 0.738)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.746, rim/outside 7.8 (aggregate of 104 individuals; 2/104 membrane-like individually; rim level 0.61)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 3.02 (aggregate of 104 individuals; 73/104 membrane-like individually; rim level 0.561)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=375, R_eq 4.18): ['surfactant s']; #6 (t=275, R_eq 4.18): ['surfactant s']; #20 (t=425, R_eq 5.23): ['surfactant s']; #44 (t=545, R_eq 5.92): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 104 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
