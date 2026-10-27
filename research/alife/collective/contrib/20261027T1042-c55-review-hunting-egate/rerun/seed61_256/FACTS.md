# Evidence pack: driven-condensate-prey-predator (seed 61)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py`, family `active-emulsion`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 121 frames x 500 steps x dt 0.2 = time 12000; grid [256, 256]; wall 2025s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out /tmp/claude-0/-home-user-physim/cb6f7f87-7e13-5a25-b6c0-c6ef3066597c/scratchpad/hunt/pack256 --seeds 61 --size 256 256 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.142, 1.1698], min area 6 px

## Measurements
- components: final 42, mean 62.3, max 115; occupancy final 0.06
- tracks: 233; persistent (alive >= 50% of run): 16; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 54.55 (1 = constant size)
- enclosures: components with a hole mean 0.27, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [57, 48, 34], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 38, persistent splits 18 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.026, nucleations 154
- channel total drift (end/start - 1): [-0.0536, None, -0.5081, -0.5513]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 62: holes 0, rim-vs-core 0.17, rim-vs-outside 0.61, heterogeneity 0.07; core [0.919, 0.0, 0.001, 0.735] rim [0.77, 0.0, 0.048, 0.661]
  - track 18 at frame 63: holes 0, rim-vs-core 0.18, rim-vs-outside 0.60, heterogeneity 0.07; core [0.919, 0.0, 0.001, 0.735] rim [0.765, 0.0, 0.048, 0.656]
  - track 57 at frame 67: holes 0, rim-vs-core 0.20, rim-vs-outside 0.47, heterogeneity 0.06; core [0.903, 0.0, 0.008, 0.74] rim [0.732, 0.0, 0.083, 0.671]
  - track 186 at frame 109: holes 0, rim-vs-core 0.20, rim-vs-outside 0.22, heterogeneity 0.03; core [0.011, 0.789, 0.54, 0.01] rim [0.019, 0.588, 0.537, 0.016]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 340 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 5.15 (aggregate of 340 individuals; 14/340 membrane-like individually; rim level 0.444)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.947, rim/outside 9.17 (aggregate of 340 individuals; 6/340 membrane-like individually; rim level 0.39)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.54, rim/outside 0.888 (aggregate of 340 individuals; 0/340 membrane-like individually; rim level 0.373)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 5.9 (aggregate of 340 individuals; 14/340 membrane-like individually; rim level 0.439)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=6200, R_eq 10.59): none; #18 (t=6300, R_eq 10.52): none; #57 (t=6700, R_eq 8.5): none; #186 (t=10900, R_eq 2.76): none
- species `prey` (channels ['prey a'], own threshold): components final 15, mean 31.9, max 60; tracks 252, persistent 10; splits 48, persistent splits 2 (K=5), max generation 1, merges 0, merge/split 0; moving tracks 21
- species `predator` (channels ['predator b'], own threshold): components final 30, mean 38.3, max 66; tracks 225, persistent 0; splits 35, persistent splits 11 (K=5), max generation 2, merges 3, merge/split 0.086; moving tracks 3

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 340 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
