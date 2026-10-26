# Evidence pack: cips-consumer (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 370s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/pack_na1/seed0 --seeds 0 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0371, 1.9954], min area 6 px

## Measurements
- components: final 38, mean 39.9, max 82; occupancy final 0.20
- tracks: 991; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 40, 34], H1 [0, 0, 0]
- motion: 127 long-lived tracks moved >= 1 body length; max speed 0.0212/time; max body lengths 4.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 441, persistent splits 87 (0 more failed only because the siblings re-merged within K), max generation 9, merges 15, merge/split ratio 0.034, nucleations 75
- channel total drift (end/start - 1): [-0.0026, -0.0056, None, -0.5939]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 423 at frame 58: holes 0, rim-vs-core 0.47, rim-vs-outside 0.39, heterogeneity 0.29; core [0.746, 0.57, 0.599, 0.149] rim [0.443, 0.483, 0.264, 0.227]
  - track 103 at frame 15: holes 0, rim-vs-core 0.31, rim-vs-outside 0.56, heterogeneity 0.27; core [0.841, 0.403, 0.472, 0.083] rim [0.613, 0.375, 0.271, 0.142]
  - track 194 at frame 27: holes 0, rim-vs-core 0.30, rim-vs-outside 0.59, heterogeneity 0.27; core [0.86, 0.385, 0.468, 0.081] rim [0.623, 0.411, 0.309, 0.154]
  - track 811 at frame 102: holes 0, rim-vs-core 0.24, rim-vs-outside 0.54, heterogeneity 0.16; core [0.927, 0.025, 0.007, 0.01] rim [0.8, 0.151, 0.151, 0.078]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 233 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 9.75 (aggregate of 233 individuals; 18/233 membrane-like individually; rim level 0.65)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 9.36 (aggregate of 233 individuals; 22/233 membrane-like individually; rim level 0.351)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.689, rim/outside 12.5 (aggregate of 233 individuals; 17/233 membrane-like individually; rim level 0.285)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.45, rim/outside 0.774 (aggregate of 233 individuals; 0/233 membrane-like individually; rim level 0.233)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #423 (t=5800, R_eq 5.41): none; #103 (t=1500, R_eq 6.48): none; #194 (t=2700, R_eq 6.21): none; #811 (t=10200, R_eq 6.08): ['consumer q', 'product r']
- species `prey` (channels ['prey a'], own threshold): components final 36, mean 37.4, max 67; tracks 983, persistent 0; splits 426, persistent splits 74 (K=5), max generation 6, merges 25, merge/split 0.059; moving tracks 100
- species `consumer` (channels ['consumer q'], own threshold): components final 28, mean 31.1, max 72; tracks 777, persistent 0; splits 249, persistent splits 29 (K=5), max generation 2, merges 13, merge/split 0.052; moving tracks 276

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 233 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
