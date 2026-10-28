# Evidence pack: cips-consumer (seed 57)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261028T0347-c61-review-cips-consumer/rerun/seed57 --seeds 57 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0377, 1.9941], min area 6 px

## Measurements
- components: final 36, mean 39.4, max 84; occupancy final 0.19
- tracks: 984; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [42, 38, 33], H1 [0, 0, 0]
- motion: 127 long-lived tracks moved >= 1 body length; max speed 0.0259/time; max body lengths 6.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 436, persistent splits 84 (0 more failed only because the siblings re-merged within K), max generation 8, merges 19, merge/split ratio 0.044, nucleations 69
- channel total drift (end/start - 1): [-0.0136, -0.0292, None, -0.5819]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 585 at frame 84: holes 0, rim-vs-core 0.40, rim-vs-outside 0.54, heterogeneity 0.29; core [0.78, 0.528, 0.557, 0.106] rim [0.536, 0.436, 0.256, 0.175]
  - track 412 at frame 50: holes 0, rim-vs-core 0.31, rim-vs-outside 0.56, heterogeneity 0.28; core [0.853, 0.369, 0.427, 0.079] rim [0.595, 0.408, 0.27, 0.156]
  - track 61 at frame 14: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.27; core [0.737, 0.584, 0.59, 0.147] rim [0.535, 0.339, 0.248, 0.204]
  - track 885 at frame 110: holes 0, rim-vs-core 0.39, rim-vs-outside 0.28, heterogeneity 0.23; core [0.802, 0.397, 0.423, 0.102] rim [0.648, 0.17, 0.148, 0.153]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 232 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.919, rim/outside 10.4 (aggregate of 232 individuals; 19/232 membrane-like individually; rim level 0.671)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.725, rim/outside 9.16 (aggregate of 232 individuals; 15/232 membrane-like individually; rim level 0.342)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.648, rim/outside 13.1 (aggregate of 232 individuals; 9/232 membrane-like individually; rim level 0.29)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.47, rim/outside 0.771 (aggregate of 232 individuals; 0/232 membrane-like individually; rim level 0.235)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #585 (t=8400, R_eq 6.21): none; #412 (t=5000, R_eq 6.43): none; #61 (t=1400, R_eq 5.26): none; #885 (t=11000, R_eq 4.75): none
- species `prey` (channels ['prey a'], own threshold): components final 33, mean 37.0, max 65; tracks 973, persistent 0; splits 425, persistent splits 76 (K=5), max generation 9, merges 24, merge/split 0.056; moving tracks 99
- species `consumer` (channels ['consumer q'], own threshold): components final 27, mean 31.7, max 81; tracks 809, persistent 0; splits 255, persistent splits 30 (K=5), max generation 3, merges 24, merge/split 0.094; moving tracks 312

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 232 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
