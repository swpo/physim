# Evidence pack: fch-pchemoton-noK-clip (seed 5)

- world: `../../world_noK_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 401 frames x 300 steps x dt 0.01 = time 1200; grid [192, 192]; wall 754s; status ok
- command: `python -m labkit.run collective/contrib/c17-kb-wip/world_noK_clip.py --out collective/contrib/c17-kb-wip/noK_clip/seed5 --seeds 5 --frames 400 --no-movie`
- segmentation: matter > 0.47 of robust range [-0.0455, 1.3237], min area 6 px

## Measurements
- components: final 0, mean 1.9, max 5; occupancy final 0.00
- tracks: 5; persistent (alive >= 50% of run): 0; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 5
- channel total drift (end/start - 1): [-1.3663, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 81: holes 0, rim-vs-core 0.11, rim-vs-outside 0.32, heterogeneity 0.03; core [1.0, 1.0, 0.0] rim [0.885, 1.0, 0.0]
  - track 4 at frame 81: holes 0, rim-vs-core 0.13, rim-vs-outside 0.27, heterogeneity 0.03; core [1.0, 1.0, 0.0] rim [0.868, 1.0, 0.0]
  - track 1 at frame 81: holes 0, rim-vs-core 0.14, rim-vs-outside 0.26, heterogeneity 0.03; core [1.0, 1.0, 0.0] rim [0.856, 1.0, 0.0]
  - track 2 at frame 81: holes 0, rim-vs-core 0.15, rim-vs-outside 0.26, heterogeneity 0.03; core [1.0, 1.0, 0.0] rim [0.846, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 10 components >= 12 px at frames [67, 134]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 9.62 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 1)
  - radial precursor P: flat profile (no radial structure; level 1; aggregate of 10 individuals)
  - radial catalyst K: flat profile (no radial structure; level 0; aggregate of 10 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=243, R_eq 5.05): none; #4 (t=243, R_eq 4.92): none; #1 (t=243, R_eq 4.95): none; #2 (t=243, R_eq 4.98): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
