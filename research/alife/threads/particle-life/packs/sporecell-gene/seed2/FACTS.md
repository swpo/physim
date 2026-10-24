# Evidence pack: sporecell-gene (seed 2)

- world: `../../../worlds/sporecell-gene/world.py`, family `particle`
- parent: sporecell; mutation: no long-range shell (R2=1, turnover); core comes in two heritable kinds copied through catalysis with mutation mu; weak cross-kind adhesion; kind 1 less self-adhesive
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 206s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell-gene/world.py --out threads/particle-life/packs/sporecell-gene --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 7.3622], min area 6 px

## Measurements
- components: final 5, mean 3.4, max 6; occupancy final 0.02
- tracks: 44; persistent (alive >= 50% of run): 1; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.91 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 4], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.144/time; max body lengths 1.4
- replication: splits 0, persistent splits 0, max generation 0, merges 1, nucleations 43
- channel total drift (end/start - 1): [-0.8566, 66.36, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 119: holes 0, rim-vs-core 0.28, rim-vs-outside 0.32, heterogeneity 0.19; core [0.0, 0.689, 0.0, 0.822] rim [0.0, 0.455, 0.0, 0.666]
  - track 27 at frame 168: holes 0, rim-vs-core 0.23, rim-vs-outside 0.27, heterogeneity 0.10; core [0.002, 0.966, 0.0, 0.139] rim [0.008, 0.767, 0.0, 0.25]
  - track 5 at frame 72: holes 0, rim-vs-core 0.34, rim-vs-outside 0.18, heterogeneity 0.19; core [0.033, 0.807, 0.0, 0.644] rim [0.006, 0.466, 0.0, 0.65]
  - track 28 at frame 163: holes 0, rim-vs-core 0.13, rim-vs-outside 0.26, heterogeneity 0.15; core [0.0, 0.782, 0.0, 0.499] rim [0.0, 0.711, 0.0, 0.396]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
