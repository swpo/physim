# Evidence pack: cips-consumer (seed 8)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 260s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/seed8 --seeds 8 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0376, 1.9994], min area 6 px

## Measurements
- components: final 43, mean 38.8, max 81; occupancy final 0.19
- tracks: 907; persistent (alive >= 50% of run): 0; longest 31 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 43, 39], H1 [0, 0, 0]
- motion: 131 long-lived tracks moved >= 1 body length; max speed 0.0211/time; max body lengths 4.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 394, persistent splits 90 (0 more failed only because the siblings re-merged within K), max generation 9, merges 29, merge/split ratio 0.074, nucleations 78
- channel total drift (end/start - 1): [-0.0119, -0.0202, None, -0.5911]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 594 at frame 87: holes 0, rim-vs-core 0.24, rim-vs-outside 0.60, heterogeneity 0.27; core [0.795, 0.421, 0.431, 0.093] rim [0.597, 0.435, 0.314, 0.144]
  - track 635 at frame 89: holes 0, rim-vs-core 0.44, rim-vs-outside 0.35, heterogeneity 0.28; core [0.742, 0.547, 0.547, 0.126] rim [0.514, 0.381, 0.219, 0.183]
  - track 75 at frame 13: holes 0, rim-vs-core 0.48, rim-vs-outside 0.37, heterogeneity 0.28; core [0.748, 0.624, 0.67, 0.144] rim [0.503, 0.461, 0.301, 0.204]
  - track 804 at frame 111: holes 0, rim-vs-core 0.08, rim-vs-outside 0.52, heterogeneity 0.03; core [0.9, 0.031, 0.003, 0.016] rim [0.838, 0.03, 0.003, 0.061]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 10.3 (aggregate of 224 individuals; 16/224 membrane-like individually; rim level 0.677)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 8.53 (aggregate of 224 individuals; 23/224 membrane-like individually; rim level 0.34)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 12.4 (aggregate of 224 individuals; 19/224 membrane-like individually; rim level 0.283)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.59, rim/outside 0.771 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.239)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #594 (t=8700, R_eq 7.4): none; #635 (t=8900, R_eq 5.08): none; #75 (t=1300, R_eq 4.85): none; #804 (t=11100, R_eq 6.48): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 36.1, max 65; tracks 860, persistent 0; splits 370, persistent splits 85 (K=5), max generation 8, merges 34, merge/split 0.092; moving tracks 106
- species `consumer` (channels ['consumer q'], own threshold): components final 32, mean 29.1, max 73; tracks 680, persistent 0; splits 201, persistent splits 27 (K=5), max generation 2, merges 19, merge/split 0.095; moving tracks 268

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
