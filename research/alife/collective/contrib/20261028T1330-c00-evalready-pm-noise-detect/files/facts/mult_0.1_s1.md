# Evidence pack: phase-membrane-noise (seed 1)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on ['S', 'K', 'L']
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 28s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/mult_0.1_s1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3144], min area 6 px

## Measurements
- components: final 3, mean 2.0, max 81; occupancy final 0.00
- tracks: 279; persistent (alive >= 50% of run): 0; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [233, 101, 12], H1 [164, 15, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 1000, default): splits 7, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 0.857, nucleations 151
- channel total drift (end/start - 1): [-0.0054, -1.0, -1.0, -0.1339]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 4: holes 17, rim-vs-core 0.02, rim-vs-outside 0.52, heterogeneity 0.11; core [0.008, 0.547, 0.343, 0.589] rim [0.008, 0.545, 0.344, 0.571]
  - track 69 at frame 8: holes 0, rim-vs-core 0.17, rim-vs-outside 0.39, heterogeneity 0.11; core [0.304, 0.168, 0.403, 0.769] rim [0.318, 0.127, 0.35, 0.609]
  - track 76 at frame 8: holes 0, rim-vs-core 0.30, rim-vs-outside 0.23, heterogeneity 0.17; core [0.315, 0.233, 0.489, 0.722] rim [0.322, 0.111, 0.35, 0.484]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
