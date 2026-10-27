# Evidence pack: cips-fuel-turnover (seed 2)

- world: `../../20261026T2102-c48-cips-fuel-powered-division/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1100-c40-cips-layered-divide-claim; mutation: c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 597s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py --out collective/contrib/20261027T0458-c51-review-cips-fuel-division/pack_s2 --seeds 2 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0217, 0.975], min area 6 px

## Measurements
- components: final 15, mean 10.9, max 15; occupancy final 0.08
- tracks: 22; persistent (alive >= 50% of run): 10; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 15, 15], H1 [0, 0, 0]
- motion: 6 long-lived tracks moved >= 1 body length; max speed 0.00345/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0225, 0.5271, -0.0858, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 62: holes 0, rim-vs-core 0.43, rim-vs-outside 0.69, heterogeneity 0.17; core [0.978, 0.924, 0.071, 0.072] rim [0.811, 0.753, 0.173, 0.419]
  - track 5 at frame 63: holes 0, rim-vs-core 0.59, rim-vs-outside 0.63, heterogeneity 0.17; core [0.986, 0.951, 0.045, 0.084] rim [0.767, 0.698, 0.235, 0.534]
  - track 6 at frame 63: holes 0, rim-vs-core 0.54, rim-vs-outside 0.61, heterogeneity 0.16; core [0.98, 0.934, 0.044, 0.077] rim [0.78, 0.708, 0.218, 0.492]
  - track 18 at frame 102: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.17; core [0.989, 0.958, 0.056, 0.077] rim [0.782, 0.712, 0.24, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 71 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 35.7 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.869)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 12.6 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.837)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 27.2, rim/outside 0.645 (aggregate of 71 individuals; 0/71 membrane-like individually; rim level 0.488)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.64, rim/outside 19.2 (aggregate of 71 individuals; 66/71 membrane-like individually; rim level 0.507)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #1 (t=6200, R_eq 8.63): ['s']; #5 (t=6300, R_eq 7.94): ['s']; #6 (t=6300, R_eq 8.33): ['s']; #18 (t=10200, R_eq 7.4): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
