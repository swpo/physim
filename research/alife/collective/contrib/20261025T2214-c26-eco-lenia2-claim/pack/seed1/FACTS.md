# Evidence pack: eco-lenia2 (seed 1)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack --seeds 0 1 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9993], min area 6 px

## Measurements
- components: final 58, mean 53.1, max 76; occupancy final 0.39
- tracks: 3948; persistent (alive >= 50% of run): 1; longest 273 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.07 (1 = constant size)
- enclosures: components with a hole mean 1.94, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 6, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [107, 81, 48], H1 [19, 4, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.164/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 40, default): splits 1013, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 992, merge/split ratio 0.979, nucleations 993
- channel total drift (end/start - 1): [18.8037, 13.7917, 9.4068, 6.4271, 5.8075, 7.021, -0.3967]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2071 at frame 366: holes 0, rim-vs-core 0.39, rim-vs-outside 0.86, heterogeneity 0.39; core [0.392, 0.262, 0.299, 0.59, 0.314, 0.583, 0.636] rim [0.285, 0.33, 0.07, 0.553, 0.587, 0.649, 0.648]
  - track 2343 at frame 378: holes 0, rim-vs-core 0.28, rim-vs-outside 1.10, heterogeneity 0.12; core [0.0, 0.0, 0.0, 1.0, 0.917, 0.933, 0.599] rim [0.0, 0.006, 0.0, 0.789, 1.0, 0.763, 0.614]
  - track 589 at frame 139: holes 0, rim-vs-core 0.26, rim-vs-outside 1.30, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.782, 1.0, 0.707] rim [0.0, 0.0, 0.0, 0.871, 1.0, 0.955, 0.725]
  - track 3321 at frame 441: holes 0, rim-vs-core 0.39, rim-vs-outside 0.85, heterogeneity 0.12; core [0.0, 0.001, 0.0, 1.0, 1.0, 0.667, 0.744] rim [0.0, 0.001, 0.0, 0.803, 1.0, 0.332, 0.743]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 265 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.658, rim/outside 3.96 (aggregate of 265 individuals; 16/265 membrane-like individually; rim level 0.247)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 1.91 (aggregate of 265 individuals; 46/265 membrane-like individually; rim level 0.274)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.704, rim/outside 1.2 (aggregate of 265 individuals; 59/265 membrane-like individually; rim level 0.132)
  - radial B0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 3.88 (aggregate of 265 individuals; 62/265 membrane-like individually; rim level 0.503)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 2.22 (aggregate of 265 individuals; 87/265 membrane-like individually; rim level 0.503)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 2.84 (aggregate of 265 individuals; 92/265 membrane-like individually; rim level 0.466)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.974 (aggregate of 265 individuals; 0/265 membrane-like individually; rim level 0.519)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2071 (t=732, R_eq 11.53): ['B0', 'B2']; #2343 (t=756, R_eq 6.65): none; #589 (t=278, R_eq 6.63): ['B1']; #3321 (t=882, R_eq 2.52): ['B2']
- species `A` (channels ['A0'], own threshold): components final 29, mean 21.5, max 33; tracks 418, persistent 12; splits 124, persistent splits 13 (K=20), max generation 4, merges 80, merge/split 0.645; moving tracks 8
- species `B` (channels ['B0'], own threshold): components final 66, mean 61.3, max 78; tracks 2852, persistent 18; splits 644, persistent splits 17 (K=20), max generation 2, merges 561, merge/split 0.871; moving tracks 8

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 16 of 265 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
