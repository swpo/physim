# Evidence pack: wavepin-crawler-synth (seed 9)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: polarity protein made in the cytosol from a resource S (ksyn S) and degraded (kdeg): protein total no longer fixed
- run: 121 frames x 200 steps x dt 0.001 = time 24; grid [256, 256]; wall 314s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27l/world.py --out collective/contrib/wip-c27l/pack_percell --seeds 9 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.10
- tracks: 1; persistent (alive >= 50% of run): 1; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.54 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 13.8/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.1414, -0.3703, -0.3685, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.14, rim-vs-outside 1.15, heterogeneity 0.22; core [1.0, 0.623, 0.627, 0.0] rim [0.937, 0.554, 0.523, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.8, rim/outside 48.8 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.478)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside)
- membrane-like channels per top track at mid-life: #0 (t=12.2, R_eq 42.18): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
