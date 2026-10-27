# Evidence pack: driven-condensate-prey-predator (seed 7)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 2291s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out /tmp/claude-0/hu/pack/seed7 --seeds 7 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.1404, 1.1626], min area 6 px

## Measurements
- components: final 51, mean 63.0, max 110; occupancy final 0.09
- tracks: 231; persistent (alive >= 50% of run): 18; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 48.10 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [62, 53, 33], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 35, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 160
- channel total drift (end/start - 1): [-0.0334, None, -0.5131, -0.5453]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 63: holes 0, rim-vs-core 0.19, rim-vs-outside 0.61, heterogeneity 0.07; core [0.921, 0.0, 0.002, 0.751] rim [0.756, 0.0, 0.054, 0.66]
  - track 52 at frame 71: holes 0, rim-vs-core 0.25, rim-vs-outside 0.49, heterogeneity 0.08; core [0.926, 0.0, 0.012, 0.802] rim [0.726, 0.0, 0.08, 0.668]
  - track 61 at frame 79: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.07; core [0.911, 0.005, 0.009, 0.763] rim [0.731, 0.001, 0.08, 0.67]
  - track 184 at frame 101: holes 0, rim-vs-core 0.26, rim-vs-outside 0.25, heterogeneity 0.04; core [0.029, 0.823, 0.508, 0.027] rim [0.036, 0.562, 0.506, 0.032]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 359 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 5.32 (aggregate of 359 individuals; 15/359 membrane-like individually; rim level 0.458)
  - radial predator b: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.935, rim/outside 8.47 (aggregate of 359 individuals; 2/359 membrane-like individually; rim level 0.369)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.6, rim/outside 0.879 (aggregate of 359 individuals; 0/359 membrane-like individually; rim level 0.365)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.881, rim/outside 6.08 (aggregate of 359 individuals; 17/359 membrane-like individually; rim level 0.451)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=6300, R_eq 10.51): none; #52 (t=7100, R_eq 9.24): none; #61 (t=7900, R_eq 8.5): none; #184 (t=10100, R_eq 2.26): none
- species `prey` (channels ['prey a'], own threshold): components final 27, mean 33.7, max 57; tracks 281, persistent 11; splits 58, persistent splits 1 (K=5), max generation 1, merges 1, merge/split 0.017; moving tracks 19
- species `predator` (channels ['predator b'], own threshold): components final 32, mean 37.2, max 62; tracks 212, persistent 0; splits 30, persistent splits 21 (K=5), max generation 2, merges 3, merge/split 0.1; moving tracks 2

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 359 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
