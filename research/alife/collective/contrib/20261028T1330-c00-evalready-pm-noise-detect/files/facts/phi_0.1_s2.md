# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.1 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 22s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.1_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.3557], min area 6 px

## Measurements
- components: final 0, mean 1.4, max 83; occupancy final 0.00
- tracks: 195; persistent (alive >= 50% of run): 0; longest 5 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [245, 95, 13], H1 [160, 22, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 1000, default): splits 4, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.5, nucleations 91
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -0.3613]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 4: holes 22, rim-vs-core 0.02, rim-vs-outside 0.51, heterogeneity 0.09; core [0.003, 0.561, 0.313, 0.527] rim [0.004, 0.559, 0.313, 0.551]
  - track 9 at frame 7: holes 0, rim-vs-core 0.04, rim-vs-outside 0.31, heterogeneity 0.05; core [0.312, 0.105, 0.194, 0.519] rim [0.31, 0.112, 0.201, 0.561]
  - track 17 at frame 7: holes 0, rim-vs-core 0.09, rim-vs-outside 0.27, heterogeneity 0.05; core [0.284, 0.149, 0.231, 0.478] rim [0.284, 0.141, 0.224, 0.567]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
