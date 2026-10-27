# Evidence pack: marangoni-flames (seed 0)

- world: `../../../world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 18s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/world.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/packs/m15 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7551], min area 6 px

## Measurements
- components: final 10, mean 6.7, max 46; occupancy final 0.01
- tracks: 124; persistent (alive >= 50% of run): 5; longest 533 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0235/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 20, default): splits 38, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.158, nucleations 6
- channel total drift (end/start - 1): [-0.9557, -0.1139, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 109 at frame 282: holes 0, rim-vs-core 0.55, rim-vs-outside 0.68, heterogeneity 0.15; core [0.95, 0.032, 0.52, 0.999] rim [0.67, 0.132, 0.951, 0.834]
  - track 113 at frame 282: holes 0, rim-vs-core 0.57, rim-vs-outside 0.69, heterogeneity 0.15; core [0.96, 0.035, 0.551, 0.999] rim [0.646, 0.138, 0.982, 0.823]
  - track 111 at frame 257: holes 0, rim-vs-core 0.57, rim-vs-outside 0.70, heterogeneity 0.15; core [0.961, 0.031, 0.517, 0.999] rim [0.663, 0.136, 0.967, 0.842]
  - track 114 at frame 464: holes 0, rim-vs-core 0.54, rim-vs-outside 0.75, heterogeneity 0.15; core [0.977, 0.041, 0.58, 1.0] rim [0.665, 0.139, 0.983, 0.837]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 34.8 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.845)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.6, rim/outside 0.621 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.254)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.48, rim/outside 3.35 (aggregate of 40 individuals; 40/40 membrane-like individually; rim level 0.952)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 80.2 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.932)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #109 (t=282, R_eq 2.93): ['|u|']; #113 (t=282, R_eq 2.88): ['|u|']; #111 (t=257, R_eq 2.93): ['|u|']; #114 (t=464, R_eq 2.71): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
