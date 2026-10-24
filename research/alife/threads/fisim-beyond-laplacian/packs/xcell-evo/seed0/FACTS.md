# Evidence pack: xcell-evo (seed 0)

- world: `../../../worlds/xcell-evo/world.py`, family `fisim-extended-rd`
- parent: xcell-her-noise0.3 (+ resource/maintenance idea from the lenia-multichannel and autopoiesis threads); mutation: xcell-her + additive activator noise 0.3 (marker loss at unequal division = in-run variation) + a membrane-trapped waste q (tau=40, D=2, K=0.15) as a maintenance cost that gives continual death and birth. The marker changes waste production by W[q,h]=-0.5. Selection: h-on cells make half the waste (a private maintenance benefit).
- run: 201 frames x 200 steps x dt 0.02 = time 800; grid [160, 160]; wall 550s; status ok
- command: `python -m labkit.run threads/fisim-beyond-laplacian/worlds/xcell-evo/world.py --out threads/fisim-beyond-laplacian/packs/xcell-evo --seeds 0 1 2 --frames 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.9438], min area 6 px

## Measurements
- components: final 24, mean 20.8, max 24; occupancy final 0.16
- tracks: 35; persistent (alive >= 50% of run): 22; longest 201 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 21.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.198/time; max body lengths 6.8
- replication: splits 11, persistent splits 11, max generation 3, merges 0, nucleations 3
- channel total drift (end/start - 1): [0.4288, None, 0.7131, -0.427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.32, rim-vs-outside 0.72, heterogeneity 0.22; core [0.893, 0.657, 0.76, 0.42] rim [0.702, 0.76, 0.543, 0.329]
  - track 6 at frame 101: holes 0, rim-vs-core 0.54, rim-vs-outside 0.49, heterogeneity 0.16; core [0.917, 0.617, 0.095, 0.823] rim [0.567, 0.899, 0.059, 0.526]
  - track 7 at frame 101: holes 0, rim-vs-core 0.45, rim-vs-outside 0.60, heterogeneity 0.16; core [0.932, 0.59, 0.095, 0.839] rim [0.644, 0.854, 0.07, 0.624]
  - track 33 at frame 185: holes 0, rim-vs-core 0.49, rim-vs-outside 0.61, heterogeneity 0.16; core [0.925, 0.563, 0.093, 0.859] rim [0.638, 0.85, 0.064, 0.588]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
