# Evidence pack: cips-consumer (seed 7)

- world: `../../20261026T1800-c43-chasing-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 76 frames x 400 steps x dt 0.1 (--dt; world META dt 0.25) = time 3000; grid [128, 128]; wall 170s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1800-c43-chasing-consumer/world.py --out collective/contrib/c49rev3/rerun_chih0 --seeds 7 --frames 75 --dt 0.1 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0387, 1.9994], min area 6 px

## Measurements
- components: final 32, mean 41.2, max 82; occupancy final 0.19
- tracks: 366; persistent (alive >= 50% of run): 7; longest 67 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.00 (1 = constant size)
- enclosures: components with a hole mean 0.24, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 37, 32], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.0281/time; max body lengths 3.4
- replication (lineage window K = 5 frames = time 200, --lineage-k): splits 128, persistent splits 44 (0 more failed only because the siblings re-merged within K), max generation 5, merges 24, merge/split ratio 0.188, nucleations 61
- channel total drift (end/start - 1): [0.0106, 0.019, None, -0.5798]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 34: holes 0, rim-vs-core 0.39, rim-vs-outside 0.46, heterogeneity 0.21; core [0.929, 0.023, 0.005, 0.031] rim [0.678, 0.246, 0.175, 0.136]
  - track 197 at frame 48: holes 0, rim-vs-core 0.51, rim-vs-outside 0.37, heterogeneity 0.29; core [0.736, 0.604, 0.626, 0.143] rim [0.514, 0.374, 0.239, 0.209]
  - track 169 at frame 27: holes 0, rim-vs-core 0.40, rim-vs-outside 0.40, heterogeneity 0.28; core [0.744, 0.522, 0.527, 0.112] rim [0.6, 0.316, 0.222, 0.169]
  - track 337 at frame 69: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.24; core [0.82, 0.377, 0.435, 0.093] rim [0.658, 0.172, 0.149, 0.146]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 232 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 11.1 (aggregate of 232 individuals; 12/232 membrane-like individually; rim level 0.671)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 9.59 (aggregate of 232 individuals; 28/232 membrane-like individually; rim level 0.342)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.694, rim/outside 14.2 (aggregate of 232 individuals; 17/232 membrane-like individually; rim level 0.288)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.58, rim/outside 0.774 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.238)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=1360, R_eq 6.23): ['consumer q', 'product r']; #197 (t=1920, R_eq 5.17): none; #169 (t=1080, R_eq 5.64): none; #337 (t=2760, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 35, mean 38.0, max 78; tracks 376, persistent 7; splits 133, persistent splits 39 (K=5), max generation 4, merges 14, merge/split 0.105; moving tracks 30
- species `consumer` (channels ['consumer q'], own threshold): components final 28, mean 32.7, max 70; tracks 271, persistent 6; splits 72, persistent splits 31 (K=5), max generation 4, merges 8, merge/split 0.111; moving tracks 118

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.1 only relabels time (world META dt 0.25): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 5 of 232 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
