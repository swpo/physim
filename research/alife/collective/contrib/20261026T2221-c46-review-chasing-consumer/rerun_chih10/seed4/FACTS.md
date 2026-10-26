# Evidence pack: cips-consumer (seed 4)

- world: `../../../20261026T1800-c43-chasing-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 76 frames x 400 steps x dt 0.25 = time 7500; grid [128, 128]; wall 161s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1800-c43-chasing-consumer/world.py --out collective/contrib/20261026T2221-c46-review-chasing-consumer/rerun_chih10/seed4 --seeds 4 --frames 75 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0458, 2.058], min area 6 px

## Measurements
- components: final 25, mean 25.1, max 93; occupancy final 0.12
- tracks: 520; persistent (alive >= 50% of run): 1; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.76 (1 = constant size)
- enclosures: components with a hole mean 0.66, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 32, 23], H1 [4, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.0346/time; max body lengths 9.2
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 171, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 71, merge/split ratio 0.415, nucleations 84
- channel total drift (end/start - 1): [-0.2214, 0.0158, None, -0.4426]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 110 at frame 26: holes 0, rim-vs-core 0.68, rim-vs-outside 0.74, heterogeneity 0.18; core [0.851, 0.995, 0.968, 0.26] rim [0.413, 0.7, 0.552, 0.345]
  - track 220 at frame 34: holes 0, rim-vs-core 0.17, rim-vs-outside 0.45, heterogeneity 0.20; core [0.768, 0.291, 0.265, 0.034] rim [0.777, 0.176, 0.171, 0.114]
  - track 35 at frame 14: holes 0, rim-vs-core 0.38, rim-vs-outside 0.41, heterogeneity 0.20; core [0.828, 0.457, 0.429, 0.038] rim [0.752, 0.17, 0.195, 0.083]
  - track 332 at frame 53: holes 0, rim-vs-core 0.26, rim-vs-outside 0.31, heterogeneity 0.21; core [0.861, 0.341, 0.331, 0.062] rim [0.759, 0.174, 0.177, 0.134]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [12, 25, 38, 50, 62, 75]):
  - radial prey a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 6.55 (aggregate of 122 individuals; 9/122 membrane-like individually; rim level 0.648)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 11.4 (aggregate of 122 individuals; 47/122 membrane-like individually; rim level 0.483)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 12.8 (aggregate of 122 individuals; 43/122 membrane-like individually; rim level 0.421)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2.52, rim/outside 0.731 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.293)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #110 (t=2600, R_eq 3.91): none; #220 (t=3400, R_eq 6.7): ['consumer q', 'product r']; #35 (t=1400, R_eq 6.86, ring): ['consumer q', 'product r']; #332 (t=5300, R_eq 5.38): ['consumer q', 'product r']
- species `prey` (channels ['prey a'], own threshold): components final 20, mean 18.0, max 53; tracks 260, persistent 1; splits 82, persistent splits 19 (K=5), max generation 3, merges 10, merge/split 0.122; moving tracks 1
- species `consumer` (channels ['consumer q'], own threshold): components final 33, mean 37.6, max 90; tracks 818, persistent 1; splits 199, persistent splits 7 (K=5), max generation 1, merges 124, merge/split 0.623; moving tracks 110

## Warnings
- radial: 12 of 122 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
