# Evidence pack: marangoni-flames (seed 1)

- world: `../../../world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 18s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/world.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/packs/m0 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.42 of robust range [0.0, 0.5991], min area 6 px

## Measurements
- components: final 22, mean 13.7, max 54; occupancy final 0.02
- tracks: 158; persistent (alive >= 50% of run): 7; longest 350 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.17 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 22, 22], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.0356/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 20, default): splits 51, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 2, merges 8, merge/split ratio 0.157, nucleations 12
- channel total drift (end/start - 1): [-0.8735, -0.2328, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 132 at frame 429: holes 0, rim-vs-core 0.16, rim-vs-outside 0.58, heterogeneity 0.05; core [0.946, 0.014, 0.0, 0.933] rim [0.808, 0.089, 0.0, 0.896]
  - track 124 at frame 207: holes 0, rim-vs-core 0.16, rim-vs-outside 0.57, heterogeneity 0.06; core [0.908, 0.012, 0.0, 0.881] rim [0.776, 0.094, 0.0, 0.858]
  - track 136 at frame 434: holes 0, rim-vs-core 0.22, rim-vs-outside 0.63, heterogeneity 0.06; core [0.977, 0.023, 0.0, 0.986] rim [0.798, 0.092, 0.0, 0.882]
  - track 146 at frame 514: holes 0, rim-vs-core 0.21, rim-vs-outside 0.64, heterogeneity 0.06; core [0.991, 0.025, 0.0, 0.987] rim [0.81, 0.096, 0.0, 0.895]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 18.4 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.861)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.4, rim/outside 0.607 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.221)
  - radial |u|: flat profile (no radial structure; level 0; aggregate of 86 individuals)
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 53.1 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.899)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #132 (t=429, R_eq 2.52): none; #124 (t=207, R_eq 2.76): none; #136 (t=434, R_eq 2.39): none; #146 (t=514, R_eq 2.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
