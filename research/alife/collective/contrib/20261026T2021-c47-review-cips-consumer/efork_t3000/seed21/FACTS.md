# Evidence pack: cips-consumer (seed 21)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 194s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T2021-c47-review-cips-consumer/efork_t3000/seed21 --seeds 21 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0453, 1.9402], min area 6 px

## Measurements
- components: final 0, mean 16.0, max 85; occupancy final 0.00
- tracks: 317; persistent (alive >= 50% of run): 0; longest 26 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 34 long-lived tracks moved >= 1 body length; max speed 0.0192/time; max body lengths 3.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 109, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 10, merge/split ratio 0.092, nucleations 63
- channel total drift (end/start - 1): [-1.0, -0.0079, None, 0.0475]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 116 at frame 16: holes 1, rim-vs-core 0.12, rim-vs-outside 0.49, heterogeneity 0.04; core [0.92, 0.054, 0.011, 0.019] rim [0.802, 0.05, 0.008, 0.054]
  - track 104 at frame 12: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.03; core [0.945, 0.049, 0.009, 0.019] rim [0.778, 0.044, 0.006, 0.067]
  - track 164 at frame 20: holes 0, rim-vs-core 0.42, rim-vs-outside 0.56, heterogeneity 0.30; core [0.764, 0.58, 0.685, 0.1] rim [0.542, 0.493, 0.341, 0.161]
  - track 229 at frame 24: holes 0, rim-vs-core 0.70, rim-vs-outside 0.43, heterogeneity 0.24; core [0.81, 0.762, 0.865, 0.165] rim [0.603, 0.289, 0.39, 0.207]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 75 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 7.71 (aggregate of 75 individuals; 6/75 membrane-like individually; rim level 0.693)
  - radial consumer q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 9.08 (aggregate of 75 individuals; 10/75 membrane-like individually; rim level 0.332)
  - radial product r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 14.1 (aggregate of 75 individuals; 6/75 membrane-like individually; rim level 0.31)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.71, rim/outside 0.761 (aggregate of 75 individuals; 0/75 membrane-like individually; rim level 0.21)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #116 (t=1600, R_eq 7.82, ring): ['prey a']; #104 (t=1200, R_eq 4.37): none; #164 (t=2000, R_eq 6.02): none; #229 (t=2400, R_eq 3.43): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 15.2, max 74; tracks 348, persistent 0; splits 113, persistent splits 11 (K=5), max generation 2, merges 20, merge/split 0.177; moving tracks 21
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 13.0, max 77; tracks 262, persistent 0; splits 60, persistent splits 5 (K=5), max generation 2, merges 8, merge/split 0.133; moving tracks 79

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 75 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
