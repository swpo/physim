# Evidence pack: cips-gene (seed 7)

- world: `../../20261026T2216-c48-cips-gene-selection-interim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1089s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2216-c48-cips-gene-selection-interim/world.py --out collective/contrib/c53-rev-gene/pack --seeds 7 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0203, 0.9764], min area 6 px

## Measurements
- components: final 13, mean 11.0, max 14; occupancy final 0.08
- tracks: 30; persistent (alive >= 50% of run): 9; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 13, 13], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00283/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0247, 0.5752, -0.0928, None, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 62: holes 0, rim-vs-core 0.55, rim-vs-outside 1.11, heterogeneity 0.11; core [0.982, 0.934, 0.054, 0.079, 1.0, 0.0] rim [0.779, 0.701, 0.235, 0.492, 0.999, 0.0]
  - track 8 at frame 74: holes 0, rim-vs-core 0.56, rim-vs-outside 1.17, heterogeneity 0.11; core [0.986, 0.944, 0.052, 0.082, 1.0, 0.0] rim [0.778, 0.7, 0.24, 0.495, 0.999, 0.0]
  - track 13 at frame 79: holes 0, rim-vs-core 0.55, rim-vs-outside 1.21, heterogeneity 0.10; core [0.988, 0.995, 0.002, 0.1, 0.001, 1.0] rim [0.79, 0.796, 0.128, 0.551, 0.001, 1.0]
  - track 24 at frame 110: holes 0, rim-vs-core 0.51, rim-vs-outside 1.18, heterogeneity 0.11; core [0.984, 0.937, 0.044, 0.081, 1.0, 0.0] rim [0.796, 0.714, 0.22, 0.456, 0.999, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 73 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 26.6 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.849)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 11 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.819)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 19.8, rim/outside 0.653 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.488)
  - radial s: peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.97, rim/outside 15.3 (aggregate of 73 individuals; 66/73 membrane-like individually; rim level 0.46)  MEMBRANE-LIKE
  - radial g1: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 59.6 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.821)
  - radial g2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.687, rim/outside 4.13 (aggregate of 73 individuals; 0/73 membrane-like individually; rim level 0.0582)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #3 (t=6200, R_eq 8.12): ['s']; #8 (t=7400, R_eq 7.98): ['s']; #13 (t=7900, R_eq 8.2): ['s']; #24 (t=11000, R_eq 8.1): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
