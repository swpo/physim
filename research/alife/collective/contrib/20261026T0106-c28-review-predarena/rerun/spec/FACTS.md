# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 20 steps x dt 0.1 = time 600; grid [160, 160]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out /tmp/claude-0/c28pa/spec --seeds 5 --frames 300 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 32, mean 21.4, max 59; occupancy final 0.18
- tracks: 710; persistent (alive >= 50% of run): 0; longest 120 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [53, 35, 32], H1 [1, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.144/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 40, default): splits 220, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 5, merges 129, merge/split ratio 0.586, nucleations 153
- channel total drift (end/start - 1): [20.1499, 14.1249, 9.7343, None, None, None, -0.179]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 534 at frame 242: holes 0, rim-vs-core 0.51, rim-vs-outside 0.90, heterogeneity 0.15; core [1.0, 0.644, 0.452, 0.0, 0.0, 0.0, 0.658] rim [0.831, 1.0, 0.133, 0.0, 0.0, 0.0, 0.676]
  - track 550 at frame 245: holes 0, rim-vs-core 0.33, rim-vs-outside 0.94, heterogeneity 0.15; core [0.999, 0.7, 0.348, 0.0, 0.0, 0.0, 0.674] rim [0.813, 0.971, 0.32, 0.0, 0.0, 0.0, 0.697]
  - track 561 at frame 247: holes 0, rim-vs-core 0.27, rim-vs-outside 1.01, heterogeneity 0.15; core [1.0, 0.729, 0.339, 0.0, 0.0, 0.0, 0.72] rim [0.891, 0.913, 0.169, 0.0, 0.0, 0.0, 0.74]
  - track 685 at frame 265: holes 0, rim-vs-core 0.59, rim-vs-outside 1.13, heterogeneity 0.14; core [1.0, 0.672, 0.56, 0.0, 0.0, 0.0, 0.691] rim [0.94, 0.988, 0.069, 0.0, 0.0, 0.0, 0.717]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 133 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 46.3 (aggregate of 133 individuals; 1/133 membrane-like individually; rim level 0.9)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.34, rim/outside 8.92 (aggregate of 133 individuals; 96/133 membrane-like individually; rim level 0.874)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.489, rim/outside 3.9 (aggregate of 133 individuals; 13/133 membrane-like individually; rim level 0.302)
  - radial B0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 2.6 (aggregate of 133 individuals; 3/133 membrane-like individually; rim level 0.0473)
  - radial B1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.63 (aggregate of 133 individuals; 4/133 membrane-like individually; rim level 0.0342)
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 1.79 (aggregate of 133 individuals; 5/133 membrane-like individually; rim level 0.0374)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.898 (aggregate of 133 individuals; 0/133 membrane-like individually; rim level 0.581)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #534 (t=484, R_eq 6.89): ['A1']; #550 (t=490, R_eq 6.96): ['A1']; #561 (t=494, R_eq 6.86): ['A1']; #685 (t=530, R_eq 6.58): ['A1']
- species `A` (channels ['A0'], own threshold): components final 32, mean 19.1, max 34; tracks 401, persistent 0; splits 127, persistent splits 24 (K=20), max generation 5, merges 75, merge/split 0.591; moving tracks 3
- species `B` (channels ['B0'], own threshold): components final 0, mean 2.6, max 38; tracks 305, persistent 0; splits 88, persistent splits 0 (K=20), max generation 0, merges 42, merge/split 0.477; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 133 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
