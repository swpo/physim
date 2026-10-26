# Evidence pack: condensate-food-chain (seed 2)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 135s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/pack_nopred/seed2 --seeds 2 --size 128 128 --frames 120 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0256, 1.1629], min area 6 px

## Measurements
- components: final 75, mean 74.2, max 78; occupancy final 0.31
- tracks: 151; persistent (alive >= 50% of run): 75; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 14.33 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [75, 75, 75], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 22, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.318, nucleations 8
- channel total drift (end/start - 1): [0.1828, None, -0.7064, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.09; core [0.895, 0.0, 0.039, 0.869] rim [0.52, 0.0, 0.097, 0.691]
  - track 12 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.08; core [0.891, 0.0, 0.04, 0.865] rim [0.514, 0.0, 0.097, 0.69]
  - track 46 at frame 61: holes 0, rim-vs-core 0.44, rim-vs-outside 0.32, heterogeneity 0.09; core [0.883, 0.0, 0.045, 0.846] rim [0.479, 0.0, 0.1, 0.68]
  - track 143 at frame 63: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.09; core [0.899, 0.0, 0.038, 0.873] rim [0.524, 0.0, 0.096, 0.693]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 450 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 22.5 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.852)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 450 individuals)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 7.97, rim/outside 0.87 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.147)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 1.87 (aggregate of 450 individuals; 0/450 membrane-like individually; rim level 0.818)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=6100, R_eq 4.65): none; #12 (t=6100, R_eq 4.62): none; #46 (t=6100, R_eq 4.51): none; #143 (t=6300, R_eq 4.69): none
- species `prey` (channels ['prey a'], own threshold): components final 75, mean 74.2, max 78; tracks 151, persistent 75; splits 22, persistent splits 4 (K=5), max generation 1, merges 7, merge/split 0.318; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
