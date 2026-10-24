# Evidence pack: mcf-MIRd-norefill (seed 2)

- world: `../../../worlds/mcf-MIRd-norefill/world.py`, family `lenia`
- parent: mcf-MIRd; mutation: ABLATION of mcf-MIRd: food does not regrow (rho=0)
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [192, 192]; wall 77s; status ok
- command: `python -m labkit.run threads/lenia-multichannel/worlds/mcf-MIRd-norefill/world.py --out threads/lenia-multichannel/packs/mcf-MIRd-norefill --seeds 0 1 2 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 2.2, max 10; occupancy final 0.00
- tracks: 142; persistent (alive >= 50% of run): 0; longest 48 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.9
- replication: splits 47, persistent splits 1, max generation 1, merges 17, nucleations 27
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, -0.4842]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 64: holes 0, rim-vs-core 0.20, rim-vs-outside 0.82, heterogeneity 0.25; core [1.0, 0.722, 0.174, 0.167] rim [0.832, 0.645, 0.111, 0.198]
  - track 37 at frame 97: holes 0, rim-vs-core 0.22, rim-vs-outside 0.92, heterogeneity 0.22; core [0.989, 0.913, 0.122, 0.076] rim [0.834, 0.881, 0.275, 0.119]
  - track 13 at frame 47: holes 0, rim-vs-core 0.37, rim-vs-outside 0.75, heterogeneity 0.22; core [0.888, 0.021, 0.01, 0.018] rim [0.812, 0.355, 0.142, 0.03]
  - track 20 at frame 67: holes 0, rim-vs-core 0.17, rim-vs-outside 0.86, heterogeneity 0.26; core [1.0, 0.548, 0.161, 0.095] rim [0.859, 0.526, 0.071, 0.137]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
