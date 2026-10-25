# Evidence pack: fch-pchemoton-noK-clip (seed 7)

- world: `../../world_noK_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 401 frames x 300 steps x dt 0.01 = time 1200; grid [192, 192]; wall 731s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev9/world_noK_clip.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev9/noK_clip/seed7 --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.0457, 1.3379], min area 6 px

## Measurements
- components: final 0, mean 2.4, max 6; occupancy final 0.00
- tracks: 6; persistent (alive >= 50% of run): 2; longest 203 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-1.4118, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 104: holes 0, rim-vs-core 0.18, rim-vs-outside 0.25, heterogeneity 0.03; core [0.999, 1.0, 0.0] rim [0.815, 1.0, 0.0]
  - track 5 at frame 104: holes 0, rim-vs-core 0.19, rim-vs-outside 0.25, heterogeneity 0.04; core [0.998, 1.0, 0.0] rim [0.803, 1.0, 0.0]
  - track 3 at frame 71: holes 0, rim-vs-core 0.19, rim-vs-outside 0.25, heterogeneity 0.03; core [0.999, 1.0, 0.0] rim [0.807, 1.0, 0.0]
  - track 4 at frame 71: holes 0, rim-vs-core 0.18, rim-vs-outside 0.25, heterogeneity 0.03; core [0.999, 1.0, 0.0] rim [0.822, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [67, 134, 202]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 8.32 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.998)
  - radial precursor P: flat profile (no radial structure; level 1; aggregate of 14 individuals)
  - radial catalyst K: flat profile (no radial structure; level 0; aggregate of 14 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=312, R_eq 4.3): none; #5 (t=312, R_eq 4.33): none; #3 (t=213, R_eq 5.11): none; #4 (t=213, R_eq 5.05): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
