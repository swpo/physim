# Evidence pack: cips-consumer (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 226s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/twin_nocons/seed1 --seeds 1 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0257, 1.1614], min area 6 px

## Measurements
- components: final 71, mean 70.7, max 76; occupancy final 0.30
- tracks: 148; persistent (alive >= 50% of run): 71; longest 121 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 19.50 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [71, 71, 71], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 26, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.346, nucleations 8
- channel total drift (end/start - 1): [0.2542, None, None, -0.7037]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.06; core [0.894, 0.0, 0.0, 0.038] rim [0.516, 0.0, 0.0, 0.099]
  - track 7 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.06; core [0.891, 0.0, 0.0, 0.041] rim [0.508, 0.0, 0.0, 0.098]
  - track 28 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.06; core [0.89, 0.0, 0.0, 0.039] rim [0.509, 0.0, 0.0, 0.099]
  - track 140 at frame 64: holes 0, rim-vs-core 0.35, rim-vs-outside 0.33, heterogeneity 0.06; core [0.9, 0.0, 0.0, 0.042] rim [0.554, 0.0, 0.0, 0.093]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 426 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 29.6 (aggregate of 426 individuals; 0/426 membrane-like individually; rim level 0.855)
  - radial consumer q: flat profile (no radial structure; level 0; aggregate of 426 individuals)
  - radial product r: flat profile (no radial structure; level 0; aggregate of 426 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.6, rim/outside 0.858 (aggregate of 426 individuals; 0/426 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 4.79): none; #7 (t=6100, R_eq 4.58): none; #28 (t=6100, R_eq 4.79): none; #140 (t=6400, R_eq 4.37): none
- species `prey` (channels ['prey a'], own threshold): components final 71, mean 70.7, max 76; tracks 148, persistent 71; splits 26, persistent splits 2 (K=5), max generation 1, merges 9, merge/split 0.346; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
