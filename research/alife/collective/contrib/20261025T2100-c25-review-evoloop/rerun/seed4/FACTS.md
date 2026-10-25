# Evidence pack: evoloop (seed 4)

- world: `../../../20261025T1256-c16-evoloop-claim/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 12s; status ok
- command: `python -m labkit.run /home/user/physim/research/alife/collective/contrib/20261025T1256-c16-evoloop-claim/world.py --out collective/contrib/20261025T2100-c25-review-evoloop/rerun --seeds 4 5 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 33, mean 36.7, max 55; occupancy final 0.14
- tracks: 2765; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.00, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 34, 34], H1 [2, 2, 2]
- motion: 18 long-lived tracks moved >= 1 body length; max speed 0.0708/time; max body lengths 2.7
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1199, persistent splits 247 (0 more failed only because the siblings re-merged within K), max generation 28, merges 458, merge/split ratio 0.382, nucleations 82
- channel total drift (end/start - 1): [18.1203, 19.874, 24.6667, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 834 at frame 89: holes 0, rim-vs-core 1.00, rim-vs-outside 1.41, heterogeneity 0.11; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 1.0, 0.0, 0.0]
  - track 1423 at frame 126: holes 1, rim-vs-core 0.83, rim-vs-outside 1.37, heterogeneity 0.18; core [1.0, 0.125, 0.188, 0.0] rim [1.0, 0.933, 0.0, 0.0]
  - track 2673 at frame 195: holes 0, rim-vs-core 0.66, rim-vs-outside 1.20, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.655, 0.087, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 240 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.15, rim/outside 4.73 (aggregate of 240 individuals; 145/240 membrane-like individually; rim level 0.338)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.95, rim/outside 3.53 (aggregate of 240 individuals; 157/240 membrane-like individually; rim level 0.0595)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 1.09 (aggregate of 240 individuals; 14/240 membrane-like individually; rim level 0.0014)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #834 (t=8900, R_eq 1.95): ['sheath (state 2)']; #1363 (t=12100, R_eq 1.78): none; #1423 (t=12600, R_eq 5.41, ring): ['sheath (state 2)', 'genome signals (states 3-7)']; #2673 (t=19500, R_eq 11.4): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 58 of 240 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
