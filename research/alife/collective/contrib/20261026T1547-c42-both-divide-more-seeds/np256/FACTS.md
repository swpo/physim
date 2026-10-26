# Evidence pack: condensate-food-chain (seed 3)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 440s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/np256 --seeds 3 --frames 100 --lineage-k 5 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0258, 1.1613], min area 6 px

## Measurements
- components: final 295, mean 291.9, max 297; occupancy final 0.30
- tracks: 592; persistent (alive >= 50% of run): 295; longest 101 frames; alive start-to-end: 12
- size of persistent tracks: max/min area ratio 19.67 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [295, 295, 295], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 5 frames = time 500, --lineage-k): splits 92, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 1, merges 41, merge/split ratio 0.446, nucleations 30
- channel total drift (end/start - 1): [0.2045, None, -0.7053, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.894, 0.0, 0.04, 0.912] rim [0.512, 0.0, 0.097, 0.798]
  - track 27 at frame 50: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.08; core [0.894, 0.0, 0.037, 0.92] rim [0.518, 0.0, 0.098, 0.797]
  - track 31 at frame 50: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.08; core [0.887, 0.0, 0.04, 0.914] rim [0.498, 0.0, 0.1, 0.792]
  - track 514 at frame 52: holes 0, rim-vs-core 0.43, rim-vs-outside 0.30, heterogeneity 0.08; core [0.882, 0.0, 0.041, 0.909] rim [0.475, 0.0, 0.101, 0.789]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 1770 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 23.6 (aggregate of 1770 individuals; 0/1770 membrane-like individually; rim level 0.851)
  - radial predator b: flat profile (no radial structure; level 0; aggregate of 1770 individuals)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 8.12, rim/outside 0.866 (aggregate of 1770 individuals; 0/1770 membrane-like individually; rim level 0.148)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.906, rim/outside 1.4 (aggregate of 1770 individuals; 0/1770 membrane-like individually; rim level 0.881)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=5000, R_eq 4.62): none; #27 (t=5000, R_eq 4.82): none; #31 (t=5000, R_eq 4.79): none; #514 (t=5200, R_eq 4.79): none
- species `prey` (channels ['prey a'], own threshold): components final 295, mean 291.9, max 297; tracks 592, persistent 295; splits 92, persistent splits 24 (K=5), max generation 1, merges 41, merge/split 0.446; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 0.0, max 0; tracks 0, persistent 0; splits 0, persistent splits 0 (K=5), max generation 0, merges 0, merge/split n/a; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
