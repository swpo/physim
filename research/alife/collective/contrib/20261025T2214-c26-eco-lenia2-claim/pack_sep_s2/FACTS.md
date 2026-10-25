# Evidence pack: eco-lenia2 (seed 2)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 298s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack_sep_s2 --seeds 2 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.998], min area 6 px

## Measurements
- components: final 46, mean 44.0, max 71; occupancy final 0.27
- tracks: 1075; persistent (alive >= 50% of run): 30; longest 484 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.35 (1 = constant size)
- enclosures: components with a hole mean 1.18, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [57, 45, 28], H1 [2, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.513/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 40, default): splits 238, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 252, merge/split ratio 1.06, nucleations 352
- channel total drift (end/start - 1): [18.7088, 13.4263, 9.6656, 6.9586, 6.3226, 7.7776, -0.1403]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 97 at frame 261: holes 0, rim-vs-core 0.21, rim-vs-outside 0.22, heterogeneity 0.07; core [0.0, 0.0, 0.02, 1.0, 0.795, 1.0, 0.853] rim [0.0, 0.0, 0.031, 1.0, 1.0, 1.0, 0.848]
  - track 486 at frame 282: holes 0, rim-vs-core 0.26, rim-vs-outside 0.70, heterogeneity 0.41; core [0.67, 0.649, 0.336, 0.597, 0.637, 0.634, 0.759] rim [0.561, 0.71, 0.14, 0.519, 0.619, 0.539, 0.786]
  - track 495 at frame 282: holes 0, rim-vs-core 0.57, rim-vs-outside 0.58, heterogeneity 0.40; core [0.821, 0.726, 0.493, 0.787, 0.566, 0.819, 0.744] rim [0.542, 0.776, 0.152, 0.515, 0.597, 0.583, 0.774]
  - track 838 at frame 353: holes 0, rim-vs-core 0.32, rim-vs-outside 0.55, heterogeneity 0.43; core [0.568, 0.538, 0.398, 0.5, 0.406, 0.495, 0.647] rim [0.516, 0.6, 0.107, 0.487, 0.517, 0.49, 0.675]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 266 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.681, rim/outside 7.99 (aggregate of 266 individuals; 13/266 membrane-like individually; rim level 0.404)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 3.44 (aggregate of 266 individuals; 51/266 membrane-like individually; rim level 0.452)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.773, rim/outside 2.12 (aggregate of 266 individuals; 94/266 membrane-like individually; rim level 0.218)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.54 (aggregate of 266 individuals; 13/266 membrane-like individually; rim level 0.628)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.82 (aggregate of 266 individuals; 87/266 membrane-like individually; rim level 0.598)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.828, rim/outside 7.02 (aggregate of 266 individuals; 25/266 membrane-like individually; rim level 0.623)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.972 (aggregate of 266 individuals; 0/266 membrane-like individually; rim level 0.684)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #97 (t=522, R_eq 5.73): ['B1']; #486 (t=564, R_eq 8): none; #495 (t=564, R_eq 7.27): ['A1']; #838 (t=706, R_eq 8.48): ['A2']
- species `A` (channels ['A0'], own threshold): components final 29, mean 26.4, max 35; tracks 300, persistent 29; splits 92, persistent splits 19 (K=20), max generation 5, merges 56, merge/split 0.609; moving tracks 5
- species `B` (channels ['B0'], own threshold): components final 48, mean 53.1, max 93; tracks 1847, persistent 35; splits 385, persistent splits 3 (K=20), max generation 1, merges 335, merge/split 0.87; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 266 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
