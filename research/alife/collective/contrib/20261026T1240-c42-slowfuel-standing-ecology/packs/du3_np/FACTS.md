# Evidence pack: condensate-food-chain (seed 0)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 121s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_np --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0444, 1.0803], min area 6 px

## Measurements
- components: final 109, mean 107.9, max 110; occupancy final 0.27
- tracks: 178; persistent (alive >= 50% of run): 109; longest 121 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 11.67 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [109, 109, 109], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000592/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 12, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 0.333, nucleations 8
- channel total drift (end/start - 1): [0.0821, None, -0.6067, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 61: holes 0, rim-vs-core 0.39, rim-vs-outside 0.34, heterogeneity 0.09; core [0.884, 0.0, 0.048, 0.924] rim [0.539, 0.0, 0.159, 0.767]
  - track 56 at frame 61: holes 0, rim-vs-core 0.41, rim-vs-outside 0.33, heterogeneity 0.09; core [0.87, 0.0, 0.059, 0.901] rim [0.498, 0.0, 0.165, 0.756]
  - track 58 at frame 61: holes 0, rim-vs-core 0.34, rim-vs-outside 0.42, heterogeneity 0.09; core [0.907, 0.0, 0.039, 0.937] rim [0.614, 0.0, 0.137, 0.797]
  - track 59 at frame 61: holes 0, rim-vs-core 0.25, rim-vs-outside 0.46, heterogeneity 0.09; core [0.865, 0.0, 0.062, 0.895] rim [0.641, 0.0, 0.125, 0.811]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 654 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 30.5 (aggregate of 654 individuals; 0/654 membrane-like individually; rim level 0.783)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 654 individuals)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 13.7, rim/outside 0.816 (aggregate of 654 individuals; 0/654 membrane-like individually; rim level 0.264)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 1.63 (aggregate of 654 individuals; 0/654 membrane-like individually; rim level 0.85)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=6100, R_eq 3.83): none; #56 (t=6100, R_eq 3.66): none; #58 (t=6100, R_eq 3.83): none; #59 (t=6100, R_eq 3.57): none
- species `prey` (channels ['prey a'], own threshold): components final 109, mean 107.9, max 110; tracks 178, persistent 109; splits 12, persistent splits 0 (K=20), max generation 0, merges 4, merge/split 0.333; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
