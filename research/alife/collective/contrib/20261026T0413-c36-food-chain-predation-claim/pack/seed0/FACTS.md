# Evidence pack: condensate-food-chain (seed 0)

- world: `../../world.py`, family `active-emulsion`
- parent: threads/active-droplets/worlds/ad1-fuel; mutation: two immiscible autocatalytic condensates in a closed chain: prey made from fuel, predator made from prey material; decay -> waste -> fuel
- run: 101 frames x 200 steps x dt 0.5 = time 10000; grid [256, 256]; wall 700s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/fc/packK/s0 --seeds 0 --frames 100 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0094, 1.2968], min area 6 px

## Measurements
- components: final 173, mean 160.3, max 226; occupancy final 0.31
- tracks: 885; persistent (alive >= 50% of run): 135; longest 101 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 22.47 (1 = constant size)
- enclosures: components with a hole mean 0.42, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [175, 174, 173], H1 [0, 0, 0]
- motion: 20 long-lived tracks moved >= 1 body length; max speed 0.00574/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 2000, default): splits 233, persistent splits 40 (0 more failed only because the siblings re-merged within K), max generation 3, merges 91, merge/split ratio 0.391, nucleations 26
- channel total drift (end/start - 1): [0.2892, -0.9927, -0.7317, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 61 at frame 50: holes 0, rim-vs-core 0.29, rim-vs-outside 0.52, heterogeneity 0.06; core [0.94, 0.0, 0.025, 0.962] rim [0.66, 0.0, 0.079, 0.896]
  - track 91 at frame 50: holes 0, rim-vs-core 0.27, rim-vs-outside 0.53, heterogeneity 0.06; core [0.95, 0.0, 0.026, 0.961] rim [0.693, 0.0, 0.075, 0.902]
  - track 163 at frame 50: holes 0, rim-vs-core 0.30, rim-vs-outside 0.52, heterogeneity 0.06; core [0.95, 0.0, 0.027, 0.957] rim [0.656, 0.0, 0.077, 0.898]
  - track 801 at frame 83: holes 0, rim-vs-core 0.36, rim-vs-outside 0.32, heterogeneity 0.06; core [0.904, 0.0, 0.04, 0.941] rim [0.554, 0.0, 0.087, 0.884]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 947 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 15.3 (aggregate of 947 individuals; 1/947 membrane-like individually; rim level 0.856)
  - radial predator b: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.61 (aggregate of 947 individuals; 5/947 membrane-like individually; rim level 0.0204)
  - radial fuel u: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 4.96, rim/outside 0.872 (aggregate of 947 individuals; 0/947 membrane-like individually; rim level 0.141)
  - radial waste w: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 1.17 (aggregate of 947 individuals; 0/947 membrane-like individually; rim level 0.917)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #61 (t=5000, R_eq 6.48): none; #91 (t=5000, R_eq 6.02): none; #163 (t=5000, R_eq 6.02): none; #801 (t=8300, R_eq 5.92): none
- species `prey` (channels ['prey a'], own threshold): components final 173, mean 153.6, max 200; tracks 638, persistent 135; splits 153, persistent splits 39 (K=20), max generation 3, merges 42, merge/split 0.275; moving tracks 20
- species `predator` (channels ['predator b'], own threshold): components final 0, mean 11.6, max 74; tracks 270, persistent 0; splits 70, persistent splits 0 (K=20), max generation 0, merges 18, merge/split 0.257; moving tracks 0

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 947 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
