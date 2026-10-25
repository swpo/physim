# Evidence pack: evoloop (seed 51)

- world: `../../20261025T1457-c16-evoloop-not-open-ended/world.py`, family `cellular-automaton`
- parent: new class (Sayama 1999 evoloop; Langton 1984 loops); mutation: none (benchmark model); founder loop size m as a parameter
- run: 201 frames x 100 steps x dt 1.0 = time 20000; grid [300, 300]; wall 13s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1457-c16-evoloop-not-open-ended/world.py --out /home/user/physim/research/alife/collective/contrib/20261025T1636-c19-review-evoloop-oe/rerun --seeds 51 --frames 200 --spf 100 --lineage-k 3 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 41, mean 35.3, max 52; occupancy final 0.15
- tracks: 2699; persistent (alive >= 50% of run): 0; longest 45 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 2.96, final 3; holes at thresholds 0.2/0.35/0.5 final [3, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 44, 44], H1 [3, 3, 3]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0796/time; max body lengths 2.1
- replication (lineage window K = 3 frames = time 300, --lineage-k): splits 1156, persistent splits 200 (0 more failed only because the siblings re-merged within K), max generation 30, merges 464, merge/split ratio 0.401, nucleations 76
- channel total drift (end/start - 1): [25.5164, 21.6374, 26.3667, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1855 at frame 163: holes 0, rim-vs-core 0.66, rim-vs-outside 1.35, heterogeneity 0.10; core [1.0, 0.25, 0.0, 0.0] rim [1.0, 0.909, 0.0, 0.0]
  - track 1900 at frame 160: holes 0, rim-vs-core 0.27, rim-vs-outside 1.13, heterogeneity 0.18; core [1.0, 0.284, 0.0, 0.0] rim [1.0, 0.517, 0.129, 0.0]
  - track 2643 at frame 198: holes 0, rim-vs-core 0.62, rim-vs-outside 1.18, heterogeneity 0.18; core [1.0, 0.0, 0.0, 0.0] rim [1.0, 0.616, 0.083, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 228 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial sheath (state 2): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.23, rim/outside 4.81 (aggregate of 228 individuals; 147/228 membrane-like individually; rim level 0.331)  MEMBRANE-LIKE
  - radial genome signals (states 3-7): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2, rim/outside 3.28 (aggregate of 228 individuals; 161/228 membrane-like individually; rim level 0.0527)  MEMBRANE-LIKE
  - radial dissolution (state 8): peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 1.06 (aggregate of 228 individuals; 9/228 membrane-like individually; rim level 0.0012)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): sheath (state 2), genome signals (states 3-7)
- membrane-like channels per top track at mid-life: #1855 (t=16300, R_eq 2.88, ring): ['sheath (state 2)']; #1048 (t=10100, R_eq 6.96): ['genome signals (states 3-7)']; #1900 (t=16000, R_eq 9.52): ['sheath (state 2)', 'genome signals (states 3-7)']; #2643 (t=19800, R_eq 10.19): ['sheath (state 2)', 'genome signals (states 3-7)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 65 of 228 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
