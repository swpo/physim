# Evidence pack: eco-lenia2 (seed 5)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/eco-MIRd-Rplus; mutation: maintenance decay of all matter; no-interaction (separate food) twin; food forks
- run: 301 frames x 40 steps x dt 0.1 = time 1200; grid [256, 256]; wall 1528s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0003-c26-lenia-predator-arena/world.py --out /tmp/claude-0/c28ps/L256 --seeds 5 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.999], min area 6 px

## Measurements
- components: final 78, mean 66.0, max 81; occupancy final 0.18
- tracks: 610; persistent (alive >= 50% of run): 73; longest 261 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.57 (1 = constant size)
- enclosures: components with a hole mean 0.24, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [125, 91, 78], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.0239/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 80, default): splits 222, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 3, merges 77, merge/split ratio 0.347, nucleations 113
- channel total drift (end/start - 1): [51.1333, 37.0953, 26.3508, None, None, None, -0.1281]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 105 at frame 171: holes 0, rim-vs-core 0.28, rim-vs-outside 0.98, heterogeneity 0.16; core [0.971, 0.732, 0.393, 0.0, 0.0, 0.0, 0.724] rim [0.833, 0.934, 0.254, 0.0, 0.0, 0.0, 0.753]
  - track 132 at frame 171: holes 0, rim-vs-core 0.32, rim-vs-outside 0.94, heterogeneity 0.15; core [1.0, 0.761, 0.389, 0.0, 0.0, 0.0, 0.758] rim [0.852, 0.952, 0.184, 0.0, 0.0, 0.0, 0.785]
  - track 138 at frame 174: holes 0, rim-vs-core 0.39, rim-vs-outside 0.97, heterogeneity 0.15; core [1.0, 0.718, 0.393, 0.0, 0.0, 0.0, 0.751] rim [0.847, 0.983, 0.158, 0.0, 0.0, 0.0, 0.779]
  - track 500 at frame 192: holes 0, rim-vs-core 0.41, rim-vs-outside 0.85, heterogeneity 0.15; core [0.999, 0.866, 0.497, 0.0, 0.0, 0.0, 0.627] rim [0.774, 0.823, 0.158, 0.0, 0.0, 0.0, 0.659]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 438 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 74.1 (aggregate of 438 individuals; 2/438 membrane-like individually; rim level 0.972)
  - radial A1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 4.05, rim/outside 12.1 (aggregate of 438 individuals; 393/438 membrane-like individually; rim level 0.966)  MEMBRANE-LIKE
  - radial A2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.461, rim/outside 5.94 (aggregate of 438 individuals; 19/438 membrane-like individually; rim level 0.37)
  - radial B0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.61 (aggregate of 438 individuals; 2/438 membrane-like individually; rim level 0.0121)
  - radial B1: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 1.35 (aggregate of 438 individuals; 3/438 membrane-like individually; rim level 0.0121)
  - radial B2: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 1.32 (aggregate of 438 individuals; 5/438 membrane-like individually; rim level 0.011)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 0.93 (aggregate of 438 individuals; 0/438 membrane-like individually; rim level 0.715)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A1
- membrane-like channels per top track at mid-life: #105 (t=684, R_eq 7.11): ['A1']; #132 (t=684, R_eq 6.93): ['A1']; #138 (t=696, R_eq 6.86): ['A1']; #500 (t=768, R_eq 7.31): ['A1']
- species `A` (channels ['A0'], own threshold): components final 78, mean 65.5, max 81; tracks 515, persistent 73; splits 191, persistent splits 27 (K=20), max generation 3, merges 65, merge/split 0.34; moving tracks 6
- species `B` (channels ['B0'], own threshold): components final 0, mean 0.1, max 3; tracks 5, persistent 0; splits 2, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 438 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
