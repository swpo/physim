# Evidence pack: condensate-food-chain (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 121 frames x 200 steps x dt 0.5 = time 12000; grid [128, 128]; wall 182s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1302-c42-foodchain-both-divide-claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/cl/qa6 --seeds 0 --size 128 128 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0406, 1.3535], min area 6 px

## Measurements
- components: final 37, mean 38.0, max 75; occupancy final 0.23
- tracks: 498; persistent (alive >= 50% of run): 0; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 1.44, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 36, 24], H1 [3, 2, 1]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00169/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 2000, default): splits 146, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 1, merges 66, merge/split ratio 0.452, nucleations 60
- channel total drift (end/start - 1): [-0.499, 3.7951, -0.3654, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 82 at frame 31: holes 0, rim-vs-core 0.13, rim-vs-outside 0.41, heterogeneity 0.05; core [0.002, 0.822, 0.652, 0.186] rim [0.007, 0.695, 0.625, 0.203]
  - track 142 at frame 31: holes 0, rim-vs-core 0.18, rim-vs-outside 0.22, heterogeneity 0.03; core [0.005, 0.796, 0.635, 0.079] rim [0.01, 0.619, 0.631, 0.078]
  - track 81 at frame 23: holes 0, rim-vs-core 0.23, rim-vs-outside 0.26, heterogeneity 0.04; core [0.002, 0.861, 0.609, 0.209] rim [0.01, 0.634, 0.608, 0.209]
  - track 258 at frame 67: holes 0, rim-vs-core 0.22, rim-vs-outside 0.27, heterogeneity 0.04; core [0.004, 0.839, 0.695, 0.185] rim [0.012, 0.619, 0.693, 0.186]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 196 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial prey a: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 2.3 (aggregate of 196 individuals; 17/196 membrane-like individually; rim level 0.171)
  - radial predator b: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.982, rim/outside 4.75 (aggregate of 196 individuals; 21/196 membrane-like individually; rim level 0.545)
  - radial fuel u: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.13, rim/outside 0.972 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.559)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 1.22 (aggregate of 196 individuals; 0/196 membrane-like individually; rim level 0.314)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #82 (t=3100, R_eq 6.63): none; #142 (t=3100, R_eq 3.78): none; #81 (t=2300, R_eq 3.99): none; #258 (t=6700, R_eq 4.58): none
- species `prey` (channels ['prey a'], own threshold): components final 8, mean 12.2, max 70; tracks 313, persistent 0; splits 77, persistent splits 0 (K=20), max generation 0, merges 15, merge/split 0.195; moving tracks 1
- species `predator` (channels ['predator b'], own threshold): components final 30, mean 29.3, max 38; tracks 371, persistent 0; splits 97, persistent splits 2 (K=20), max generation 1, merges 46, merge/split 0.474; moving tracks 11

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 34 of 196 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
