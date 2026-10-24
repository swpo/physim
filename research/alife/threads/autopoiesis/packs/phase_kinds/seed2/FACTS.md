# Evidence pack: phase-kinds (seed 2)

- world: `../../../worlds/phase_kinds/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_protocell; mutation: two heritable catalyst kinds; mutant K2 replicates faster (c2=0.3 vs c1=0.2) with equal link output; stochastic point mutation K1->K2 (p_mut per step); parent: membrane is an Allen-Cahn domain wall (always closed) instead of a polymerized field; the inside phase is tilted by catalyst-made links; K and L mobility ~ phi^2
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 52s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds/world.py --out threads/autopoiesis/packs/phase_kinds --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.6303], min area 6 px

## Measurements
- components: final 31, mean 30.2, max 45; occupancy final 0.25
- tracks: 246; persistent (alive >= 50% of run): 9; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.76 (1 = constant size)
- enclosures: components with a hole mean 1.00, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 8]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 31], H1 [24, 14, 1]
- motion: 16 long-lived tracks moved >= 1 body length; max speed 0.00646/time; max body lengths 2.1
- replication: splits 120, persistent splits 48, max generation 6, merges 0, nucleations 0
- channel total drift (end/start - 1): [-0.4326, -1.0, None, 7.0382, 5.7772]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 75: holes 0, rim-vs-core 0.34, rim-vs-outside 1.13, heterogeneity 0.14; core [0.11, 0.941, 0.0, 0.809, 0.572] rim [0.239, 0.662, 0.0, 0.762, 0.698]
  - track 24 at frame 75: holes 0, rim-vs-core 0.48, rim-vs-outside 1.04, heterogeneity 0.15; core [0.115, 0.933, 0.0, 0.809, 0.593] rim [0.303, 0.524, 0.0, 0.729, 0.724]
  - track 47 at frame 82: holes 0, rim-vs-core 0.48, rim-vs-outside 1.02, heterogeneity 0.15; core [0.119, 0.933, 0.0, 0.816, 0.619] rim [0.302, 0.508, 0.0, 0.714, 0.703]
  - track 145 at frame 134: holes 0, rim-vs-core 0.66, rim-vs-outside 0.72, heterogeneity 0.16; core [0.139, 0.0, 0.911, 0.955, 0.782] rim [0.327, 0.0, 0.378, 0.682, 0.574]

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
