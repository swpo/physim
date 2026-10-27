# Evidence pack: cips-consumer (seed 91)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 800 steps x dt 0.125 (--dt; world META dt 0.25) = time 12000; grid [128, 128]; wall 455s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T2016-c59-review-cips-consumer/rerun/seed91_dthalf --seeds 91 --frames 120 --spf 800 --dt 0.125 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0374, 2.0028], min area 6 px

## Measurements
- components: final 39, mean 40.1, max 81; occupancy final 0.19
- tracks: 973; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 39, 32], H1 [1, 0, 0]
- motion: 141 long-lived tracks moved >= 1 body length; max speed 0.0226/time; max body lengths 8.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 428, persistent splits 102 (0 more failed only because the siblings re-merged within K), max generation 9, merges 22, merge/split ratio 0.051, nucleations 76
- channel total drift (end/start - 1): [0.0022, -0.0291, None, -0.5881]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 552 at frame 88: holes 0, rim-vs-core 0.29, rim-vs-outside 0.57, heterogeneity 0.28; core [0.771, 0.548, 0.583, 0.146] rim [0.537, 0.552, 0.419, 0.203]
  - track 709 at frame 104: holes 0, rim-vs-core 0.31, rim-vs-outside 0.49, heterogeneity 0.30; core [0.715, 0.603, 0.586, 0.136] rim [0.622, 0.445, 0.337, 0.165]
  - track 349 at frame 47: holes 0, rim-vs-core 0.45, rim-vs-outside 0.34, heterogeneity 0.29; core [0.75, 0.518, 0.513, 0.128] rim [0.475, 0.384, 0.193, 0.203]
  - track 881 at frame 113: holes 0, rim-vs-core 0.08, rim-vs-outside 0.49, heterogeneity 0.03; core [0.861, 0.061, 0.011, 0.012] rim [0.821, 0.053, 0.007, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 243 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 10.8 (aggregate of 243 individuals; 14/243 membrane-like individually; rim level 0.693)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 9.16 (aggregate of 243 individuals; 19/243 membrane-like individually; rim level 0.339)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.661, rim/outside 12.9 (aggregate of 243 individuals; 11/243 membrane-like individually; rim level 0.283)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.61, rim/outside 0.773 (aggregate of 243 individuals; 0/243 membrane-like individually; rim level 0.231)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #552 (t=8800, R_eq 4.72): none; #709 (t=10400, R_eq 5.35): none; #349 (t=4700, R_eq 5.56): none; #881 (t=11300, R_eq 6.21): none
- species `prey` (channels ['prey a'], own threshold): components final 37, mean 37.5, max 67; tracks 919, persistent 0; splits 400, persistent splits 88 (K=5), max generation 9, merges 26, merge/split 0.065; moving tracks 124
- species `consumer` (channels ['consumer q'], own threshold): components final 29, mean 31.2, max 71; tracks 773, persistent 0; splits 230, persistent splits 29 (K=5), max generation 4, merges 28, merge/split 0.122; moving tracks 285

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.125 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 6 of 243 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
