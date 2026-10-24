# Evidence pack: mcf-mIRde (seed 0)

- world: `../../../worlds/mcf-mIRde/world.py`, family `lenia`
- parent: mc-mIRde; mutation: matter can only be built from a consumed, regrowing, diffusing food field F (yield 2): population limited by food supply
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [192, 192]; wall 72s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-mIRde/world.py --out threads/lenia-multichannel/packs/mcf-mIRde --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 2.466], min area 6 px

## Measurements
- components: final 0, mean 1.8, max 15; occupancy final 0.00
- tracks: 95; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.32, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.63/time; max body lengths 1.4
- replication: splits 30, persistent splits 0, max generation 0, merges 12, nucleations 18
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.0027]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.74, heterogeneity 0.31; core [0.483, 0.959, 0.262, 0.021] rim [0.688, 0.748, 0.324, 0.036]
  - track 13 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.59, heterogeneity 0.31; core [0.642, 0.936, 0.279, 0.014] rim [0.603, 0.643, 0.342, 0.055]
  - track 12 at frame 43: holes 0, rim-vs-core 0.30, rim-vs-outside 0.61, heterogeneity 0.31; core [0.642, 0.936, 0.279, 0.014] rim [0.603, 0.643, 0.342, 0.053]
  - track 9 at frame 30: holes 0, rim-vs-core 0.32, rim-vs-outside 0.75, heterogeneity 0.32; core [0.746, 0.904, 0.366, 0.02] rim [0.643, 0.646, 0.509, 0.078]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
