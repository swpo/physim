# Evidence pack: evoloop (seed 21)

- world: `../orig/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 12s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27e/orig/world.py --out collective/contrib/wip-c27e/rerun --seeds 21 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 43, mean 35.9, max 56; occupancy final 0.16
- tracks: 2642; persistent (alive >= 50% of run): 0; longest 57 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.91, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 46, 46], H1 [4, 4, 4]
- motion: 30 long-lived tracks moved >= 1 body length; max speed 0.203/time; max body lengths 4.6
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1132, persistent splits 240 (0 more failed only because the siblings re-merged within K), max generation 29, merges 447, merge/split ratio 0.395, nucleations 88
- channel total drift (end/start - 1): [21.0453, 23.6183, 29.6333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1942 at frame 171: holes 0, rim-vs-core 1.00, rim-vs-outside 1.41, heterogeneity 0.11; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 1.0, 0.0, 0.0]
  - track 833 at frame 86: holes 0, rim-vs-core 0.60, rim-vs-outside 1.36, heterogeneity 0.21; core [1.0, 0.333, 0.167, 0.0] rim [1.0, 0.923, 0.077, 0.0]
  - track 2551 at frame 197: holes 0, rim-vs-core 0.67, rim-vs-outside 1.20, heterogeneity 0.19; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.659, 0.094, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 235 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.66, rim/outside 5.18 (aggregate of 235 individuals; 152/235 membrane-like individually; rim level 0.369)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.51, rim/outside 3.58 (aggregate of 235 individuals; 174/235 membrane-like individually; rim level 0.0604)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 1.17 (aggregate of 235 individuals; 8/235 membrane-like individually; rim level 0.0021)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #875 (t=10300, R_eq 1.95): ['sheath (state 2)']; #1942 (t=17100, R_eq 1.95): ['sheath (state 2)']; #833 (t=8600, R_eq 4.65): ['sheath (state 2)', 'genome signals (states 3-7)']; #2551 (t=19700, R_eq 11.4): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 56 of 235 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
