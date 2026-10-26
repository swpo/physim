# Evidence pack: phoretic-colloids (seed 5)

- world: `../../../20261026T0529-c33-phoretic-swimdivide-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 1601 frames x 1 steps x dt 0.5 = time 800; grid [128, 128]; wall 188s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0529-c33-phoretic-swimdivide-claim/world.py --out collective/contrib/c39-rev-phor-wip/recip/seed5 --seeds 5 --frames 1600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.8564], min area 6 px

## Measurements
- components: final 10, mean 14.4, max 27; occupancy final 0.04
- tracks: 227; persistent (alive >= 50% of run): 9; longest 1495 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [0, 0, 0]
- motion: 21 long-lived tracks moved >= 1 body length; max speed 0.256/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 21, merge/split ratio n/a, nucleations 206
- channel total drift (end/start - 1): [-0.53, 2.565, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 81 at frame 861: holes 0, rim-vs-core 0.37, rim-vs-outside 0.33, heterogeneity 0.22; core [0.669, 0.654, 0.739] rim [0.339, 0.603, 0.575]
  - track 163 at frame 928: holes 0, rim-vs-core 0.26, rim-vs-outside 0.29, heterogeneity 0.16; core [0.725, 0.533, 0.579] rim [0.507, 0.43, 0.484]
  - track 172 at frame 955: holes 0, rim-vs-core 0.27, rim-vs-outside 0.51, heterogeneity 0.24; core [0.738, 0.594, 0.829] rim [0.483, 0.605, 0.737]
  - track 192 at frame 1035: holes 0, rim-vs-core 0.25, rim-vs-outside 0.28, heterogeneity 0.14; core [0.495, 0.749, 0.611] rim [0.339, 0.592, 0.491]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [269, 538, 807, 1062, 1331, 1600]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 32.5 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.639)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.952, rim/outside 27.6 (aggregate of 81 individuals; 10/81 membrane-like individually; rim level 0.6)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 3.41 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.659)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #81 (t=430.5, R_eq 4.48): ['B density']; #163 (t=464, R_eq 3.39): none; #172 (t=477.5, R_eq 5.08): ['B density']; #192 (t=517.5, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
