# Evidence pack: phase-kinds-parasite (seed 2)

- world: `../../../worlds/phase_kinds_parasite/world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: mutant kind K2 is selfish: faster (c2=0.3 vs 0.2) but makes no links (b2=0)
- run: 161 frames x 200 steps x dt 1.0 = time 32000; grid [128, 128]; wall 49s; status ok
- command: `python -m labkit.run threads/autopoiesis/worlds/phase_kinds_parasite/world.py --out threads/autopoiesis/packs/phase_kinds_parasite --seeds 0 1 2 --frames 160 --spf 200`
- segmentation: matter > 0.35 of robust range [0.0, 1.5228], min area 6 px

## Measurements
- components: final 0, mean 20.9, max 44; occupancy final 0.00
- tracks: 156; persistent (alive >= 50% of run): 4; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.27 (1 = constant size)
- enclosures: components with a hole mean 0.99, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00276/time; max body lengths 1.7
- replication: splits 75, persistent splits 39, max generation 4, merges 0, nucleations 0
- channel total drift (end/start - 1): [0.006, -1.0, None, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 67: holes 0, rim-vs-core 0.34, rim-vs-outside 1.15, heterogeneity 0.15; core [0.078, 0.933, 0.0, 0.856, 0.582] rim [0.212, 0.648, 0.0, 0.797, 0.687]
  - track 33 at frame 66: holes 0, rim-vs-core 0.40, rim-vs-outside 1.05, heterogeneity 0.16; core [0.097, 0.911, 0.0, 0.866, 0.687] rim [0.222, 0.559, 0.0, 0.714, 0.652]
  - track 47 at frame 70: holes 0, rim-vs-core 0.48, rim-vs-outside 1.04, heterogeneity 0.16; core [0.085, 0.926, 0.0, 0.862, 0.621] rim [0.274, 0.505, 0.0, 0.751, 0.702]
  - track 80 at frame 66: holes 0, rim-vs-core 0.47, rim-vs-outside 1.06, heterogeneity 0.15; core [0.085, 0.927, 0.0, 0.863, 0.62] rim [0.269, 0.521, 0.0, 0.768, 0.716]

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, lineage.png, timeseries.png, movie.mp4, metrics.json

Measurements are screens, not verdicts: judge them against the images.
