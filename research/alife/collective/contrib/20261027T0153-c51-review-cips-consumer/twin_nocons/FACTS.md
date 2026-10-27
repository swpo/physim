# Evidence pack: cips-consumer (seed 7)

- world: `../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 123s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T0153-c51-review-cips-consumer/twin_nocons --seeds 7 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0258, 1.1622], min area 6 px

## Measurements
- components: final 75, mean 74.3, max 78; occupancy final 0.30
- tracks: 135; persistent (alive >= 50% of run): 75; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 18.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 75, 75], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00069/time; max body lengths 1.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 19, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 8, merge/split ratio 0.421, nucleations 9
- channel total drift (end/start - 1): [0.2458, None, None, -0.7049]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 61: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.06; core [0.883, 0.0, 0.0, 0.04] rim [0.48, 0.0, 0.0, 0.101]
  - track 18 at frame 61: holes 0, rim-vs-core 0.37, rim-vs-outside 0.32, heterogeneity 0.06; core [0.889, 0.0, 0.0, 0.047] rim [0.518, 0.0, 0.0, 0.096]
  - track 29 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.29, heterogeneity 0.06; core [0.881, 0.0, 0.0, 0.042] rim [0.487, 0.0, 0.0, 0.099]
  - track 133 at frame 63: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.06; core [0.892, 0.0, 0.0, 0.037] rim [0.515, 0.0, 0.0, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 450 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 24.8 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.849)
  - radial consumer q: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial product r: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.58, rim/outside 0.863 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.146)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=6100, R_eq 4.85): none; #18 (t=6100, R_eq 4.18): none; #29 (t=6100, R_eq 4.65): none; #133 (t=6300, R_eq 4.75): none
- species `prey` (channels ['prey a'], own threshold): components final 75, mean 74.3, max 78; tracks 135, persistent 75; splits 19, persistent splits 1 (K=5), max generation 1, merges 8, merge/split 0.421; moving tracks 1
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
