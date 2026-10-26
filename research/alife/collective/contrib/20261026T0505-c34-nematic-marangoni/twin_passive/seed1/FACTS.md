# Evidence pack: active-nematic-marangoni (seed 1)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 397s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0505-c34-nematic-marangoni/twin_passive --seeds 0 1 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.8154, 0.937], min area 6 px

## Measurements
- components: final 3, mean 2.8, max 3; occupancy final 0.02
- tracks: 3; persistent (alive >= 50% of run): 3; longest 193 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 100, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 3
- channel total drift (end/start - 1): [-0.4928, -0.6689, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 104: holes 0, rim-vs-core 0.95, rim-vs-outside 0.62, heterogeneity 0.30; core [0.986, 0.973, 0.087, 0.626] rim [0.72, 0.612, 0.701, 0.054]
  - track 1 at frame 108: holes 0, rim-vs-core 0.96, rim-vs-outside 0.61, heterogeneity 0.30; core [0.981, 0.966, 0.084, 0.603] rim [0.711, 0.602, 0.727, 0.051]
  - track 2 at frame 109: holes 0, rim-vs-core 0.86, rim-vs-outside 0.60, heterogeneity 0.29; core [0.98, 0.966, 0.072, 0.615] rim [0.707, 0.599, 0.562, 0.081]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.938, rim/outside 44.3 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.938)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 61.1 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.885)
  - radial surfactant s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 9.8, rim/outside 18.9 (aggregate of 18 individuals; 18/18 membrane-like individually; rim level 0.824)  MEMBRANE-LIKE
  - radial cargo c: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.38, rim/outside 27.4 (aggregate of 18 individuals; 9/18 membrane-like individually; rim level 0.821)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #0 (t=520, R_eq 6.15): ['surfactant s']; #1 (t=540, R_eq 6.18): ['surfactant s']; #2 (t=545, R_eq 6.53): ['surfactant s', 'cargo c']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
