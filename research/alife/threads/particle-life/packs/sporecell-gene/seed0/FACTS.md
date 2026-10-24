# Evidence pack: sporecell-gene (seed 0)

- world: `../../../worlds/sporecell-gene/world.py`, family `particle`
- parent: sporecell; mutation: no long-range shell (R2=1, turnover); core comes in two heritable kinds copied through catalysis with mutation mu; weak cross-kind adhesion; kind 1 less self-adhesive
- run: 201 frames x 100 steps x dt 0.02 = time 400; grid [128, 128]; wall 136s; status ok
- command: `python -m labkit.run threads/particle-life/worlds/sporecell-gene/world.py --out threads/particle-life/packs/sporecell-gene --seeds 0 1 2 --frames 200 --spf 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 5.4626], min area 6 px

## Measurements
- components: final 10, mean 7.2, max 13; occupancy final 0.03
- tracks: 109; persistent (alive >= 50% of run): 2; longest 129 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 9], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.359/time; max body lengths 3.4
- replication: splits 0, persistent splits 0, max generation 0, merges 0, nucleations 109
- channel total drift (end/start - 1): [-0.864, 167.8, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 136: holes 0, rim-vs-core 0.38, rim-vs-outside 0.28, heterogeneity 0.07; core [0.001, 0.962, 0.0, 0.067] rim [0.004, 0.601, 0.0, 0.193]
  - track 41 at frame 146: holes 0, rim-vs-core 0.28, rim-vs-outside 0.22, heterogeneity 0.06; core [0.071, 0.906, 0.0, 0.014] rim [0.039, 0.625, 0.0, 0.045]
  - track 48 at frame 151: holes 0, rim-vs-core 0.29, rim-vs-outside 0.20, heterogeneity 0.10; core [0.0, 0.883, 0.0, 0.146] rim [0.0, 0.599, 0.0, 0.219]
  - track 51 at frame 156: holes 0, rim-vs-core 0.18, rim-vs-outside 0.21, heterogeneity 0.12; core [0.052, 0.77, 0.0, 0.143] rim [0.035, 0.615, 0.0, 0.227]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, particles.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
