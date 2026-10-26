# Evidence pack: r-two56-gauss (seed 0)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/scan/gauss_x4 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7699], min area 6 px

## Measurements
- components: final 1, mean 2.0, max 6; occupancy final 1.00
- tracks: 15; persistent (alive >= 50% of run): 1; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.55 (1 = constant size)
- enclosures: components with a hole mean 0.44, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 193]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [233, 72, 1], H1 [226, 82, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 9.49/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 10, default): splits 5, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 4, merge/split ratio 0.8, nucleations 0
- channel total drift (end/start - 1): [2.2037, 0.9647]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 141: holes 0, rim-vs-core 0.00, rim-vs-outside 0.46, heterogeneity 0.13; core [0.576, 0.354] rim [0.578, 0.354]
  - track 2 at frame 37: holes 7, rim-vs-core 0.10, rim-vs-outside 0.64, heterogeneity 0.26; core [0.578, 0.354] rim [0.676, 0.326]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 1.04 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.353)
  - radial A1: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.67, rim/outside 1.32 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.334)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=70.5, R_eq 108.04): none; #1 (t=25, R_eq 31.33, ring): none; #14 (t=59, R_eq 17.24, ring): none; #2 (t=18.5, R_eq 70.68): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 11 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 6 of 11 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
