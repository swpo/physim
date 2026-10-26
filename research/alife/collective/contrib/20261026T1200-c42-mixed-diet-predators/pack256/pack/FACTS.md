# Evidence pack: condensate-food-chain (seed 0)

- world: `../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 596s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/world.py --out /tmp/claude-0/-home-user-physim/4e890ad6-3240-5329-a5c6-2d12ecca7a99/scratchpad/claim/pack --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0315, 1.5241], min area 6 px

## Measurements
- components: final 58, mean 93.3, max 225; occupancy final 0.21
- tracks: 1430; persistent (alive >= 50% of run): 0; longest 33 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 12.63, final 14; holes at thresholds 0.2/0.35/0.5 final [17, 14, 7]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [92, 53, 18], H1 [24, 13, 3]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00541/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 430, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 141, merge/split ratio 0.328, nucleations 232
- channel total drift (end/start - 1): [-0.4088, 3.449, -0.4155, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 343 at frame 19: holes 1, rim-vs-core 0.09, rim-vs-outside 0.20, heterogeneity 0.04; core [0.005, 0.697, 0.561, 0.179] rim [0.008, 0.611, 0.546, 0.198]
  - track 182 at frame 17: holes 0, rim-vs-core 0.06, rim-vs-outside 0.34, heterogeneity 0.03; core [0.003, 0.72, 0.555, 0.166] rim [0.007, 0.656, 0.547, 0.171]
  - track 204 at frame 18: holes 0, rim-vs-core 0.28, rim-vs-outside 0.50, heterogeneity 0.08; core [0.892, 0.013, 0.027, 0.913] rim [0.651, 0.023, 0.105, 0.797]
  - track 333 at frame 18: holes 0, rim-vs-core 0.04, rim-vs-outside 0.35, heterogeneity 0.03; core [0.004, 0.697, 0.611, 0.121] rim [0.008, 0.653, 0.605, 0.122]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 430 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 2.97 (aggregate of 430 individuals; 32/430 membrane-like individually; rim level 0.203)
  - radial predator b: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.76 (aggregate of 430 individuals; 95/430 membrane-like individually; rim level 0.47)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.968 (aggregate of 430 individuals; 0/430 membrane-like individually; rim level 0.52)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 1.38 (aggregate of 430 individuals; 0/430 membrane-like individually; rim level 0.312)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #343 (t=1900, R_eq 5.01, ring): ['predator b']; #182 (t=1700, R_eq 7.14): none; #204 (t=1800, R_eq 8.23): none; #333 (t=1800, R_eq 7.36): none
- species `prey` (channels ['prey a'], own threshold): components final 21, mean 27.0, max 196; tracks 662, persistent 0; splits 117, persistent splits 0 (K=20), max generation 0, merges 25, merge/split 0.214; moving tracks 0
- species `predator` (channels ['predator b'], own threshold): components final 50, mean 77.2, max 128; tracks 1218, persistent 0; splits 371, persistent splits 0 (K=20), max generation 0, merges 98, merge/split 0.264; moving tracks 10

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 121 of 430 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
