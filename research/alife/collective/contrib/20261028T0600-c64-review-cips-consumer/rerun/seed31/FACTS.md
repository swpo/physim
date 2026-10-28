# Evidence pack: cips-consumer (seed 31)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 214s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261028T0600-c64-review-cips-consumer/rerun/seed31 --seeds 31 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0382, 1.9971], min area 6 px

## Measurements
- components: final 41, mean 38.9, max 88; occupancy final 0.19
- tracks: 952; persistent (alive >= 50% of run): 0; longest 31 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.15, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 41, 38], H1 [0, 0, 0]
- motion: 133 long-lived tracks moved >= 1 body length; max speed 0.0217/time; max body lengths 4.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 419, persistent splits 90 (0 more failed only because the siblings re-merged within K), max generation 10, merges 19, merge/split ratio 0.045, nucleations 79
- channel total drift (end/start - 1): [0.0158, -0.0014, None, -0.5923]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 468 at frame 68: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.29; core [0.741, 0.57, 0.576, 0.124] rim [0.526, 0.377, 0.215, 0.189]
  - track 370 at frame 50: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.26; core [0.851, 0.321, 0.337, 0.071] rim [0.629, 0.258, 0.167, 0.147]
  - track 774 at frame 108: holes 0, rim-vs-core 0.38, rim-vs-outside 0.57, heterogeneity 0.27; core [0.751, 0.611, 0.617, 0.136] rim [0.546, 0.47, 0.339, 0.186]
  - track 899 at frame 116: holes 0, rim-vs-core 0.27, rim-vs-outside 0.30, heterogeneity 0.23; core [0.849, 0.307, 0.319, 0.068] rim [0.668, 0.198, 0.157, 0.131]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 224 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.912, rim/outside 10.4 (aggregate of 224 individuals; 18/224 membrane-like individually; rim level 0.67)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.768, rim/outside 8.56 (aggregate of 224 individuals; 19/224 membrane-like individually; rim level 0.333)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.663, rim/outside 13 (aggregate of 224 individuals; 14/224 membrane-like individually; rim level 0.275)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.58, rim/outside 0.766 (aggregate of 224 individuals; 0/224 membrane-like individually; rim level 0.232)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #468 (t=6800, R_eq 5.35): none; #370 (t=5000, R_eq 5.32): ['consumer q']; #774 (t=10800, R_eq 6.26): none; #899 (t=11600, R_eq 5.5): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 36.6, max 68; tracks 947, persistent 0; splits 418, persistent splits 85 (K=5), max generation 11, merges 23, merge/split 0.055; moving tracks 111
- species `consumer` (channels ['consumer q'], own threshold): components final 31, mean 30.0, max 72; tracks 754, persistent 0; splits 231, persistent splits 23 (K=5), max generation 4, merges 18, merge/split 0.078; moving tracks 294

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 224 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
