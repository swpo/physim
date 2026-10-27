# Evidence pack: cips-consumer (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 221s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/twin_nocons/seed0 --seeds 0 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0254, 1.1628], min area 6 px

## Measurements
- components: final 77, mean 76.3, max 77; occupancy final 0.30
- tracks: 174; persistent (alive >= 50% of run): 77; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 7.06 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [77, 77, 77], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 27, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.37, nucleations 12
- channel total drift (end/start - 1): [0.2063, None, None, -0.7071]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.31, heterogeneity 0.06; core [0.888, 0.0, 0.0, 0.039] rim [0.5, 0.0, 0.0, 0.096]
  - track 28 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.06; core [0.891, 0.0, 0.0, 0.038] rim [0.511, 0.0, 0.0, 0.095]
  - track 60 at frame 61: holes 0, rim-vs-core 0.29, rim-vs-outside 0.43, heterogeneity 0.06; core [0.904, 0.0, 0.0, 0.036] rim [0.616, 0.0, 0.0, 0.08]
  - track 172 at frame 67: holes 0, rim-vs-core 0.38, rim-vs-outside 0.31, heterogeneity 0.06; core [0.89, 0.0, 0.0, 0.045] rim [0.518, 0.0, 0.0, 0.094]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 462 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.858, rim/outside 26.7 (aggregate of 462 individuals; 0/462 membrane-like individually; rim level 0.849)
  - radial consumer q: flat profile (no radial structure; level 0; aggregate of 462 individuals)
  - radial product r: flat profile (no radial structure; level 0; aggregate of 462 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 7.96, rim/outside 0.867 (aggregate of 462 individuals; 0/462 membrane-like individually; rim level 0.143)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=6100, R_eq 4.58): none; #28 (t=6100, R_eq 4.58): none; #60 (t=6100, R_eq 4.62): none; #172 (t=6700, R_eq 4.18): none
- species `prey` (channels ['prey a'], own threshold): components final 77, mean 76.3, max 77; tracks 174, persistent 77; splits 27, persistent splits 7 (K=5), max generation 2, merges 10, merge/split 0.37; moving tracks 0
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
