# Evidence pack: active-nematic-marangoni (seed 0)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 374s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/twin_passive --seeds 0 1 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8419, 0.9472], min area 6 px

## Measurements
- components: final 9, mean 8.2, max 9; occupancy final 0.07
- tracks: 9; persistent (alive >= 50% of run): 9; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 9], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 9
- channel total drift (end/start - 1): [-0.5044, -0.1153, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.78, rim-vs-outside 0.32, heterogeneity 0.25; core [0.916, 0.854, 0.092, 0.263] rim [0.61, 0.47, 0.644, 0.001]
  - track 1 at frame 108: holes 0, rim-vs-core 0.87, rim-vs-outside 0.31, heterogeneity 0.29; core [0.9, 0.823, 0.35, 0.282] rim [0.58, 0.435, 1.0, 0.0]
  - track 2 at frame 108: holes 0, rim-vs-core 0.66, rim-vs-outside 0.58, heterogeneity 0.23; core [0.965, 0.933, 0.034, 0.343] rim [0.69, 0.56, 0.35, 0.003]
  - track 3 at frame 109: holes 0, rim-vs-core 0.75, rim-vs-outside 0.31, heterogeneity 0.25; core [0.912, 0.842, 0.094, 0.314] rim [0.618, 0.473, 0.586, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 54 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 29.8 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.894)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 54.4 (aggregate of 54 individuals; 0/54 membrane-like individually; rim level 0.788)
  - radial surfactant s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 10.5, rim/outside 16.3 (aggregate of 54 individuals; 54/54 membrane-like individually; rim level 0.603)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.11, rim/outside 44.4 (aggregate of 54 individuals; 40/54 membrane-like individually; rim level 0.527)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s, cargo c
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 6): ['surfactant s', 'cargo c']; #1 (t=540, R_eq 5.47): ['surfactant s', 'cargo c']; #2 (t=540, R_eq 6.23): ['surfactant s', 'cargo c']; #3 (t=545, R_eq 5.47): ['surfactant s', 'cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
