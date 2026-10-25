# Evidence pack: eco-lenia2 (seed 3)

- world: `../../20261025T2214-c26-eco-lenia2-claim/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 437s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2214-c26-eco-lenia2-claim/world.py --out collective/contrib/20261025T2220-c21-review-ecolenia2/pack --seeds 3 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 39, mean 48.1, max 92; occupancy final 0.40
- tracks: 3445; persistent (alive >= 50% of run): 1; longest 313 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.19 (1 = constant size)
- enclosures: components with a hole mean 1.73, final 2; holes at thresholds 0.2/0.35/0.5 final [4, 2, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [123, 77, 38], H1 [16, 5, 2]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.0829/time; max body lengths 2.3
- replication (lineage window K = 20 frames = time 40, default): splits 866, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 5, merges 881, merge/split ratio 1.02, nucleations 877
- channel total drift (end/start - 1): [18.2995, 13.4319, 9.4293, 6.7015, 6.0025, 7.2512, -0.2992]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1767 at frame 345: holes 0, rim-vs-core 0.17, rim-vs-outside 1.23, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.942, 1.0, 0.575] rim [0.0, 0.016, 0.0, 0.88, 0.988, 0.884, 0.599]
  - track 1618 at frame 290: holes 0, rim-vs-core 0.20, rim-vs-outside 1.33, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.85, 1.0, 0.601] rim [0.0, 0.0, 0.0, 0.867, 1.0, 0.961, 0.619]
  - track 2379 at frame 403: holes 0, rim-vs-core 0.19, rim-vs-outside 1.23, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.995, 0.934, 0.61] rim [0.0, 0.0, 0.015, 0.825, 0.985, 0.871, 0.621]
  - track 3318 at frame 483: holes 0, rim-vs-core 0.60, rim-vs-outside 0.83, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 1.0, 0.831, 0.671] rim [0.0, 0.0, 0.0, 0.76, 1.0, 0.281, 0.673]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 217 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.65, rim/outside 3.52 (aggregate of 217 individuals; 29/217 membrane-like individually; rim level 0.22)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 1.86 (aggregate of 217 individuals; 48/217 membrane-like individually; rim level 0.259)
  - radial A2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 1.19 (aggregate of 217 individuals; 67/217 membrane-like individually; rim level 0.138)
  - radial B0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 4.24 (aggregate of 217 individuals; 47/217 membrane-like individually; rim level 0.499)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 2.48 (aggregate of 217 individuals; 72/217 membrane-like individually; rim level 0.507)
  - radial B2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 3.22 (aggregate of 217 individuals; 74/217 membrane-like individually; rim level 0.459)
  - radial F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.971 (aggregate of 217 individuals; 0/217 membrane-like individually; rim level 0.548)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1767 (t=690, R_eq 6.56): none; #1618 (t=580, R_eq 6.65): ['A2', 'B1']; #2379 (t=806, R_eq 6.56): none; #3318 (t=966, R_eq 2.65): none
- species `A` (channels ['A0'], own threshold): components final 28, mean 21.7, max 34; tracks 408, persistent 18; splits 112, persistent splits 12 (K=20), max generation 3, merges 89, merge/split 0.795; moving tracks 7
- species `B` (channels ['B0'], own threshold): components final 56, mean 57.5, max 92; tracks 2438, persistent 25; splits 515, persistent splits 11 (K=20), max generation 2, merges 482, merge/split 0.936; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 217 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
