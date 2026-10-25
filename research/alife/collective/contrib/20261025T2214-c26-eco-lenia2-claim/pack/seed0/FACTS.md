# Evidence pack: eco-lenia2 (seed 0)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 501 frames x 20 steps x dt 0.1 = time 1000; grid [160, 160]; wall 299s; status ok
- command: `python -m labkit.run collective/contrib/_c26work/le/world.py --out collective/contrib/_c26work/le/pack --seeds 0 1 --frames 500 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 43, mean 45.8, max 89; occupancy final 0.40
- tracks: 3170; persistent (alive >= 50% of run): 0; longest 195 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.80, final 1; holes at thresholds 0.2/0.35/0.5 final [4, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [110, 72, 34], H1 [14, 3, 1]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.166/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 40, default): splits 806, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 3, merges 803, merge/split ratio 0.996, nucleations 813
- channel total drift (end/start - 1): [18.7516, 13.4103, 9.7973, 6.7486, 6.2274, 7.3985, -0.3134]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 820 at frame 160: holes 0, rim-vs-core 0.19, rim-vs-outside 1.27, heterogeneity 0.10; core [0.0, 0.0, 0.0, 0.998, 1.0, 0.618, 0.449] rim [0.0, 0.0, 0.0, 0.842, 0.985, 0.719, 0.486]
  - track 1808 at frame 286: holes 0, rim-vs-core 0.22, rim-vs-outside 1.28, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.864, 1.0, 0.623] rim [0.0, 0.0, 0.0, 0.857, 1.0, 0.909, 0.639]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 211 components >= 12 px at frames [84, 168, 252, 332, 416, 500]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.513, rim/outside 2.94 (aggregate of 211 individuals; 17/211 membrane-like individually; rim level 0.17)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 1.71 (aggregate of 211 individuals; 29/211 membrane-like individually; rim level 0.217)
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 1.05 (aggregate of 211 individuals; 52/211 membrane-like individually; rim level 0.109)
  - radial B0: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 3.81 (aggregate of 211 individuals; 60/211 membrane-like individually; rim level 0.508)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 2.31 (aggregate of 211 individuals; 90/211 membrane-like individually; rim level 0.48)
  - radial B2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 2.91 (aggregate of 211 individuals; 94/211 membrane-like individually; rim level 0.444)
  - radial F: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.967 (aggregate of 211 individuals; 0/211 membrane-like individually; rim level 0.51)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #820 (t=320, R_eq 6.6): ['A2', 'B2']; #1808 (t=572, R_eq 6.65): ['B1']; #2373 (t=774, R_eq 1.38): ['B2']; #2648 (t=866, R_eq 1.87): none
- species `A` (channels ['A0'], own threshold): components final 32, mean 21.9, max 34; tracks 497, persistent 11; splits 132, persistent splits 7 (K=20), max generation 4, merges 108, merge/split 0.818; moving tracks 8
- species `B` (channels ['B0'], own threshold): components final 62, mean 58.7, max 93; tracks 2123, persistent 28; splits 451, persistent splits 5 (K=20), max generation 1, merges 399, merge/split 0.885; moving tracks 6

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 211 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
