# Evidence pack: digestion-predators-prey-turnover (seed 5)

- world: `../../c62work/world_turn.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 61 frames x 500 steps x dt 0.2 = time 6000; grid [128, 128]; wall 154s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_turn.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/turn/E --seeds 5 --size 128 128 --frames 60 --no-movie`
- segmentation: matter > 0.48 of robust range [0.1695, 0.8539], min area 6 px

## Measurements
- components: final 38, mean 31.8, max 38; occupancy final 0.16
- tracks: 38; persistent (alive >= 50% of run): 37; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 38
- channel total drift (end/start - 1): [-0.0196, None, -0.638, -0.596, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 31: holes 0, rim-vs-core 0.39, rim-vs-outside 0.28, heterogeneity 0.07; core [0.879, 0.0, 0.023, 0.848, 0.0] rim [0.603, 0.0, 0.075, 0.584, 0.0]
  - track 1 at frame 32: holes 0, rim-vs-core 0.20, rim-vs-outside 0.45, heterogeneity 0.06; core [0.87, 0.0, 0.024, 0.84, 0.0] rim [0.727, 0.0, 0.052, 0.703, 0.0]
  - track 2 at frame 32: holes 0, rim-vs-core 0.39, rim-vs-outside 0.28, heterogeneity 0.07; core [0.875, 0.0, 0.02, 0.836, 0.0] rim [0.594, 0.0, 0.074, 0.572, 0.0]
  - track 3 at frame 32: holes 0, rim-vs-core 0.37, rim-vs-outside 0.30, heterogeneity 0.06; core [0.896, 0.0, 0.028, 0.883, 0.0] rim [0.639, 0.0, 0.075, 0.626, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 207 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 16.7 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.834)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 207 individuals)
  - radial fuel F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 7.77, rim/outside 0.684 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.139)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.843, rim/outside 14.4 (aggregate of 207 individuals; 0/207 membrane-like individually; rim level 0.821)
  - radial digestion q: flat profile (no radial structure; level 0; aggregate of 207 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=3100, R_eq 4.79): none; #1 (t=3200, R_eq 5.05): none; #2 (t=3200, R_eq 5.05): none; #3 (t=3200, R_eq 4.41): none
- species `prey` (channels ['prey a'], own threshold): components final 38, mean 34.0, max 38; tracks 39, persistent 37; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
