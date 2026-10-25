# Evidence pack: evoloop (seed 5)

- world: `../../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 13s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T2100-c25-review-evoloop/rerun --seeds 4 5 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 35, mean 37.1, max 54; occupancy final 0.13
- tracks: 2773; persistent (alive >= 50% of run): 0; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 4.53, final 4; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 37, 37], H1 [4, 4, 4]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.0754/time; max body lengths 3.0
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1213, persistent splits 255 (0 more failed only because the siblings re-merged within K), max generation 28, merges 461, merge/split ratio 0.38, nucleations 76
- channel total drift (end/start - 1): [16.7766, 18.5305, 22.7333, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1517 at frame 131: holes 0, rim-vs-core 0.65, rim-vs-outside 1.19, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.646, 0.073, 0.0]
  - track 2718 at frame 198: holes 0, rim-vs-core 0.66, rim-vs-outside 1.20, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.656, 0.088, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 234 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.45, rim/outside 4.96 (aggregate of 234 individuals; 147/234 membrane-like individually; rim level 0.357)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.43, rim/outside 3.96 (aggregate of 234 individuals; 176/234 membrane-like individually; rim level 0.065)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 1.17 (aggregate of 234 individuals; 7/234 membrane-like individually; rim level 0.0023)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #1456 (t=13600, R_eq 1.87): none; #1517 (t=13100, R_eq 10.69): none; #1633 (t=13800, R_eq 8.54, ring): ['genome signals (states 3-7)']; #2718 (t=19800, R_eq 11.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 61 of 234 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
