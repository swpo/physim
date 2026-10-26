# Evidence pack: eco-lenia2-dt (seed 3)

- world: `../world_dt.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 401 frames x 20 steps x dt 0.05 (--dt; world META dt 0.1) = time 400; grid [160, 160]; wall 218s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0045-c32-review-ecolenia-dthalf/world_dt.py --out collective/contrib/20261026T0045-c32-review-ecolenia-dthalf/rerun_dt005 --seeds 3 --frames 400 --spf 20 --dt 0.05 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9995], min area 6 px

## Measurements
- components: final 38, mean 50.9, max 85; occupancy final 0.34
- tracks: 2043; persistent (alive >= 50% of run): 5; longest 318 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.36 (1 = constant size)
- enclosures: components with a hole mean 2.62, final 2; holes at thresholds 0.2/0.35/0.5 final [1, 2, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [96, 58, 41], H1 [3, 3, 1]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.374/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 20, default): splits 526, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 506, merge/split ratio 0.962, nucleations 479
- channel total drift (end/start - 1): [12.6676, 9.8736, 7.2679, 6.5783, 6.0532, 7.4423, -0.4329]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 681 at frame 242: holes 0, rim-vs-core 0.62, rim-vs-outside 1.34, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.387, 0.998, 0.68] rim [0.0, 0.0, 0.0, 0.89, 1.0, 0.983, 0.7]
  - track 776 at frame 242: holes 0, rim-vs-core 0.27, rim-vs-outside 1.21, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.797, 1.0, 0.672] rim [0.0, 0.0, 0.0, 0.847, 1.0, 0.923, 0.694]
  - track 990 at frame 262: holes 0, rim-vs-core 0.29, rim-vs-outside 1.33, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.76, 1.0, 0.736] rim [0.0, 0.0, 0.0, 0.832, 1.0, 0.991, 0.754]
  - track 1712 at frame 346: holes 0, rim-vs-core 0.30, rim-vs-outside 1.11, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.91, 1.0, 0.615] rim [0.0, 0.0, 0.0, 0.809, 1.0, 0.789, 0.637]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 268 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.653, rim/outside 3.11 (aggregate of 268 individuals; 13/268 membrane-like individually; rim level 0.101)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 1.72 (aggregate of 268 individuals; 23/268 membrane-like individually; rim level 0.12)
  - radial A2: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 1.2 (aggregate of 268 individuals; 59/268 membrane-like individually; rim level 0.0814)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 6.61 (aggregate of 268 individuals; 44/268 membrane-like individually; rim level 0.652)
  - radial B1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.53 (aggregate of 268 individuals; 105/268 membrane-like individually; rim level 0.595)
  - radial B2: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 4.68 (aggregate of 268 individuals; 76/268 membrane-like individually; rim level 0.556)
  - radial F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.93 (aggregate of 268 individuals; 0/268 membrane-like individually; rim level 0.481)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #681 (t=242, R_eq 6.48): ['B1']; #776 (t=242, R_eq 6.58): ['B1']; #990 (t=262, R_eq 6.6): ['B1']; #1712 (t=346, R_eq 6.65): ['B1']
- species `A` (channels ['A0'], own threshold): components final 20, mean 12.2, max 23; tracks 274, persistent 0; splits 77, persistent splits 5 (K=20), max generation 2, merges 55, merge/split 0.714; moving tracks 7
- species `B` (channels ['B0'], own threshold): components final 48, mean 58.4, max 92; tracks 1565, persistent 22; splits 370, persistent splits 13 (K=20), max generation 3, merges 337, merge/split 0.911; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 18 of 268 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
