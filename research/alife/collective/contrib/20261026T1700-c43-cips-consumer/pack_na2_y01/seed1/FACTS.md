# Evidence pack: cips-consumer (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 378s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/pack/seed1 --seeds 1 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0659, 1.8231], min area 6 px

## Measurements
- components: final 28, mean 30.4, max 68; occupancy final 0.10
- tracks: 1496; persistent (alive >= 50% of run): 0; longest 18 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.58, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [41, 29, 21], H1 [2, 1, 0]
- motion: 38 long-lived tracks moved >= 1 body length; max speed 0.0419/time; max body lengths 3.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 480, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 69, merge/split ratio 0.144, nucleations 416
- channel total drift (end/start - 1): [-0.2027, 0.0362, None, -0.427]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 209 at frame 21: holes 0, rim-vs-core 0.32, rim-vs-outside 0.24, heterogeneity 0.09; core [0.287, 0.714, 0.2, 0.532] rim [0.351, 0.409, 0.117, 0.532]
  - track 873 at frame 77: holes 0, rim-vs-core 0.46, rim-vs-outside 0.29, heterogeneity 0.14; core [0.317, 0.807, 0.339, 0.465] rim [0.362, 0.389, 0.158, 0.468]
  - track 51 at frame 7: holes 0, rim-vs-core 0.23, rim-vs-outside 0.25, heterogeneity 0.06; core [0.244, 0.717, 0.166, 0.492] rim [0.265, 0.494, 0.11, 0.496]
  - track 1285 at frame 105: holes 0, rim-vs-core 0.28, rim-vs-outside 0.33, heterogeneity 0.16; core [0.868, 0.121, 0.196, 0.025] rim [0.706, 0.015, 0.015, 0.116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 6.5 (aggregate of 170 individuals; 28/170 membrane-like individually; rim level 0.609)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.647, rim/outside 6.86 (aggregate of 170 individuals; 29/170 membrane-like individually; rim level 0.374)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.57, rim/outside 13.2 (aggregate of 170 individuals; 21/170 membrane-like individually; rim level 0.298)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.04, rim/outside 0.797 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.328)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #209 (t=2100, R_eq 2.33): none; #873 (t=7700, R_eq 2.93): none; #51 (t=700, R_eq 2.33): none; #1285 (t=10500, R_eq 5.94): none
- species `prey` (channels ['prey a'], own threshold): components final 26, mean 27.1, max 45; tracks 1420, persistent 0; splits 413, persistent splits 0 (K=5), max generation 0, merges 81, merge/split 0.196; moving tracks 37
- species `consumer` (channels ['consumer q'], own threshold): components final 26, mean 27.4, max 67; tracks 1682, persistent 0; splits 33, persistent splits 0 (K=5), max generation 0, merges 4, merge/split 0.121; moving tracks 56

## Warnings
- radial: 7 of 170 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
