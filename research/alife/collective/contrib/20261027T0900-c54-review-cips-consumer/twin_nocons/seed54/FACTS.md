# Evidence pack: cips-consumer (seed 54)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 161s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0900-c54-review-cips-consumer/twin_nocons/seed54 --seeds 54 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0259, 1.1616], min area 6 px

## Measurements
- components: final 73, mean 72.1, max 73; occupancy final 0.30
- tracks: 147; persistent (alive >= 50% of run): 73; longest 121 frames; alive start-to-end: 4
- size of persistent tracks: max/min area ratio 13.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [73, 73, 73], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 27, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 11, merge/split ratio 0.407, nucleations 7
- channel total drift (end/start - 1): [0.2627, None, None, -0.7045]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.06; core [0.89, 0.0, 0.0, 0.038] rim [0.507, 0.0, 0.0, 0.1]
  - track 27 at frame 61: holes 0, rim-vs-core 0.41, rim-vs-outside 0.29, heterogeneity 0.06; core [0.883, 0.0, 0.0, 0.04] rim [0.477, 0.0, 0.0, 0.101]
  - track 33 at frame 61: holes 0, rim-vs-core 0.35, rim-vs-outside 0.32, heterogeneity 0.05; core [0.903, 0.0, 0.0, 0.035] rim [0.555, 0.0, 0.0, 0.094]
  - track 123 at frame 63: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.06; core [0.882, 0.0, 0.0, 0.04] rim [0.478, 0.0, 0.0, 0.102]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 438 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 28.8 (aggregate of 438 individuals; 0/438 membrane-like individually; rim level 0.854)
  - radial consumer q: flat profile (no radial structure; level 0; aggregate of 438 individuals)
  - radial product r: flat profile (no radial structure; level 0; aggregate of 438 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.12, rim/outside 0.86 (aggregate of 438 individuals; 0/438 membrane-like individually; rim level 0.148)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=6100, R_eq 4.89): none; #27 (t=6100, R_eq 4.79): none; #33 (t=6100, R_eq 4.69): none; #123 (t=6300, R_eq 4.85): none
- species `prey` (channels ['prey a'], own threshold): components final 73, mean 72.1, max 73; tracks 147, persistent 73; splits 27, persistent splits 7 (K=5), max generation 1, merges 11, merge/split 0.407; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
