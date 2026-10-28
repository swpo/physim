# Evidence pack: driven-condensate-prey-predator (seed 58)

- world: `../../../20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 1714s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261028T0409-c61-review-hunting/rerun/seed58 --seeds 58 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.33 of robust range [0.1445, 1.2284], min area 6 px

## Measurements
- components: final 120, mean 97.9, max 141; occupancy final 0.06
- tracks: 340; persistent (alive >= 50% of run): 60; longest 108 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 45.89 (1 = constant size)
- enclosures: components with a hole mean 0.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [142, 121, 69], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 40, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.025, nucleations 256
- channel total drift (end/start - 1): [-0.1912, None, -0.4466, -0.6144]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 59: holes 0, rim-vs-core 0.30, rim-vs-outside 0.29, heterogeneity 0.05; core [0.028, 0.866, 0.534, 0.033] rim [0.039, 0.566, 0.532, 0.042]
  - track 8 at frame 45: holes 0, rim-vs-core 0.36, rim-vs-outside 0.27, heterogeneity 0.06; core [0.013, 0.879, 0.497, 0.012] rim [0.027, 0.516, 0.493, 0.023]
  - track 27 at frame 44: holes 0, rim-vs-core 0.32, rim-vs-outside 0.25, heterogeneity 0.05; core [0.008, 0.862, 0.486, 0.004] rim [0.019, 0.538, 0.482, 0.012]
  - track 296 at frame 114: holes 0, rim-vs-core 0.20, rim-vs-outside 0.26, heterogeneity 0.03; core [0.031, 0.786, 0.532, 0.032] rim [0.036, 0.587, 0.531, 0.036]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 586 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 2.97 (aggregate of 586 individuals; 13/586 membrane-like individually; rim level 0.264)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 10.8 (aggregate of 586 individuals; 1/586 membrane-like individually; rim level 0.538)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.952 (aggregate of 586 individuals; 0/586 membrane-like individually; rim level 0.403)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 3.31 (aggregate of 586 individuals; 12/586 membrane-like individually; rim level 0.265)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #37 (t=5900, R_eq 2.46): none; #8 (t=4500, R_eq 3.04): none; #27 (t=4400, R_eq 2.99): none; #296 (t=11400, R_eq 2.03): none
- species `prey` (channels ['prey a'], own threshold): components final 23, mean 32.5, max 67; tracks 392, persistent 1; splits 63, persistent splits 0 (K=5), max generation 0, merges 0, merge/split 0; moving tracks 18
- species `predator` (channels ['predator b'], own threshold): components final 101, mean 73.9, max 107; tracks 331, persistent 12; splits 39, persistent splits 21 (K=5), max generation 3, merges 4, merge/split 0.103; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 586 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
