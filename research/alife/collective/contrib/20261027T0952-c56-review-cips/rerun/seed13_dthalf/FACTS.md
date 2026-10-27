# Evidence pack: cips-consumer (seed 13)

- world: `../../../collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 800 steps x dt 0.25 = time 24000; grid [128, 128]; wall 475s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out c56work/cr/pack_s13_dthalf --seeds 13 --frames 120 --spf 800 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.038, 1.9955], min area 6 px

## Measurements
- components: final 33, mean 38.3, max 83; occupancy final 0.19
- tracks: 898; persistent (alive >= 50% of run): 0; longest 36 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.18, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 35, 30], H1 [1, 0, 0]
- motion: 134 long-lived tracks moved >= 1 body length; max speed 0.0131/time; max body lengths 4.3
- replication (lineage window K = 5 frames = time 1000, --lineage-k): splits 393, persistent splits 78 (0 more failed only because the siblings re-merged within K), max generation 11, merges 24, merge/split ratio 0.061, nucleations 70
- channel total drift (end/start - 1): [-0.0171, 0.0136, None, -0.5813]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 313 at frame 50: holes 0, rim-vs-core 0.29, rim-vs-outside 0.58, heterogeneity 0.26; core [0.9, 0.261, 0.327, 0.049] rim [0.652, 0.386, 0.285, 0.129]
  - track 87 at frame 16: holes 0, rim-vs-core 0.27, rim-vs-outside 0.56, heterogeneity 0.27; core [0.873, 0.335, 0.396, 0.053] rim [0.645, 0.378, 0.27, 0.128]
  - track 394 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.32, heterogeneity 0.28; core [0.771, 0.455, 0.458, 0.102] rim [0.538, 0.336, 0.196, 0.168]
  - track 859 at frame 117: holes 0, rim-vs-core 0.14, rim-vs-outside 0.26, heterogeneity 0.03; core [0.899, 0.043, 0.006, 0.026] rim [0.777, 0.04, 0.004, 0.095]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 212 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.905, rim/outside 10.7 (aggregate of 212 individuals; 11/212 membrane-like individually; rim level 0.675)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 7.87 (aggregate of 212 individuals; 26/212 membrane-like individually; rim level 0.32)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.641, rim/outside 11.8 (aggregate of 212 individuals; 19/212 membrane-like individually; rim level 0.268)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.72, rim/outside 0.758 (aggregate of 212 individuals; 0/212 membrane-like individually; rim level 0.233)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #313 (t=10000, R_eq 6.38): none; #87 (t=3200, R_eq 6.08): none; #394 (t=12200, R_eq 5.38): none; #859 (t=23400, R_eq 5.64): none
- species `prey` (channels ['prey a'], own threshold): components final 31, mean 36.1, max 70; tracks 903, persistent 0; splits 385, persistent splits 75 (K=5), max generation 11, merges 33, merge/split 0.086; moving tracks 109
- species `consumer` (channels ['consumer q'], own threshold): components final 27, mean 29.0, max 66; tracks 712, persistent 0; splits 218, persistent splits 22 (K=5), max generation 3, merges 18, merge/split 0.083; moving tracks 249

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 212 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
