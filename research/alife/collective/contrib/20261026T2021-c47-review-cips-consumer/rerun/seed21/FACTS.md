# Evidence pack: cips-consumer (seed 21)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 281s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T2021-c47-review-cips-consumer/rerun/seed21 --seeds 21 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0378, 1.9978], min area 6 px

## Measurements
- components: final 39, mean 39.4, max 86; occupancy final 0.20
- tracks: 932; persistent (alive >= 50% of run): 0; longest 30 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 40, 35], H1 [0, 0, 0]
- motion: 140 long-lived tracks moved >= 1 body length; max speed 0.0239/time; max body lengths 3.6
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 405, persistent splits 71 (0 more failed only because the siblings re-merged within K), max generation 8, merges 20, merge/split ratio 0.049, nucleations 76
- channel total drift (end/start - 1): [-0.0043, -0.0079, None, -0.5993]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 483 at frame 69: holes 0, rim-vs-core 0.31, rim-vs-outside 0.43, heterogeneity 0.28; core [0.763, 0.495, 0.494, 0.119] rim [0.6, 0.364, 0.264, 0.154]
  - track 356 at frame 50: holes 0, rim-vs-core 0.29, rim-vs-outside 0.31, heterogeneity 0.23; core [0.878, 0.243, 0.258, 0.064] rim [0.639, 0.165, 0.133, 0.145]
  - track 115 at frame 16: holes 1, rim-vs-core 0.12, rim-vs-outside 0.48, heterogeneity 0.04; core [0.902, 0.056, 0.009, 0.034] rim [0.79, 0.051, 0.007, 0.07]
  - track 852 at frame 111: holes 0, rim-vs-core 0.56, rim-vs-outside 0.39, heterogeneity 0.26; core [0.742, 0.669, 0.708, 0.157] rim [0.528, 0.371, 0.288, 0.206]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 228 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 10.3 (aggregate of 228 individuals; 13/228 membrane-like individually; rim level 0.666)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.838, rim/outside 8.9 (aggregate of 228 individuals; 33/228 membrane-like individually; rim level 0.339)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.7, rim/outside 12.3 (aggregate of 228 individuals; 22/228 membrane-like individually; rim level 0.274)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.68, rim/outside 0.772 (aggregate of 228 individuals; 0/228 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #483 (t=6900, R_eq 5.92): none; #356 (t=5000, R_eq 5.78): ['consumer q', 'product r']; #115 (t=1600, R_eq 7.72, ring): ['prey a']; #852 (t=11100, R_eq 4.22): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 37.3, max 73; tracks 966, persistent 0; splits 416, persistent splits 63 (K=5), max generation 7, merges 29, merge/split 0.07; moving tracks 111
- species `consumer` (channels ['consumer q'], own threshold): components final 30, mean 30.9, max 77; tracks 779, persistent 0; splits 246, persistent splits 30 (K=5), max generation 2, merges 23, merge/split 0.093; moving tracks 313

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 228 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
