# Evidence pack: cips-consumer (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 65 frames x 400 steps x dt 0.25 = time 6400; grid [128, 128]; wall 203s; status non-finite fields at frame 65
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/pack/seed0 --seeds 0 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0638, 1.8087], min area 6 px

## Measurements
- components: final 32, mean 31.1, max 65; occupancy final 0.11
- tracks: 835; persistent (alive >= 50% of run): 0; longest 15 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.51, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 33, 22], H1 [0, 0, 0]
- motion: 22 long-lived tracks moved >= 1 body length; max speed 0.0411/time; max body lengths 2.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 267, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 49, merge/split ratio 0.184, nucleations 232
- channel total drift (end/start - 1): [-0.2024, -0.0056, None, -0.4397]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 655 at frame 55: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.24; core [0.788, 0.414, 0.564, 0.136] rim [0.662, 0.089, 0.169, 0.204]
  - track 338 at frame 29: holes 0, rim-vs-core 0.43, rim-vs-outside 0.18, heterogeneity 0.20; core [0.6, 0.512, 0.393, 0.395] rim [0.489, 0.199, 0.122, 0.431]
  - track 134 at frame 11: holes 0, rim-vs-core 0.74, rim-vs-outside 0.29, heterogeneity 0.17; core [0.424, 0.884, 0.649, 0.39] rim [0.454, 0.257, 0.262, 0.41]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [10, 21, 32, 42, 52, 64]):
  - radial prey a: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 6.43 (aggregate of 188 individuals; 28/188 membrane-like individually; rim level 0.616)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.668, rim/outside 5.97 (aggregate of 188 individuals; 31/188 membrane-like individually; rim level 0.339)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.587, rim/outside 12.3 (aggregate of 188 individuals; 29/188 membrane-like individually; rim level 0.27)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 2, rim/outside 0.804 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.323)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #655 (t=5500, R_eq 4.18): none; #338 (t=2900, R_eq 3.09): none; #327 (t=2800, R_eq 1.38): none; #134 (t=1100, R_eq 3.24): none
- species `prey` (channels ['prey a'], own threshold): components final 29, mean 29.1, max 50; tracks 826, persistent 0; splits 248, persistent splits 1 (K=5), max generation 1, merges 58, merge/split 0.234; moving tracks 13
- species `consumer` (channels ['consumer q'], own threshold): components final 27, mean 27.7, max 63; tracks 940, persistent 0; splits 11, persistent splits 0 (K=5), max generation 0, merges 2, merge/split 0.182; moving tracks 33

## Warnings
- RUN FAILED: non-finite fields at frame 65 (only 65 frames analysed)
- radial: 3 of 188 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
