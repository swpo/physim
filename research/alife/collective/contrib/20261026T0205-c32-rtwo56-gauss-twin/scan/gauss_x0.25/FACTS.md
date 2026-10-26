# Evidence pack: r-two56-gauss (seed 0)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 10s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/scan/gauss_x0.25 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.721], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.37
- tracks: 1; persistent (alive >= 50% of run): 1; longest 201 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.04 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 1, 1], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.1822, -0.1926]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.01, rim-vs-outside 0.63, heterogeneity 0.22; core [0.575, 0.354] rim [0.57, 0.344]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.996, rim/outside 58.3 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.573)
  - radial A1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 37 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.36)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=50.5, R_eq 66.02): none

## Warnings
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
