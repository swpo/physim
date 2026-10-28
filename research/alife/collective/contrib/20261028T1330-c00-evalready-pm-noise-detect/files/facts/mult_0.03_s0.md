# Evidence pack: phase-membrane-noise (seed 0)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 30s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.03_s0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3807], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 23; occupancy final 0.00
- tracks: 98; persistent (alive >= 50% of run): 0; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [242, 100, 15], H1 [164, 7, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 10, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.8, nucleations 32
- channel total drift (end/start - 1): [-0.0004, -1.0, -1.0, -0.8218]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 95 at frame 12: holes 0, rim-vs-core 0.27, rim-vs-outside 0.52, heterogeneity 0.12; core [0.043, 0.616, 0.271, 0.82] rim [0.102, 0.516, 0.341, 0.584]
  - track 90 at frame 12: holes 0, rim-vs-core 0.20, rim-vs-outside 0.21, heterogeneity 0.06; core [0.108, 0.591, 0.34, 0.591] rim [0.126, 0.514, 0.336, 0.402]
  - track 8 at frame 1: holes 83, rim-vs-core 0.58, rim-vs-outside 0.51, heterogeneity 0.22; core [0.228, 0.972, 0.994, 0.696] rim [0.47, 0.525, 0.841, 0.461]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
