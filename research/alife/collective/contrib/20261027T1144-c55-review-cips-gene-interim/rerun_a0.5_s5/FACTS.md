# Evidence pack: cips-gene (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2216-c48-cips-gene-selection-interim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 101 frames x 1000 steps x dt 0.1 = time 10000; grid [192, 192]; wall 793s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2216-c48-cips-gene-selection-interim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/gene/pack_a0.5 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0201, 0.9755], min area 6 px

## Measurements
- components: final 9, mean 8.3, max 11; occupancy final 0.06
- tracks: 20; persistent (alive >= 50% of run): 7; longest 98 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 9, 9], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00302/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0184, 0.4003, -0.067, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 52: holes 0, rim-vs-core 0.57, rim-vs-outside 1.16, heterogeneity 0.11; core [0.984, 0.937, 0.039, 0.09, 0.999, 0.0] rim [0.774, 0.693, 0.228, 0.519, 0.999, 0.0]
  - track 6 at frame 67: holes 0, rim-vs-core 0.56, rim-vs-outside 1.15, heterogeneity 0.12; core [0.986, 0.946, 0.042, 0.087, 0.999, 0.0] rim [0.778, 0.706, 0.227, 0.511, 0.999, 0.0]
  - track 8 at frame 69: holes 0, rim-vs-core 0.55, rim-vs-outside 1.14, heterogeneity 0.11; core [0.984, 0.939, 0.051, 0.079, 1.0, 0.0] rim [0.783, 0.705, 0.231, 0.495, 0.999, 0.0]
  - track 10 at frame 70: holes 0, rim-vs-core 0.34, rim-vs-outside 1.24, heterogeneity 0.11; core [0.984, 0.934, 0.071, 0.08, 0.999, 0.0] rim [0.856, 0.801, 0.163, 0.356, 0.998, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 51 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 21.5 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.811)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.856, rim/outside 10.6 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.802)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 18.4, rim/outside 0.641 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.482)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.17, rim/outside 13.2 (aggregate of 51 individuals; 42/51 membrane-like individually; rim level 0.456)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.865, rim/outside 37.9 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.719)
  - radial g2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 8.1 (aggregate of 51 individuals; 0/51 membrane-like individually; rim level 0.115)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #4 (t=5200, R_eq 8.33): ['s']; #6 (t=6700, R_eq 8.18): ['s']; #8 (t=6900, R_eq 8): ['s']; #10 (t=7000, R_eq 7.74): ['s']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
