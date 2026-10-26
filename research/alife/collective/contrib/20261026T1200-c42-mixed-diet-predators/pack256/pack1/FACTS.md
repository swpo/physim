# Evidence pack: condensate-food-chain (seed 1)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 596s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/pack1 --seeds 1 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0355, 1.5251], min area 6 px

## Measurements
- components: final 83, mean 86.0, max 218; occupancy final 0.18
- tracks: 1375; persistent (alive >= 50% of run): 0; longest 31 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 13.43, final 8; holes at thresholds 0.2/0.35/0.5 final [12, 8, 6]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [115, 64, 22], H1 [16, 11, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 2000, default): splits 419, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 154, merge/split ratio 0.368, nucleations 248
- channel total drift (end/start - 1): [-0.2704, 2.2681, -0.424, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 165 at frame 16: holes 0, rim-vs-core 0.15, rim-vs-outside 0.22, heterogeneity 0.02; core [0.004, 0.77, 0.683, 0.042] rim [0.011, 0.623, 0.681, 0.041]
  - track 317 at frame 17: holes 0, rim-vs-core 0.06, rim-vs-outside 0.37, heterogeneity 0.03; core [0.003, 0.729, 0.631, 0.13] rim [0.008, 0.666, 0.627, 0.129]
  - track 329 at frame 18: holes 0, rim-vs-core 0.04, rim-vs-outside 0.37, heterogeneity 0.03; core [0.005, 0.693, 0.686, 0.062] rim [0.009, 0.658, 0.681, 0.063]
  - track 331 at frame 18: holes 0, rim-vs-core 0.07, rim-vs-outside 0.38, heterogeneity 0.05; core [0.002, 0.729, 0.535, 0.249] rim [0.006, 0.662, 0.53, 0.249]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 403 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 2.48 (aggregate of 403 individuals; 35/403 membrane-like individually; rim level 0.165)
  - radial predator b: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.8 (aggregate of 403 individuals; 104/403 membrane-like individually; rim level 0.491)
  - radial fuel u: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.11, rim/outside 0.974 (aggregate of 403 individuals; 0/403 membrane-like individually; rim level 0.561)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 1.39 (aggregate of 403 individuals; 0/403 membrane-like individually; rim level 0.267)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #165 (t=1600, R_eq 5.23): none; #317 (t=1700, R_eq 8.1): none; #329 (t=1800, R_eq 7.09): none; #331 (t=1800, R_eq 7.18): none
- species `prey` (channels ['prey a'], own threshold): components final 25, mean 21.7, max 172; tracks 628, persistent 0; splits 97, persistent splits 0 (K=20), max generation 0, merges 25, merge/split 0.258; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 69, mean 75.2, max 127; tracks 1198, persistent 0; splits 368, persistent splits 0 (K=20), max generation 0, merges 122, merge/split 0.332; moving tracks 10

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 132 of 403 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
