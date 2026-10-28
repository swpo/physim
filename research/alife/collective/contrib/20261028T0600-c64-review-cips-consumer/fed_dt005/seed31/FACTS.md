# Evidence pack: cips-consumer (seed 31)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 2000 steps x dt 0.05 (--dt; world META dt 0.25) = time 12000; grid [128, 128]; wall 1049s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261028T0600-c64-review-cips-consumer/fed_dt005/seed31 --seeds 31 --frames 120 --spf 2000 --dt 0.05 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0375, 1.9965], min area 6 px

## Measurements
- components: final 32, mean 39.4, max 87; occupancy final 0.20
- tracks: 918; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 37, 30], H1 [0, 0, 0]
- motion: 131 long-lived tracks moved >= 1 body length; max speed 0.0221/time; max body lengths 5.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 395, persistent splits 92 (0 more failed only because the siblings re-merged within K), max generation 7, merges 23, merge/split ratio 0.058, nucleations 81
- channel total drift (end/start - 1): [0.0264, -0.0014, None, -0.5943]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 135 at frame 31: holes 0, rim-vs-core 0.34, rim-vs-outside 0.34, heterogeneity 0.25; core [0.753, 0.478, 0.475, 0.138] rim [0.56, 0.342, 0.239, 0.183]
  - track 352 at frame 57: holes 0, rim-vs-core 0.35, rim-vs-outside 0.54, heterogeneity 0.27; core [0.746, 0.55, 0.544, 0.12] rim [0.562, 0.425, 0.281, 0.164]
  - track 218 at frame 35: holes 0, rim-vs-core 0.36, rim-vs-outside 0.60, heterogeneity 0.27; core [0.808, 0.527, 0.591, 0.123] rim [0.569, 0.449, 0.333, 0.179]
  - track 809 at frame 111: holes 0, rim-vs-core 0.24, rim-vs-outside 0.29, heterogeneity 0.25; core [0.769, 0.339, 0.299, 0.086] rim [0.633, 0.216, 0.153, 0.152]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 9.72 (aggregate of 227 individuals; 13/227 membrane-like individually; rim level 0.666)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 7.35 (aggregate of 227 individuals; 27/227 membrane-like individually; rim level 0.319)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.656, rim/outside 11.1 (aggregate of 227 individuals; 15/227 membrane-like individually; rim level 0.25)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.57, rim/outside 0.776 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #135 (t=3100, R_eq 5.32): none; #352 (t=5700, R_eq 6.82): none; #218 (t=3500, R_eq 6.31): none; #809 (t=11100, R_eq 5.7): none
- species `prey` (channels ['prey a'], own threshold): components final 29, mean 36.9, max 64; tracks 916, persistent 0; splits 398, persistent splits 86 (K=5), max generation 8, merges 33, merge/split 0.083; moving tracks 99
- species `consumer` (channels ['consumer q'], own threshold): components final 27, mean 30.3, max 71; tracks 740, persistent 0; splits 230, persistent splits 37 (K=5), max generation 3, merges 15, merge/split 0.065; moving tracks 291

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 10 of 227 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
