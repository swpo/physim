# Evidence pack: cips-consumer (seed 1717)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 81 frames x 400 steps x dt 0.25 = time 8000; grid [128, 128]; wall 130s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out /tmp/claude-0/rv/efork/seed1717 --seeds 1717 --frames 80 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0434, 1.9402], min area 6 px

## Measurements
- components: final 0, mean 16.2, max 81; occupancy final 0.00
- tracks: 322; persistent (alive >= 50% of run): 0; longest 18 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 35 long-lived tracks moved >= 1 body length; max speed 0.0194/time; max body lengths 2.4
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 115, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 11, merge/split ratio 0.096, nucleations 74
- channel total drift (end/start - 1): [-1.0, -0.0208, None, 0.0459]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 10: holes 0, rim-vs-core 0.17, rim-vs-outside 0.29, heterogeneity 0.03; core [0.937, 0.026, 0.003, 0.015] rim [0.777, 0.024, 0.002, 0.073]
  - track 51 at frame 9: holes 0, rim-vs-core 0.64, rim-vs-outside 0.48, heterogeneity 0.26; core [0.765, 0.769, 0.849, 0.163] rim [0.623, 0.338, 0.401, 0.199]
  - track 75 at frame 9: holes 0, rim-vs-core 0.24, rim-vs-outside 0.53, heterogeneity 0.22; core [0.859, 0.248, 0.316, 0.027] rim [0.802, 0.138, 0.113, 0.068]
  - track 234 at frame 23: holes 0, rim-vs-core 0.17, rim-vs-outside 0.39, heterogeneity 0.23; core [0.86, 0.277, 0.331, 0.076] rim [0.74, 0.193, 0.249, 0.104]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [13, 27]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.892, rim/outside 7.32 (aggregate of 79 individuals; 6/79 membrane-like individually; rim level 0.668)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.734, rim/outside 9.71 (aggregate of 79 individuals; 7/79 membrane-like individually; rim level 0.344)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 13.6 (aggregate of 79 individuals; 8/79 membrane-like individually; rim level 0.319)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.63, rim/outside 0.768 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.205)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=1000, R_eq 5.38): none; #51 (t=900, R_eq 3.99): none; #75 (t=900, R_eq 6.38): ['consumer q', 'product r']; #234 (t=2300, R_eq 4.98): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 15.5, max 67; tracks 346, persistent 0; splits 121, persistent splits 9 (K=5), max generation 2, merges 23, merge/split 0.19; moving tracks 28
- species `consumer` (channels ['consumer q'], own threshold): components final 0, mean 13.4, max 76; tracks 247, persistent 0; splits 57, persistent splits 12 (K=5), max generation 3, merges 6, merge/split 0.105; moving tracks 85

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
