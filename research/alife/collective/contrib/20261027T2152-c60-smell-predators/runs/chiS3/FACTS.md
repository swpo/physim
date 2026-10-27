# Evidence pack: digestion-predators-smell (seed 71)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261027T2200-c60-smell-tmp/world.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 315s; status ok
- command: `python -m labkit.run collective/contrib/20261027T2200-c60-smell-tmp/world.py --out /tmp/claude-0/smell/chiS3 --seeds 71 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.24 of robust range [0.1527, 1.5978], min area 6 px

## Measurements
- components: final 36, mean 36.8, max 51; occupancy final 0.10
- tracks: 214; persistent (alive >= 50% of run): 13; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 18.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 12, 5], H1 [1, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.009/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 2000, default): splits 44, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 48, merge/split ratio 1.09, nucleations 80
- channel total drift (end/start - 1): [-0.0118, None, -0.6206, -0.5934, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 43: holes 0, rim-vs-core 0.13, rim-vs-outside 0.07, heterogeneity 0.04; core [0.244, 0.346, 0.176, 0.249, 0.112] rim [0.242, 0.232, 0.177, 0.245, 0.061]
  - track 0 at frame 35: holes 0, rim-vs-core 0.47, rim-vs-outside 0.23, heterogeneity 0.16; core [0.288, 0.659, 0.199, 0.323, 0.462] rim [0.207, 0.332, 0.217, 0.227, 0.147]
  - track 1 at frame 32: holes 0, rim-vs-core 0.62, rim-vs-outside 0.17, heterogeneity 0.25; core [0.366, 0.631, 0.176, 0.422, 0.593] rim [0.294, 0.208, 0.193, 0.331, 0.162]
  - track 50 at frame 54: holes 0, rim-vs-core 0.45, rim-vs-outside 0.15, heterogeneity 0.14; core [0.312, 0.583, 0.165, 0.335, 0.39] rim [0.303, 0.221, 0.17, 0.32, 0.129]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 221 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 1.93 (aggregate of 221 individuals; 9/221 membrane-like individually; rim level 0.351)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.596, rim/outside 4.72 (aggregate of 221 individuals; 1/221 membrane-like individually; rim level 0.297)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 0.914 (aggregate of 221 individuals; 0/221 membrane-like individually; rim level 0.172)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.96, rim/outside 1.94 (aggregate of 221 individuals; 13/221 membrane-like individually; rim level 0.36)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.531, rim/outside 8.64 (aggregate of 221 individuals; 3/221 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=4300, R_eq 3.57): none; #0 (t=3500, R_eq 4.07): none; #1 (t=3200, R_eq 4.3): none; #50 (t=5400, R_eq 3.48): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 21.6, max 37; tracks 128, persistent 3; splits 7, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 0.429; moving tracks 28
- species `predator` (channels ['predator b'], own threshold): components final 5, mean 19.6, max 43; tracks 126, persistent 0; splits 3, persistent splits 0 (K=20), max generation 0, merges 3, merge/split 1; moving tracks 26

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 221 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
