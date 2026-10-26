# Evidence pack: eco-lenia2 (seed 7)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 401 frames x 10 steps x dt 0.1 = time 400; grid [240, 240]; wall 406s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0228-c32-review-pred240/world.py --out collective/contrib/20261026T0228-c32-review-pred240/pack --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 49, mean 36.8, max 79; occupancy final 0.13
- tracks: 1477; persistent (alive >= 50% of run): 2; longest 236 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.41 (1 = constant size)
- enclosures: components with a hole mean 0.77, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 52, 49], H1 [2, 1, 1]
- motion: 19 long-lived tracks moved >= 1 body length; max speed 0.793/time; max body lengths 2.5
- replication (lineage window K = 20 frames = time 20, default): splits 496, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 6, merges 254, merge/split ratio 0.512, nucleations 253
- channel total drift (end/start - 1): [32.3362, 24.2552, 18.6686, None, None, None, -0.341]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 87 at frame 225: holes 0, rim-vs-core 0.53, rim-vs-outside 1.08, heterogeneity 0.14; core [1.0, 0.671, 0.496, 0.0, 0.0, 0.0, 0.586] rim [0.908, 0.995, 0.092, 0.0, 0.0, 0.0, 0.618]
  - track 186 at frame 289: holes 0, rim-vs-core 0.27, rim-vs-outside 0.95, heterogeneity 0.14; core [1.0, 0.994, 0.346, 0.0, 0.0, 0.0, 0.485] rim [0.815, 0.814, 0.258, 0.0, 0.0, 0.0, 0.517]
  - track 73 at frame 198: holes 0, rim-vs-core 0.30, rim-vs-outside 0.86, heterogeneity 0.14; core [1.0, 0.951, 0.198, 0.0, 0.0, 0.0, 0.641] rim [0.839, 0.708, 0.262, 0.0, 0.0, 0.0, 0.663]
  - track 1209 at frame 370: holes 0, rim-vs-core 0.40, rim-vs-outside 0.89, heterogeneity 0.15; core [1.0, 0.665, 0.365, 0.0, 0.0, 0.0, 0.534] rim [0.828, 0.977, 0.185, 0.0, 0.0, 0.0, 0.554]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 237 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 40.9 (aggregate of 237 individuals; 2/237 membrane-like individually; rim level 0.793)
  - radial A1: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.9, rim/outside 6.9 (aggregate of 237 individuals; 129/237 membrane-like individually; rim level 0.762)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.49, rim/outside 2.49 (aggregate of 237 individuals; 37/237 membrane-like individually; rim level 0.214)
  - radial B0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.63 (aggregate of 237 individuals; 11/237 membrane-like individually; rim level 0.107)
  - radial B1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 1.9 (aggregate of 237 individuals; 10/237 membrane-like individually; rim level 0.0849)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 1.93 (aggregate of 237 individuals; 12/237 membrane-like individually; rim level 0.08)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.37, rim/outside 0.857 (aggregate of 237 individuals; 0/237 membrane-like individually; rim level 0.466)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #87 (t=225, R_eq 6.75): ['A1']; #186 (t=289, R_eq 7.31): none; #73 (t=198, R_eq 7.11): none; #1209 (t=370, R_eq 6.93): ['A1']
- species `A` (channels ['A0'], own threshold): components final 49, mean 29.3, max 53; tracks 645, persistent 3; splits 206, persistent splits 30 (K=20), max generation 6, merges 109, merge/split 0.529; moving tracks 22
- species `B` (channels ['B0'], own threshold): components final 0, mean 8.1, max 34; tracks 814, persistent 0; splits 277, persistent splits 0 (K=20), max generation 0, merges 132, merge/split 0.477; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 237 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
