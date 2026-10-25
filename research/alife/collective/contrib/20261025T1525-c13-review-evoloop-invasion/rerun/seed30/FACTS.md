# Evidence pack: evoloop (seed 30)

- world: `../../world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1525-c13-review-evoloop-invasion/world.py --out collective/contrib/20261025T1525-c13-review-evoloop-invasion/rerun/seed30 --seeds 30 --spf 100 --frames 200 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 42, mean 37.4, max 62; occupancy final 0.17
- tracks: 2808; persistent (alive >= 50% of run): 0; longest 43 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.38, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 49], H1 [1, 1, 1]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.0826/time; max body lengths 3.9
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1205, persistent splits 248 (0 more failed only because the siblings re-merged within K), max generation 27, merges 511, merge/split ratio 0.424, nucleations 83
- channel total drift (end/start - 1): [23.0266, 24.0916, 29.4, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1046 at frame 99: holes 0, rim-vs-core 0.39, rim-vs-outside 1.16, heterogeneity 0.12; core [1.0, 0.185, 0.0, 0.0] rim [1.0, 0.579, 0.0, 0.0]
  - track 361 at frame 50: holes 0, rim-vs-core 0.54, rim-vs-outside 1.31, heterogeneity 0.12; core [1.0, 0.3, 0.0, 0.0] rim [1.0, 0.84, 0.0, 0.0]
  - track 2587 at frame 190: holes 0, rim-vs-core 0.21, rim-vs-outside 1.15, heterogeneity 0.17; core [1.0, 0.356, 0.0, 0.0] rim [1.0, 0.557, 0.066, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 2.46, rim/outside 5.11 (aggregate of 247 individuals; 163/247 membrane-like individually; rim level 0.348)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.43, rim/outside 3.92 (aggregate of 247 individuals; 185/247 membrane-like individually; rim level 0.0618)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 1.08 (aggregate of 247 individuals; 9/247 membrane-like individually; rim level 0.0013)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #1462 (t=12900, R_eq 1.6): ['sheath (state 2)']; #1046 (t=9900, R_eq 6.23): ['sheath (state 2)']; #361 (t=5000, R_eq 3.34): none; #2587 (t=19000, R_eq 8.43): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 57 of 247 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
