# Evidence pack: cips-turnover (seed 2)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 1000 steps x dt 0.05 (--dt; world META dt 0.1) = time 12000; grid [256, 256]; wall 1878s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0342-c32-review-coop-rods/world.py --out collective/contrib/20261026T0342-c32-review-coop-rods/pack_s2_res15 --seeds 2 --size 256 256 --frames 240 --spf 1000 --dt 0.05 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0088, 0.9834], min area 6 px

## Measurements
- components: final 8, mean 4.7, max 8; occupancy final 0.11
- tracks: 8; persistent (alive >= 50% of run): 8; longest 159 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 62.27 (1 = constant size)
- enclosures: components with a hole mean 0.20, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 8
- channel total drift (end/start - 1): [0.0004, -0.5647, 0.6088]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 161: holes 1, rim-vs-core 0.24, rim-vs-outside 0.75, heterogeneity 0.11; core [0.97, 0.889, 0.036] rim [0.816, 0.733, 0.135]
  - track 1 at frame 163: holes 0, rim-vs-core 0.18, rim-vs-outside 0.87, heterogeneity 0.10; core [0.965, 0.872, 0.014] rim [0.869, 0.782, 0.135]
  - track 2 at frame 169: holes 0, rim-vs-core 0.31, rim-vs-outside 0.72, heterogeneity 0.12; core [0.984, 0.936, 0.049] rim [0.805, 0.74, 0.214]
  - track 3 at frame 169: holes 0, rim-vs-core 0.21, rim-vs-outside 0.83, heterogeneity 0.11; core [0.987, 0.944, 0.05] rim [0.87, 0.805, 0.159]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 32 components >= 12 px at frames [121, 159, 200, 240]):
  - radial e: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 35.3 (aggregate of 32 individuals; 4/32 membrane-like individually; rim level 0.844)
  - radial p: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.973, rim/outside 15.6 (aggregate of 32 individuals; 3/32 membrane-like individually; rim level 0.824)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.7, rim/outside 0.653 (aggregate of 32 individuals; 0/32 membrane-like individually; rim level 0.517)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=8050, R_eq 21.36, ring): ['e', 'p']; #1 (t=8150, R_eq 19.75): none; #2 (t=8450, R_eq 17.52): none; #3 (t=8450, R_eq 16.18): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- --dt 0.05 only relabels time (world META dt 0.1): the world's integration step is unchanged, so this run is NOT a dt/2 (or any time-step) test; change the world's own step for that
- radial: 4 of 32 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
