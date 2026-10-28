# Evidence pack: growing-digestion-predators (seed 5)

- world: `../../c62work/world_grow.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 276s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_grow.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/grow/Q2 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1501, 1.8397], min area 6 px

## Measurements
- components: final 40, mean 39.8, max 52; occupancy final 0.14
- tracks: 113; persistent (alive >= 50% of run): 31; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 38, 19], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 2000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 113
- channel total drift (end/start - 1): [-0.1718, None, -0.5476, -0.6532, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 30: holes 0, rim-vs-core 0.41, rim-vs-outside 0.28, heterogeneity 0.21; core [0.151, 0.667, 0.319, 0.2, 0.238] rim [0.244, 0.313, 0.298, 0.324, 0.105]
  - track 0 at frame 27: holes 0, rim-vs-core 0.44, rim-vs-outside 0.18, heterogeneity 0.08; core [0.042, 0.738, 0.396, 0.077, 0.248] rim [0.076, 0.332, 0.388, 0.115, 0.096]
  - track 1 at frame 28: holes 0, rim-vs-core 0.20, rim-vs-outside 0.38, heterogeneity 0.07; core [0.033, 0.728, 0.409, 0.067, 0.228] rim [0.047, 0.537, 0.406, 0.082, 0.165]
  - track 7 at frame 29: holes 0, rim-vs-core 0.45, rim-vs-outside 0.19, heterogeneity 0.08; core [0.032, 0.764, 0.412, 0.068, 0.25] rim [0.066, 0.346, 0.404, 0.103, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 247 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.918, rim/outside 2.11 (aggregate of 247 individuals; 3/247 membrane-like individually; rim level 0.271)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.688, rim/outside 7 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.41)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.967 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.268)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 1.96 (aggregate of 247 individuals; 2/247 membrane-like individually; rim level 0.291)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.597, rim/outside 10.6 (aggregate of 247 individuals; 0/247 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=3000, R_eq 6.43): ['prey a', 'product p']; #0 (t=2700, R_eq 5.32): none; #1 (t=2800, R_eq 5.7): none; #7 (t=2900, R_eq 5.86): none
- species `prey` (channels ['prey a'], own threshold): components final 4, mean 17.3, max 44; tracks 126, persistent 0; splits 4, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.25; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 33, mean 20.7, max 42; tracks 112, persistent 0; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
