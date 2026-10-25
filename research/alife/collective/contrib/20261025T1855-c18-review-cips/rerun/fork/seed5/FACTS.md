# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 273s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev10/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev10/fork --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0001, 0.9974], min area 6 px

## Measurements
- components: final 0, mean 112.9, max 297; occupancy final 0.00
- tracks: 378; persistent (alive >= 50% of run): 0; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 6, 1], H1 [12, 7, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 200, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 70, merge/split ratio 70, nucleations 306
- channel total drift (end/start - 1): [0.0, -1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 88: holes 0, rim-vs-core 0.27, rim-vs-outside 0.50, heterogeneity 0.09; core [0.987, 0.968, 0.619] rim [0.794, 0.798, 0.692]
  - track 1 at frame 88: holes 0, rim-vs-core 0.25, rim-vs-outside 0.48, heterogeneity 0.08; core [0.984, 0.939, 0.646] rim [0.801, 0.773, 0.705]
  - track 2 at frame 88: holes 0, rim-vs-core 0.14, rim-vs-outside 0.58, heterogeneity 0.08; core [0.971, 0.9, 0.656] rim [0.853, 0.825, 0.682]
  - track 4 at frame 88: holes 0, rim-vs-core 0.29, rim-vs-outside 0.49, heterogeneity 0.09; core [0.978, 0.928, 0.65] rim [0.759, 0.754, 0.712]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 732 components >= 12 px at frames [50, 101, 151]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.936, rim/outside 38.4 (aggregate of 732 individuals; 0/732 membrane-like individually; rim level 0.925)
  - radial p: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 2.89 (aggregate of 732 individuals; 0/732 membrane-like individually; rim level 0.706)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.891 (aggregate of 732 individuals; 0/732 membrane-like individually; rim level 0.628)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=880, R_eq 3.91): none; #1 (t=880, R_eq 3.34): none; #2 (t=880, R_eq 3.29): none; #4 (t=880, R_eq 3.39): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
