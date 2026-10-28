# Evidence pack: cips-consumer (seed 72)

- world: `../../claim_world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 307s; status ok
- command: `python -m labkit.run collective/contrib/20261028T0745-c63-review-cips-consumer/claim_world.py --out collective/contrib/20261028T0745-c63-review-cips-consumer/rerun/seed72 --seeds 72 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0379, 1.9987], min area 6 px

## Measurements
- components: final 37, mean 38.0, max 79; occupancy final 0.19
- tracks: 822; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.11, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 37, 34], H1 [0, 0, 0]
- motion: 127 long-lived tracks moved >= 1 body length; max speed 0.026/time; max body lengths 5.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 360, persistent splits 83 (0 more failed only because the siblings re-merged within K), max generation 8, merges 12, merge/split ratio 0.033, nucleations 77
- channel total drift (end/start - 1): [-0.0207, 0.0023, None, -0.588]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 410 at frame 68: holes 0, rim-vs-core 0.33, rim-vs-outside 0.56, heterogeneity 0.28; core [0.827, 0.457, 0.519, 0.101] rim [0.589, 0.445, 0.307, 0.168]
  - track 107 at frame 18: holes 0, rim-vs-core 0.29, rim-vs-outside 0.55, heterogeneity 0.26; core [0.893, 0.264, 0.318, 0.05] rim [0.642, 0.314, 0.217, 0.144]
  - track 601 at frame 93: holes 0, rim-vs-core 0.35, rim-vs-outside 0.57, heterogeneity 0.28; core [0.864, 0.384, 0.453, 0.079] rim [0.575, 0.429, 0.285, 0.158]
  - track 754 at frame 116: holes 0, rim-vs-core 0.07, rim-vs-outside 0.35, heterogeneity 0.03; core [0.886, 0.03, 0.003, 0.026] rim [0.824, 0.028, 0.002, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 10 (aggregate of 226 individuals; 9/226 membrane-like individually; rim level 0.671)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 8.64 (aggregate of 226 individuals; 19/226 membrane-like individually; rim level 0.332)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.676, rim/outside 12.4 (aggregate of 226 individuals; 14/226 membrane-like individually; rim level 0.264)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.69, rim/outside 0.775 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.239)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #410 (t=6800, R_eq 6.23): none; #107 (t=1800, R_eq 6.21): ['consumer q', 'product r']; #601 (t=9300, R_eq 6.18): none; #754 (t=11600, R_eq 5.73): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 36.0, max 78; tracks 830, persistent 0; splits 348, persistent splits 71 (K=5), max generation 10, merges 24, merge/split 0.069; moving tracks 107
- species `consumer` (channels ['consumer q'], own threshold): components final 27, mean 28.6, max 78; tracks 694, persistent 0; splits 213, persistent splits 19 (K=5), max generation 5, merges 19, merge/split 0.089; moving tracks 259

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 226 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
