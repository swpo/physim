# Evidence pack: phoretic-colloids (seed 3)

- world: `../../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 97s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/wip-c37/phatt/rerun_kd01/seed3 --seeds 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 3.8372], min area 6 px

## Measurements
- components: final 6, mean 6.7, max 9; occupancy final 0.03
- tracks: 19; persistent (alive >= 50% of run): 7; longest 345 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 4], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.339/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 15
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 229: holes 0, rim-vs-core 0.47, rim-vs-outside 0.20, heterogeneity 0.15; core [0.6, 0.722, 0.593] rim [0.66, 0.258, 0.525]
  - track 8 at frame 235: holes 0, rim-vs-core 0.07, rim-vs-outside 0.32, heterogeneity 0.12; core [0.65, 0.567, 0.521] rim [0.602, 0.523, 0.499]
  - track 10 at frame 245: holes 0, rim-vs-core 0.55, rim-vs-outside 0.23, heterogeneity 0.20; core [0.721, 0.622, 0.705] rim [0.762, 0.08, 0.603]
  - track 12 at frame 249: holes 0, rim-vs-core 0.20, rim-vs-outside 0.83, heterogeneity 0.18; core [1.0, 0.689, 1.0] rim [0.93, 0.507, 0.963]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 10.3 (aggregate of 43 individuals; 13/43 membrane-like individually; rim level 0.738)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.603, rim/outside 18.4 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.568)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.914, rim/outside 1.98 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.671)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=114.5, R_eq 4.22): ['A density']; #8 (t=117.5, R_eq 3.66): none; #10 (t=122.5, R_eq 4.79): ['A density']; #12 (t=124.5, R_eq 6.08): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
