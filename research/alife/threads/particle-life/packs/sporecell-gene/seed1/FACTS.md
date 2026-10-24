# Evidence pack: sporecell-gene (seed 1)

- world: `../../../worlds/sporecell-gene/world.py`, family `particle`
- parent: sporecell; mutation: no long-range shell (R2=1, turnover); core comes in two heritable kinds copied through catalysis with mutation mu; weak cross-kind adhesion; kind 1 less self-adhesive
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 202s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell-gene/world.py --out threads/particle-life/packs/sporecell-gene --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.7282], min area 6 px

## Measurements
- components: final 4, mean 3.2, max 6; occupancy final 0.01
- tracks: 78; persistent (alive >= 50% of run): 1; longest 142 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.95 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 5, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.302/time; max body lengths 2.4
- replication: splits 0, persistent splits 0, max generation 0, merges 1, nucleations 77
- channel total drift (end/start - 1): [-0.8593, 91.2, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 129: holes 0, rim-vs-core 0.20, rim-vs-outside 0.38, heterogeneity 0.16; core [0.0, 0.455, 0.0, 0.887] rim [0.0, 0.615, 0.0, 0.762]
  - track 8 at frame 96: holes 0, rim-vs-core 0.30, rim-vs-outside 0.24, heterogeneity 0.17; core [0.049, 0.929, 0.0, 0.435] rim [0.01, 0.642, 0.0, 0.528]
  - track 39 at frame 155: holes 0, rim-vs-core 0.09, rim-vs-outside 0.24, heterogeneity 0.05; core [0.023, 1.0, 0.0, 0.067] rim [0.035, 0.918, 0.0, 0.112]
  - track 17 at frame 108: holes 0, rim-vs-core 0.06, rim-vs-outside 0.22, heterogeneity 0.03; core [0.025, 1.0, 0.0, 0.032] rim [0.035, 0.945, 0.0, 0.055]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
