# Evidence pack: growing-digestion-predators (seed 5)

- world: `../../c62work/world_grow.py`, family `active-emulsion`
- parent: collective/contrib/20261027T0325-c52-digestion-ecology-claim; mutation: predator fuel-depletion drift chiF 0.5 -> 0.25; before (c52): predator material conserved and condensed only up its own digestion product (active chi on both trophic levels); before: prey condensate whose miscibility gap is opened only by its own fuel-driven catalysis product (active chi); prey matter recycled from predator waste, not made from fuel
- run: 81 frames x 500 steps x dt 0.2 = time 8000; grid [128, 128]; wall 232s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/c62work/world_grow.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/grow/R4 --seeds 5 --size 128 128 --frames 80 --no-movie`
- segmentation: matter > 0.21 of robust range [0.1501, 1.8157], min area 6 px

## Measurements
- components: final 59, mean 47.7, max 66; occupancy final 0.13
- tracks: 276; persistent (alive >= 50% of run): 5; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.88 (1 = constant size)
- enclosures: components with a hole mean 0.05, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [56, 35, 10], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 0.00578/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 50, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 29, merge/split ratio 0.58, nucleations 146
- channel total drift (end/start - 1): [-0.1777, None, -0.5481, -0.6532, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 27: holes 0, rim-vs-core 0.41, rim-vs-outside 0.14, heterogeneity 0.19; core [0.136, 0.592, 0.259, 0.167, 0.219] rim [0.24, 0.233, 0.24, 0.276, 0.084]
  - track 13 at frame 26: holes 0, rim-vs-core 0.52, rim-vs-outside 0.17, heterogeneity 0.26; core [0.199, 0.646, 0.268, 0.252, 0.449] rim [0.225, 0.223, 0.27, 0.269, 0.144]
  - track 32 at frame 27: holes 0, rim-vs-core 0.36, rim-vs-outside 0.12, heterogeneity 0.20; core [0.169, 0.523, 0.266, 0.203, 0.174] rim [0.247, 0.204, 0.248, 0.286, 0.065]
  - track 2 at frame 23: holes 0, rim-vs-core 0.78, rim-vs-outside 0.20, heterogeneity 0.25; core [0.233, 0.718, 0.229, 0.291, 0.758] rim [0.315, 0.159, 0.232, 0.353, 0.223]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 290 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 2.11 (aggregate of 290 individuals; 29/290 membrane-like individually; rim level 0.263)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.675, rim/outside 6.16 (aggregate of 290 individuals; 3/290 membrane-like individually; rim level 0.375)
  - radial fuel F: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.957 (aggregate of 290 individuals; 0/290 membrane-like individually; rim level 0.257)
  - radial product p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.99 (aggregate of 290 individuals; 29/290 membrane-like individually; rim level 0.274)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.623, rim/outside 8.66 (aggregate of 290 individuals; 4/290 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=2700, R_eq 4.51): none; #13 (t=2600, R_eq 5.41): ['prey a', 'product p']; #32 (t=2700, R_eq 4.79): none; #2 (t=2300, R_eq 4.48): ['prey a', 'product p']
- species `prey` (channels ['prey a'], own threshold): components final 13, mean 27.8, max 44; tracks 198, persistent 0; splits 26, persistent splits 1 (K=20), max generation 1, merges 2, merge/split 0.077; moving tracks 18
- species `predator` (channels ['predator b'], own threshold): components final 34, mean 26.3, max 45; tracks 200, persistent 0; splits 26, persistent splits 0 (K=20), max generation 0, merges 1, merge/split 0.038; moving tracks 8

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 290 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
