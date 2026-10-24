# Evidence pack: eco-MIRd-Rplus (seed 0)

- world: `../../../worlds/eco-MIRd-Rplus/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: two species (separate channel sets and rules) sharing one food field with space exclusion
- run: 301 frames x 10 steps x dt 0.1 = time 300; grid [160, 160]; wall 99s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/eco-MIRd-Rplus/world.py --out threads/lenia-multichannel/packs/eco-MIRd-Rplus --seeds 0 1 2 --frames 300`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 86, mean 71.6, max 97; occupancy final 0.26
- tracks: 2000; persistent (alive >= 50% of run): 7; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.57 (1 = constant size)
- enclosures: components with a hole mean 2.83, final 1; holes at thresholds 0.2/0.35/0.5 final [8, 1, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [151, 106, 62], H1 [24, 5, 1]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.454/time; max body lengths 2.5
- replication: splits 480, persistent splits 10, max generation 2, merges 468, nucleations 573
- channel total drift (end/start - 1): [4.1067, 3.3027, 2.9697, 6.0074, 4.6053, 5.6058, -0.8575]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 89 at frame 161: holes 0, rim-vs-core 0.45, rim-vs-outside 1.09, heterogeneity 0.14; core [0.0, 0.0, 0.0, 1.0, 0.736, 1.0, 0.347] rim [0.0, 0.0, 0.0, 0.831, 1.0, 0.677, 0.344]
  - track 187 at frame 166: holes 0, rim-vs-core 0.08, rim-vs-outside 1.26, heterogeneity 0.11; core [0.0, 0.0, 0.0, 0.956, 0.978, 0.729, 0.364] rim [0.0, 0.0, 0.0, 0.875, 1.0, 0.743, 0.359]
  - track 444 at frame 179: holes 0, rim-vs-core 0.26, rim-vs-outside 1.29, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.777, 1.0, 0.393] rim [0.0, 0.0, 0.0, 0.891, 1.0, 0.938, 0.386]
  - track 1358 at frame 245: holes 0, rim-vs-core 0.34, rim-vs-outside 0.73, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.0, 0.348, 0.442] rim [0.0, 0.0, 0.0, 0.724, 0.0, 0.143, 0.442]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
