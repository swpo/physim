# Evidence pack: cips-consumer (seed 1)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 378s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/pack_na1/seed1 --seeds 1 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0378, 1.995], min area 6 px

## Measurements
- components: final 40, mean 37.4, max 86; occupancy final 0.19
- tracks: 898; persistent (alive >= 50% of run): 0; longest 38 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 43, 35], H1 [2, 0, 0]
- motion: 132 long-lived tracks moved >= 1 body length; max speed 0.0205/time; max body lengths 5.1
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 402, persistent splits 79 (0 more failed only because the siblings re-merged within K), max generation 8, merges 10, merge/split ratio 0.025, nucleations 70
- channel total drift (end/start - 1): [0.0248, 0.0362, None, -0.5909]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 186 at frame 34: holes 0, rim-vs-core 0.39, rim-vs-outside 0.34, heterogeneity 0.28; core [0.784, 0.461, 0.471, 0.113] rim [0.508, 0.392, 0.214, 0.189]
  - track 579 at frame 88: holes 0, rim-vs-core 0.34, rim-vs-outside 0.54, heterogeneity 0.28; core [0.835, 0.407, 0.453, 0.079] rim [0.561, 0.426, 0.26, 0.153]
  - track 570 at frame 86: holes 0, rim-vs-core 0.32, rim-vs-outside 0.55, heterogeneity 0.27; core [0.831, 0.406, 0.449, 0.098] rim [0.571, 0.422, 0.276, 0.163]
  - track 728 at frame 104: holes 0, rim-vs-core 0.39, rim-vs-outside 0.54, heterogeneity 0.28; core [0.773, 0.529, 0.552, 0.12] rim [0.516, 0.476, 0.275, 0.188]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 215 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 11 (aggregate of 215 individuals; 11/215 membrane-like individually; rim level 0.67)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 8.39 (aggregate of 215 individuals; 26/215 membrane-like individually; rim level 0.344)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.674, rim/outside 12.3 (aggregate of 215 individuals; 19/215 membrane-like individually; rim level 0.29)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.71, rim/outside 0.763 (aggregate of 215 individuals; 0/215 membrane-like individually; rim level 0.24)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #186 (t=3400, R_eq 5.67): none; #579 (t=8800, R_eq 6.33): none; #570 (t=8600, R_eq 6.21): none; #728 (t=10400, R_eq 6.02): none
- species `prey` (channels ['prey a'], own threshold): components final 34, mean 35.1, max 64; tracks 873, persistent 0; splits 383, persistent splits 79 (K=5), max generation 8, merges 17, merge/split 0.044; moving tracks 121
- species `consumer` (channels ['consumer q'], own threshold): components final 33, mean 29.3, max 67; tracks 725, persistent 0; splits 232, persistent splits 31 (K=5), max generation 4, merges 13, merge/split 0.056; moving tracks 274

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 215 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
