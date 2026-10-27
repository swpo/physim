# Evidence pack: digestion-predators-smell (seed 71)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2200-c60-smell-tmp/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 321s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2200-c60-smell-tmp/world.py --out /tmp/claude-0/smell/short2 --seeds 71 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.25 of robust range [0.1527, 1.5435], min area 6 px

## Measurements
- components: final 3, mean 28.2, max 48; occupancy final 0.00
- tracks: 180; persistent (alive >= 50% of run): 4; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 18, 2], H1 [21, 4, 0]
- motion: 29 long-lived tracks moved >= 1 body length; max speed 0.00858/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 2000, default): splits 30, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 36, merge/split ratio 1.2, nucleations 82
- channel total drift (end/start - 1): [-0.0067, None, -0.6224, -0.5923, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 34: holes 0, rim-vs-core 0.50, rim-vs-outside 0.18, heterogeneity 0.12; core [0.192, 0.726, 0.198, 0.201, 0.433] rim [0.217, 0.312, 0.196, 0.224, 0.158]
  - track 0 at frame 30: holes 0, rim-vs-core 0.26, rim-vs-outside 0.35, heterogeneity 0.16; core [0.185, 0.676, 0.212, 0.199, 0.367] rim [0.213, 0.44, 0.205, 0.229, 0.277]
  - track 3 at frame 28: holes 0, rim-vs-core 0.67, rim-vs-outside 0.16, heterogeneity 0.24; core [0.28, 0.717, 0.158, 0.306, 0.632] rim [0.29, 0.236, 0.166, 0.306, 0.167]
  - track 21 at frame 30: holes 0, rim-vs-core 0.67, rim-vs-outside 0.13, heterogeneity 0.19; core [0.346, 0.63, 0.146, 0.37, 0.661] rim [0.314, 0.181, 0.157, 0.328, 0.167]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 160 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.934, rim/outside 2.07 (aggregate of 160 individuals; 3/160 membrane-like individually; rim level 0.371)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.659, rim/outside 3.85 (aggregate of 160 individuals; 1/160 membrane-like individually; rim level 0.296)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 0.902 (aggregate of 160 individuals; 0/160 membrane-like individually; rim level 0.167)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.937, rim/outside 2.07 (aggregate of 160 individuals; 3/160 membrane-like individually; rim level 0.375)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.578, rim/outside 6.64 (aggregate of 160 individuals; 2/160 membrane-like individually; rim level 0.145)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=3400, R_eq 4.15): none; #0 (t=3000, R_eq 4.72): none; #3 (t=2800, R_eq 5.26): ['prey a', 'product p']; #21 (t=3000, R_eq 4.22): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 14.0, max 37; tracks 79, persistent 3; splits 6, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.167; moving tracks 15
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 10.6, max 36; tracks 88, persistent 0; splits 3, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.333; moving tracks 6

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 160 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
