# Evidence pack: cips-consumer (seed 31)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 2000 steps x dt 0.05 (--dt; world META dt 0.25) = time 12000; grid [128, 128]; wall 1026s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261028T0600-c64-review-cips-consumer/noeat_dt005/seed31 --seeds 31 --frames 120 --spf 2000 --dt 0.05 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0284, 2.1644], min area 6 px

## Measurements
- components: final 77, mean 76.5, max 83; occupancy final 0.20
- tracks: 112; persistent (alive >= 50% of run): 77; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 77, 74], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000703/time; max body lengths 1.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 8, merge/split ratio 0.615, nucleations 75
- channel total drift (end/start - 1): [0.228, -0.0014, None, -0.7063]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 61: holes 0, rim-vs-core 0.59, rim-vs-outside 0.32, heterogeneity 0.21; core [0.949, 0.565, 0.523, 0.025] rim [0.768, 0.131, 0.176, 0.064]
  - track 1 at frame 61: holes 0, rim-vs-core 0.68, rim-vs-outside 0.42, heterogeneity 0.22; core [0.933, 0.741, 0.652, 0.03] rim [0.821, 0.211, 0.234, 0.05]
  - track 5 at frame 61: holes 0, rim-vs-core 0.28, rim-vs-outside 0.59, heterogeneity 0.22; core [0.953, 0.56, 0.546, 0.019] rim [0.826, 0.357, 0.394, 0.049]
  - track 7 at frame 61: holes 0, rim-vs-core 0.15, rim-vs-outside 0.58, heterogeneity 0.21; core [0.922, 0.41, 0.396, 0.035] rim [0.818, 0.333, 0.327, 0.052]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 462 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.923, rim/outside 29.1 (aggregate of 462 individuals; 0/462 membrane-like individually; rim level 0.916)
  - radial consumer q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.516, rim/outside 22.5 (aggregate of 462 individuals; 1/462 membrane-like individually; rim level 0.404)
  - radial product r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.509, rim/outside 26.5 (aggregate of 462 individuals; 1/462 membrane-like individually; rim level 0.376)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 6.66, rim/outside 0.72 (aggregate of 462 individuals; 0/462 membrane-like individually; rim level 0.113)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=6100, R_eq 3.66): none; #1 (t=6100, R_eq 3.66): none; #5 (t=6100, R_eq 3.99): none; #7 (t=6100, R_eq 3.66): none
- species `prey` (channels ['prey a'], own threshold): components final 77, mean 76.3, max 80; tracks 151, persistent 77; splits 27, persistent splits 4 (K=5), max generation 1, merges 13, merge/split 0.481; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 63, mean 63.3, max 76; tracks 82, persistent 63; splits 0, persistent splits 0 (K=5), max generation 0, merges 6, merge/split n/a; moving tracks 8

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
