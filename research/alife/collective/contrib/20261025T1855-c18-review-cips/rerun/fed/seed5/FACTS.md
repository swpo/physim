# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 277s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev10/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev10/fed --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0, 0.999], min area 6 px

## Measurements
- components: final 188, mean 211.4, max 297; occupancy final 0.14
- tracks: 410; persistent (alive >= 50% of run): 210; longest 282 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [190, 189, 186], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00223/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 104, merge/split ratio n/a, nucleations 306
- channel total drift (end/start - 1): [0.0, -0.2142, 0.1476]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 0, rim-vs-core 0.27, rim-vs-outside 0.49, heterogeneity 0.09; core [0.974, 0.842, 0.19] rim [0.789, 0.688, 0.305]
  - track 1 at frame 161: holes 0, rim-vs-core 0.31, rim-vs-outside 0.50, heterogeneity 0.10; core [0.976, 0.862, 0.153] rim [0.762, 0.683, 0.292]
  - track 2 at frame 161: holes 0, rim-vs-core 0.14, rim-vs-outside 0.59, heterogeneity 0.09; core [0.969, 0.833, 0.161] rim [0.86, 0.76, 0.216]
  - track 3 at frame 161: holes 0, rim-vs-core 0.30, rim-vs-outside 0.50, heterogeneity 0.10; core [0.969, 0.833, 0.168] rim [0.743, 0.669, 0.291]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1324 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.95, rim/outside 48.9 (aggregate of 1324 individuals; 0/1324 membrane-like individually; rim level 0.941)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 3.98 (aggregate of 1324 individuals; 0/1324 membrane-like individually; rim level 0.816)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 5.22, rim/outside 0.678 (aggregate of 1324 individuals; 0/1324 membrane-like individually; rim level 0.453)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1610, R_eq 3.09): none; #1 (t=1610, R_eq 3.43): none; #2 (t=1610, R_eq 3.24): none; #3 (t=1610, R_eq 3.24): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
