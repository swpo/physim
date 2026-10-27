# Evidence pack: cips-consumer (seed 92)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 121 frames x 400 steps x dt 0.25 = time 12000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261027T2016-c59-review-cips-consumer/rerun/seed92 --seeds 92 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0378, 1.9931], min area 6 px

## Measurements
- components: final 41, mean 38.9, max 91; occupancy final 0.20
- tracks: 895; persistent (alive >= 50% of run): 0; longest 37 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 43, 40], H1 [0, 0, 0]
- motion: 128 long-lived tracks moved >= 1 body length; max speed 0.0209/time; max body lengths 4.3
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 390, persistent splits 83 (0 more failed only because the siblings re-merged within K), max generation 7, merges 21, merge/split ratio 0.054, nucleations 74
- channel total drift (end/start - 1): [-0.0119, -0.034, None, -0.5978]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 339 at frame 55: holes 0, rim-vs-core 0.10, rim-vs-outside 0.35, heterogeneity 0.03; core [0.925, 0.038, 0.004, 0.033] rim [0.834, 0.038, 0.004, 0.062]
  - track 276 at frame 43: holes 0, rim-vs-core 0.42, rim-vs-outside 0.59, heterogeneity 0.28; core [0.783, 0.595, 0.661, 0.137] rim [0.549, 0.47, 0.341, 0.192]
  - track 355 at frame 52: holes 0, rim-vs-core 0.34, rim-vs-outside 0.31, heterogeneity 0.26; core [0.831, 0.342, 0.348, 0.073] rim [0.572, 0.252, 0.16, 0.15]
  - track 808 at frame 114: holes 0, rim-vs-core 0.37, rim-vs-outside 0.34, heterogeneity 0.27; core [0.833, 0.392, 0.422, 0.101] rim [0.558, 0.317, 0.199, 0.181]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 238 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 10 (aggregate of 238 individuals; 19/238 membrane-like individually; rim level 0.653)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 9 (aggregate of 238 individuals; 14/238 membrane-like individually; rim level 0.362)
  - radial product r: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.696, rim/outside 12.8 (aggregate of 238 individuals; 9/238 membrane-like individually; rim level 0.285)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.42, rim/outside 0.783 (aggregate of 238 individuals; 0/238 membrane-like individually; rim level 0.24)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #339 (t=5500, R_eq 4.62): none; #276 (t=4300, R_eq 6.18): none; #355 (t=5200, R_eq 5.56): ['consumer q']; #808 (t=11400, R_eq 5.53): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 36.5, max 69; tracks 891, persistent 0; splits 389, persistent splits 72 (K=5), max generation 8, merges 27, merge/split 0.069; moving tracks 104
- species `consumer` (channels ['consumer q'], own threshold): components final 32, mean 29.3, max 70; tracks 716, persistent 0; splits 212, persistent splits 23 (K=5), max generation 3, merges 27, merge/split 0.127; moving tracks 282

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 238 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
