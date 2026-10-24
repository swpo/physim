# Evidence pack: ad5n-neutral (seed 0)

- world: `../../../worlds/ad5n-neutral/world.py`, family `phase-field`
- parent: ad5-evolve; mutation: neutral control: all four alleles have the same catalytic rate k=0.13
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 274s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad5n-neutral/world.py --out threads/active-droplets/packs/ad5n-neutral --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [-1.0641, 1.4272], min area 6 px

## Measurements
- components: final 9, mean 8.4, max 9; occupancy final 0.12
- tracks: 14; persistent (alive >= 50% of run): 9; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.63 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0015/time; max body lengths 2.0
- replication: splits 5, persistent splits 4, max generation 2, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.0825, -0.5594, 1.0299, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 103: holes 0, rim-vs-core 0.43, rim-vs-outside 0.78, heterogeneity 0.08; core [0.969, 0.056, 0.043, 0.0, 0.0, 0.988] rim [0.691, 0.121, 0.03, 0.0, 0.0, 0.674]
  - track 5 at frame 103: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.08; core [0.961, 0.046, 0.927, 0.0, 0.0, 0.0] rim [0.608, 0.135, 0.509, 0.0, 0.0, 0.0]
  - track 7 at frame 104: holes 0, rim-vs-core 0.36, rim-vs-outside 0.97, heterogeneity 0.07; core [0.961, 0.046, 0.0, 1.0, 1.0, 0.0] rim [0.628, 0.142, 0.0, 0.898, 0.983, 0.0]
  - track 12 at frame 121: holes 0, rim-vs-core 0.54, rim-vs-outside 0.63, heterogeneity 0.08; core [0.957, 0.039, 0.936, 0.0, 0.0, 0.0] rim [0.62, 0.134, 0.525, 0.0, 0.0, 0.0]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
