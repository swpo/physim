# Evidence pack: marangoni-flames (seed 1)

- world: `../../../world.py`, family `reactive-marangoni`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 19s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/world.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/mg/packs/m15 --seeds 0 1 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.38 of robust range [0.0, 0.6642], min area 6 px

## Measurements
- components: final 19, mean 15.3, max 52; occupancy final 0.02
- tracks: 144; persistent (alive >= 50% of run): 13; longest 593 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.12 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.0254/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 20, default): splits 45, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.2, nucleations 13
- channel total drift (end/start - 1): [-0.8791, -0.2276, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 308: holes 0, rim-vs-core 0.57, rim-vs-outside 0.65, heterogeneity 0.15; core [0.937, 0.023, 0.548, 0.958] rim [0.62, 0.118, 0.955, 0.734]
  - track 39 at frame 308: holes 0, rim-vs-core 0.58, rim-vs-outside 0.64, heterogeneity 0.16; core [0.921, 0.019, 0.517, 0.926] rim [0.612, 0.121, 0.946, 0.723]
  - track 111 at frame 308: holes 0, rim-vs-core 0.53, rim-vs-outside 0.71, heterogeneity 0.15; core [0.971, 0.033, 0.551, 1.0] rim [0.68, 0.107, 0.941, 0.797]
  - track 132 at frame 459: holes 0, rim-vs-core 0.56, rim-vs-outside 0.67, heterogeneity 0.16; core [0.965, 0.025, 0.553, 0.989] rim [0.644, 0.113, 0.94, 0.753]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 94 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 33.1 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.827)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 16.2, rim/outside 0.626 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.234)
  - radial |u|: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.35, rim/outside 3.31 (aggregate of 94 individuals; 94/94 membrane-like individually; rim level 0.951)  MEMBRANE-LIKE
  - radial burn r: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 86.7 (aggregate of 94 individuals; 0/94 membrane-like individually; rim level 0.918)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): |u|
- membrane-like channels per top track at mid-life: #38 (t=308, R_eq 2.82): ['|u|']; #39 (t=308, R_eq 2.93): ['|u|']; #111 (t=308, R_eq 2.33): ['|u|']; #132 (t=459, R_eq 2.65): ['|u|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
