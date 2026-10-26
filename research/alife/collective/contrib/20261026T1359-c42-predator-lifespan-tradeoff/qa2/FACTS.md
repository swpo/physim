# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 168s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa2 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0532, 1.1981], min area 6 px

## Measurements
- components: final 3, mean 9.7, max 67; occupancy final 0.54
- tracks: 212; persistent (alive >= 50% of run): 3; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.96 (1 = constant size)
- enclosures: components with a hole mean 0.86, final 1; holes at thresholds 0.2/0.35/0.5 final [5, 5, 5]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [9, 5, 5]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 2000, default): splits 20, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 66, merge/split ratio 3.3, nucleations 10
- channel total drift (end/start - 1): [-0.8903, 11.8423, -0.376, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 124 at frame 62: holes 0, rim-vs-core 0.22, rim-vs-outside 0.43, heterogeneity 0.05; core [0.003, 0.918, 0.477, 0.048] rim [0.011, 0.7, 0.478, 0.046]
  - track 204 at frame 76: holes 0, rim-vs-core 0.26, rim-vs-outside 0.49, heterogeneity 0.06; core [0.001, 0.958, 0.501, 0.033] rim [0.01, 0.696, 0.486, 0.043]
  - track 209 at frame 77: holes 0, rim-vs-core 0.33, rim-vs-outside 0.36, heterogeneity 0.05; core [0.003, 0.962, 0.409, 0.059] rim [0.019, 0.63, 0.413, 0.056]
  - track 25 at frame 22: holes 0, rim-vs-core 0.31, rim-vs-outside 0.47, heterogeneity 0.05; core [0.001, 0.979, 0.534, 0.036] rim [0.012, 0.673, 0.532, 0.035]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 2.4 (aggregate of 36 individuals; 1/36 membrane-like individually; rim level 0.124)
  - radial predator b: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.887, rim/outside 2.26 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.629)
  - radial fuel u: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.986 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.45)
  - radial waste w: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 1.19 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.104)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #124 (t=6200, R_eq 5.44): none; #204 (t=7600, R_eq 9.8): none; #209 (t=7700, R_eq 5.47): none; #25 (t=2200, R_eq 6.02): none
- species `prey` (channels ['prey a'], own threshold): components final 0, mean 3.8, max 59; tracks 149, persistent 0; splits 18, persistent splits 0 (K=20), max generation 0, merges 15, merge/split 0.833; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 3, mean 6.9, max 37; tracks 93, persistent 2; splits 2, persistent splits 0 (K=20), max generation 0, merges 42, merge/split 21; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 5 of 36 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
