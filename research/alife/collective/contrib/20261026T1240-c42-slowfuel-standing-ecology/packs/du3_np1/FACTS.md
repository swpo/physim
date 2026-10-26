# Evidence pack: condensate-food-chain (seed 1)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 132s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_np1 --seeds 1 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0444, 1.0802], min area 6 px

## Measurements
- components: final 109, mean 107.2, max 109; occupancy final 0.26
- tracks: 191; persistent (alive >= 50% of run): 109; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 11.14 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [109, 109, 109], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00054/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 2000, default): splits 28, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 0.357, nucleations 8
- channel total drift (end/start - 1): [0.1248, None, -0.6051, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 61: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.09; core [0.872, 0.0, 0.058, 0.906] rim [0.499, 0.0, 0.162, 0.774]
  - track 20 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.33, heterogeneity 0.08; core [0.885, 0.0, 0.049, 0.924] rim [0.545, 0.0, 0.152, 0.789]
  - track 39 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.09; core [0.874, 0.0, 0.054, 0.914] rim [0.51, 0.0, 0.16, 0.776]
  - track 181 at frame 65: holes 0, rim-vs-core 0.39, rim-vs-outside 0.32, heterogeneity 0.08; core [0.877, 0.0, 0.058, 0.902] rim [0.521, 0.0, 0.156, 0.781]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 652 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 32.5 (aggregate of 652 individuals; 0/652 membrane-like individually; rim level 0.78)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 652 individuals)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 13.6, rim/outside 0.81 (aggregate of 652 individuals; 0/652 membrane-like individually; rim level 0.26)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 1.56 (aggregate of 652 individuals; 0/652 membrane-like individually; rim level 0.858)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=6100, R_eq 3.57): none; #20 (t=6100, R_eq 3.61): none; #39 (t=6100, R_eq 3.66): none; #181 (t=6500, R_eq 3.43): none
- species `prey` (channels ['prey a'], own threshold): components final 109, mean 107.2, max 109; tracks 191, persistent 109; splits 28, persistent splits 5 (K=20), max generation 1, merges 10, merge/split 0.357; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
