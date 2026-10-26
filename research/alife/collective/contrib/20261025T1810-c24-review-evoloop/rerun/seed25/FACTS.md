# Evidence pack: evoloop (seed 25)

- world: `../../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 19s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1810-c24-review-evoloop/rerun/seed25 --seeds 25 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 46, mean 36.6, max 55; occupancy final 0.17
- tracks: 2656; persistent (alive >= 50% of run): 0; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.96, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 50, 50], H1 [3, 3, 3]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.0832/time; max body lengths 4.9
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1169, persistent splits 230 (0 more failed only because the siblings re-merged within K), max generation 29, merges 413, merge/split ratio 0.353, nucleations 72
- channel total drift (end/start - 1): [22.5063, 24.8817, 30.6333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2575 at frame 198: holes 0, rim-vs-core 0.66, rim-vs-outside 1.20, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.653, 0.095, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 241 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.43, rim/outside 5.08 (aggregate of 241 individuals; 152/241 membrane-like individually; rim level 0.351)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.4, rim/outside 3.88 (aggregate of 241 individuals; 172/241 membrane-like individually; rim level 0.063)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 1.16 (aggregate of 241 individuals; 12/241 membrane-like individually; rim level 0.0022)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #571 (t=8100, R_eq 1.38): none; #1947 (t=17600, R_eq 1.6): ['sheath (state 2)']; #294 (t=5700, R_eq 2.03): none; #2575 (t=19800, R_eq 10.09): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 241 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
