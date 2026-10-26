# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 20 steps x dt 0.1 = time 600; grid [160, 160]; wall 201s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out /tmp/claude-0/c28pa/comp --seeds 5 --frames 300 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9991], min area 6 px

## Measurements
- components: final 49, mean 48.1, max 83; occupancy final 0.37
- tracks: 2606; persistent (alive >= 50% of run): 1; longest 176 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 1.89, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [114, 75, 39], H1 [4, 1, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.112/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 40, default): splits 678, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 2, merges 632, merge/split ratio 0.932, nucleations 652
- channel total drift (end/start - 1): [17.0383, 12.3043, 9.3364, 6.444, 6.3413, 6.6927, -0.3753]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 677 at frame 131: holes 0, rim-vs-core 0.29, rim-vs-outside 1.29, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.726, 1.0, 0.719] rim [0.0, 0.0, 0.0, 0.922, 1.0, 0.958, 0.737]
  - track 830 at frame 124: holes 0, rim-vs-core 0.25, rim-vs-outside 1.26, heterogeneity 0.12; core [0.0, 0.0, 0.0, 1.0, 0.998, 0.489, 0.525] rim [0.0, 0.0, 0.0, 0.858, 0.921, 0.675, 0.564]
  - track 665 at frame 106: holes 0, rim-vs-core 0.20, rim-vs-outside 1.24, heterogeneity 0.09; core [0.0, 0.0, 0.0, 1.0, 0.85, 0.997, 0.616] rim [0.0, 0.0, 0.0, 0.89, 1.0, 0.925, 0.636]
  - track 2367 at frame 275: holes 0, rim-vs-core 0.34, rim-vs-outside 1.36, heterogeneity 0.11; core [0.0, 0.0, 0.0, 1.0, 0.683, 1.0, 0.666] rim [0.0, 0.0, 0.0, 0.852, 0.989, 0.97, 0.68]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.675, rim/outside 3.07 (aggregate of 231 individuals; 18/231 membrane-like individually; rim level 0.158)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 1.57 (aggregate of 231 individuals; 37/231 membrane-like individually; rim level 0.188)
  - radial A2: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 1.13 (aggregate of 231 individuals; 61/231 membrane-like individually; rim level 0.109)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.988, rim/outside 5.76 (aggregate of 231 individuals; 46/231 membrane-like individually; rim level 0.598)
  - radial B1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 3.14 (aggregate of 231 individuals; 95/231 membrane-like individually; rim level 0.544)
  - radial B2: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 3.88 (aggregate of 231 individuals; 76/231 membrane-like individually; rim level 0.53)
  - radial F: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.12, rim/outside 0.959 (aggregate of 231 individuals; 0/231 membrane-like individually; rim level 0.486)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #677 (t=262, R_eq 6.43): ['B1']; #830 (t=248, R_eq 6.7): ['B2']; #665 (t=212, R_eq 6.51): ['B1']; #2367 (t=550, R_eq 6.65): ['A2', 'B1']
- species `A` (channels ['A0'], own threshold): components final 27, mean 16.6, max 33; tracks 340, persistent 1; splits 100, persistent splits 10 (K=20), max generation 3, merges 61, merge/split 0.61; moving tracks 10
- species `B` (channels ['B0'], own threshold): components final 59, mean 57.4, max 82; tracks 1921, persistent 24; splits 446, persistent splits 2 (K=20), max generation 1, merges 364, merge/split 0.816; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
