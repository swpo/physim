# Evidence pack: eco-lenia2 (seed 2)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 289s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack_s2 --seeds 2 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 38, mean 43.4, max 83; occupancy final 0.40
- tracks: 2610; persistent (alive >= 50% of run): 1; longest 373 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.27 (1 = constant size)
- enclosures: components with a hole mean 1.54, final 2; holes at thresholds 0.2/0.35/0.5 final [0, 2, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [119, 73, 34], H1 [11, 3, 1]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.56/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 40, default): splits 692, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 3, merges 637, merge/split ratio 0.921, nucleations 621
- channel total drift (end/start - 1): [18.039, 13.2423, 9.5458, 6.9857, 6.267, 7.6579, -0.3022]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1392 at frame 315: holes 0, rim-vs-core 0.21, rim-vs-outside 1.18, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 1.0, 0.931, 0.573] rim [0.015, 0.001, 0.0, 0.819, 0.978, 0.827, 0.601]
  - track 1890 at frame 382: holes 0, rim-vs-core 0.30, rim-vs-outside 1.18, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 1.0, 0.979, 0.55] rim [0.0, 0.0, 0.0, 0.793, 0.985, 0.77, 0.578]
  - track 1472 at frame 248: holes 0, rim-vs-core 0.30, rim-vs-outside 1.20, heterogeneity 0.13; core [0.0, 0.0, 0.0, 1.0, 0.78, 1.0, 0.66] rim [0.015, 0.0, 0.0, 0.788, 0.971, 0.917, 0.676]
  - track 1829 at frame 324: holes 0, rim-vs-core 0.19, rim-vs-outside 1.29, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.868, 1.0, 0.698] rim [0.0, 0.0, 0.0, 0.864, 1.0, 0.964, 0.717]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 206 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.662, rim/outside 3 (aggregate of 206 individuals; 17/206 membrane-like individually; rim level 0.222)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.6 (aggregate of 206 individuals; 39/206 membrane-like individually; rim level 0.261)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 1.06 (aggregate of 206 individuals; 54/206 membrane-like individually; rim level 0.138)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 4.13 (aggregate of 206 individuals; 42/206 membrane-like individually; rim level 0.521)
  - radial B1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.41, rim/outside 2.72 (aggregate of 206 individuals; 84/206 membrane-like individually; rim level 0.525)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 3.19 (aggregate of 206 individuals; 63/206 membrane-like individually; rim level 0.479)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.981 (aggregate of 206 individuals; 0/206 membrane-like individually; rim level 0.595)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1392 (t=630, R_eq 6.56): ['A0', 'B2']; #1890 (t=764, R_eq 6.58): none; #1472 (t=496, R_eq 6.75): ['B1']; #1829 (t=648, R_eq 6.72): ['B1']
- species `A` (channels ['A0'], own threshold): components final 28, mean 23.0, max 34; tracks 392, persistent 15; splits 105, persistent splits 10 (K=20), max generation 3, merges 67, merge/split 0.638; moving tracks 10
- species `B` (channels ['B0'], own threshold): components final 58, mean 53.9, max 81; tracks 1771, persistent 38; splits 408, persistent splits 5 (K=20), max generation 1, merges 340, merge/split 0.833; moving tracks 4

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 206 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
