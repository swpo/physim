# Evidence pack: condensate-food-chain (seed 2)

- world: `../world3.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 130s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world3.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/du3_np2 --seeds 2 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0444, 1.0805], min area 6 px

## Measurements
- components: final 108, mean 106.6, max 108; occupancy final 0.27
- tracks: 164; persistent (alive >= 50% of run): 108; longest 121 frames; alive start-to-end: 7
- size of persistent tracks: max/min area ratio 8.44 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [108, 108, 108], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000576/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 17, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.353, nucleations 9
- channel total drift (end/start - 1): [0.0621, None, -0.6062, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.879, 0.0, 0.06, 0.903] rim [0.51, 0.0, 0.163, 0.782]
  - track 5 at frame 61: holes 0, rim-vs-core 0.38, rim-vs-outside 0.35, heterogeneity 0.08; core [0.894, 0.0, 0.049, 0.924] rim [0.559, 0.0, 0.155, 0.792]
  - track 8 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.09; core [0.877, 0.0, 0.059, 0.908] rim [0.497, 0.0, 0.167, 0.778]
  - track 162 at frame 66: holes 0, rim-vs-core 0.41, rim-vs-outside 0.30, heterogeneity 0.08; core [0.865, 0.0, 0.07, 0.889] rim [0.482, 0.0, 0.169, 0.775]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 648 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 28.5 (aggregate of 648 individuals; 0/648 membrane-like individually; rim level 0.787)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 648 individuals)
  - radial fuel u: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 13.4, rim/outside 0.821 (aggregate of 648 individuals; 0/648 membrane-like individually; rim level 0.268)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 1.52 (aggregate of 648 individuals; 0/648 membrane-like individually; rim level 0.861)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 3.57): none; #5 (t=6100, R_eq 3.7): none; #8 (t=6100, R_eq 3.7): none; #162 (t=6600, R_eq 3.43): none
- species `prey` (channels ['prey a'], own threshold): components final 108, mean 106.6, max 108; tracks 164, persistent 108; splits 17, persistent splits 1 (K=20), max generation 1, merges 6, merge/split 0.353; moving tracks 3
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=20), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
