# Evidence pack: cips-layered-divide (seed 13)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 566s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T2036-c46-review-moat-cut/rerun/seed13 --seeds 13 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0204, 0.977], min area 6 px

## Measurements
- components: final 19, mean 12.1, max 19; occupancy final 0.09
- tracks: 32; persistent (alive >= 50% of run): 5; longest 89 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.51 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [19, 19, 19], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00358/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 13, persistent splits 13 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [0.0, -0.5738, 0.6199, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 77: holes 0, rim-vs-core 0.55, rim-vs-outside 0.60, heterogeneity 0.16; core [0.974, 0.913, 0.056, 0.074] rim [0.766, 0.699, 0.219, 0.508]
  - track 10 at frame 79: holes 0, rim-vs-core 0.55, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.945, 0.046, 0.081] rim [0.783, 0.703, 0.231, 0.487]
  - track 13 at frame 80: holes 0, rim-vs-core 0.54, rim-vs-outside 0.62, heterogeneity 0.16; core [0.986, 0.946, 0.048, 0.079] rim [0.784, 0.703, 0.233, 0.481]
  - track 18 at frame 99: holes 0, rim-vs-core 0.32, rim-vs-outside 0.79, heterogeneity 0.16; core [0.984, 0.937, 0.072, 0.076] rim [0.864, 0.807, 0.162, 0.326]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 37.1 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.89)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 12.7 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.846)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 25.1, rim/outside 0.652 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.491)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.21, rim/outside 22.2 (aggregate of 81 individuals; 75/81 membrane-like individually; rim level 0.577)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #8 (t=7700, R_eq 8.83): ['s']; #10 (t=7900, R_eq 7.88): ['s']; #13 (t=8000, R_eq 7.82): ['s']; #18 (t=9900, R_eq 7.55): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
