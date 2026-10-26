# Evidence pack: cips-layered-chemostat (seed 0)

- world: `../world_wash.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c44: initial noise 0.03 -> 0.02 (fewer nucleations); otherwise c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 301 frames x 1000 steps x dt 0.1 = time 30000; grid [192, 192]; wall 2041s; status ok
- command: `python -m labkit.run world_wash.py --out W800 --seeds 0 --frames 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0212, 0.9755], min area 6 px

## Measurements
- components: final 9, mean 10.3, max 15; occupancy final 0.05
- tracks: 58; persistent (alive >= 50% of run): 1; longest 194 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.16 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 9, 9], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.00362/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 26, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 4, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.017, -0.6807, 0.7343, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 134: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.16; core [0.986, 0.955, 0.046, 0.084] rim [0.776, 0.709, 0.231, 0.508]
  - track 9 at frame 111: holes 0, rim-vs-core 0.58, rim-vs-outside 0.59, heterogeneity 0.17; core [0.975, 0.928, 0.045, 0.085] rim [0.758, 0.7, 0.221, 0.538]
  - track 10 at frame 111: holes 0, rim-vs-core 0.38, rim-vs-outside 0.75, heterogeneity 0.16; core [0.986, 0.954, 0.038, 0.087] rim [0.846, 0.785, 0.165, 0.364]
  - track 46 at frame 272: holes 0, rim-vs-core 0.57, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.951, 0.043, 0.085] rim [0.772, 0.701, 0.228, 0.513]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 69 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.917, rim/outside 41.4 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.905)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 13.1 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.863)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 30.1, rim/outside 0.652 (aggregate of 69 individuals; 0/69 membrane-like individually; rim level 0.481)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.25, rim/outside 21.7 (aggregate of 69 individuals; 67/69 membrane-like individually; rim level 0.537)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #11 (t=13400, R_eq 8.04): ['s']; #9 (t=11100, R_eq 8.74): ['s']; #10 (t=11100, R_eq 8.14): ['s']; #46 (t=27200, R_eq 8.08): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
