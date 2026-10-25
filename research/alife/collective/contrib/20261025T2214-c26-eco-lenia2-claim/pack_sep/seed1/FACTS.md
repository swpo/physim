# Evidence pack: eco-lenia2 (seed 1)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 235s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack_sep --seeds 0 1 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.998], min area 6 px

## Measurements
- components: final 45, mean 43.1, max 66; occupancy final 0.26
- tracks: 1329; persistent (alive >= 50% of run): 15; longest 438 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.21 (1 = constant size)
- enclosures: components with a hole mean 1.94, final 1; holes at thresholds 0.2/0.35/0.5 final [3, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [68, 38, 30], H1 [5, 1, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.13/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 40, default): splits 284, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 296, merge/split ratio 1.04, nucleations 470
- channel total drift (end/start - 1): [19.2274, 13.7749, 9.8762, 6.6723, 6.2341, 7.2025, -0.1149]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 467 at frame 282: holes 0, rim-vs-core 0.63, rim-vs-outside 0.72, heterogeneity 0.38; core [0.862, 0.754, 0.299, 0.798, 0.792, 0.882, 0.728] rim [0.616, 0.736, 0.171, 0.445, 0.617, 0.477, 0.761]
  - track 494 at frame 286: holes 0, rim-vs-core 0.46, rim-vs-outside 0.72, heterogeneity 0.39; core [0.813, 0.674, 0.395, 0.713, 0.602, 0.37, 0.743] rim [0.563, 0.72, 0.139, 0.564, 0.462, 0.555, 0.776]
  - track 422 at frame 265: holes 0, rim-vs-core 0.38, rim-vs-outside 0.64, heterogeneity 0.41; core [0.76, 0.63, 0.401, 0.64, 0.469, 0.745, 0.712] rim [0.571, 0.676, 0.192, 0.541, 0.57, 0.549, 0.741]
  - track 1081 at frame 403: holes 0, rim-vs-core 0.39, rim-vs-outside 0.59, heterogeneity 0.42; core [0.543, 0.318, 0.327, 0.458, 0.421, 0.49, 0.74] rim [0.5, 0.563, 0.072, 0.509, 0.567, 0.547, 0.75]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 256 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.679, rim/outside 11 (aggregate of 256 individuals; 16/256 membrane-like individually; rim level 0.432)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 4.15 (aggregate of 256 individuals; 63/256 membrane-like individually; rim level 0.486)
  - radial A2: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.637, rim/outside 2.28 (aggregate of 256 individuals; 71/256 membrane-like individually; rim level 0.217)
  - radial B0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 6.62 (aggregate of 256 individuals; 23/256 membrane-like individually; rim level 0.601)
  - radial B1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 3.42 (aggregate of 256 individuals; 74/256 membrane-like individually; rim level 0.584)
  - radial B2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 5.38 (aggregate of 256 individuals; 40/256 membrane-like individually; rim level 0.576)
  - radial F: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.973 (aggregate of 256 individuals; 0/256 membrane-like individually; rim level 0.717)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #467 (t=564, R_eq 7.44): none; #494 (t=572, R_eq 7.53): ['A1']; #422 (t=530, R_eq 7.57): ['A2']; #1081 (t=806, R_eq 8.35): ['A2']
- species `A` (channels ['A0'], own threshold): components final 30, mean 26.9, max 35; tracks 284, persistent 26; splits 87, persistent splits 15 (K=20), max generation 4, merges 55, merge/split 0.632; moving tracks 1
- species `B` (channels ['B0'], own threshold): components final 52, mean 58.4, max 92; tracks 3037, persistent 23; splits 618, persistent splits 3 (K=20), max generation 1, merges 558, merge/split 0.903; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 256 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
