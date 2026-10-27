# Evidence pack: cips-consumer (seed 7)

- world: `../../20261026T1800-c43-chasing-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 76 frames x 400 steps x dt 0.1 (--dt; world META dt 0.25) = time 3000; grid [128, 128]; wall 175s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1800-c43-chasing-consumer/world.py --out collective/contrib/c49rev3/rerun_chih10 --seeds 7 --frames 75 --dt 0.1 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.047, 2.0671], min area 6 px

## Measurements
- components: final 22, mean 25.8, max 91; occupancy final 0.11
- tracks: 561; persistent (alive >= 50% of run): 1; longest 42 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.40 (1 = constant size)
- enclosures: components with a hole mean 0.74, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 31, 17], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.0644/time; max body lengths 2.0
- replication (lineage window K = 5 frames = time 200, --lineage-k): splits 199, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 89, merge/split ratio 0.447, nucleations 73
- channel total drift (end/start - 1): [-0.2037, 0.019, None, -0.4271]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 344 at frame 55: holes 0, rim-vs-core 0.71, rim-vs-outside 0.74, heterogeneity 0.19; core [0.844, 0.996, 0.964, 0.241] rim [0.368, 0.718, 0.529, 0.348]
  - track 205 at frame 28: holes 0, rim-vs-core 0.82, rim-vs-outside 0.30, heterogeneity 0.22; core [0.658, 0.871, 0.762, 0.17] rim [0.612, 0.213, 0.279, 0.209]
  - track 471 at frame 66: holes 0, rim-vs-core 0.44, rim-vs-outside 0.31, heterogeneity 0.17; core [0.876, 0.368, 0.359, 0.04] rim [0.839, 0.023, 0.091, 0.077]
  - track 356 at frame 42: holes 0, rim-vs-core 0.52, rim-vs-outside 0.26, heterogeneity 0.20; core [0.716, 0.572, 0.495, 0.096] rim [0.694, 0.145, 0.199, 0.139]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 6.58 (aggregate of 130 individuals; 6/130 membrane-like individually; rim level 0.652)
  - radial consumer q: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.958, rim/outside 12.4 (aggregate of 130 individuals; 45/130 membrane-like individually; rim level 0.509)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 13 (aggregate of 130 individuals; 37/130 membrane-like individually; rim level 0.436)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.54, rim/outside 0.735 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.295)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #344 (t=2200, R_eq 4.44): none; #205 (t=1120, R_eq 5.08): none; #471 (t=2640, R_eq 5.84): ['consumer q', 'product r']; #356 (t=1680, R_eq 5.59): ['consumer q', 'product r']
- species `prey` (channels ['prey a'], own threshold): components final 14, mean 18.7, max 48; tracks 251, persistent 1; splits 83, persistent splits 10 (K=5), max generation 2, merges 9, merge/split 0.108; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 33, mean 36.1, max 92; tracks 816, persistent 1; splits 222, persistent splits 7 (K=5), max generation 1, merges 151, merge/split 0.68; moving tracks 78

## Warnings
- --dt 0.1 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 14 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
