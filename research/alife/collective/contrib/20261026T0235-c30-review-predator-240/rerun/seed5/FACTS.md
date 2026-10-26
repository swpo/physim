# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 30 steps x dt 0.1 = time 900; grid [240, 240]; wall 1593s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out collective/contrib/20261026T0235-c30-review-predator-240/rerun/seed5 --seeds 5 --frames 300 --spf 30 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 69, mean 48.5, max 73; occupancy final 0.18
- tracks: 1813; persistent (alive >= 50% of run): 5; longest 187 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.47 (1 = constant size)
- enclosures: components with a hole mean 0.65, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [136, 85, 68], H1 [3, 1, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.207/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 60, default): splits 602, persistent splits 62 (0 more failed only because the siblings re-merged within K), max generation 5, merges 271, merge/split ratio 0.45, nucleations 357
- channel total drift (end/start - 1): [45.1101, 32.0149, 23.2085, None, None, None, -0.1546]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 844 at frame 209: holes 0, rim-vs-core 0.24, rim-vs-outside 0.95, heterogeneity 0.14; core [0.998, 0.903, 0.403, 0.0, 0.0, 0.0, 0.637] rim [0.805, 0.877, 0.261, 0.0, 0.0, 0.0, 0.68]
  - track 871 at frame 209: holes 0, rim-vs-core 0.26, rim-vs-outside 0.89, heterogeneity 0.14; core [1.0, 0.951, 0.248, 0.0, 0.0, 0.0, 0.677] rim [0.826, 0.771, 0.205, 0.0, 0.0, 0.0, 0.702]
  - track 903 at frame 212: holes 0, rim-vs-core 0.40, rim-vs-outside 0.83, heterogeneity 0.15; core [0.998, 0.995, 0.312, 0.0, 0.0, 0.0, 0.599] rim [0.782, 0.698, 0.158, 0.0, 0.0, 0.0, 0.613]
  - track 1698 at frame 255: holes 0, rim-vs-core 0.43, rim-vs-outside 0.87, heterogeneity 0.16; core [1.0, 0.668, 0.451, 0.0, 0.0, 0.0, 0.687] rim [0.817, 1.0, 0.249, 0.0, 0.0, 0.0, 0.711]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 296 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.974, rim/outside 62.3 (aggregate of 296 individuals; 2/296 membrane-like individually; rim level 0.918)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.34, rim/outside 8.92 (aggregate of 296 individuals; 207/296 membrane-like individually; rim level 0.896)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.472, rim/outside 3.8 (aggregate of 296 individuals; 32/296 membrane-like individually; rim level 0.288)
  - radial B0: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 2.1 (aggregate of 296 individuals; 3/296 membrane-like individually; rim level 0.0327)
  - radial B1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.61 (aggregate of 296 individuals; 3/296 membrane-like individually; rim level 0.0332)
  - radial B2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.52 (aggregate of 296 individuals; 3/296 membrane-like individually; rim level 0.0322)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.2, rim/outside 0.901 (aggregate of 296 individuals; 0/296 membrane-like individually; rim level 0.591)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #844 (t=627, R_eq 7.11): ['A1']; #871 (t=627, R_eq 7.14): none; #903 (t=636, R_eq 7.38): none; #1698 (t=765, R_eq 6.96): ['A1']
- species `A` (channels ['A0'], own threshold): components final 69, mean 43.7, max 71; tracks 956, persistent 5; splits 341, persistent splits 62 (K=20), max generation 4, merges 132, merge/split 0.387; moving tracks 9
- species `B` (channels ['B0'], own threshold): components final 0, mean 5.1, max 34; tracks 868, persistent 0; splits 257, persistent splits 0 (K=20), max generation 0, merges 133, merge/split 0.518; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 296 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
