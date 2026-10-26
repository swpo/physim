# Evidence pack: active-nematic-rodsource (seed 4)

- world: `../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5
- run: 201 frames x 200 steps x dt 0.025 (--dt; world META dt 0.05) = time 1000; grid [128, 128]; wall 557s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0305-c32-review-rodsource/world.py --out collective/contrib/20261026T0305-c32-review-rodsource/pack4_dthalf --seeds 4 --spf 200 --dt 0.025 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8296, 0.6326], min area 6 px

## Measurements
- components: final 31, mean 23.3, max 32; occupancy final 0.07
- tracks: 109; persistent (alive >= 50% of run): 12; longest 163 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 31, 30], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.107/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 16, merge/split ratio 0.39, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.3602, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 119: holes 0, rim-vs-core 0.52, rim-vs-outside 0.35, heterogeneity 0.17; core [0.949, 0.904, 0.281] rim [0.741, 0.603, 0.654]
  - track 28 at frame 119: holes 0, rim-vs-core 0.54, rim-vs-outside 0.32, heterogeneity 0.17; core [0.942, 0.807, 0.327] rim [0.739, 0.539, 0.745]
  - track 36 at frame 129: holes 0, rim-vs-core 0.46, rim-vs-outside 0.34, heterogeneity 0.14; core [0.951, 0.832, 0.276] rim [0.768, 0.584, 0.613]
  - track 66 at frame 166: holes 0, rim-vs-core 0.53, rim-vs-outside 0.37, heterogeneity 0.17; core [0.957, 0.933, 0.277] rim [0.761, 0.647, 0.683]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 159 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 4.91 (aggregate of 159 individuals; 0/159 membrane-like individually; rim level 0.77)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.75, rim/outside 8.66 (aggregate of 159 individuals; 0/159 membrane-like individually; rim level 0.651)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.86, rim/outside 2.96 (aggregate of 159 individuals; 132/159 membrane-like individually; rim level 0.574)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #27 (t=595, R_eq 3.04): ['surfactant s']; #28 (t=595, R_eq 2.71): ['surfactant s']; #36 (t=645, R_eq 2.65): ['surfactant s']; #66 (t=830, R_eq 3.04): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.025 only relabels time (world META dt 0.05): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
