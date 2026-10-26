# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 181s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa4 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0261, 1.179], min area 6 px

## Measurements
- components: final 68, mean 67.6, max 74; occupancy final 0.30
- tracks: 184; persistent (alive >= 50% of run): 68; longest 121 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 3.96 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [68, 68, 68], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000843/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 28, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 13, merge/split ratio 0.464, nucleations 9
- channel total drift (end/start - 1): [0.2212, -1.0, -0.7031, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.08; core [0.893, 0.0, 0.038, 0.915] rim [0.506, 0.0, 0.108, 0.762]
  - track 31 at frame 61: holes 0, rim-vs-core 0.40, rim-vs-outside 0.33, heterogeneity 0.08; core [0.904, 0.0, 0.037, 0.917] rim [0.538, 0.0, 0.102, 0.775]
  - track 68 at frame 61: holes 0, rim-vs-core 0.22, rim-vs-outside 0.48, heterogeneity 0.08; core [0.864, 0.0, 0.048, 0.89] rim [0.652, 0.0, 0.077, 0.827]
  - track 174 at frame 65: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.08; core [0.892, 0.0, 0.042, 0.905] rim [0.503, 0.0, 0.103, 0.772]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 404 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 22.2 (aggregate of 404 individuals; 0/404 membrane-like individually; rim level 0.863)
  - radial predator b: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.928 (aggregate of 404 individuals; 0/404 membrane-like individually; rim level 0.0042)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.2, rim/outside 0.863 (aggregate of 404 individuals; 0/404 membrane-like individually; rim level 0.156)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.894, rim/outside 1.5 (aggregate of 404 individuals; 0/404 membrane-like individually; rim level 0.869)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=6100, R_eq 5.29): none; #31 (t=6100, R_eq 5.05): none; #68 (t=6100, R_eq 4.95): none; #174 (t=6500, R_eq 4.92): none
- species `prey` (channels ['prey a'], own threshold): components final 68, mean 67.0, max 72; tracks 167, persistent 68; splits 24, persistent splits 5 (K=20), max generation 1, merges 10, merge/split 0.417; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.9, max 8; tracks 9, persistent 0; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
