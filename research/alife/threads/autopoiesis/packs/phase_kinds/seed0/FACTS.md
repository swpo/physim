# Evidence pack: phase-kinds (seed 0)

- world: `../../../worlds/phase_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: two catalyst kinds (fast/selfish vs link-making) with stochastic point mutation K1->K2; parent: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 45s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds/world.py --out threads/autopoiesis/packs/phase_kinds --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.6294], min area 6 px

## Measurements
- components: final 23, mean 29.6, max 45; occupancy final 0.22
- tracks: 257; persistent (alive >= 50% of run): 7; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.92 (1 = constant size)
- enclosures: components with a hole mean 1.22, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 10]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [18, 13, 1]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.00634/time; max body lengths 2.3
- replication: splits 125, persistent splits 47, max generation 6, merges 1, nucleations 0
- channel total drift (end/start - 1): [-0.3806, -1.0, None, 5.9875, 4.7859]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 85: holes 0, rim-vs-core 0.44, rim-vs-outside 1.06, heterogeneity 0.14; core [0.115, 0.929, 0.0, 0.79, 0.596] rim [0.29, 0.556, 0.0, 0.74, 0.742]
  - track 26 at frame 65: holes 0, rim-vs-core 0.27, rim-vs-outside 1.12, heterogeneity 0.14; core [0.132, 0.933, 0.0, 0.819, 0.669] rim [0.229, 0.691, 0.0, 0.759, 0.662]
  - track 59 at frame 77: holes 0, rim-vs-core 0.45, rim-vs-outside 1.07, heterogeneity 0.14; core [0.121, 0.959, 0.0, 0.837, 0.606] rim [0.284, 0.578, 0.0, 0.758, 0.754]
  - track 232 at frame 153: holes 0, rim-vs-core 0.38, rim-vs-outside 1.05, heterogeneity 0.14; core [0.057, 0.0, 0.857, 0.714, 0.675] rim [0.257, 0.0, 0.54, 0.767, 0.679]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
