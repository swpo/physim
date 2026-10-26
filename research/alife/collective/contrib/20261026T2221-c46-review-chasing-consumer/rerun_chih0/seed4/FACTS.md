# Evidence pack: cips-consumer (seed 4)

- world: `../../../20261026T1800-c43-chasing-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 76 frames x 400 steps x dt 0.25 = time 7500; grid [128, 128]; wall 153s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1800-c43-chasing-consumer/world.py --out collective/contrib/20261026T2221-c46-review-chasing-consumer/rerun_chih0/seed4 --seeds 4 --frames 75 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0378, 2.0049], min area 6 px

## Measurements
- components: final 40, mean 41.9, max 88; occupancy final 0.20
- tracks: 353; persistent (alive >= 50% of run): 11; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.43 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 40, 39], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.00986/time; max body lengths 3.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 123, persistent splits 43 (0 more failed only because the siblings re-merged within K), max generation 4, merges 21, merge/split ratio 0.171, nucleations 60
- channel total drift (end/start - 1): [-0.0146, 0.0158, None, -0.599]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 148 at frame 35: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.28; core [0.73, 0.494, 0.475, 0.133] rim [0.464, 0.41, 0.201, 0.199]
  - track 206 at frame 49: holes 0, rim-vs-core 0.09, rim-vs-outside 0.48, heterogeneity 0.03; core [0.854, 0.052, 0.008, 0.019] rim [0.791, 0.049, 0.006, 0.088]
  - track 196 at frame 48: holes 0, rim-vs-core 0.41, rim-vs-outside 0.36, heterogeneity 0.28; core [0.801, 0.439, 0.461, 0.115] rim [0.504, 0.353, 0.202, 0.196]
  - track 312 at frame 69: holes 0, rim-vs-core 0.38, rim-vs-outside 0.30, heterogeneity 0.25; core [0.851, 0.361, 0.418, 0.1] rim [0.695, 0.151, 0.151, 0.166]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 244 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.87, rim/outside 10.4 (aggregate of 244 individuals; 11/244 membrane-like individually; rim level 0.659)
  - radial consumer q: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 9.67 (aggregate of 244 individuals; 31/244 membrane-like individually; rim level 0.354)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.698, rim/outside 12.6 (aggregate of 244 individuals; 21/244 membrane-like individually; rim level 0.286)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.49, rim/outside 0.784 (aggregate of 244 individuals; 0/244 membrane-like individually; rim level 0.239)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #148 (t=3500, R_eq 5.84): none; #206 (t=4900, R_eq 6.56): none; #196 (t=4800, R_eq 5.5): none; #312 (t=6900, R_eq 5.23): none
- species `prey` (channels ['prey a'], own threshold): components final 40, mean 38.7, max 75; tracks 363, persistent 9; splits 125, persistent splits 38 (K=5), max generation 3, merges 13, merge/split 0.104; moving tracks 33
- species `consumer` (channels ['consumer q'], own threshold): components final 31, mean 31.9, max 72; tracks 255, persistent 4; splits 61, persistent splits 24 (K=5), max generation 3, merges 9, merge/split 0.148; moving tracks 113

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 244 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
