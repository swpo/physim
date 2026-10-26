# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 180s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa3 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0264, 1.183], min area 6 px

## Measurements
- components: final 65, mean 64.7, max 75; occupancy final 0.30
- tracks: 188; persistent (alive >= 50% of run): 65; longest 121 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 4.05 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [65, 65, 65], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.000822/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 31, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 1, merges 13, merge/split ratio 0.419, nucleations 9
- channel total drift (end/start - 1): [0.2187, -1.0, -0.7013, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.08; core [0.897, 0.0, 0.041, 0.918] rim [0.503, 0.0, 0.108, 0.79]
  - track 66 at frame 61: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.08; core [0.877, 0.0, 0.046, 0.906] rim [0.656, 0.0, 0.08, 0.842]
  - track 74 at frame 61: holes 0, rim-vs-core 0.42, rim-vs-outside 0.30, heterogeneity 0.08; core [0.888, 0.0, 0.046, 0.904] rim [0.483, 0.0, 0.107, 0.792]
  - track 172 at frame 65: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.08; core [0.896, 0.0, 0.041, 0.917] rim [0.515, 0.0, 0.106, 0.793]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 385 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 22 (aggregate of 385 individuals; 0/385 membrane-like individually; rim level 0.866)
  - radial predator b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 1.06 (aggregate of 385 individuals; 0/385 membrane-like individually; rim level 0.0051)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 9.22, rim/outside 0.861 (aggregate of 385 individuals; 0/385 membrane-like individually; rim level 0.161)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.904, rim/outside 1.44 (aggregate of 385 individuals; 0/385 membrane-like individually; rim level 0.877)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=6100, R_eq 5.14): none; #66 (t=6100, R_eq 5.05): none; #74 (t=6100, R_eq 4.82): none; #172 (t=6500, R_eq 5.05): none
- species `prey` (channels ['prey a'], own threshold): components final 65, mean 63.7, max 73; tracks 176, persistent 65; splits 28, persistent splits 7 (K=20), max generation 1, merges 9, merge/split 0.321; moving tracks 2
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 1.3, max 14; tracks 16, persistent 0; splits 1, persistent splits 0 (K=20), max generation 0, merges 0, merge/split 0; moving tracks 1

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
