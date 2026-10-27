# Evidence pack: digestion-predators-smell (seed 71)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2200-c60-smell-tmp/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2200-c60-smell-tmp/world.py --out /tmp/claude-0/smell/short1 --seeds 71 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.22 of robust range [0.1527, 1.7224], min area 6 px

## Measurements
- components: final 47, mean 40.0, max 51; occupancy final 0.16
- tracks: 158; persistent (alive >= 50% of run): 19; longest 79 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [45, 42, 31], H1 [0, 0, 0]
- motion: 56 long-lived tracks moved >= 1 body length; max speed 0.00877/time; max body lengths 5.9
- replication (lineage window K = 20 frames = time 2000, default): splits 22, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 30, merge/split ratio 1.36, nucleations 84
- channel total drift (end/start - 1): [-0.035, None, -0.6141, -0.5977, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 41: holes 0, rim-vs-core 0.59, rim-vs-outside 0.18, heterogeneity 0.27; core [0.399, 0.593, 0.169, 0.47, 0.514] rim [0.349, 0.158, 0.184, 0.4, 0.125]
  - track 21 at frame 43: holes 0, rim-vs-core 0.52, rim-vs-outside 0.16, heterogeneity 0.25; core [0.416, 0.556, 0.15, 0.467, 0.453] rim [0.333, 0.188, 0.169, 0.363, 0.105]
  - track 22 at frame 43: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.23; core [0.507, 0.444, 0.121, 0.549, 0.432] rim [0.311, 0.334, 0.154, 0.336, 0.198]
  - track 11 at frame 42: holes 0, rim-vs-core 0.41, rim-vs-outside 0.13, heterogeneity 0.11; core [0.201, 0.604, 0.204, 0.217, 0.238] rim [0.223, 0.227, 0.205, 0.235, 0.076]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 252 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 2.41 (aggregate of 252 individuals; 31/252 membrane-like individually; rim level 0.382)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.468, rim/outside 7.78 (aggregate of 252 individuals; 4/252 membrane-like individually; rim level 0.305)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.892 (aggregate of 252 individuals; 0/252 membrane-like individually; rim level 0.176)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 2.47 (aggregate of 252 individuals; 26/252 membrane-like individually; rim level 0.402)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.411, rim/outside 13.7 (aggregate of 252 individuals; 7/252 membrane-like individually; rim level 0.176)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=4100, R_eq 4.48): none; #21 (t=4300, R_eq 4.44): none; #22 (t=4300, R_eq 4.37): none; #11 (t=4200, R_eq 4.26): none
- species `prey` (channels ['prey a'], own threshold): components final 39, mean 36.0, max 43; tracks 154, persistent 16; splits 10, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.4; moving tracks 54
- species `predator` (channels ['predator b'], own threshold): components final 41, mean 29.3, max 45; tracks 126, persistent 14; splits 4, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.25; moving tracks 49

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 252 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
