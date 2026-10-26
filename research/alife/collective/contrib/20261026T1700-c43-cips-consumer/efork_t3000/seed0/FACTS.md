# Evidence pack: cips-consumer (seed 0)

- world: `../../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 256s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T1700-c43-cips-consumer/efork_t3000/seed0 --seeds 0 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0439, 1.9467], min area 6 px

## Measurements
- components: final 0, mean 16.1, max 82; occupancy final 0.00
- tracks: 321; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 32 long-lived tracks moved >= 1 body length; max speed 0.0211/time; max body lengths 3.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 117, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 2, merges 7, merge/split ratio 0.06, nucleations 66
- channel total drift (end/start - 1): [-1.0, -0.0056, None, 0.0436]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 104 at frame 15: holes 0, rim-vs-core 0.34, rim-vs-outside 0.55, heterogeneity 0.28; core [0.83, 0.426, 0.525, 0.069] rim [0.612, 0.356, 0.285, 0.129]
  - track 43 at frame 11: holes 0, rim-vs-core 0.41, rim-vs-outside 0.36, heterogeneity 0.28; core [0.826, 0.458, 0.55, 0.075] rim [0.587, 0.318, 0.253, 0.136]
  - track 70 at frame 11: holes 0, rim-vs-core 0.32, rim-vs-outside 0.61, heterogeneity 0.27; core [0.891, 0.322, 0.437, 0.057] rim [0.613, 0.431, 0.363, 0.129]
  - track 262 at frame 26: holes 0, rim-vs-core 0.53, rim-vs-outside 0.42, heterogeneity 0.26; core [0.709, 0.683, 0.747, 0.14] rim [0.51, 0.43, 0.333, 0.177]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.903, rim/outside 8.7 (aggregate of 85 individuals; 6/85 membrane-like individually; rim level 0.7)
  - radial consumer q: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.678, rim/outside 12.3 (aggregate of 85 individuals; 9/85 membrane-like individually; rim level 0.351)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.649, rim/outside 15.9 (aggregate of 85 individuals; 6/85 membrane-like individually; rim level 0.359)
  - radial fuel u: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.6, rim/outside 0.776 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.213)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #104 (t=1500, R_eq 6.6): none; #43 (t=1100, R_eq 4.98): none; #70 (t=1100, R_eq 6.53): none; #262 (t=2600, R_eq 3.99): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 15.2, max 66; tracks 350, persistent 0; splits 109, persistent splits 11 (K=5), max generation 1, merges 20, merge/split 0.183; moving tracks 23
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 13.1, max 72; tracks 249, persistent 0; splits 60, persistent splits 6 (K=5), max generation 2, merges 4, merge/split 0.067; moving tracks 74

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
