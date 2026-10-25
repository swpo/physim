# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 352s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py --out /tmp/claude-0/c28eco/pack_sep --seeds 5 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.998], min area 6 px

## Measurements
- components: final 43, mean 43.6, max 57; occupancy final 0.27
- tracks: 1353; persistent (alive >= 50% of run): 21; longest 440 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.89 (1 = constant size)
- enclosures: components with a hole mean 1.49, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [58, 40, 29], H1 [1, 1, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.104/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 40, default): splits 289, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 334, merge/split ratio 1.16, nucleations 461
- channel total drift (end/start - 1): [20.005, 14.2401, 9.5301, 6.7949, 6.1396, 7.3472, -0.1254]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 480 at frame 282: holes 0, rim-vs-core 0.31, rim-vs-outside 0.62, heterogeneity 0.41; core [0.722, 0.646, 0.404, 0.591, 0.398, 0.638, 0.625] rim [0.539, 0.667, 0.26, 0.517, 0.552, 0.536, 0.665]
  - track 544 at frame 286: holes 0, rim-vs-core 0.55, rim-vs-outside 1.40, heterogeneity 0.29; core [0.974, 0.717, 0.432, 1.0, 0.842, 1.0, 0.717] rim [0.88, 0.979, 0.187, 0.692, 0.952, 0.75, 0.745]
  - track 559 at frame 290: holes 0, rim-vs-core 0.52, rim-vs-outside 0.81, heterogeneity 0.38; core [0.83, 0.735, 0.403, 0.788, 0.839, 0.863, 0.655] rim [0.586, 0.748, 0.182, 0.554, 0.702, 0.571, 0.691]
  - track 878 at frame 345: holes 0, rim-vs-core 0.55, rim-vs-outside 0.28, heterogeneity 0.11; core [0.0, 0.014, 0.015, 1.0, 0.454, 1.0, 0.861] rim [0.0, 0.082, 0.065, 1.0, 1.0, 1.0, 0.853]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 261 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.671, rim/outside 11.5 (aggregate of 261 individuals; 8/261 membrane-like individually; rim level 0.454)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.79 (aggregate of 261 individuals; 73/261 membrane-like individually; rim level 0.505)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.621, rim/outside 2.62 (aggregate of 261 individuals; 76/261 membrane-like individually; rim level 0.233)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 6.76 (aggregate of 261 individuals; 18/261 membrane-like individually; rim level 0.584)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 4.08 (aggregate of 261 individuals; 68/261 membrane-like individually; rim level 0.568)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 5.55 (aggregate of 261 individuals; 39/261 membrane-like individually; rim level 0.556)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.968 (aggregate of 261 individuals; 0/261 membrane-like individually; rim level 0.724)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #480 (t=564, R_eq 7.82): none; #544 (t=572, R_eq 6.86): ['A1', 'B1']; #559 (t=580, R_eq 7.38): ['A1']; #878 (t=690, R_eq 5.64): ['B1']
- species `A` (channels ['A0'], own threshold): components final 32, mean 28.0, max 34; tracks 213, persistent 30; splits 68, persistent splits 16 (K=20), max generation 3, merges 39, merge/split 0.574; moving tracks 1
- species `B` (channels ['B0'], own threshold): components final 55, mean 55.1, max 85; tracks 2631, persistent 29; splits 579, persistent splits 4 (K=20), max generation 2, merges 492, merge/split 0.85; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 261 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
