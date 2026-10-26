# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 20 steps x dt 0.1 = time 600; grid [160, 160]; wall 217s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out /tmp/claude-0/c28pa/om10 --seeds 5 --frames 300 --spf 20 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 51, mean 51.5, max 75; occupancy final 0.30
- tracks: 1938; persistent (alive >= 50% of run): 21; longest 283 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.50 (1 = constant size)
- enclosures: components with a hole mean 1.22, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [103, 73, 49], H1 [3, 1, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.397/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 40, default): splits 473, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 2, merges 441, merge/split ratio 0.932, nucleations 573
- channel total drift (end/start - 1): [9.3543, 7.0652, 5.3231, 6.5793, 6.245, 7.0832, -0.3438]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 127 at frame 156: holes 0, rim-vs-core 0.21, rim-vs-outside 1.18, heterogeneity 0.07; core [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.752] rim [0.0, 0.0, 0.0, 0.881, 1.0, 0.832, 0.777]
  - track 591 at frame 171: holes 0, rim-vs-core 0.31, rim-vs-outside 1.26, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.738, 1.0, 0.748] rim [0.0, 0.0, 0.0, 0.85, 1.0, 0.952, 0.772]
  - track 288 at frame 156: holes 0, rim-vs-core 0.18, rim-vs-outside 1.24, heterogeneity 0.10; core [0.0, 0.0, 0.0, 1.0, 0.909, 0.975, 0.697] rim [0.0, 0.0, 0.0, 0.862, 1.0, 0.905, 0.704]
  - track 1707 at frame 267: holes 0, rim-vs-core 0.15, rim-vs-outside 1.36, heterogeneity 0.08; core [0.0, 0.0, 0.0, 1.0, 0.997, 1.0, 0.633] rim [0.0, 0.0, 0.0, 0.923, 0.873, 0.991, 0.62]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 284 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.754, rim/outside 2.87 (aggregate of 284 individuals; 6/284 membrane-like individually; rim level 0.0946)
  - radial A1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 1.57 (aggregate of 284 individuals; 23/284 membrane-like individually; rim level 0.0998)
  - radial A2: peak at rho=1.35 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 1.14 (aggregate of 284 individuals; 29/284 membrane-like individually; rim level 0.0629)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 10.1 (aggregate of 284 individuals; 25/284 membrane-like individually; rim level 0.759)
  - radial B1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 5.41 (aggregate of 284 individuals; 137/284 membrane-like individually; rim level 0.703)  MEMBRANE-LIKE
  - radial B2: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 7.13 (aggregate of 284 individuals; 71/284 membrane-like individually; rim level 0.699)
  - radial F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 0.955 (aggregate of 284 individuals; 0/284 membrane-like individually; rim level 0.582)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): B1
- membrane-like channels per top track at mid-life: #127 (t=312, R_eq 6.56): none; #591 (t=342, R_eq 6.65): ['B1']; #288 (t=312, R_eq 6.51): none; #1707 (t=534, R_eq 6.6): ['A2', 'B1']
- species `A` (channels ['A0'], own threshold): components final 15, mean 7.5, max 18; tracks 147, persistent 2; splits 38, persistent splits 3 (K=20), max generation 1, merges 35, merge/split 0.921; moving tracks 6
- species `B` (channels ['B0'], own threshold): components final 54, mean 53.2, max 75; tracks 1594, persistent 32; splits 362, persistent splits 0 (K=20), max generation 0, merges 305, merge/split 0.843; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 284 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
