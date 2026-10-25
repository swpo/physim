# Evidence pack: evoloop (seed 31)

- world: `../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T1447-c19-review-evoloop/rerun --seeds 31 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 35, mean 36.1, max 56; occupancy final 0.14
- tracks: 2675; persistent (alive >= 50% of run): 0; longest 44 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 3.07, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [3, 3, 3]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.0762/time; max body lengths 2.3
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1163, persistent splits 237 (0 more failed only because the siblings re-merged within K), max generation 29, merges 428, merge/split ratio 0.368, nucleations 82
- channel total drift (end/start - 1): [18.8547, 20.7099, 26.2667, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1614 at frame 145: holes 0, rim-vs-core 0.92, rim-vs-outside 1.36, heterogeneity 0.12; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.917, 0.0, 0.0]
  - track 729 at frame 82: holes 0, rim-vs-core 0.88, rim-vs-outside 1.33, heterogeneity 0.11; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.882, 0.0, 0.0]
  - track 2580 at frame 195: holes 0, rim-vs-core 0.66, rim-vs-outside 1.20, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.656, 0.09, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 236 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 4.32 (aggregate of 236 individuals; 128/236 membrane-like individually; rim level 0.308)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 3.11 (aggregate of 236 individuals; 146/236 membrane-like individually; rim level 0.0497)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.18 (aggregate of 236 individuals; 12/236 membrane-like individually; rim level 0.0023)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #2064 (t=18000, R_eq 1.6): ['sheath (state 2)']; #1614 (t=14500, R_eq 3.24): none; #729 (t=8200, R_eq 4.44): none; #2580 (t=19500, R_eq 10.78): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 66 of 236 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
