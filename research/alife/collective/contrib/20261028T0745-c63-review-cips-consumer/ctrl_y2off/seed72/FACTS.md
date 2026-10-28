# Evidence pack: cips-consumer (seed 72)

- world: `../../ctrl_world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 300s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0745-c63-review-cips-consumer/ctrl_world.py --out collective/contrib/20261028T0745-c63-review-cips-consumer/ctrl_y2off/seed72 --seeds 72 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0303, 2.1619], min area 6 px

## Measurements
- components: final 59, mean 52.3, max 75; occupancy final 0.21
- tracks: 337; persistent (alive >= 50% of run): 55; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.25 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [59, 59, 58], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.0223/time; max body lengths 3.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 121, persistent splits 39 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.05, nucleations 90
- channel total drift (end/start - 1): [0.1792, 0.0023, None, -0.6967]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 232 at frame 72: holes 0, rim-vs-core 0.85, rim-vs-outside 0.48, heterogeneity 0.20; core [0.929, 0.942, 0.865, 0.037] rim [0.65, 0.32, 0.357, 0.094]
  - track 253 at frame 74: holes 0, rim-vs-core 0.62, rim-vs-outside 0.34, heterogeneity 0.24; core [0.935, 0.626, 0.595, 0.028] rim [0.745, 0.183, 0.205, 0.079]
  - track 257 at frame 74: holes 0, rim-vs-core 0.64, rim-vs-outside 0.36, heterogeneity 0.22; core [0.946, 0.627, 0.594, 0.028] rim [0.756, 0.159, 0.208, 0.078]
  - track 309 at frame 79: holes 0, rim-vs-core 0.13, rim-vs-outside 0.25, heterogeneity 0.02; core [0.969, 0.026, 0.001, 0.025] rim [0.846, 0.025, 0.001, 0.064]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 321 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 25.6 (aggregate of 321 individuals; 2/321 membrane-like individually; rim level 0.884)
  - radial consumer q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.593, rim/outside 14.1 (aggregate of 321 individuals; 6/321 membrane-like individually; rim level 0.36)
  - radial product r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.56, rim/outside 22.7 (aggregate of 321 individuals; 5/321 membrane-like individually; rim level 0.314)
  - radial fuel u: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 6.08, rim/outside 0.718 (aggregate of 321 individuals; 0/321 membrane-like individually; rim level 0.146)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #232 (t=7200, R_eq 4.62): none; #253 (t=7400, R_eq 4.62): none; #257 (t=7400, R_eq 4.37): none; #309 (t=7900, R_eq 3.78): none
- species `prey` (channels ['prey a'], own threshold): components final 59, mean 51.7, max 78; tracks 366, persistent 55; splits 124, persistent splits 40 (K=5), max generation 4, merges 15, merge/split 0.121; moving tracks 24
- species `consumer` (channels ['consumer q'], own threshold): components final 39, mean 36.1, max 75; tracks 280, persistent 35; splits 65, persistent splits 17 (K=5), max generation 2, merges 9, merge/split 0.138; moving tracks 86

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 321 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
