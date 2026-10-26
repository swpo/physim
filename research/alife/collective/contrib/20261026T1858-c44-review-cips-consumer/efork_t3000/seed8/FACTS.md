# Evidence pack: cips-consumer (seed 8)

- world: `../../world_claim.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 179s; status ok
- command: `python -m labkit.run world_claim.py --out efork_t3000/seed8 --seeds 8 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0437, 1.931], min area 6 px

## Measurements
- components: final 0, mean 15.4, max 81; occupancy final 0.00
- tracks: 302; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.0192/time; max body lengths 4.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 104, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 2, merges 14, merge/split ratio 0.135, nucleations 72
- channel total drift (end/start - 1): [-1.0, -0.0202, None, 0.0416]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 75 at frame 13: holes 0, rim-vs-core 0.49, rim-vs-outside 0.40, heterogeneity 0.28; core [0.772, 0.614, 0.723, 0.124] rim [0.498, 0.472, 0.347, 0.185]
  - track 135 at frame 16: holes 0, rim-vs-core 0.16, rim-vs-outside 0.29, heterogeneity 0.03; core [0.903, 0.063, 0.014, 0.02] rim [0.751, 0.05, 0.008, 0.081]
  - track 28 at frame 9: holes 0, rim-vs-core 0.22, rim-vs-outside 0.45, heterogeneity 0.16; core [0.812, 0.203, 0.239, 0.016] rim [0.802, 0.05, 0.087, 0.071]
  - track 215 at frame 25: holes 0, rim-vs-core 0.15, rim-vs-outside 0.27, heterogeneity 0.03; core [0.89, 0.043, 0.007, 0.017] rim [0.756, 0.04, 0.005, 0.078]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 8.01 (aggregate of 76 individuals; 6/76 membrane-like individually; rim level 0.708)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 8.72 (aggregate of 76 individuals; 10/76 membrane-like individually; rim level 0.31)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.71, rim/outside 13.3 (aggregate of 76 individuals; 7/76 membrane-like individually; rim level 0.296)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.85, rim/outside 0.754 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.205)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #75 (t=1300, R_eq 4.92): none; #135 (t=1600, R_eq 5.78): none; #28 (t=900, R_eq 6.05): ['consumer q', 'product r']; #215 (t=2500, R_eq 5.89): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 14.2, max 66; tracks 303, persistent 0; splits 92, persistent splits 13 (K=5), max generation 2, merges 27, merge/split 0.293; moving tracks 20
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 12.3, max 73; tracks 239, persistent 0; splits 50, persistent splits 6 (K=5), max generation 2, merges 11, merge/split 0.22; moving tracks 70

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 76 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
