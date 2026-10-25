# Evidence pack: evoloop (seed 1)

- world: `../../world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1256-c16-evoloop-claim/pack --seeds 1 2 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 44, mean 35.9, max 62; occupancy final 0.17
- tracks: 2732; persistent (alive >= 50% of run): 0; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.06, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 48, 48], H1 [3, 3, 3]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.0794/time; max body lengths 2.7
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1186, persistent splits 224 (0 more failed only because the siblings re-merged within K), max generation 27, merges 474, merge/split ratio 0.4, nucleations 65
- channel total drift (end/start - 1): [22.4062, 24.084, 28.7667, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2629 at frame 197: holes 0, rim-vs-core 0.67, rim-vs-outside 1.20, heterogeneity 0.19; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.659, 0.09, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 231 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.38, rim/outside 5.2 (aggregate of 231 individuals; 157/231 membrane-like individually; rim level 0.332)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.34, rim/outside 3.84 (aggregate of 231 individuals; 167/231 membrane-like individually; rim level 0.0591)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.19 (aggregate of 231 individuals; 12/231 membrane-like individually; rim level 0.0026)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #390 (t=6600, R_eq 1.78): ['sheath (state 2)']; #789 (t=8600, R_eq 1.6): ['sheath (state 2)']; #1726 (t=15000, R_eq 1.6): ['sheath (state 2)']; #2629 (t=19700, R_eq 11.73): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 59 of 231 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
