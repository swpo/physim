# Evidence pack: evoloop (seed 2)

- world: `../../world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1256-c16-evoloop-claim/pack --seeds 1 2 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 42, mean 36.8, max 56; occupancy final 0.17
- tracks: 2698; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.09, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 45, 45], H1 [3, 3, 3]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.0645/time; max body lengths 2.9
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1161, persistent splits 218 (0 more failed only because the siblings re-merged within K), max generation 28, merges 467, merge/split ratio 0.402, nucleations 75
- channel total drift (end/start - 1): [22.8656, 25.1107, 29.8, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1681 at frame 146: holes 0, rim-vs-core 1.00, rim-vs-outside 1.41, heterogeneity 0.11; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 1.0, 0.0, 0.0]
  - track 879 at frame 91: holes 0, rim-vs-core 0.85, rim-vs-outside 1.34, heterogeneity 0.12; core [1.0, 0.042, 0.0, 0.0] rim [1.0, 0.892, 0.0, 0.0]
  - track 2444 at frame 188: holes 0, rim-vs-core 0.27, rim-vs-outside 1.14, heterogeneity 0.18; core [1.0, 0.284, 0.0, 0.0] rim [1.0, 0.521, 0.128, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.06, rim/outside 4.79 (aggregate of 231 individuals; 135/231 membrane-like individually; rim level 0.328)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.83, rim/outside 3.38 (aggregate of 231 individuals; 151/231 membrane-like individually; rim level 0.053)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 1.05 (aggregate of 231 individuals; 6/231 membrane-like individually; rim level 0.0009)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #1547 (t=13600, R_eq 1.6): ['sheath (state 2)']; #1681 (t=14600, R_eq 3.29): ['sheath (state 2)']; #879 (t=9100, R_eq 5.59, ring): none; #2444 (t=18800, R_eq 9.54): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 66 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
