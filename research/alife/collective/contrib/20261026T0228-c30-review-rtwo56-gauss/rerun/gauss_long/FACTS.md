# Evidence pack: r-two56-gauss (seed 5)

- world: `../../../20261026T0205-c32-rtwo56-gauss-twin/world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 601 frames x 5 steps x dt 0.1 = time 300; grid [192, 192]; wall 36s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0228-c30-review-rtwo56-gauss/rerun/gauss_long --seeds 5 --frames 600 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.7782], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 4; occupancy final 1.00
- tracks: 6; persistent (alive >= 50% of run): 1; longest 343 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.01 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 262]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [471, 148, 1], H1 [515, 204, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 10, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [2.2174, 0.9762]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 131: holes 0, rim-vs-core 0.05, rim-vs-outside 0.64, heterogeneity 0.24; core [0.577, 0.354] rim [0.544, 0.385]
  - track 2 at frame 262: holes 1, rim-vs-core 0.04, rim-vs-outside 0.20, heterogeneity 0.02; core [0.0, 0.78] rim [0.005, 0.738]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial A0: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.579)
  - radial A1: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside n/a (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.358)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=217, R_eq 108.32): none; #0 (t=65.5, R_eq 93.61): none; #2 (t=131, R_eq 4.65, ring): ['A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
