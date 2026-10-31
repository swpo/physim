# Evidence pack: phase-membrane-noise (seed 2)

- world: `../../pm_noise.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi'], multiplicative (sd x value) on []
- run: 161 frames x 50 steps x dt 1.0 = time 8000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs/phi_0.03_s2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4263], min area 6 px

## Measurements
- components: final 0, mean 0.7, max 18; occupancy final 0.00
- tracks: 90; persistent (alive >= 50% of run): 0; longest 4 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [247, 102, 13], H1 [145, 14, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 1000, default): splits 11, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 0.636, nucleations 33
- channel total drift (end/start - 1): [0.0, -1.0, -1.0, -0.8338]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 5: holes 0, rim-vs-core 0.12, rim-vs-outside 0.14, heterogeneity 0.04; core [0.0, 0.643, 0.342, 0.438] rim [0.0, 0.647, 0.326, 0.314]
  - track 44 at frame 7: holes 0, rim-vs-core 0.08, rim-vs-outside 0.08, heterogeneity 0.03; core [0.002, 0.62, 0.292, 0.397] rim [0.001, 0.622, 0.282, 0.317]
  - track 55 at frame 8: holes 0, rim-vs-core 0.49, rim-vs-outside 0.65, heterogeneity 0.17; core [0.105, 0.795, 0.539, 0.903] rim [0.259, 0.48, 0.555, 0.56]
  - track 88 at frame 12: holes 1, rim-vs-core 0.15, rim-vs-outside 0.61, heterogeneity 0.11; core [0.032, 0.619, 0.248, 0.754] rim [0.084, 0.536, 0.317, 0.667]
- radial profiles: no component with area >= 12 px at the sampled frames

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
