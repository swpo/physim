# Evidence pack: cips-consumer (seed 7)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 41 frames x 400 steps x dt 0.25 = time 4000; grid [128, 128]; wall 75s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/c49rev2/efork_t3000/seed7 --seeds 7 --frames 40 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0403, 1.9784], min area 6 px

## Measurements
- components: final 0, mean 32.1, max 81; occupancy final 0.00
- tracks: 312; persistent (alive >= 50% of run): 3; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 33 long-lived tracks moved >= 1 body length; max speed 0.0218/time; max body lengths 3.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 113, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.062, nucleations 70
- channel total drift (end/start - 1): [-1.0, 0.0191, None, 0.0386]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 87 at frame 16: holes 0, rim-vs-core 0.36, rim-vs-outside 0.37, heterogeneity 0.27; core [0.739, 0.531, 0.505, 0.136] rim [0.504, 0.387, 0.276, 0.197]
  - track 110 at frame 13: holes 0, rim-vs-core 0.35, rim-vs-outside 0.46, heterogeneity 0.28; core [0.683, 0.603, 0.58, 0.141] rim [0.585, 0.409, 0.313, 0.164]
  - track 55 at frame 11: holes 0, rim-vs-core 0.33, rim-vs-outside 0.56, heterogeneity 0.28; core [0.811, 0.449, 0.507, 0.093] rim [0.569, 0.438, 0.296, 0.156]
  - track 250 at frame 27: holes 0, rim-vs-core 0.14, rim-vs-outside 0.53, heterogeneity 0.12; core [0.903, 0.123, 0.141, 0.014] rim [0.835, 0.063, 0.052, 0.063]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [7, 13, 20, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 8.17 (aggregate of 157 individuals; 7/157 membrane-like individually; rim level 0.694)
  - radial consumer q: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 9.51 (aggregate of 157 individuals; 23/157 membrane-like individually; rim level 0.348)
  - radial product r: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.708, rim/outside 13.6 (aggregate of 157 individuals; 14/157 membrane-like individually; rim level 0.306)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.59, rim/outside 0.771 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.221)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #87 (t=1600, R_eq 5.84): none; #110 (t=1300, R_eq 5.44): none; #55 (t=1100, R_eq 6.15): none; #250 (t=2700, R_eq 6.56): ['consumer q', 'product r']
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 29.8, max 70; tracks 317, persistent 2; splits 106, persistent splits 14 (K=5), max generation 2, merges 15, merge/split 0.142; moving tracks 19
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 25.2, max 66; tracks 250, persistent 3; splits 60, persistent splits 5 (K=5), max generation 1, merges 3, merge/split 0.05; moving tracks 75

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 157 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
