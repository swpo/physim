# Evidence pack: digestion-predators-smell (seed 71)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2200-c60-smell-tmp/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 312s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2200-c60-smell-tmp/world.py --out /tmp/claude-0/smell/chiS1 --seeds 71 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1527, 1.7944], min area 6 px

## Measurements
- components: final 45, mean 39.4, max 52; occupancy final 0.18
- tracks: 133; persistent (alive >= 50% of run): 22; longest 78 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 22.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 44, 38], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.00873/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 2000, default): splits 17, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 27, merge/split ratio 1.59, nucleations 72
- channel total drift (end/start - 1): [-0.0483, None, -0.6113, -0.5995, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 42: holes 0, rim-vs-core 0.47, rim-vs-outside 0.16, heterogeneity 0.26; core [0.526, 0.41, 0.114, 0.575, 0.351] rim [0.35, 0.146, 0.15, 0.375, 0.067]
  - track 10 at frame 42: holes 0, rim-vs-core 0.35, rim-vs-outside 0.13, heterogeneity 0.19; core [0.335, 0.482, 0.18, 0.378, 0.222] rim [0.278, 0.19, 0.193, 0.307, 0.06]
  - track 11 at frame 42: holes 0, rim-vs-core 0.38, rim-vs-outside 0.12, heterogeneity 0.15; core [0.263, 0.543, 0.191, 0.289, 0.228] rim [0.257, 0.201, 0.197, 0.275, 0.066]
  - track 53 at frame 51: holes 0, rim-vs-core 0.50, rim-vs-outside 0.18, heterogeneity 0.24; core [0.472, 0.5, 0.13, 0.524, 0.408] rim [0.386, 0.141, 0.147, 0.419, 0.092]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 258 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.97 (aggregate of 258 individuals; 46/258 membrane-like individually; rim level 0.407)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.405, rim/outside 8.13 (aggregate of 258 individuals; 2/258 membrane-like individually; rim level 0.281)
  - radial fuel F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.874 (aggregate of 258 individuals; 0/258 membrane-like individually; rim level 0.181)
  - radial product p: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 3.05 (aggregate of 258 individuals; 33/258 membrane-like individually; rim level 0.432)
  - radial digestion q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.356, rim/outside 14 (aggregate of 258 individuals; 5/258 membrane-like individually; rim level 0.166)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=4200, R_eq 4.89): none; #10 (t=4200, R_eq 4.82): none; #11 (t=4200, R_eq 4.55): none; #53 (t=5100, R_eq 4.33): none
- species `prey` (channels ['prey a'], own threshold): components final 42, mean 39.6, max 49; tracks 143, persistent 24; splits 19, persistent splits 3 (K=20), max generation 1, merges 14, merge/split 0.737; moving tracks 49
- species `predator` (channels ['predator b'], own threshold): components final 42, mean 30.2, max 47; tracks 111, persistent 26; splits 7, persistent splits 3 (K=20), max generation 1, merges 6, merge/split 0.857; moving tracks 44

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 258 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
