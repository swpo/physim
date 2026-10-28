# Evidence pack: digestion-predators-prey-turnover (seed 5)

- world: `../../c62work/world_turn.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 61 frames x 500 steps x dt 0.2 = time 6000; grid [128, 128]; wall 150s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_turn.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/turn/H --seeds 5 --size 128 128 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.3318, 0.667], min area 6 px

## Measurements
- components: final 63, mean 54.3, max 63; occupancy final 0.21
- tracks: 99; persistent (alive >= 50% of run): 60; longest 61 frames; alive start-to-end: 20
- size of persistent tracks: max/min area ratio 11.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 63, 61], H1 [13, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00113/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.167, nucleations 36
- channel total drift (end/start - 1): [-0.0566, None, -0.7737, -0.7352, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 30: holes 0, rim-vs-core 0.23, rim-vs-outside 0.17, heterogeneity 0.04; core [0.841, 0.0, 0.007, 0.251, 0.0] rim [0.617, 0.0, 0.02, 0.184, 0.0]
  - track 2 at frame 30: holes 0, rim-vs-core 0.18, rim-vs-outside 0.15, heterogeneity 0.03; core [0.791, 0.0, 0.016, 0.238, 0.0] rim [0.618, 0.0, 0.024, 0.186, 0.0]
  - track 4 at frame 30: holes 0, rim-vs-core 0.22, rim-vs-outside 0.16, heterogeneity 0.03; core [0.821, 0.0, 0.009, 0.245, 0.0] rim [0.607, 0.0, 0.021, 0.181, 0.0]
  - track 93 at frame 45: holes 0, rim-vs-core 0.13, rim-vs-outside 0.13, heterogeneity 0.02; core [0.74, 0.0, 0.018, 0.222, 0.0] rim [0.616, 0.0, 0.024, 0.184, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 337 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 4.72 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.747)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 337 individuals)
  - radial fuel F: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.96, rim/outside 0.747 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.035)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.17 (aggregate of 337 individuals; 0/337 membrane-like individually; rim level 0.223)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 337 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=3000, R_eq 4.26): none; #2 (t=3000, R_eq 3.43): none; #4 (t=3000, R_eq 4.22): none; #93 (t=4500, R_eq 3.14): none
- species `prey` (channels ['prey a'], own threshold): components final 64, mean 58.0, max 64; tracks 111, persistent 60; splits 33, persistent splits 7 (K=20), max generation 1, merges 4, merge/split 0.121; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
