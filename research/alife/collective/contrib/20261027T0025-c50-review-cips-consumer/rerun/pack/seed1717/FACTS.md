# Evidence pack: cips-consumer (seed 1717)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 182s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/rv/pack/seed1717 --seeds 1717 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0368, 1.995], min area 6 px

## Measurements
- components: final 40, mean 39.5, max 81; occupancy final 0.20
- tracks: 941; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.09, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 42, 37], H1 [0, 0, 0]
- motion: 133 long-lived tracks moved >= 1 body length; max speed 0.0208/time; max body lengths 5.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 414, persistent splits 85 (0 more failed only because the siblings re-merged within K), max generation 9, merges 25, merge/split ratio 0.06, nucleations 83
- channel total drift (end/start - 1): [-0.0062, -0.0208, None, -0.5972]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 369 at frame 55: holes 0, rim-vs-core 0.26, rim-vs-outside 0.48, heterogeneity 0.28; core [0.753, 0.485, 0.476, 0.12] rim [0.565, 0.445, 0.313, 0.159]
  - track 225 at frame 35: holes 0, rim-vs-core 0.38, rim-vs-outside 0.34, heterogeneity 0.27; core [0.784, 0.45, 0.451, 0.101] rim [0.547, 0.32, 0.194, 0.163]
  - track 414 at frame 56: holes 0, rim-vs-core 0.36, rim-vs-outside 0.34, heterogeneity 0.28; core [0.784, 0.446, 0.453, 0.108] rim [0.516, 0.4, 0.223, 0.184]
  - track 639 at frame 85: holes 0, rim-vs-core 0.11, rim-vs-outside 0.49, heterogeneity 0.03; core [0.906, 0.038, 0.004, 0.013] rim [0.819, 0.035, 0.003, 0.076]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 226 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 9.93 (aggregate of 226 individuals; 17/226 membrane-like individually; rim level 0.657)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 9.11 (aggregate of 226 individuals; 24/226 membrane-like individually; rim level 0.352)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.674, rim/outside 13.1 (aggregate of 226 individuals; 18/226 membrane-like individually; rim level 0.276)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.67, rim/outside 0.771 (aggregate of 226 individuals; 0/226 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #369 (t=5500, R_eq 5.7): none; #225 (t=3500, R_eq 5.14): ['consumer q']; #414 (t=5600, R_eq 5.89): none; #639 (t=8500, R_eq 6.13): none
- species `prey` (channels ['prey a'], own threshold): components final 41, mean 37.4, max 66; tracks 946, persistent 0; splits 417, persistent splits 74 (K=5), max generation 8, merges 36, merge/split 0.086; moving tracks 106
- species `consumer` (channels ['consumer q'], own threshold): components final 35, mean 30.6, max 76; tracks 738, persistent 0; splits 231, persistent splits 30 (K=5), max generation 3, merges 19, merge/split 0.082; moving tracks 286

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 226 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
