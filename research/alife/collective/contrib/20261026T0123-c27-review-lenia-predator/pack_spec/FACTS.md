# Evidence pack: eco-lenia2 (seed 3)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 101 frames x 40 steps x dt 0.1 = time 400; grid [160, 160]; wall 208s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27t/world.py --out collective/contrib/wip-c27t/pack_spec --seeds 3 --frames 100 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 0, mean 13.2, max 53; occupancy final 0.00
- tracks: 358; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.37, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.181/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 80, default): splits 119, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 58, merge/split ratio 0.487, nucleations 71
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None, None, None, -0.006]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 41: holes 0, rim-vs-core 0.35, rim-vs-outside 0.93, heterogeneity 0.14; core [1.0, 0.737, 0.348, 0.0, 0.0, 0.0, 0.464] rim [0.821, 0.999, 0.2, 0.0, 0.0, 0.0, 0.484]
  - track 60 at frame 52: holes 0, rim-vs-core 0.56, rim-vs-outside 0.96, heterogeneity 0.15; core [1.0, 0.683, 0.583, 0.0, 0.0, 0.0, 0.57] rim [0.907, 1.0, 0.135, 0.0, 0.0, 0.0, 0.597]
  - track 39 at frame 44: holes 0, rim-vs-core 0.32, rim-vs-outside 0.96, heterogeneity 0.14; core [1.0, 0.712, 0.235, 0.0, 0.0, 0.0, 0.554] rim [0.833, 0.959, 0.128, 0.0, 0.0, 0.0, 0.582]
  - track 59 at frame 51: holes 0, rim-vs-core 0.28, rim-vs-outside 0.96, heterogeneity 0.15; core [1.0, 0.757, 0.405, 0.0, 0.0, 0.0, 0.626] rim [0.864, 0.895, 0.197, 0.0, 0.0, 0.0, 0.641]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 70 components >= 12 px at frames [17, 33, 50, 67]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 28.4 (aggregate of 70 individuals; 4/70 membrane-like individually; rim level 0.713)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.93, rim/outside 6.72 (aggregate of 70 individuals; 36/70 membrane-like individually; rim level 0.714)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.504, rim/outside 2.25 (aggregate of 70 individuals; 15/70 membrane-like individually; rim level 0.197)
  - radial B0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.96 (aggregate of 70 individuals; 5/70 membrane-like individually; rim level 0.152)
  - radial B1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 1.76 (aggregate of 70 individuals; 4/70 membrane-like individually; rim level 0.137)
  - radial B2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 2.24 (aggregate of 70 individuals; 8/70 membrane-like individually; rim level 0.118)  MEMBRANE-LIKE
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.845 (aggregate of 70 individuals; 0/70 membrane-like individually; rim level 0.443)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1, B2
- membrane-like channels per top track at mid-life: #29 (t=164, R_eq 6.82): ['A1']; #60 (t=208, R_eq 6.75): ['A1']; #39 (t=176, R_eq 6.96): ['A1']; #59 (t=204, R_eq 6.96): ['A1']
- species `A` (channels ['A0'], own threshold): components final 0, mean 9.5, max 31; tracks 159, persistent 0; splits 60, persistent splits 4 (K=20), max generation 1, merges 21, merge/split 0.35; moving tracks 2
- species `B` (channels ['B0'], own threshold): components final 0, mean 4.4, max 41; tracks 207, persistent 0; splits 54, persistent splits 0 (K=20), max generation 0, merges 32, merge/split 0.593; moving tracks 0

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 70 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
