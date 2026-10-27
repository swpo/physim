# Evidence pack: reacting-thermals (seed 32)

- world: `../../../20261027T0040-c49-reacting-thermals-claim/world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [128, 128]; wall 39s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py --out collective/contrib/c53-audit-work/rerun --seeds 31 32 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.31 of robust range [0.0, 0.795], min area 6 px

## Measurements
- components: final 20, mean 13.6, max 46; occupancy final 0.02
- tracks: 405; persistent (alive >= 50% of run): 0; longest 227 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 38, 28], H1 [0, 0, 0]
- motion: 138 long-lived tracks moved >= 1 body length; max speed 1.17/time; max body lengths 41.5
- replication (lineage window K = 20 frames = time 20, default): splits 104, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 7, merges 19, merge/split ratio 0.183, nucleations 149
- channel total drift (end/start - 1): [-0.8618, -0.3493, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 290 at frame 514: holes 0, rim-vs-core 0.26, rim-vs-outside 0.66, heterogeneity 0.15; core [0.966, 0.102, 0.651, 0.995] rim [0.757, 0.146, 0.635, 0.85]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 5.09 (aggregate of 59 individuals; 2/59 membrane-like individually; rim level 0.628)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.74, rim/outside 0.679 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.257)
  - radial vorticity: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.05 (aggregate of 59 individuals; 16/59 membrane-like individually; rim level 0.468)
  - radial burn r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.957, rim/outside 6.05 (aggregate of 59 individuals; 7/59 membrane-like individually; rim level 0.65)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #213 (t=454, R_eq 1.78): none; #256 (t=469, R_eq 1.87): none; #290 (t=514, R_eq 2.46): none; #363 (t=565, R_eq 2.03): ['vorticity']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
