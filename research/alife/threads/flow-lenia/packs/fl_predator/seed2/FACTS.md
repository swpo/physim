# Evidence pack: fl_predator (seed 2)

- world: `../../../worlds/fl_predator/world.py`, family `flow-lenia`
- parent: flow-lenia/fl_forager (prey and predator both use glider rule C2_r202); mutation: two glider species with their own rules; predator matter converts prey matter it overlaps (mass-conserving), is drawn up a blurred prey field and decays to food; prey eat food
- run: 301 frames x 40 steps x dt 0.2 = time 2400; grid [128, 128]; wall 259s; status ok
- command: `python -m labkit.run threads/flow-lenia/worlds/fl_predator/world.py --out threads/flow-lenia/packs/fl_predator/seed2 --frames 300 --seeds 2`
- segmentation: matter > 0.07 of robust range [0.0, 2.0316], min area 6 px

## Measurements
- components: final 9, mean 9.2, max 15; occupancy final 0.05
- tracks: 385; persistent (alive >= 50% of run): 0; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.24, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 9, 7], H1 [3, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.331/time; max body lengths 10.9
- replication: splits 106, persistent splits 0, max generation 0, merges 76, nucleations 102
- channel total drift (end/start - 1): [0.2235, -0.5026, 0.0514]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 305 at frame 262: holes 0, rim-vs-core 0.51, rim-vs-outside 0.09, heterogeneity 0.14; core [0.581, 0.005, 0.015] rim [0.069, 0.004, 0.06]
  - track 265 at frame 204: holes 0, rim-vs-core 0.59, rim-vs-outside 0.06, heterogeneity 0.13; core [0.636, 0.006, 0.05] rim [0.048, 0.004, 0.114]
  - track 332 at frame 277: holes 0, rim-vs-core 0.58, rim-vs-outside 0.10, heterogeneity 0.13; core [0.67, 0.0, 0.046] rim [0.09, 0.0, 0.103]
  - track 243 at frame 179: holes 0, rim-vs-core 0.52, rim-vs-outside 0.15, heterogeneity 0.15; core [0.665, 0.053, 0.117] rim [0.147, 0.054, 0.158]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
