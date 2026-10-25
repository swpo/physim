# Evidence pack: eco-lenia2 (seed 3)

- world: `../../20261025T2214-c26-eco-lenia2-claim/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 443s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py --out collective/contrib/20261025T2220-c21-review-ecolenia2/pack_sep --seeds 3 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.998], min area 6 px

## Measurements
- components: final 44, mean 44.3, max 55; occupancy final 0.29
- tracks: 1172; persistent (alive >= 50% of run): 24; longest 441 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.22 (1 = constant size)
- enclosures: components with a hole mean 1.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 44, 25], H1 [1, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.19/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 40, default): splits 290, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 286, merge/split ratio 0.986, nucleations 337
- channel total drift (end/start - 1): [19.5558, 14.0377, 9.6579, 7.0647, 5.9979, 7.9846, -0.1417]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 450 at frame 282: holes 0, rim-vs-core 0.51, rim-vs-outside 0.78, heterogeneity 0.39; core [0.813, 0.671, 0.437, 0.78, 0.816, 0.843, 0.747] rim [0.597, 0.726, 0.164, 0.571, 0.681, 0.578, 0.777]
  - track 462 at frame 286: holes 1, rim-vs-core 0.58, rim-vs-outside 0.63, heterogeneity 0.42; core [0.514, 0.483, 0.195, 0.744, 0.498, 0.769, 0.66] rim [0.647, 0.648, 0.243, 0.369, 0.402, 0.395, 0.64]
  - track 500 at frame 286: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.15; core [0.006, 0.162, 0.077, 1.0, 0.454, 1.0, 0.692] rim [0.0, 0.112, 0.043, 0.995, 1.0, 1.0, 0.698]
  - track 1096 at frame 450: holes 0, rim-vs-core 0.52, rim-vs-outside 0.24, heterogeneity 0.13; core [0.0, 0.033, 0.0, 1.0, 0.496, 1.0, 0.787] rim [0.0, 0.066, 0.131, 0.989, 1.0, 1.0, 0.782]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 264 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.652, rim/outside 6.15 (aggregate of 264 individuals; 11/264 membrane-like individually; rim level 0.369)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 2.93 (aggregate of 264 individuals; 48/264 membrane-like individually; rim level 0.416)
  - radial A2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 2.09 (aggregate of 264 individuals; 83/264 membrane-like individually; rim level 0.22)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 7.09 (aggregate of 264 individuals; 13/264 membrane-like individually; rim level 0.598)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 3.89 (aggregate of 264 individuals; 84/264 membrane-like individually; rim level 0.558)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 5.65 (aggregate of 264 individuals; 22/264 membrane-like individually; rim level 0.598)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.974 (aggregate of 264 individuals; 0/264 membrane-like individually; rim level 0.685)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #450 (t=564, R_eq 7.31): ['A1']; #462 (t=572, R_eq 8.14): none; #500 (t=572, R_eq 5.73): ['B1']; #1096 (t=900, R_eq 5.56): ['B1']
- species `A` (channels ['A0'], own threshold): components final 31, mean 27.1, max 36; tracks 321, persistent 24; splits 100, persistent splits 12 (K=20), max generation 4, merges 62, merge/split 0.62; moving tracks 3
- species `B` (channels ['B0'], own threshold): components final 51, mean 51.1, max 82; tracks 1690, persistent 35; splits 364, persistent splits 4 (K=20), max generation 1, merges 311, merge/split 0.854; moving tracks 6

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 264 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
