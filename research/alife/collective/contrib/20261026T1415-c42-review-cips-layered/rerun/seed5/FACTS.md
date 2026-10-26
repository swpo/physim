# Evidence pack: cips-layered-divide (seed 5)

- world: `../../../20261026T1100-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1517s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py --out collective/contrib/20261026T1415-c42-review-cips-layered/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0214, 0.9747], min area 6 px

## Measurements
- components: final 17, mean 12.0, max 17; occupancy final 0.09
- tracks: 29; persistent (alive >= 50% of run): 10; longest 164 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.00354/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 5
- channel total drift (end/start - 1): [0.0, -0.5864, 0.6334, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 119: holes 0, rim-vs-core 0.37, rim-vs-outside 0.78, heterogeneity 0.17; core [0.985, 0.94, 0.073, 0.077] rim [0.846, 0.791, 0.177, 0.363]
  - track 7 at frame 119: holes 0, rim-vs-core 0.56, rim-vs-outside 0.63, heterogeneity 0.17; core [0.986, 0.943, 0.044, 0.084] rim [0.773, 0.696, 0.232, 0.505]
  - track 8 at frame 119: holes 0, rim-vs-core 0.59, rim-vs-outside 0.60, heterogeneity 0.17; core [0.978, 0.925, 0.06, 0.077] rim [0.759, 0.69, 0.238, 0.535]
  - track 23 at frame 161: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.99, 0.957, 0.066, 0.076] rim [0.785, 0.712, 0.248, 0.48]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 77 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 34.9 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.876)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 12.8 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.839)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.8, rim/outside 0.655 (aggregate of 77 individuals; 0/77 membrane-like individually; rim level 0.497)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.71, rim/outside 20.2 (aggregate of 77 individuals; 71/77 membrane-like individually; rim level 0.538)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #5 (t=11900, R_eq 7.63): ['s']; #7 (t=11900, R_eq 8.16): ['s']; #8 (t=11900, R_eq 8.27): ['s']; #23 (t=16100, R_eq 7.4): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
