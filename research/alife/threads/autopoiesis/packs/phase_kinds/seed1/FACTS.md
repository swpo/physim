# Evidence pack: phase-kinds (seed 1)

- world: `../../../worlds/phase_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: two heritable catalyst kinds; mutant K2 replicates faster (c2=0.3 vs c1=0.2) with equal link output; stochastic point mutation K1->K2 (p_mut per step); parent: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds/world.py --out threads/autopoiesis/packs/phase_kinds --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.6268], min area 6 px

## Measurements
- components: final 27, mean 30.4, max 46; occupancy final 0.28
- tracks: 247; persistent (alive >= 50% of run): 9; longest 110 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.86 (1 = constant size)
- enclosures: components with a hole mean 1.30, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 15]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [27, 27, 27], H1 [25, 20, 0]
- motion: 23 long-lived tracks moved >= 1 body length; max speed 0.00598/time; max body lengths 2.0
- replication: splits 121, persistent splits 47, max generation 5, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.4543, -1.0, None, 7.3469, 7.2791]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 45 at frame 82: holes 0, rim-vs-core 0.47, rim-vs-outside 1.10, heterogeneity 0.14; core [0.119, 0.964, 0.0, 0.84, 0.584] rim [0.291, 0.583, 0.0, 0.767, 0.775]
  - track 64 at frame 86: holes 0, rim-vs-core 0.45, rim-vs-outside 1.07, heterogeneity 0.14; core [0.122, 0.956, 0.0, 0.84, 0.62] rim [0.287, 0.568, 0.0, 0.757, 0.756]
  - track 59 at frame 81: holes 0, rim-vs-core 0.45, rim-vs-outside 1.08, heterogeneity 0.14; core [0.114, 0.944, 0.0, 0.811, 0.588] rim [0.286, 0.575, 0.0, 0.76, 0.767]
  - track 139 at frame 134: holes 0, rim-vs-core 0.80, rim-vs-outside 0.71, heterogeneity 0.19; core [0.176, 0.0, 0.959, 0.996, 0.724] rim [0.374, 0.0, 0.334, 0.543, 0.616]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
