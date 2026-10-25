# Evidence pack: evoloop (seed 7)

- world: `../../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1336-c09-review-evoloop/rerun --seeds 6 7 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 34, mean 36.2, max 56; occupancy final 0.12
- tracks: 2742; persistent (alive >= 50% of run): 0; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.28, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 36, 36], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.26/time; max body lengths 3.4
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1186, persistent splits 234 (0 more failed only because the siblings re-merged within K), max generation 35, merges 467, merge/split ratio 0.394, nucleations 73
- channel total drift (end/start - 1): [16.3563, 16.8359, 20.8667, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2210 at frame 176: holes 0, rim-vs-core 0.21, rim-vs-outside 1.13, heterogeneity 0.18; core [1.0, 0.331, 0.0, 0.0] rim [1.0, 0.51, 0.1, 0.0]
  - track 2645 at frame 195: holes 0, rim-vs-core 0.66, rim-vs-outside 1.20, heterogeneity 0.20; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.65, 0.106, 0.003]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 230 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 3.82, rim/outside 6.09 (aggregate of 230 individuals; 167/230 membrane-like individually; rim level 0.419)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.86, rim/outside 4.42 (aggregate of 230 individuals; 182/230 membrane-like individually; rim level 0.0774)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.07 (aggregate of 230 individuals; 2/230 membrane-like individually; rim level 0.0009)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #2017 (t=17600, R_eq 1.6): ['sheath (state 2)']; #2210 (t=17600, R_eq 8.39): ['sheath (state 2)', 'genome signals (states 3-7)']; #1631 (t=13400, R_eq 1.6): ['sheath (state 2)']; #2645 (t=19500, R_eq 11.73): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 41 of 230 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
